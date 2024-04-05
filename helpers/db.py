import json
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus

with open("settings.json") as f:
    settings = json.load(f)
    user, password, host, port, db_name = (
        settings["db"]["user"],
        settings["db"]["password"],
        settings["db"]["host"],
        settings["db"]["port"],
        settings["db"]["db_name"],
    )

# Encode the password
encoded_password = quote_plus(password)

connection_url = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{int(float(port))}/{db_name}"

engine = create_engine(connection_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session)
