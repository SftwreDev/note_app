from database import Base
from models.notes import notes_tags_association
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    note_id = Column(Integer, ForeignKey('notes.id'))
    note = relationship("Notes", secondary=notes_tags_association, back_populates="tags")
