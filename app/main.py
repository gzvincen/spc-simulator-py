from fastapi import FastAPI

# app = FastAPI()

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.pulsar_worker import worker
import uvicorn
from app.utils import PORT
from app.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 启动时逻辑
    worker.start()
    yield  # ⏸️ 应用运行中
    # 🛑 关闭时逻辑
    worker.stop()


app = FastAPI(title="Pulsar FastAPI Worker", version="1.0.0", lifespan=lifespan)


# @app.on_event("startup")
# async def startup_event():
#     worker.start()
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     worker.stop()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# @app.post("/push")
# async def push_message(data: dict):
#     """手动发送消息到 topic2"""
#     import json
#
#     worker.producer.send(json.dumps(data).encode("utf-8"))
#     return {"sent": True, "data": data}


# @app.post("/reload")
# async def reload_worker():
#     """未来可以在这里添加逻辑，例如重新加载动态脚本"""
#     worker.stop()
#     worker.start()
#     return {"reloaded": True}


# 测试用，新建项目时创建的
@app.get("/")
async def root():
    return {"message": "Hello SPC Simulator"}


if __name__ == "__main__":
    logger.info("SPC Simulator Python 启动服务")
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)
