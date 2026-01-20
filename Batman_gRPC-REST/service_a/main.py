import threading
import uvicorn
import json
from fastapi import FastAPI

from grpc_server import serve

# สร้าง FastAPI Application
app = FastAPI(title="Service A (Main Server)")

# -----------------------------
# Load JSON data (ตอน start app)
# -----------------------------
with open("batman_movies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# REST APIs
# -----------------------------
@app.get("/")
def read_root():
    # ส่งข้อความต้อนรับเมื่อเข้าหน้าแรก
    return {"message": "Welcome to Service A"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    # ส่งข้อมูล User (ในตัวอย่างนี้เป็นข้อมูลจำลอง)
    return {
        "user_name": "Ven",
        "email": "ven@example.com",
        "is_active": True
    }

@app.get("/movies")
def get_movies():
    # ดึงข้อมูลหนัง Batman ทั้งหมดจากไฟล์ JSON
    return data["movies"]

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    # ค้นหาหนังตาม ID ที่ระบุ
    for movie in data["movies"]:
        if movie["movie_id"] == movie_id:
            return movie
    return {"error": "Movie not found"}

# -----------------------------
# gRPC Server
# -----------------------------
def start_grpc():
    serve()

# -----------------------------
# Run servers
# -----------------------------
if __name__ == "__main__":
    # รัน gRPC Server ใน Thread แยกต่างหาก เพื่อไม่ให้บล็อกการทำงานของ REST API (FastAPI)
    threading.Thread(target=start_grpc, daemon=True).start()
    # รัน FastAPI (REST API) บน Port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
