from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from delvify.models import Base


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("tasklist.id"), nullable=False)
    title = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)
    deadline = Column(DateTime, nullable=True, default=None)
    is_completed = Column(Boolean, nullable=False, default=False)
    is_notified = Column(Boolean, nullable=False, default=False)

    list = relationship("TaskList", back_populates="tasks")
