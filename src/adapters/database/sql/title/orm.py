from sqlalchemy import Column, Integer, String

from src.adapters.database.common.db import Base


class TitleModel(Base):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True, index=True)
    title_ru = Column(String, index=True)
    title_en = Column(String, index=True)
    image_url = Column(String)
    status = Column(String)
    score = Column(String)
    episodes = Column(Integer)
    episodes_aired = Column(Integer)
    volumes = Column(Integer)
    chapters = Column(Integer)
