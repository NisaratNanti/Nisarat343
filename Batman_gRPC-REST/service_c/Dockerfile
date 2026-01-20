# ใช้ Image พื้นฐานเป็น Python 3.9 แบบ slim
FROM python:3.9-slim

WORKDIR /app

# Copy และติดตั้ง Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy โค้ดของ Service C
COPY service_c/ .

EXPOSE 8002

CMD ["python", "main.py"]
