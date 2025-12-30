# api/cruds/task.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
import api.schemas.task as task_schema


# ==================== CREATE ====================
async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_schema.TaskCreateResponse:
    """새 작업 생성"""
    db_task = task_model.Task(title=task_create.title)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    # 새 작업은 Done 레코드 없음 → done=False
    return task_schema.TaskCreateResponse(
        id=db_task.id,
        title=db_task.title,
        done=False
    )


# ==================== READ (단일) ====================
async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    """ID로 단일 작업 조회"""
    result: Result = await db.execute(
        select(task_model.Task).where(task_model.Task.id == task_id)
    )
    return result.scalars().first()


# ==================== READ (전체 목록) ====================
async def get_tasks(db: AsyncSession) -> List[task_model.Task]:
    """전체 작업 목록 조회"""
    result: Result = await db.execute(select(task_model.Task).order_by(task_model.Task.id))
    return result.scalars().all()


# ==================== DONE / UNDONE ====================
async def done_task(db: AsyncSession, task: task_model.Task) -> dict:
    """작업 완료 표시 - Done 레코드 생성"""
    if task.done is None:  # 아직 완료되지 않은 경우
        done_record = task_model.Done(id=task.id)
        db.add(done_record)
        await db.commit()
    
    return {"task_id": task.id}


async def undone_task(db: AsyncSession, task: task_model.Task) -> dict:
    """작업 완료 해제 - Done 레코드 삭제"""
    if task.done is not None:  # 완료된 상태인 경우
        await db.delete(task.done)
        await db.commit()
    
    return {"task_id": task.id}