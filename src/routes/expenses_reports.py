'''
'''

# Import Modules:

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
			expenses, total = FlaskSqlAlchemy.group_expense_by_date()
			response = {
				"meta": self.meta,
				"expenses": expenses,
				"total": total
			}
			return response, self.success_code, self.headers

		except Exception as e:
			# print(e)
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, self.headers