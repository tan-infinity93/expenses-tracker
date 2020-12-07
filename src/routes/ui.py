'''
'''

# Import Modules:

from datetime import datetime
from flask import render_template, make_response
from flask_restful import Resource

# Class Definitions:

class HomeUI(Resource):
	'''
	'''
	def __init__(self):
		'''
		'''
		self.meta = {
			"version": 1.0,
			"timestamp": datetime.now().isoformat()
		}
		self.headers = {"Content-Type": "text/html"}
		self.success_code = 200
		self.bad_code = 400
		self.exception_code = 500

	def get(self):
		'''
		'''
		try:
			return make_response(
				render_template('index.html'), self.success_code, self.headers
			)

		except Exception as e:
			headers = {"Content-Type": "application/json"}
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, headers

class ReportsUI(Resource):
	'''
	'''
	def __init__(self):
		'''
		'''
		self.meta = {
			"version": 1.0,
			"timestamp": datetime.now().isoformat()
		}
		self.headers = {"Content-Type": "text/html"}
		self.success_code = 200
		self.bad_code = 400
		self.exception_code = 500

	def get(self):
		'''
		'''
		try:
			return make_response(
				render_template('reports.html'), self.success_code, self.headers
			)

		except Exception as e:
			headers = {"Content-Type": "application/json"}
			response = {
				"meta": self.meta,
				"message": "unable to process request"
			}
			return response, self.exception_code, headers