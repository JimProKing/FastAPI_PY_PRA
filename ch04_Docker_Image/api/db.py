# from sqlalchemy import create_engine #DB와 연결하는 엔진 만들어주는 함수
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker #DB와 소통하는 세션을 만들어주는 함수
from sqlalchemy.orm import declarative_base #ORM의 베이스 클래스


# DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8" #DB URL 설정
# 비동기 대응 함수로 수정
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

# db_engine = create_engine( #DB 엔진 생성
#     DB_URL,
#     echo=True, #SQL 쿼리 로깅 활성화
# )
# db_session=sessionmaker( #DB 세션 생성
#     autocommit=False,
#     autoflush=False,
#     bind=db_engine
# )

async_engine = create_async_engine(ASYNC_DB_URL, echo=True) #비동기 DB 엔진 생성
async_session = sessionmaker( #비동기 DB 세션 생성
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

Base = declarative_base() #ORM 베이스 클래스 생성

# def get_db(): #DB 세션을 제공하는 제너레이터 함수
#     with db_session() as session:   
#         yield session
async def get_db(): #비동기 DB 세션을 제공하는 비동기 제너레이터 함수
    async with async_session() as session:
        yield session