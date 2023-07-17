from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from delvify.models import Base


class TaskList(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    user_email = Column(String, index=False, nullable=False)
    title = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="list", cascade="all,delete")
