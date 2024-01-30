from peewee import *
import platform
from configuration import Db_path
import json

class QuestionDB():
	def __init__(self):
		
		# путь к файлу с бд в зависимости от системы где я запускаю бот
		# этот кусок кода совсем не обязателен, я написал его для своего удобства
		# для телефона =)
		if platform.system()=='Linux':
			self.db_path=Db_path.MOBILE_PATH
		elif platform.system()=='Windows':
			self.db_path=Db_path.WIN_PATH
		else:
			print('система не определена')
		
		# создаем объект бд
		self.db = SqliteDatabase(self.db_path)
		
		
		#описание модели бд
		class Question(Model):
			class Meta:
				database=self.db
				table_name='Questions'

			id = AutoField(primary_key=True)
			question=TextField(column_name='question')
			answers=TextField()
			right=TextField()
			picture=TextField()
			question_type=TextField()
		#при создании этого объекта
		#создается объект модели таблицв

		class Player(Model):
			class Meta:
				database=self.db
				table_name='Players'
				
			id=PrimaryKeyField(primary_key=True)
			player_id=IntegerField()
			player_progress=TextField()

		self.Question=Question
		self.Player=Player
		self.db.connect()
		self.db.create_tables([Question, Player])
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()
		print('db closed')
	
	def close(self):
		self.db.close()


	# ********Функции для проверки работы бд************

	#получение всех записей в бд
	def get_all_rows(self):
		cursor=self.db.cursor()
		cursor.execute('SELECT * FROM Questions')
		result=cursor.fetchall()
		print(result)

	#получить названия всех таблиц бд
	def get_tables_names(self):
		list_names=self.db.get_tables()
		for name in list_names:
			print('table: ', name)
	
	#получить имена столбцов
	def get_fields(self):
		print(self.Question._meta.fields)

	# выводит всех игроков
	def all_players(self):
		cursor = self.db.cursor()
		cursor.execute('SELECT * FROM Players')
		result = cursor.fetchall()
		print(result)

	def get_player_fields(self):
		print(self.Player._meta.fields)

	def add_id_test_player(self):
		new_player = self.Player.create(player_id=2222, player_progress='[18]')
		print('player add')

	def edit_player(self, player_id):
		player = self.Player.get(player_id=player_id)
		player.player_progress='[18]'
		player.save()


	# ************Функции для работы бота***********

	#запрос на получение записи по номеру ид
	def get_question(self, num):
		row=self.Question.get(id=num)
		result=[row.id, row.question, row.answers, row.right, row.picture, row.question_type]
		return result


	#добавление нового ид в бд
	def add_id_player(self,num):
		new_player=self.Player.create(player_id=num, player_progress='[18]')

	#проверка игрока что он играл ранее
	def check_id(self, player_id):
		#cursor=self.db.cursor()
		#cursor.execute(f'SELECT * FROM Players WHERE player_id={player_id}')
		#result=cursor.fetchall()
		result=self.Player.get_or_none(player_id=player_id)
		if result:
			return True
		else:
			return False





	# возвращает номера вопросов которые еще не сыгранны
	def resume_game(self, player_id):
		player=self.Player.get(player_id=player_id)
		result=player.player_progress
		print('result', result)
		if result:
			return json.loads(result)
		else:
			print('пустой player_progress игрока')
	
	# сохраняет в бд список вопросов после получения нового вопроса
	def save_progress(self, player_id, progress):
		player=self.Player.get(player_id=player_id)
		progress=json.dumps(progress)
		player.player_progress=f'{progress}'
		player.save()


	# получение списка номеров вопросов в бд для новой игры
	def new_game(self, player_id):
		numbers = list(range(1, self.Question.select().count() + 1))
		self.save_progress(player_id, numbers)
		return numbers




#для проверки				
#with QuestionDB() as q:
	#print(q.get_all_rows())
	#print(q.get_question(2))
	#print(q.get_number_of_questions())
	#q.get_tables_names()
	#q.get_fields()
	#q.add_id_player(1)
	#print(q.check_id(5137175701))
	#q.add_id_test_player()
	#q.all_players()
	#q.get_player_fields()
	#q.new_game()
	#print(q.resume_game(1111))

