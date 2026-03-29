import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException
from supabase import create_client

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]

        user = supabase.auth.get_user(token)

        if user.user is None:
            raise Exception("Invalid user")
        return user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
