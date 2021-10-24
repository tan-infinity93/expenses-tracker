'''
'''

# Import Modules:

import traceback
from datetime import datetime
from flask import request, current_app as c_app
from flask_restful import Resource
from bindings.flask_sqlalchemy import FlaskSqlAlchemy

# Class Definitions:

class BaseResource(Resource):
	'''
	'''
	def __init__(self):
		'''
		'''
		self.meta = {
			"version": 1.0,
			"timestamp": datetime.now().isoformat()
		}
		self.headers = {"Content-Type": "application/json"}
		self.success_code = 200
		self.bad_code = 400
		self.exception_code = 500

class ExpensesReports(BaseResource):
	'''
	'''
	def get(self):
		'''
		'''
		try:
			args_data = request.args.to_dict()
			start_date = args_data.get('startdate')
			end_date = args_data.get('enddate')
			expenses, total = FlaskSqlAlchemy.group_expense_by_date(start_date, end_date)
			response = {
				"meta": self.meta,
				"expenses": expenses,
				"total": total
			}
			return response, self.success_code, self.headers

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, self.headers

class ExpensesRatio(BaseResource):
	'''
	'''
	def get(self):
		'''
		'''
		try:
			args_data = request.args.to_dict()
			start_date = args_data.get('startdate')
			end_date = args_data.get('enddate')
			monthly_salary, total = FlaskSqlAlchemy.get_expenses_ratio(start_date, end_date)
			print(monthly_salary)
			print(total)
			response = {
				"meta": self.meta,
				"ratio": round(((total * 100) / monthly_salary), 2),
				"total": total
			}
			return response, self.success_code, self.headers

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, self.headers