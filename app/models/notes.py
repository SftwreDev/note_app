from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

notes_tags_association = Table(
    'notes_tags', Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    tags = relationship("Tags", secondary=notes_tags_association, back_populates="note")
