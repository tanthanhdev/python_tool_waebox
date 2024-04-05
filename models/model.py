from sqlalchemy import Column, Integer, String, MetaData, Table, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    logo = Column(String(255), nullable=False)
    link_detail = Column(String(255), nullable=False)
    # relationship
    players = relationship("Player", back_populates="team")
    # default
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'{self.name}'

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    club_number = Column(Integer, nullable=True)
    logo = Column(String(255), nullable=False)
    nationality = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    # relationship
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="players")
    # default
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'{self.name}'