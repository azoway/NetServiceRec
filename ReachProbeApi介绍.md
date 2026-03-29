# ReachProbeApi 项目简介与使用指南

> 仓库：<https://github.com/azoway/ReachProbeApi>  
> 许可：MIT

## 项目是什么

**ReachProbeApi** 是一个轻量级的 HTTP API 服务，用于对指定**域名或 IP** 与**端口**做 **TCP 可达性探测**。服务会按需解析 DNS，对解析出的地址做 IP 策略校验，再发起 TCP 连接尝试，并返回是否可达、尝试次数、耗时等信息。

适合场景包括：运维探活、网络连通性自检、脚本里快速判断「某主机某端口是否能连上」等，而不需要自己写套接字与超时逻辑。

---

## 主要特性

| 能力 | 说明 |
|------|------|
| 单文件运行 | 核心逻辑集中在 `main.py`，部署简单 |
| 配置灵活 | 支持 `config.json`，且可用环境变量覆盖 |
| 探活接口 | `POST /reachprobeapi/v1` |
| 健康检查 | `GET /healthz` |
| 可选鉴权 | 通过请求头 `X-API-Key` 启用 API Key |
| 限流 | 进程内内存限流，减轻滥用 |
| IP 策略 | 可限制私网、回环、组播、保留地址等 |
| 有界探测 | 通过时间预算等限制，避免单次请求拖很久 |

---

## 目录结构

```text
.
├── main.py
├── config.json
├── requirements.txt
└── tests/
```

---

## 快速开始

### 1. 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows 可用 .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python3 main.py
```

默认监听 **`0.0.0.0:8899`**。

### 3. 使用 PM2 守护（可选）

```bash
pm2 start main.py --interpreter python3 --name reachprobeapi
```

---

## API 说明

### `POST /reachprobeapi/v1`

对 `target` + `port` 做 TCP 探测。

**请求体示例：**

```json
{
  "target": "dns.google",
  "port": 443
}
```

`target` 可以是主机名、IPv4 或 IPv6；需要时会先 DNS 解析。

**响应体示例：**

```json
{
  "target": "dns.google",
  "port": 443,
  "resolved_addresses": ["8.8.8.8", "8.8.4.4"],
  "reachable": true,
  "attempts": 3,
  "successful_connects": 2,
  "duration_ms": 137
}
```

字段含义一目了然：`reachable` 表示是否至少有一次 TCP 连接成功；`attempts` / `successful_connects` 反映多轮探测结果；`duration_ms` 为本次请求侧耗时。

### `GET /healthz`

用于负载均衡或编排层面的存活检查：

```json
{
  "status": "ok"
}
```

---

## 使用示例（curl）

**1）探测公共 DNS 端口**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -d '{"target":"dns.google","port":53}'
```

**2）探测 HTTPS 是否可达**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -d '{"target":"example.com","port":443}'
```

**3）直接使用 IPv4**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -d '{"target":"1.1.1.1","port":443}'
```

**4）直接使用 IPv6**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -d '{"target":"2606:4700:4700::1111","port":443}'
```

**5）启用 API Key（需在配置中开启 `require_api_key` 并设置 `api_key`）**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change_me" \
  -d '{"target":"example.com","port":443}'
```

**6）用 jq 只提取关键字段**

```bash
curl -sS -X POST "http://127.0.0.1:8899/reachprobeapi/v1" \
  -H "Content-Type: application/json" \
  -d '{"target":"dns.google","port":443}' | jq '{target, reachable, successful_connects, duration_ms}'
```

---

## 配置说明

加载顺序为：**代码默认值 → `config.json` → 环境变量**（环境变量优先级最高）。

指定其它配置文件：

```bash
export IPTOOLS_CONFIG_FILE=/path/to/config.json
```

### 常用配置项

| `config.json` 键 | 环境变量 | 默认值 | 说明 |
|------------------|----------|--------|------|
| `telnet_count` | `TELNET_COUNT` | `3` | 探测轮数，范围 `1..10` |
| `telnet_timeout_sec` | `TELNET_TIMEOUT_SEC` | `1` | 单次连接超时（秒），`1..5` |
| `max_resolved_addresses` | `MAX_RESOLVED_ADDRESSES` | `4` | 最多使用几条 DNS 结果，`1..16` |
| `probe_time_budget_sec` | `PROBE_TIME_BUDGET_SEC` | `10` | 单次请求总时间上限（秒），`1..60` |
| `require_api_key` | `REQUIRE_API_KEY` | `false` | 是否要求 `X-API-Key` |
| `api_key` | `API_KEY` | `null` | API Key 明文 |
| `rate_limit_requests` | `RATE_LIMIT_REQUESTS` | `30` | 限流窗口内允许请求数 |
| `rate_limit_window_sec` | `RATE_LIMIT_WINDOW_SEC` | `60` | 限流窗口长度（秒） |
| `allow_private_ip` | `ALLOW_PRIVATE_IP` | `false` | 是否允许探测私网 IP |
| `allow_loopback_ip` | `ALLOW_LOOPBACK_IP` | `false` | 是否允许回环地址 |
| `allow_multicast_ip` | `ALLOW_MULTICAST_IP` | `false` | 是否允许多播地址 |
| `allow_reserved_ip` | `ALLOW_RESERVED_IP` | `false` | 是否允许保留地址 |
| `server_host` | `SERVER_HOST` | `0.0.0.0` | 监听地址 |
| `server_port` | `SERVER_PORT` | `8899` | 监听端口 |

### 生产环境环境变量示例

```bash
export REQUIRE_API_KEY=true
export API_KEY='replace_with_strong_key'
export RATE_LIMIT_REQUESTS=20
export RATE_LIMIT_WINDOW_SEC=60
export TELNET_COUNT=2
export TELNET_TIMEOUT_SEC=1
export MAX_RESOLVED_ADDRESSES=4
export PROBE_TIME_BUDGET_SEC=8
```

---

## 公网部署时的安全建议

此类服务若对公网开放，可能被用于**扫描他人内网或第三方资产**，需格外谨慎：

- 除非完全信任调用方，否则保持 **`ALLOW_PRIVATE_IP=false`**、**`ALLOW_LOOPBACK_IP=false`**。
- 对外暴露前务必开启 **API Key**，并配合网关做 **TLS、WAF、IP 白名单** 等。
- 在网络层尽量限制**出站访问**范围，并对进程做 CPU、内存与日志监控。

---

## 小结

ReachProbeApi 把「域名/IP + 端口 → TCP 是否可达」封装成稳定、可配置的 HTTP 接口，适合集成到自动化运维或自建探活流程中。更多细节与更新以官方仓库 README 为准：[ReachProbeApi on GitHub](https://github.com/azoway/ReachProbeApi)。
