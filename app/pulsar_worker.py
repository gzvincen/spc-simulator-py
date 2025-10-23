import threading
import json
import time

import pulsar
from app import settings
from app.log import logger


class PulsarWorker:
    def __init__(self):
        self.client = pulsar.Client(settings.PULSAR_SERVICE_URL)

        # 订阅 topic1
        self.consumer = self.client.subscribe(
            settings.SPC_SIMULATOR_TOPIC, subscription_name=settings.SUBSCRIPTION_NAME
        )

        self.running = False
        self.thread = None

    def start(self):
        """启动监听线程"""
        if self.running:
            logger.info("⚠️ Pulsar Worker is already running.")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(
            f"🚀 Pulsar Worker started, listening on: {settings.SPC_SIMULATOR_TOPIC}"
        )

    def _run(self):
        """核心循环：持续监听消息"""
        while self.running:
            try:
                msg = self.consumer.receive(timeout_millis=3000)
                if not msg:
                    continue

                try:
                    data = json.loads(msg.data())
                    # data = msg.data().decode("utf-8")
                    logger.info(f"📩 Received data: {data}")

                    # 模拟业务处理逻辑
                    # do something
                    # time.sleep(1)

                    # 发送结果到 replay topic
                    # 创建 producer（replay topic）
                    data["spc-simulator-consumer-ext-info"] = "SPC-Simulator-replay-msg"
                    properties = msg.properties()
                    logger.info(f"📩 Received properties: {properties}")

                    reply_topic_ = properties["CIM_replyTopic"]
                    reply_tag_ = properties["CIM_replyTag"]
                    # handle_properties = {f"CIM2_{k}": v for k, v in properties.items()}
                    properties["MESSAGE_TAG"] = reply_tag_

                    logger.info(
                        f"📩 Reply topic: {reply_topic_}, Reply tag: {reply_tag_}"
                    )
                    logger.info(f"📩 Reply data: {data}")
                    logger.info(f"📩 Reply properties: {properties}")

                    self.producer = self.client.create_producer(reply_topic_)
                    self.producer.send(
                        content=json.dumps(data).encode("utf-8"), properties=properties
                    )
                    logger.info(
                        f"📤 Reply sent to reply topic success. topic: [{reply_topic_}], tag: [{reply_tag_}]"
                    )

                    # 正常确认消息
                    self.consumer.acknowledge(msg)

                except Exception as e:
                    logger.info(f"❌ Error processing message: {e}")
                    self.consumer.negative_acknowledge(msg)

            except pulsar.Timeout:
                # 超时只是说明暂时没消息，继续循环即可
                logger.info("⏰ Timeout 超时只是说明暂时没消息，继续循环即可")
                continue
            except Exception as e:
                # 其他异常，比如网络问题等
                logger.info(f"⚠️ PulsarWorker loop error: {e}")
                time.sleep(1)

        logger.info("🛑 Pulsar Worker stopped")

    def stop(self):
        """安全关闭 worker"""
        if not self.running:
            logger.info("⚠️ Pulsar Worker is not running.")
            return

        logger.info("🛑 Stopping Pulsar Worker...")
        self.running = False

        # 等待线程退出
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

        try:
            self.consumer.close()
            # self.producer.close()
            self.client.close()
        except Exception as e:
            logger.info(f"⚠️ Error closing Pulsar resources: {e}")


# 单例模式
worker = PulsarWorker()
