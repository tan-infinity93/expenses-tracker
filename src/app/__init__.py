'''
'''

# Import Modules:

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from config import get_config

# Create Flask App Factory:

def create_app(config_name):
	app = Flask(__name__, template_folder='../templates/', static_folder='../static')
	CORS(app)
	app.config.update(get_config(config_name))

	# App Binding:

	# from bindings.flask_logger import FlaskLogger
	from bindings.flask_sqlalchemy import FlaskSqlAlchemy

	# log_app = FlaskLogger()
	# log_app.init_app(app)

	flask_sqlalchemy_app = FlaskSqlAlchemy()
	flask_sqlalchemy_app.init_app(app)

	api = Api(app, catch_all_404s=True)

	# print(app.config.keys())

	# Add API Routes:

	from routes.welcome import Welcome
	from routes.ui import HomeUI, ReportsUI
	from routes.expenses import ExpensesCategory, ManageExpenses
	from routes.expenses_reports import ExpensesReports

	api.add_resource(Welcome, '/expenses/v1/welcome', methods=['GET'], endpoint='welcome_api')
	api.add_resource(HomeUI, '/expenses/v1/home', methods=['GET'], endpoint='home_ui')
	api.add_resource(ReportsUI, '/expenses/v1/reports', methods=['GET'], endpoint='reports_ui')
	api.add_resource(ExpensesCategory, '/expenses/v1/categories', methods=['GET'], endpoint='expenses_category')
	api.add_resource(ManageExpenses, '/expenses/v1/manage-get', methods=['GET'], endpoint='expenses_get')
	api.add_resource(ManageExpenses, '/expenses/v1/manage-add', methods=['POST'], endpoint='expenses_add')
	api.add_resource(ManageExpenses, '/expenses/v1/manage-del', methods=['DELETE'], endpoint='expenses_del')
	api.add_resource(ExpensesReports, '/expenses/v1/sreports', methods=['GET'], endpoint='expenses_reports')
	return app
