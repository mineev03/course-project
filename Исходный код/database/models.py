from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hall(Base):
    __tablename__ = 'halls'

    id = Column(Integer, primary_key=True)
    capacity = Column(String, nullable=False)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    id_movie = Column(Integer, ForeignKey(Movie.id))
    id_hall = Column(Integer, ForeignKey(Hall.id))
    time = Column(String, nullable=False)
    place_number = Column(String, nullable=False)
