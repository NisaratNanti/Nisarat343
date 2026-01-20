import grpc
from concurrent import futures
import json

import user_pb2
import user_pb2_grpc

# โหลดข้อมูล Batman
with open("batman_movies.json", "r", encoding="utf-8") as f:
    data = json.load(f)["movies"]

# สร้าง Class สำหรับจัดการความต้องการ gRPC (gRPC Servicer)
class UserService(user_pb2_grpc.UserServiceServicer):

    def GetUser(self, request, context):
        # ฟังก์ชันดึงข้อมูล User ผ่าน gRPC
        return user_pb2.UserResponse(
            user_name="Ven",
            email="ven@example.com",
            is_active=True
        )

    def GetMovie(self, request, context):
        # ฟังก์ชันค้นหาข้อมูลหนัง Batman ตาม ID ผ่าน gRPC
        for m in data:
            if m["movie_id"] == request.movie_id:
                return user_pb2.Movie(
                    movie_id=m["movie_id"],
                    title=m["title"],
                    release_year=m["release_year"],
                    universe=m["universe"],
                    director=m["director"],
                    duration_min=m["duration_min"],
                    rating=m["rating"],
                    box_office=m["box_office"],
                    description=m["description"],
                    cast=[
                        user_pb2.Cast(
                            actor_name=c["actor_name"],
                            character_name=c["character_name"],
                            role_type=c["role_type"]
                        ) for c in m["cast"]
                    ],
                    villains=[
                        user_pb2.Villain(
                            name=v["name"],
                            actor=v["actor"]
                        ) for v in m["villains"]
                    ],
                    reviews=[
                        user_pb2.Review(
                            source=r["source"],
                            score=r["score"]
                        ) for r in m["reviews"]
                    ]
                )

        context.abort(grpc.StatusCode.NOT_FOUND, "Movie not found")

def serve():
    # สร้าง gRPC Server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # เพิ่ม UserService เข้ามาในระบบ
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(), server
    )
    # กำหนด Port สำหรับ gRPC Server (0.0.0.0 คืออนุญาตการเชื่อมต่อจากภายนอก)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    print("[OK] gRPC Server started on port 50051")
    # รอให้ Server ทำงานต่อไปเรื่อยๆ จนกว่าจะมีการสั่งหยุด
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
