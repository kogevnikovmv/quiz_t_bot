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
			self.db_path=Db_path.TEST_WIN_PATH
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

	#новый вопрос из бд
	def get_new_question(self, num):
		return self.Question.get_by_id(num)
	
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
		new_player = self.Player.create(player_id=555556, player_progress='im not player')
		print('player add')


	# ************Функции для работы бота***********

	#запрос на получение записи по номеру ид
	def get_question(self, num):
		cursor=self.db.cursor()
		cursor.execute(f'SELECT * FROM Questions WHERE id={num}')
		result=cursor.fetchall()
		return result


	#добавление нового ид в бд
	def add_id_player(self,num):
		new_player=self.Player.create(player_id=num, player_progress='')

	#проверка игрока что он играл ранее
	def check_id(self, player_id):
		cursor=self.db.cursor()
		cursor.execute(f'SELECT * FROM Players WHERE player_id={player_id}')
		result=cursor.fetchall()
		if result:
			print(result)
			return True
		else:
			print('id не найден')
			return False





	# возвращает номера вопросов которые еще не сыгранны
	def resume_game(self, player_id):
		cursor=self.db.cursor()
		cursor.execute(f'SELECT player_progress FROM Players WHERE player_id={player_id}')
		result=cursor.fetchall()
		return json.loads(result)
	
	# удаляет сыгранный вопрос
	def save_progress(self, player_id, progress):
		player=self.Player.get(player_id=player_id)
		progress=json.loads(progress)
		player.player_progress=f'{progress}'
		player.save()


	# получение списка номеров вопросов в бд
	def new_game(self, player_id):
		numbers = list(range(1, self.Question.select().count() + 1))
		self.save_progress(player_id, numbers)
		return numbers



#для проверки				
with QuestionDB() as q:
	#print(q.get_all())
	#print(q.get_new_q(2))
	#print(q.get_number_of_questions())
	#q.get_tables_names()
	#print(*q.get(2))
	#q.get_fields()
	#q.add_id_player(1)
	#q.check_id(1)

	#q.add_id_test_player()
	q.all_players()
	#q.get_player_fields()
	q.new_game()
