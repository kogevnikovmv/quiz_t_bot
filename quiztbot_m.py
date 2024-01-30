import telebot
from telebot import types
from configuration import Token_for_bot
from get_from_db import QuestionDB
import random

bot = telebot.TeleBot(Token_for_bot.TOKEN)

# База данных с вопросами и id игроков, с их прогрессом в игре
db=QuestionDB()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    btn1 = types.KeyboardButton('Новая игра')
    buttons.append(btn1)
    # если id игрока есть в БД то добавляется кнопка "продолжить игру"
    if check_player(message) == True:
        btn2 = types.KeyboardButton('Продолжить игру')
        buttons.append(btn2)
    # если id игрока нет в БД, то id добавляется в бд
    elif check_player(message)==False:
        db.add_id_player(message.from_user.id)



    markup.add(*buttons)
    bot.send_message(message.from_user.id, 'Выберите вариант:', reply_markup=markup)





@bot.message_handler(func=lambda message: message.text == "Новая игра" or message.text == 'Следующий вопрос' or message.text == 'Продолжить игру')

def new_question(message):
    numbers=[]
    #получение вопросов, которые еще в игре
    if message.text=='Продолжить игру' or message.text=='Следующий вопрос':
        numbers=db.resume_game(message.from_user.id)
    # получаем список всех вопросов для новой игры
    elif message.text=='Новая игра':
        numbers=db.new_game(message.from_user.id)
    # если вопросы закончились, бот сообщает об этом и присылает кнопку "Новая игра"
    if numbers==[]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = []
        btn1 = types.KeyboardButton('Новая игра')
        buttons.append(btn1)
        markup.add(*buttons)
        bot.send_message(message.from_user.id, 'Вопросы закончились=) Спасибо за игру!', reply_markup=markup)
    else:
        buttons=[]
        # получаем рандомный номер вопроса
        question_number=random.choice(numbers)
        # удаляем и списка вопросов полученный номер
        numbers.remove(question_number)
        # сохраняет изменения в списке вопросов, которые еще в игре
        db.save_progress(message.from_user.id, numbers)
        # db.get на выходе получает список с id вопроса, текст вопроса, варианты ответа,
        # правильный ответ, наличие картинки у вопроса и тип вопроса(с вариантами ответов или нет)
        question=db.get_question(question_number)
        question_id=question[0]
        question_text=question[1]
        right_answer=question[3]
        answer_picture=question[4]
        question_type=question[5]
        # если у вопроса есть фото, бот пришлет его
        # название картинки соответствует номеру вопроса
        if answer_picture=='True':
            img=open(f'image\\{question_id}.JPG', 'rb')
            bot.send_photo(message.from_user.id, img)
        # для вопросов с вариантами ответов
        if question_type=='4a':
            answers=question[2].split('@')
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            for i in answers:
                buttons.append(types.KeyboardButton(i))
            markup.add(*buttons)
            # записываем ответ игрока в переменную
            human_answer = bot.send_message(message.from_user.id, f'{question_text}: ', reply_markup=markup)
            # передаем ответ игрока и правильный ответ в check_answer()
            bot.register_next_step_handler(human_answer, check_answer, right_answer, question_type)
        # для вопросов с произвольным ответом
        elif question_type=='1a':
            #записываем ответ игрока в переменную
            human_answer=bot.send_message(message.from_user.id, f'{question_text} \nНапишите Ваш вариант ответа:')
            #передаем ответ игрока и правильный ответ в check_answer()
            bot.register_next_step_handler(human_answer, check_answer, right_answer, question_type)

# проверка ответа игрока и кнопка следующего вопроса
def check_answer(human_answer, right_answer, question_type):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn= types.KeyboardButton('Следующий вопрос')
    markup.add(btn)
    # для вопросов с вариантами ответа
    if question_type=='4a':
        if human_answer.text.lower()==right_answer.lower():
            bot.send_message(human_answer.from_user.id, 'верно', reply_markup=markup)
        else:
            bot.send_message(human_answer.from_user.id, f'не верно, верный ответ: {right_answer}', reply_markup=markup)
    # для вопросов с произвольным ответом
    elif question_type=='1a':
        if human_answer.text.lower()==right_answer.lower():
            bot.send_message(human_answer.from_user.id, 'верно', reply_markup=markup)
        elif human_answer.text.lower()!=right_answer.lower():
            bot.send_message(human_answer.from_user.id, f'Верный ответ: {right_answer}, прошу сверьте с Вашим ответом.', reply_markup=markup)


# обработка не правильного сообщения от пользователя
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton('Следующий вопрос')
        markup.add(btn)
        bot.send_message(message.from_user.id, 'Некорректный запрос', reply_markup=markup)

# проверка id игрока, что он уже играл
def check_player(message):
    player_id = message.from_user.id
    result=db.check_id(player_id)
    if result==True:
        return True
    else:
        return False
        







bot.polling(none_stop=True, interval=0)