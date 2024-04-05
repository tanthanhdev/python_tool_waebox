from helpers.db import engine
from models.base import Base
from models.model import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def init_db():
    try:
        logging.info("Creating database tables...")
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error("Error creating database tables: %s", str(e))
    
# ------------- MAIN -------------
if __name__=="__main__": 
    # Initial database
    init_db()