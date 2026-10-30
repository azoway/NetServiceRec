# NVIDIA Build API Key 批量注册与管理：nvidia-register + YesCaptcha + somanyapikeys

想批量拿 NVIDIA BUILD 的 `nvapi` Key，再接到 OpenAI 兼容网关里统一调用，这条链路比较直接：用 [nvidia-register](https://github.com/zseek/nvidia-register) 自动注册账号并建 Key，用 YesCaptcha 过 hCaptcha，最后把 Key 批量导入 [somanyapikeys](https://github.com/azoway/somanyapikeys) 做池化和调度。

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

日常调用体验上，`deepseek-ai/deepseek-v4-flash` 通常比较顺。高峰时段热门模型更容易排队或限流，号池只能提高切换与容错，不能保证永远秒回。

## 适合谁，不适合谁

适合：

- 需要多份 NVIDIA Build `nvapi` Key，并想统一成一个 Base URL
- 已经会 Docker / 反代 / OpenAI 兼容客户端
- 能接受维护临时邮箱、打码余额、Key 存活和备份
- 想给脚本、Chat 客户端或 AI 工具接一个可轮换的上游

不适合：

- 只用一个官方网页账号，偶尔聊几句
- 不想碰邮箱、验证码、CSV 和密钥文件
- 期望“一次配置，永久免费且永远不排队”
- 不准备自行评估账号风控与服务条款风险

如果你更关心 Grok 号池，可以先看站内这篇：[Grok Token 号池：CLIProxyAPI + YesCaptcha](https://obvps.com/posts/grok-token-pool-cliproxyapi-yescaptcha-guide/)。如果只是想低成本试 DeepSeek，也可以看 [OpenModel 的 DeepSeek V4 Flash 活动介绍](https://obvps.com/posts/openmodel-deepseek-v4-flash-free-event/)。

## 整体链路

```text
临时邮箱 / DuckMail
        ↓
nvidia-register 注册 NVIDIA BUILD
        ↓
YesCaptcha 处理 hCaptcha
        ↓
创建组织 + 生成 nvapi Key
        ↓
accounts.csv（email,password,apikey）
        ↓
somanyapikeys 批量导入上游 Key
        ↓
客户端用网关访问密钥调 /v1
```

拆开后排错会轻松很多：

| 环节 | 出问题先看什么 |
|---|---|
| 邮箱 | 收不到验证码、域名被拒 |
| YesCaptcha | 余额、client key、任务超时 |
| nvidia-register | Playwright、浏览器、注册页变化 |
| somanyapikeys | 导入格式、端点、访问密钥、探测结果 |
| 客户端 | Base URL、模型名、网关密钥是否用错成 nvapi |

## 你需要准备什么

| 项目 | 作用 | 备注 |
|---|---|---|
| Python 3.11+ | 跑 nvidia-register | 再装 Playwright Chromium |
| 临时邮箱 | 接注册验证码 | 支持 `cloudflare_temp_email` 或 `duckmail` |
| YesCaptcha | 自动过 hCaptcha | 先小额测试，再批量 |
| nvidia-register | 注册 + 建 Key + 写 CSV | [GitHub 仓库](https://github.com/zseek/nvidia-register) |
| somanyapikeys | OpenAI 兼容 Key 池网关 | [GitHub 仓库](https://github.com/azoway/somanyapikeys) |
| VPS / 本机 | 跑注册脚本和网关 | 公网部署时务必 HTTPS + 强管理密钥 |
| 记录表 | 邮箱、密码、Key、状态 | CSV 可以起步，长期建议再加状态字段 |

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

打码只解决验证码这一步。邮箱质量差、IP 不稳、注册页改版、账号后续失效，都不是打码平台能兜底的。

## 第 1 步：配好 YesCaptcha

1. 打开 [YesCaptcha 注册入口](https://yescaptcha.com/i/zWdD7S)
2. 注册后充值少量余额
3. 在后台复制 client key / API Key
4. 先用单账号验证，不要一上来跑几十个

nvidia-register 的 `captcha.mode` 可设为：

- `manual`：自己点验证码
- `yescaptcha`：走 YesCaptcha 自动过 hCaptcha
- `captcharun`：另一个打码选项

批量场景一般会用 `yescaptcha`。验证码连续失败时先停，检查余额、密钥、代理和超时设置，硬重试只会烧点数。

## 第 2 步：用 nvidia-register 批量注册 NVIDIA Build

项目地址：
[https://github.com/zseek/nvidia-register](https://github.com/zseek/nvidia-register)

项目公开 README 写明的能力包括：

- 临时邮箱创建
- 注册 NVIDIA BUILD
- hCaptcha 处理
- 创建组织以跳过手机号要求
- 创建 API Key
- 成功后立即写入 CSV

安装：

```bash
git clone https://github.com/zseek/nvidia-register.git
cd nvidia-register
pip install -r requirements.txt
playwright install chromium
python main.py --init
```

编辑生成的 `config.toml`，至少确认这些字段：

```toml
email_provider = "cloudflare_temp_email"  # 或 duckmail

[cloudflare_temp_email]
api_url = "https://mail.your-server.com"
admin_auth = "your_admin_key"
domain = "your-domain.com"

[captcha]
mode = "yescaptcha"
yescaptcha_client_key = "你的YesCaptcha密钥"
yescaptcha_api_url = "https://api.yescaptcha.com"
poll_interval_seconds = 3
timeout_seconds = 180

[nvidia]
output_csv = "accounts.csv"
key_name = "api"
account_name = "NVIDIA Build"
key_expiry_date = "2126-05-08T08:00:00Z"

[browser]
headless = false
close_delay_seconds = 5
```

跑起来：

```bash
# 交互式询问数量
python main.py

# 直接指定数量
python main.py -n 3
```

成功记录大致是：

```csv
email,password,apikey
example@your-domain.com,aB3dE5fG7hI9,nvapi-xxxx...
```

建议第一次只注册 1 个账号。确认邮箱、验证码、组织创建、Key 落盘都正常后，再加量。

### 注册流程在干什么

项目 README 给出的路径是：

```text
build.nvidia.com 填邮箱
  → login.nvgs.nvidia.com 填密码 + hCaptcha
  → 邮箱验证码
  → 同意页
  → 创建组织（跳过手机验证）
  → NGC API 建 Key
  → 写入 CSV
```

中间任意一步失败，都先看这一步的日志，不要直接重开大批量。

### 注册时容易踩的坑

1. `manual` 模式必须有人点验证码，不适合无人值守。
2. 批量时每个账号是独立浏览器会话，但邮箱域名、IP 和节奏仍会影响成功率。
3. CSV 里同时有邮箱、密码和 `nvapi` Key，属于高敏感文件，别提交到公开仓库，也别贴到聊天截图里。
4. 上游页面、风控策略、Key 有效期和模型可用性都会变，脚本成功不等于 Key 永远可用。
5. 服务条款和账号政策以 NVIDIA / NVIDIA Build 实时规则为准，自行评估用途与风险。

## 第 3 步：用 somanyapikeys 管理 Key 池

项目地址：
[https://github.com/azoway/somanyapikeys](https://github.com/azoway/somanyapikeys)

somanyapikeys 是一个 OpenAI 兼容的中转 / Key 池网关。预置上游示例就是：

`https://integrate.api.nvidia.com/v1`

你也可以再加其他 OpenAI 兼容 `base_url`。对 NVIDIA Key 场景，它主要解决这几件事：

- 多 Key 导入与优先级调度
- 额度用尽、鉴权失败、限流时自动换 Key
- 用最小 `chat/completions` 做真实探测，而不是只靠 `GET /models`
- 请求日志、调度日志、模型映射
- Web 管理台批量导入

### 三种密钥不要混

| 名称 | 干什么 | 常见形态 |
|---|---|---|
| ADMIN_TOKEN | 登录管理台、调管理 API | `sk-admin-…` |
| 访问密钥 | 客户端请求本站 `/v1` | `sk-gw-…` |
| 上游 Key | 网关去调 NVIDIA 等厂商 | `nvapi-…` |

客户端永远只该拿到访问密钥。把 `nvapi` 直接发给下游，等于把上游资产交出去。

### 快速启动

本地：

```bash
git clone https://github.com/azoway/somanyapikeys.git
cd somanyapikeys
go run ./cmd/server
```

或 Docker：

```bash
docker compose up -d --build
```

首次启动会把完整凭证写到 `data/credentials.txt`，落盘加密密钥在 `data/key_encryption.secret`。日志通常只打前缀，完整密钥以本地文件为准。

打开管理台，例如 `http://localhost:8080/`，用 `ADMIN_TOKEN` 登录。然后：

1. 确认 API 端点里有 `https://integrate.api.nvidia.com/v1`，或按需新增
2. 进入 **导入**
3. 把 `accounts.csv` 里的 `apikey` 列批量贴进去
4. 绑定端点与优先级
5. 在 **探测** 里先测少量 Key
6. 在 **总览** 创建或复制访问密钥，给客户端使用

批量导入是这套面板最省事的点。注册脚本负责“产 Key”，网关负责“管 Key、换 Key、查日志”。

### 客户端怎么接

```bash
export ACCESS_KEY=sk-gw-你的访问密钥

curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer $ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/deepseek-v4-flash",
    "messages": [{"role":"user","content":"hello"}]
  }'
```

Python 示例：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-gw-你的访问密钥",
)

print(client.chat.completions.create(
    model="deepseek-ai/deepseek-v4-flash",
    messages=[{"role": "user", "content": "hello"}],
))
```

如果你做了模型映射，客户端 model 名可以和上游原始 id 不同。没有映射时，网关会按客户端传入的 model 原样转发。

## 使用体验怎么预期

结合当前公开接口形态和实际使用里比较常见的情况，可以这样预期：

1. `deepseek-ai/deepseek-v4-flash` 更适合日常脚本、总结、轻量代码和高频测试，体感通常比较顺。
2. 高峰时段热门模型更容易排队、限流或变慢。号池可以在 Key 失效、429、鉴权失败时切换，但不能消灭上游拥塞。
3. 先用小请求验证兼容性，再放进主工作流。至少确认：余额/额度、模型名、流式响应、错误码、换 Key 是否生效。
4. 模型列表和可用性会变。面板里探测通过，只代表当时那次探测链路可用，不代表永久稳定。

更稳妥的用法是：日常任务优先走更稳的模型，高峰热门模型留作补充，不要把整条业务压在单一热门模型上。

## 安全与运维检查

公网部署前至少过一遍：

1. `ADMIN_TOKEN`、访问密钥、加密密钥都用强随机值，不要用 `change-me-*`
2. 管理台和 `/v1` 走 HTTPS，反代可用 Caddy / Nginx
3. 客户端只发访问密钥，不要发 Admin Token 或 `nvapi`
4. 定期备份 `gateway.db`、`key_encryption.secret`、`credentials.txt`
5. 丢失加密密钥后，库里加密字段可能解不开，备份缺一不可
6. `/healthz` 可以公开给探活；`/metrics` 默认应保留鉴权或只给内网
7. 上游 Key 导出接口能拿到明文，管理台失陷代价很高

如果只是自己用，公网只暴露 `/v1` 和 `/healthz`，管理台走 SSH 隧道，会更省心。

## 常见问题

### 1. YesCaptcha 一定要买吗？

不是。nvidia-register 支持 `manual` 手动过验证。少量账号可以手点；批量无人值守时，YesCaptcha 更省时间。

YesCaptcha 入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

### 2. 注册成功的 Key 为什么导入后不能用？

先分清三类问题：Key 本身失效、端点写错、客户端用了错误密钥。顺序建议是：管理台单 Key 探测 → 看调度日志 → 再查客户端 Base URL / 访问密钥 / 模型名。

### 3. somanyapikeys 和直接把 nvapi 塞进客户端有什么差别？

直接塞一个 Key 最简单，但坏一个就断。网关的价值在批量导入、自动换 Key、探测、日志和统一 Base URL。Key 越多、调用方越多，差异越明显。

### 4. 热门模型排队时，多导入 Key 能立刻解决吗？

不一定。多 Key 对“单个 Key 限额/失效”更有用；如果上游整体拥塞，换 Key 也可能一起慢。这时更现实的做法是降级到更稳的模型，或错峰。

### 5. 这套方案能商用吗？

技术上你可以自建网关，但账号来源、自动化注册、对外分发是否合规，要自己对照 NVIDIA 及相关服务条款判断。工具本身不替你承担合规责任。

## 建议落地顺序

1. 先部署 somanyapikeys，确认管理台、访问密钥和健康检查正常
2. 注册 YesCaptcha，小额充值
3. 用 nvidia-register 产出 1 个账号和 1 个 `nvapi`
4. 导入网关并完成一次 `deepseek-ai/deepseek-v4-flash` 小请求
5. 再决定是否批量扩 Key
6. 给客户端固定 Base URL 和访问密钥，不要把上游 Key 散发出去

最小闭环就是：

```text
1 个邮箱方案 + 1 个 YesCaptcha Key + 1 个 nvapi + 1 次网关探测 + 1 次客户端请求
```

跑通这一条，再谈批量。批量只会放大你已经验证过的问题，也会放大你还没验证过的问题。

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

nvidia-register：
[https://github.com/zseek/nvidia-register](https://github.com/zseek/nvidia-register)

somanyapikeys：
[https://github.com/azoway/somanyapikeys](https://github.com/azoway/somanyapikeys)

本文基于 2026-07-23 公开 GitHub README、YesCaptcha 入口和 NVIDIA Build 相关公开接口形态整理。项目功能、注册策略、模型可用性、排队与限流都会变化，实际以各项目文档和实时服务页面为准。
