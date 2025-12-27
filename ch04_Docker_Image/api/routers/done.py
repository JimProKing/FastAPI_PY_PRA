from fastapi import APIRouter

router = APIRouter()


@router.put("/tasks/{task_id}/done")
async def mark_task_as_done(task_id: int):
    return {"task_id": task_id, "done": True}


@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done(task_id: int):
    return {"task_id": task_id, "done": False}