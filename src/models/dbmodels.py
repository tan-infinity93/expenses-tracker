'''
'''

# Import Modules:

import json
from datetime import datetime, date
from flask import current_app as c_app
from sqlalchemy import (
	Column, Boolean, Integer, Float, String, Date, DateTime, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy ORM Object:

Base = declarative_base()

# Model Classes:

class ExpensesTracker(Base):
	'''
	'''
	__tablename__ = 'expenses_tracker'
	id = Column(Integer, primary_key = True)
	expense_type = Column(String)
	expense_cost = Column(Float)
	timestamp = Column(DateTime, default = datetime.now)

	def sqlalchemy_encoder(self):
		'''
		'''
		try:
			serialized_data = {}
			for k,v in self.__dict__.items():
				if k != '_sa_instance_state':
					if isinstance(v, datetime):
						serialized_data[k] = v.isoformat()[:10]
					else:
						serialized_data[k] = v
			return serialized_data

		except Exception as e:
			raise e