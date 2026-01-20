import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Service C (REST Client)")

# กำหนด URL ของ Service A (ใช้ชื่อ service ใน Docker Network)
SERVICE_A_URL = "http://service_a:8000"


@app.get("/")
def read_root():
    # หน้าแรกของ Service C
    return {"message": "Welcome to Service C (REST Client)"}


# ดึงข้อมูล User ผ่าน REST API จาก Service A
@app.get("/user/{user_id}")
def read_user(user_id: int):
    try:
        # ส่ง HTTP GET request ไปที่ Service A
        response = requests.get(f"{SERVICE_A_URL}/user/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


# ดึงข้อมูลหนัง Batman ทั้งหมดผ่าน REST API จาก Service A
@app.get("/movies")
def read_movies():
    try:
        response = requests.get(f"{SERVICE_A_URL}/movies")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


# ดึงข้อมูลหนัง Batman ตาม ID ผ่าน REST API จาก Service A
@app.get("/movies/{movie_id}")
def read_movie(movie_id: int):
    try:
        response = requests.get(f"{SERVICE_A_URL}/movies/{movie_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # รัน Service C บน Port 8002
    uvicorn.run(app, host="0.0.0.0", port=8002)
