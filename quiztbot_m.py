import telebot
from telebot import types
from configuration import Token_for_bot
from get_from_db import QuestionDB
import random

bot = telebot.TeleBot(Token_for_bot.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    btn1 = types.KeyboardButton('Новая игра')
    buttons.append(btn1)
    if check_player(message) == True:
        btn2 = types.KeyboardButton('Продолжить игру')
        buttons.append(btn2)
    elif check_player(message)==False:
        db=QuestionDB()
        db.add_id_player(message.from_user.id)
        db.close()


    markup.add(*buttons)
    bot.send_message(message.from_user.id, 'Выберите вариант:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Новая игра" or message.text == 'Следующий вопрос' or message.text == 'Продолжить игру')

def new_question(message):
    #получение вопросов, которые еще в игре
    if message.text=='Продолжить игру':
    	db=QuestionDB()
    	numbers=db.resume_game()
    	db.close()
    #получение списка с номерами вопросов
    #не верно!!!!!!!!
    elif message.text=='Новая игра':
    	db=QuestionDB()
    	numbers=list(range(1, db.get_number_of_questions()+1))
    	db.close()
    	
    if len(numbers)==0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        btn1 = types.KeyboardButton('Новая игра')
        buttons.append(btn1)
        markup.add(*buttons)
        bot.send_message(message.from_user.id, 'Вопросы закончились=) Спасибо за игру!', reply_markup=markup)
    else:
        buttons=[]
        question_number=random.choice(numbers)
        numbers.remove(question_number)
        qdb=QuestionDB()
        #qdb.get на выходе получает список с кортежем внутри
        question=qdb.get(question_number)
        qdb.close()
        #распаковываем список в кортеж
        question=question[0]
        question_id=question[0]
        question_text=question[1]
        right_answer=question[3]
        answer_picture=question[4]
        question_type=question[5]
        if answer_picture=='True':
            img=open(f'image\\{question_id}.JPG', 'rb')
            bot.send_photo(message.from_user.id, img)
        if question_type=='4a':
            answers=question[2].split('@')
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            for i in answers:
                buttons.append(types.KeyboardButton(i))
            markup.add(*buttons)
            # записываем ответ игрока в переменную
            human_answer = bot.send_message(message.from_user.id, f'{question_text}: ', reply_markup=markup)
            # передаем ответ игрока и правильный ответ в check_answer()
            bot.register_next_step_handler(human_answer, check_answer, right_answer, question_type)
        elif question_type=='1a':
            #записываем ответ игрока в переменную
            human_answer=bot.send_message(message.from_user.id, f'{question_text}: ')
            #передаем ответ игрока и правильный ответ в check_answer()
            bot.register_next_step_handler(human_answer, check_answer, right_answer, question_type)

#проверка ответа игрока и кнопка следующего вопроса
def check_answer(human_answer, right_answer, question_type):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn= types.KeyboardButton('Следующий вопрос')
    markup.add(btn)
    if question_type=='4a':
        if human_answer.text.lower()==right_answer.lower():
            bot.send_message(human_answer.from_user.id, 'верно', reply_markup=markup)
        else:
            bot.send_message(human_answer.from_user.id, f'не верно, верный ответ {right_answer}', reply_markup=markup)
    elif question_type=='1a':
        if human_answer.text.lower()==right_answer.lower():
            bot.send_message(human_answer.from_user.id, 'верно', reply_markup=markup)
        elif human_answer.text.lower()!=right_answer.lower():
            bot.send_message(human_answer.from_user.id, f'Верный ответ: {right_answer}, прошу сверьте с Вашим ответом.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Следующий вопрос')
        markup.add(btn)
        bot.send_message(message.from_user.id, 'Некорректный запрос', reply_markup=markup)

#проверка ид игрока, что он уже играл
def check_player(message):
    player_id = message.from_user.id
    db=QuestionDB()
    result=db.check_id(player_id)
    db.close()
    if result==True:
        return True
    else:
        return False
        

id_player=None
numbers=[]






bot.polling(none_stop=True, interval=0)