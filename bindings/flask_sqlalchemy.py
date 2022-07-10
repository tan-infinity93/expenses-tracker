'''
'''

# Import Modules:

from datetime import datetime
from ast import literal_eval
from datetime import datetime as dt
from flask import current_app as c_app
from sqlalchemy import create_engine, func, cast, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only
from models.dbmodels import (
	Base, ExpensesTracker, MonthlySalary
)

# Class Definition:

class FlaskSqlAlchemy:

	def __init__(self, app=None, config_prefix="SQLALCHEMY_CONNECTION", **kwargs):
		'''
		'''
		self.config_prefix = config_prefix

		if app is not None:
			self.init_app(app)

	def init_app(self, app, **kwargs):
		'''
		'''
		try:
			db_uri = app.config.get('DATABASE_URL')
			connection_string = f'{db_uri}'
			engine = create_engine(connection_string)
			Session = sessionmaker(bind=engine)
			session = Session()
			app.config['BASE'] = Base
			app.config['ENGINE'] = engine
			app.config['SESSION'] = session
			Base.metadata.create_all(engine)

		except Exception as e:
			raise e

	@staticmethod
	def get_all_expenses(start_date, end_date):
		'''
		'''
		try:
			session = c_app.config.get('SESSION')
			query = session.query(ExpensesTracker)
			print(start_date)
			print(end_date)

			if start_date and end_date:
				query = query.filter(
					func.date(ExpensesTracker.timestamp).between(start_date, end_date)
				)
			query = query.order_by(func.date(ExpensesTracker.timestamp))

			expenses = [
				expense.sqlalchemy_encoder() for expense in query.all()
			]
			return expenses

		except Exception as e:
			raise e

	@staticmethod
	def group_expense_by_date(start_date=None, end_date=None):
		try:
			session = c_app.config.get('SESSION')
			# query = session.query(
			# 	ExpensesTracker.expense_type, 
			# 	func.sum(ExpensesTracker.expense_cost).label('expense_cost'),
			# 	func.date(ExpensesTracker.timestamp)
			# ).group_by(
			# 	ExpensesTracker.expense_type,
			# 	func.date(ExpensesTracker.timestamp)
			# )
			query = session.query(
				func.sum(ExpensesTracker.expense_cost).label('expense_cost'),
				func.date(ExpensesTracker.timestamp)
			).group_by(
				func.date(ExpensesTracker.timestamp)
			)

			if start_date and end_date:
				query = query.filter(
					func.date(ExpensesTracker.timestamp).between(start_date, end_date)
				)

			print(query)
			expenses = [
				{
					'cost': expense[0],
					'date': expense[1].isoformat()
				}
				for expense in query.all()
			]

			total = sum([expense['cost'] for expense in expenses])
			print(expenses)
			return expenses, total

		except Exception as e:
			raise e

	@staticmethod
	def get_expenses_ratio(start_date, end_date):
		'''
		'''
		try:
			session = c_app.config.get('SESSION')
			query = session.query(MonthlySalary)
			query = session.query(
				(MonthlySalary.salary).label('salary')
			)
			if start_date and end_date:
				time_data = dt.strptime(start_date, '%Y-%m-%d')
				month = time_data.month
				year = time_data.year
				query = query.filter(
					func.Date(MonthlySalary.timestamp) == f'{year}-{month}-01%'
				)
			monthly_salary = query.all()[0][0]
			expenses, total = FlaskSqlAlchemy.group_expense_by_date(start_date, end_date)
			return monthly_salary, total

		except Exception as e:
			raise e

	@staticmethod
	def add_expense(model_name, data):
		'''
		'''
		try:
			model_mapper = {
				'expenses_tracker': ExpensesTracker,
				'monthly_salary': MonthlySalary
			}

			session = c_app.config.get('SESSION')
			model = model_mapper.get(model_name)
			print(model(**data))
			session.add(model(**data))
			session.commit()
			# SELECT ms.timestamp FROM monthly_salary ms;

		except Exception as e:
			session.rollback()
			raise e

	@staticmethod
	def delete_expense(expense_id=None):
		'''
		'''
		try:
			session = c_app.config.get('SESSION')
			session.query(ExpensesTracker).filter(ExpensesTracker.id == expense_id).delete()
			session.commit()
		
		except Exception as e:
			session.rollback()
			raise e