from fastapi import APIRouter, Depends

from auth import get_current_user
from database import supabase
from models import TaskCreate, TaskUpdate

router = APIRouter()


# GET all tasks for the user
@router.get("/tasks")
def get_tasks(user_id: str = Depends(get_current_user)):
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    return response.data


# CREATE task
@router.post("/tasks")
def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    response = (
        supabase.table("tasks").insert({**task.dict(), "user_id": user_id}).execute()
    )
    return response.data


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, user_id: str = Depends(get_current_user)):
    response = (
        supabase.table("tasks")
        .delete()
        .eq("id", task_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data


@router.put("/tasks/{task_id}")
def update_task(
    task_id: str, task: TaskUpdate, user_id: str = Depends(get_current_user)
):
    response = (
        supabase.table("tasks")
        .update(task.dict(exclude_unset=True))
        .eq("id", task_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data
