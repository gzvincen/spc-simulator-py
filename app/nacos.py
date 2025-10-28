from v2.nacos import (
    NacosNamingService,
    ClientConfigBuilder,
    GRPCConfig,
    Instance,
    SubscribeServiceParam,
    RegisterInstanceParam,
    DeregisterInstanceParam,
    BatchRegisterInstanceParam,
    GetServiceParam,
    ListServiceParam,
    ListInstanceParam,
    NacosConfigService,
    ConfigParam,
)
import os
import asyncio
import yaml
import re


async def get_config(data_id: str):
    # 构建客户端配置
    client_config = (
        ClientConfigBuilder()
        .server_address(os.getenv("NACOS_ADDR", "10.140.32.24:8848"))
        .namespace_id(os.getenv("NACOS_NAMESPACE", "sv"))
        .username(os.getenv("NACOS_USERNAME", "nacos"))
        .password(os.getenv("NACOS_PASSWORD", "1qaz@2wsx"))
        .log_level("INFO")
        .grpc_config(GRPCConfig(grpc_timeout=5000))
        .build()
    )

    config_client = await NacosConfigService.create_config_service(client_config)
    content = await config_client.get_config(
        ConfigParam(data_id=data_id, group="DEFAULT_GROUP")
    )
    print("原始配置:\n", content)

    # 1️⃣ 替换 ${VAR:default} 形式的变量
    def substitute_env_vars(s):
        pattern = re.compile(r"\$\{([^:}]+)(?::([^}]*))?\}")

        def replacer(match):
            var_name, default_value = match.groups()
            return os.getenv(var_name, default_value or "")

        return pattern.sub(replacer, s)

    replaced = substitute_env_vars(content)

    # 2️⃣ 解析 YAML
    data = yaml.safe_load(replaced)
    # topic = data["getech"]["cim"]["mes"]["spc"]["topic"]
    # print("\n替换后 topic:", topic)
    return data


def get_spc_topic():
    config = asyncio.run(get_config("gom-std.yaml"))
    topic = config["getech"]["cim"]["mes"]["spc"]["topic"]
    print("\n替换后 topic:", topic)
    return topic


def get_pulsar_url():
    config = asyncio.run(get_config("gmes-common.yaml"))
    pulsar_url = config["spring"]["messagebus"]["mq"]["brokers"]
    print("\n替换后 pulsar_url:", pulsar_url)
    return pulsar_url


if __name__ == "__main__":
    # asyncio.run(get_config("gom-std.yaml"))
    topic_ = get_spc_topic()
    print("最后拿到的 topic: ", topic_)
    pulsar_url_ = get_pulsar_url()
    print("最后拿到的 pulsar_url: ", pulsar_url_)
    pass
