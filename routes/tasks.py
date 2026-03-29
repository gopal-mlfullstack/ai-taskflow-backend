from auth import get_current_user
from database import supabase
from fastapi import APIRouter, Depends
from models import TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/tasks")
def get_tasks(user_id: str = Depends(get_current_user)):
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    return response.data


@router.post("/tasks")
def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    data = task.dict()
    if data.get("due_date"):
        data["due_date"] = data["due_date"].isoformat()
    response = supabase.table("tasks").insert({**data, "user_id": user_id}).execute()
    return response.data


# UPDATE task
@router.put("/tasks/{task_id}")
def update_task(
    task_id: str, task: TaskUpdate, user_id: str = Depends(get_current_user)
):
    data = task.dict(exclude_unset=True)

    if data.get("due_date"):
        data["due_date"] = data["due_date"].isoformat()

    response = (
        supabase.table("tasks")
        .update(data)
        .eq("id", task_id)
        .eq("user_id", user_id)
        .execute()
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
