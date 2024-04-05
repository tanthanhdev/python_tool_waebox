from sqlalchemy.orm import declarative_base
from helpers.db import db_session

Base = declarative_base()
Base.query = db_session.query_property()
