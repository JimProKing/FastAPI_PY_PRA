# api/schemas/task.py

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str | None = Field(None, example="세탁소 맡긴 것 찾으러 가기")
    done: bool = Field(False, description="완료 플래그")


class TaskBase(BaseModel):
    title: str | None = Field(None, example="세탁소 맡긴 것 찾으러 가기")


class TaskCreate(BaseModel):
    title: str = Field(..., example="새로운 할 일")


class TaskCreateResponse(TaskCreate):
    id: int
    done: bool = False

    class Config:
        orm_mode = True  # ← 이게 없으면 from_orm()이 에러 납니다!


# done 토글 엔드포인트 응답 모델
class TaskDoneResponse(BaseModel):
    task_id: int = Field(..., example=1)

    # 이건 dict로 직접 만들기 때문에 orm_mode 필요 없음