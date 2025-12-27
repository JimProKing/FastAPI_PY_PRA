from fastapi import APIRouter
import api.schemas.task as task_schema


router = APIRouter()

# @router.get("/tasks")
# async def list_tasks():
#     pass

@router.get("/tasks",response_model=list[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1,title="세탁소 맡긴 것 찾으러 가기")]

@router.post("/tasks")
async def create_task():
    pass

@router.put("/tasks/{task_id}")
async def update_task(task_id):
    pass

@router.delete("/tasks/{task_id}")
async def delete_task(task_id):
    pass