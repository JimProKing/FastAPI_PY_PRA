# app/tests/test_main.py (최종 통과 버전 - 2025년 12월 30일 기준)

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        yield client

    app.dependency_overrides.clear()
    await async_engine.dispose()


@pytest.mark.asyncio
async def test_create_and_read(async_client: AsyncClient):
    # 1. 작업 생성
    response = await async_client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == status.HTTP_200_OK

    created_task = response.json()
    assert created_task["title"] == "Test Task"
    assert created_task.get("done", False) is False
    task_id = created_task["id"]

    # 2. 전체 목록에서 해당 task가 있는지 확인 (개별 조회 없으니까!)
    response = await async_client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK

    tasks = response.json()
    assert any(t["id"] == task_id and t["title"] == "Test Task" for t in tasks)


@pytest.mark.asyncio
async def test_done_flag(async_client: AsyncClient):
    # 1. 작업 생성
    response = await async_client.post("/tasks/", json={"title": "Task to be done"})
    assert response.status_code == status.HTTP_200_OK
    task_id = response.json()["id"]

    # 2. 완료 표시
    response = await async_client.put(f"/tasks/{task_id}/done")
    assert response.status_code == status.HTTP_200_OK

    # 3. 목록에서 done=True 인지 확인
    response = await async_client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    task = next(t for t in tasks if t["id"] == task_id)
    assert task["done"] is True

    # 4. 완료 해제
    response = await async_client.delete(f"/tasks/{task_id}/done")
    assert response.status_code == status.HTTP_200_OK

    # 5. 다시 확인
    response = await async_client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    task = next(t for t in tasks if t["id"] == task_id)
    assert task["done"] is False