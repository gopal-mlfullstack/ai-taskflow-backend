import os

from dotenv import load_dotenv
from fastapi import APIRouter
from groq import Groq
from groq.types.chat import ChatCompletionContentPartParam
from pydantic import BaseModel

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class AISuggestRequest(BaseModel):
    task_title: str
    task_description: str
    action: str


def build_prompt(data: AISuggestRequest):
    if data.action == "priority":
        return f"""
        Task: {data.task_title}
        Description: {data.task_description}
        Given this task, reply with only one word: low, medium, or high priority.
        """
    elif data.action == "rewrite":
        return f"""
        Task: {data.task_title}
        Description: {data.task_description}
        Rewrite this task description to be clearer and more actionable. Reply with only the rewriiten description.
        """
    elif data.action == "subtask":
        return f"""
        Task: {data.task_title}
        Description: {data.task_description}
        Break this task into 3-5 actionable subtasks. Reply as a numbered list only.
        """

    else:
        return "Invalid action"


@router.post("/ai/suggest")
def suggest(data: AISuggestRequest):
    try:
        prompt = build_prompt(data)
        messages: list[ChatCompletionContentPartParam] = [
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            max_tokens=800,
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        return {"error": "AI service temporarily unavailable", "details": str(e)}
