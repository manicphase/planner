from sqlalchemy import Column, Date, Integer

from planner.model import Base


class Iteration(Base):
    __tablename__ = 'Iteration'
    id = Column(Integer, autoincrement=True, primary_key=True)
    startdate = Column(Date, nullable=False)
