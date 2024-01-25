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

			id = AutoField()
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
		
	#получение всех записей в бд
	def get_all(self):
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
	# ошибка
	#не работант как надо, выводит только id
	#, а не всю строку целеком
	def get_new_q(self, num):
		return self.Question.get_by_id(num)
	
	#получить имена столбцов
	def get_fields(self):
		print(self.Question._meta.fields)
		
	#запрос на получение записи по номеру ид
	def get(self, num):
		cursor=self.db.cursor()
		cursor.execute(f'SELECT * FROM Questions WHERE id={num}')
		result=cursor.fetchall()
		return result
		
	#получение кол-ва вопросов
	def get_number_of_questions(self):
		return self.Question.select().count()

	#добавление нового ид в бд
	def add_id_player(self,num):
		#не здесь должно быть это
		numbers=list(range(1, self.get_number_of_questions()+1))
		
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

	# выводит всех игроков			
	def all_players(self):
		cursor=self.db.cursor()
		cursor.execute('SELECT * FROM Players')
		result=cursor.fetchall()
		print(result)
	
	# возвращает номера вопросов в игре
	def resume_game(self, player_id):
		cursor=self.db.cursor()
		cursor.execute(f'SELECT player_progress FROM Players WHERE player_id={player_id}')
		result=cursor.fetchall()
		return json.loads(result)
	
	# удаляет сыгранный вопрос
	def save_progress(self, player_id, progress):
		print()

	def get_player_fields(self):
		print(self.Player._meta.fields)
	

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
	q.all_players()
	q.get_player_fields()