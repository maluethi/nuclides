import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///nuclides.db', echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Elements(Base):
    __tablename__ = 'elements'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    Z = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(2), nullable=False)
    NStart = Column(Integer)
    NRange = Column(Integer, nullable=False)


class Nuclides(Base):
    __tablename__ = 'nuclides'

    id = Column(Integer, nullable=False, primary_key=True)
    Z = Column(Integer, ForeignKey('elements.Z'))
    N = Column(Integer, nullable=False)
    mass = Column(Float)
    mass_error = Column(Float)
    mass_excess = Column(Float)
    mass_exces_uncertainty = Column(Float)
    stable = Column(Boolean)
    abundance = Column(Float)
    abundance_error = Column(Float)
    element = relationship(Elements)
    isomer = Column(Boolean)


class Decays(Base):
    __tablename__ = 'decays'
    id = Column(Integer, primary_key=True)
    nuclide_id = Column(Integer, ForeignKey('nuclides.id'))
    nuclide = relationship(Nuclides)

    decay_mode = Column(String(10))

    branching = Column(Float)
    branching_error = Column(Float)
    branching_relation = Column(String(1))

    half_life = Column(Float, nullable=False)
    half_life_error = Column(Float)
    half_life_relation = Column(String(1))




if __name__ == '__main__':

    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
