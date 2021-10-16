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

class MonthlySalary(BaseResource):
	'''
	'''
	def get(self):
		'''
		'''
		try:
			args_data = request.args.to_dict()
			start_date = args_data.get('startdate')
			end_date = args_data.get('enddate')

			expenses = FlaskSqlAlchemy.get_all_expenses(start_date, end_date)
			response = {
				"meta": self.meta,
				"expenses": expenses
			}
			return response, self.success_code, self.headers

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.meta,
				"message": "unable to process request",
				"e": str(e)
			}
			return response, self.exception_code, self.headers

	def post(self):
		'''
		'''
		try:
			post_data = request.get_json()
			post_data = {'salary': 76834}

			print(post_data)
			salary = post_data.get('salary')
			salary_date = datetime.strptime(
				post_data.get('salary_date', 
					datetime.now().replace(microsecond=0).isoformat()
				), 
				'%Y-%m-%dT%H:%M:%S'
			)
			FlaskSqlAlchemy.add_expense('monthly_salary', {
				'salary': salary, 'timestamp': salary_date
			})

			response = {
				"meta": self.meta,
				"message": "salary added successfully"
			}
			return response, self.success_code, self.headers

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, self.headers

	def delete(self):
		'''
		'''
		try:
			args_data = request.args.to_dict()
			expense_id = args_data.get('expense_id')
			FlaskSqlAlchemy.delete_expense(expense_id)

			response = {
				"meta": self.meta,
				"message": "salary deleted successfully"
			}
			return response, self.success_code, self.headers

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, self.headers