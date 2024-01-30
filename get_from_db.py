from peewee import *
import platform
from configuration import Db_path
import json

class QuestionDB():
	def __init__(self):
		
		# путь к файлу с бд в зависимости от системы где я запускаю бот
		# этот кусок кода совсем не обязателен, я написал его для своего удобства.

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
		self.db.close()
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()
		print('db closed')
	
	def close(self):
		self.db.close()

	# ************ Функции для работы бота ***********

	# запрос на получение записи по номеру id
	def get_question(self, num):
		self.db.connect()
		row = self.Question.get(id=num)
		result = [row.id, row.question, row.answers, row.right, row.picture, row.question_type]
		self.db.close()
		return result

	# добавление нового id в БД
	def add_id_player(self, num):
		self.db.connect()
		new_player = self.Player.create(player_id=num, player_progress='[18]')
		self.db.close()

	# проверка игрока что он играл ранее
	def check_id(self, player_id):
		self.db.connect()
		result = self.Player.get_or_none(player_id=player_id)
		self.db.close()
		if result:
			return True
		else:
			return False

	# возвращает номера вопросов которые еще не сыгранны
	def resume_game(self, player_id):
		self.db.connect()
		player = self.Player.get(player_id=player_id)
		result = player.player_progress
		self.db.close()
		if result:
			return json.loads(result)
		else:
			print('пустой player_progress игрока')

	# сохраняет в БД список вопросов после получения нового вопроса
	def save_progress(self, player_id, progress):
		self.db.connect()
		player = self.Player.get(player_id=player_id)
		progress = json.dumps(progress)
		player.player_progress = f'{progress}'
		player.save()
		self.db.close()

	# получение списка номеров вопросов в БД для новой игры
	def new_game(self, player_id):
		self.db.connect()
		numbers = list(range(1, self.Question.select().count() + 1))
		self.db.close()
		self.save_progress(player_id, numbers)
		return numbers

	# ******** Функции для проверки работы БД ************

	# получение всех записей в БД
	def get_all_rows(self):
		cursor=self.db.cursor()
		cursor.execute('SELECT * FROM Questions')
		result=cursor.fetchall()
		print(result)

	# получить названия всех таблиц БД
	def get_tables_names(self):
		list_names=self.db.get_tables()
		for name in list_names:
			print('table: ', name)
	
	#получить имена столбцов таблицы Question
	def get_fields(self):
		print(self.Question._meta.fields)

	# выводит всех игроков
	def all_players(self):
		cursor = self.db.cursor()
		cursor.execute('SELECT * FROM Players')
		result = cursor.fetchall()
		print(result)

	# названия столбцов таблицы Игроки
	def get_player_fields(self):
		print(self.Player._meta.fields)

	# добавление тестового игрока
	def add_id_test_player(self):
		new_player = self.Player.create(player_id=2222, player_progress='[18]')
		print('player add')

	# изменение информации о игроке
	def edit_player(self, player_id):
		player = self.Player.get(player_id=player_id)
		player.player_progress='[18]'
		player.save()