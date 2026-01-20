from fastapi import FastAPI, HTTPException
from grpc_client import get_movie, get_user

# สร้าง FastAPI Application สำหรับ Service B
app = FastAPI(title="Service B (gRPC Client)")

@app.get("/movies/{movie_id}")
def read_movie(movie_id: int):
    # ดึงข้อมูลหนังจาก Service A ผ่าน gRPC
    try:
        return get_movie(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}")
def read_user(user_id: int):
    # ดึงข้อมูล User จาก Service A ผ่าน gRPC
    try:
        return get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Service B (gRPC Client)"}

@app.get("/movies")
def read_movies():
    # ตัวอย่างการดึงข้อมูลหนังหลายเรื่องพร้อมกันผ่าน gRPC โดยวนลูปดึงทีละเรื่อง
    movies = []
    for movie_id in range(1, 11):  # สมมติว่ามีหนัง ID 1 ถึง 10
        try:
            movie = get_movie(movie_id)
            movies.append(movie)
        except Exception:
            continue
    return movies


if __name__ == "__main__":
    import uvicorn
    # รัน Service B บน Port 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)