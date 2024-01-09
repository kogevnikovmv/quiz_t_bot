from peewee import *

class QuestionDB():
	def __init__(self):
		#путь до бд
		self.db = SqliteDatabase('C:\quiztbot\questions_database.db')
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
	def get_new_q(self, num):
		return self.Question.get_by_id(num)
	#получить имена столбцов

	def get_fields(self):
		print(self.Question._meta.fields)
		#print(self.Question[2])
		
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
			print('нет ид########')
			return False

#для проверки				
#with QuestionDB() as q:
	#print(q.get_all())
	#print(q.get_new_q(2))
	#print(q.get_number_of_questions())
	#q.get_tables_names()
	#print(*q.get(2))
	#q.get_fields()
	#q.add_id_player(1)
	#q.check_id(1)