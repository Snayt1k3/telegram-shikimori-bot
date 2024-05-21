from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy import String

from src.adapters.database.common.db import Base


class UserRateModel(Base):
    __tablename__ = 'user_rates'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title_id = Column(Integer, ForeignKey('titles.id'))
    target_id = Column(Integer, index=True)
    target_type = Column(String, index=True)
    score = Column(Integer)
    status = Column(String)
    episodes = Column(Integer, nullable=True)
    chapters = Column(Integer, nullable=True)
    volumes = Column(Integer, nullable=True)
    rewatches = Column(Integer, nullable=True)
