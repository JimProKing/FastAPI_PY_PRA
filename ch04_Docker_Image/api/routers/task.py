# app/api/routers/task.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
import api.schemas.task as task_schema
from api.db import get_db

router = APIRouter()


# 전체 작업 목록 조회 - 명시적 변환으로 안전하게
@router.get("/tasks", response_model=List[task_schema.TaskCreateResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await task_crud.get_tasks(db)
    # SQLAlchemy 객체 → Pydantic 스키마로 명시적 변환
    return [
        task_schema.TaskCreateResponse(
            id=task.id,
            title=task.title,
            done=task.done is not None  # Done 레코드 있으면 True
        )
        for task in tasks
    ]


# 새 작업 생성
@router.post("/tasks", response_model=task_schema.TaskCreateResponse, status_code=status.HTTP_200_OK)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await task_crud.create_task(db, task_body)


# 작업 완료 표시
@router.put("/tasks/{task_id}/done", response_model=task_schema.TaskDoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_crud.done_task(db, task)


# 작업 완료 해제
@router.delete("/tasks/{task_id}/done", response_model=task_schema.TaskDoneResponse)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_crud.undone_task(db, task)


# (선택사항) 작업 수정
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int,
    task_body: task_schema.TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # update_task 함수가 있다면 사용
    # return await task_crud.update_task(db, task_body, original=task)
    raise HTTPException(status_code=501, detail="Not implemented")


# (선택사항) 작업 삭제
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # delete_task 함수가 있다면 사용
    # return await task_crud.delete_task(db, original=task)
    raise HTTPException(status_code=501, detail="Not implemented")