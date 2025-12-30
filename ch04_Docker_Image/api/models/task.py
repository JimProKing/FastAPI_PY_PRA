# api/models/task.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))

    done = relationship(
        "Done",
        back_populates="task",
        uselist=False,                    # 1:1 관계 명시 (필수!)
        cascade="all, delete-orphan",     # Done 자동 삭제
        lazy="joined"                     # ← 이거 추가! lazy load 방지
    )

class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    task = relationship("Task", back_populates="done")