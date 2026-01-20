# ใช้ Image พื้นฐานเป็น Python 3.9 แบบ slim (ขนาดเล็ก)
FROM python:3.9-slim

# กำหนด Folder ทำงานภายใน Container
WORKDIR /app

# Copy ไฟล์รายการ Dependencies และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy โค้ดทั้งหมดของ Service
COPY service_a/ .

# ระบุ Port ที่ต้องเปิดใช้งาน
EXPOSE 8000
EXPOSE 50051

# คำสั่งสำหรับเริ่มทำงาน Service
CMD ["python", "main.py"]
