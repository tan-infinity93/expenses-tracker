'''
'''

# Import Modules:

from datetime import datetime
from ast import literal_eval
from flask import current_app as c_app
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only
from models.dbmodels import (
	Base, ExpensesTracker
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
			db_uri = app.config.get('DATABASE_URI')
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
	def get_all_expenses(start_date=None, end_date=None):
		'''
		'''
		try:
			session = c_app.config.get('SESSION')
			query = session.query(ExpensesTracker)

			if start_date and end_date:
				query = query.filter_by(
				timestamp=timestamp)
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
			query = session.query(
				ExpensesTracker.expense_type, 
				func.sum(ExpensesTracker.expense_cost).label('expense_cost'),
				func.date(ExpensesTracker.timestamp)
			).group_by(
				ExpensesTracker.expense_type,
				func.date(ExpensesTracker.timestamp)
			)

			if start_date and end_date:
				query = query.filter_by(
				timestamp=timestamp)
			expenses = [
				{
					'category': expense[0],
					'cost': expense[1],
					'date': expense[2]
				}
				for expense in query.all()
			]

			total = sum([expense['cost'] for expense in expenses])
			print(expenses)
			return expenses, total

		except Exception as e:
			raise e

	@staticmethod
	def add_expense(expense_type='', expense_cost='', expense_date=''):
		'''
		'''
		try:
			session = c_app.config.get('SESSION')
			data = ExpensesTracker(expense_type=expense_type, expense_cost=expense_cost, timestamp=expense_date)
			session.add(data)
			session.commit()

		except Exception as e:
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
			raise e