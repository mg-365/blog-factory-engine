# diagnose_queue.py 
# Supabase에서 아직 진단되지 않은 블로그만 큐에 담고, n개씩 꺼내는 역할

from supabase import create_client, Client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "blog-factory-realdb"

def get_pending_blogs(limit: int = 5):
    result = supabase.table(TABLE_NAME).select("*").order("id", desc=False).limit(100).execute()
    blogs = result.data

    queue = []
    for blog in blogs:
        if not blog.get("사이트노출"):  # 사이트노출이 False거나 없음
            queue.append(blog)
        if len(queue) >= limit:
            break

    return queue
