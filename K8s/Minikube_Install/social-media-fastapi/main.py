from fastapi import FastAPI, HTTPException
from models import Post
from typing import Dict
from uuid import uuid4
from datetime import datetime
import time

app = FastAPI(title="Social Media API v1")

# In-memory DB
posts: Dict[str, dict] = {}

@app.get("/")
def read_root():
    return {"message": "📱 Social Media FastAPI v1 — Running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/posts")
def get_all_posts():
    return list(posts.values())

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    if post_id in posts:
        return posts[post_id]
    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/posts", status_code=201)
def create_post(post: Post):
    post_id = str(uuid4())
    post_data = {
        "id": post_id,
        "author": post.author,
        "content": post.content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    posts[post_id] = post_data
    return post_data

@app.get("/cpu")
def cpu_stress():
    end = time.time() + 5
    while time.time() < end:
        _ = 3.1415 ** 5
    return {"message": "🔥 Simulated CPU Load"}
