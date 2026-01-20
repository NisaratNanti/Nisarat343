#grpc_client 
import grpc
import user_pb2
import user_pb2_grpc

def get_movie(movie_id: int):
    # เชื่อมต่อกับ gRPC Server ของ Service A (ใช้ชื่อ service 'service_a' ใน Docker Network)
    with grpc.insecure_channel("service_a:50051") as channel:
        # สร้าง Stub สำหรับเรียกใช้ฟังก์ชันใน UserService
        stub = user_pb2_grpc.UserServiceStub(channel)
        # สร้าง Request สำหรับดึงข้อมูลหนัง
        request = user_pb2.MovieRequest(movie_id=movie_id)
        # เรียกใช้ฟังก์ชัน GetMovie
        response = stub.GetMovie(request)

        # แปลงข้อมูลจาก gRPC Message เป็น Dictionary เพื่อส่งต่อให้ FastAPI
        return {
            "movie_id": response.movie_id,
            "title": response.title,
            "release_year": response.release_year,
            "universe": response.universe,
            "director": response.director,
            "rating": response.rating,
            "cast": [
                {
                    "actor_name": c.actor_name,
                    "character_name": c.character_name,
                    "role_type": c.role_type
                } for c in response.cast
                
            ],
            "villains": [
                {
                    "name": v.name,
                    "actor": v.actor
                } for v in response.villains
            ],
            "reviews": [
                {
                    "source": r.source,
                    "score": r.score
                } for r in response.reviews
            ]
        }

def get_user(user_id: int):
    # เชื่อมต่อกับ gRPC Server เพื่อดึงข้อมูล User
    with grpc.insecure_channel("service_a:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.UserRequest(user_id=user_id)
        response = stub.GetUser(request)

        return {
            "user_name": response.user_name,
            "email": response.email,
            "is_active": response.is_active
        }
