import logging
import os
import socket
import threading
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from app.utils import PORT
from app.utils import get_local_ip

# 服务标识
SYSTEM_NAME = "spc-simulator-py"

# 日志目录与路径
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"{SYSTEM_NAME}.log")


# 日志格式器
class LogStyleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )
        level = f"[{record.levelname:<5}]"
        thread_name = f"[{threading.current_thread().name}]"
        location = f"[{record.module}:{record.funcName}:{record.lineno}]"
        host = f"[{get_local_ip()}:{PORT}]"
        trace_id = "[NONE]"  # 可替换为 MDC 中的 request id 等
        system = f"[{SYSTEM_NAME}]"

        message = record.getMessage()
        return f"{timestamp} {level} {thread_name} {location} {system} {trace_id} {host} {message}"


# 配置 logger
logger = logging.getLogger("spc-simulator-py")
logger.setLevel(logging.INFO)

# 文件 handler（每日生成新文件，保存7天）
file_handler = TimedRotatingFileHandler(
    LOG_FILE, when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
file_handler.setFormatter(LogStyleFormatter())

# 控制台 handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LogStyleFormatter())

# 防止重复添加 handler
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

__all__ = ["logger"]
