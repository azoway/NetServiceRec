# Grok Token 号池怎么搭：CLIProxyAPI、grok-build-auth 和 YesCaptcha 的一条实用链路

这里说的 Grok Token 自由，不是找一个神奇脚本，也不是保证你能无限白嫖 Grok。更实际的做法是把可用的 Grok Build 账号接进 CLIProxyAPI，用多个 auth 文件做轮换和备用。账号失效了能定位，授权过期了能重跑，客户端不用到处改配置。

这条链路里，CLIProxyAPI 负责对外提供 OpenAI 兼容接口，grok-build-auth 负责 x.ai 注册、SSO、Grok Build OAuth 和导出 `type=xai` auth 文件。YesCaptcha 只处理 Turnstile 打码这一环，别指望它替你解决邮箱、IP、风控和账号质量问题。

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

## 先判断你需不需要号池

如果你只是偶尔打开 Grok 网页聊天，没必要折腾这一套。直接用官方账号最省事。

这篇更适合下面几类人：

- 已经在跑 CLIProxyAPI，想把 Grok Build 也接进去
- 有多个自有 Grok / x.ai 账号，需要统一管理状态
- 想给 OpenAI 兼容客户端、AI 编程工具或自建面板提供一个固定 Base URL
- 能接受维护邮箱、代理、auth 文件和失败记录

不适合的场景也很明确：只用一个网页账号、不想维护邮箱和代理、不想看日志，或者希望工具替你处理所有失败。号池不是魔法，后面这些问题都会来。

## 整体结构

实际跑起来大概是这样：

```text
邮箱或邮箱域名
    ↓
grok-build-auth 注册 x.ai 账号并完成 SSO
    ↓
YesCaptcha 处理 Turnstile
    ↓
完成 Grok Build OAuth PKCE
    ↓
导出 CLIProxyAPI 可读的 type=xai auth JSON
    ↓
CLIProxyAPI 读取 auth-dir，对外提供统一 API
```

这个结构的好处是排错不混乱。验证码失败看 YesCaptcha 和代理，收不到验证码看邮箱，OAuth 卡住看 grok-build-auth 的登录链路，客户端 401 看 CLIProxyAPI 里加载的账号状态。

## 需要准备什么

| 项目 | 作用 | 提醒 |
|---|---|---|
| CLIProxyAPI | 对外提供兼容 API | 先确认服务、配置和 auth-dir 正常 |
| grok-build-auth | 注册、SSO、OAuth、导出 auth | Python 3.9+，依赖看项目 requirements |
| YesCaptcha API Key | 处理 Turnstile | 先小额充值测试，不要直接批量跑 |
| 邮箱方案 | 接收 x.ai 验证码 | tempmail 快，自有域名更适合长期维护 |
| 代理 | 保持注册和 OAuth 环境稳定 | 稳定比频繁切换重要 |
| 记录表 | 记录邮箱、代理、auth、状态 | 后期排错全靠它 |

YesCaptcha 公开资料里常见换算是 `1 元 = 1000 points`。普通图片识别可以很便宜，Turnstile 通常高一些，常见区间大约 25 到 30 points 一次。具体价格、赠送和任务类型以 YesCaptcha 后台实时页面为准。

## CLIProxyAPI 这一层先跑稳

别一上来就注册账号。先把 CLIProxyAPI 跑稳。

至少确认这些点：

- 服务能启动
- 配置文件路径没错
- `auth-dir` 存在，进程有读写权限
- 管理接口或面板能看到账号状态
- 客户端能用测试 API Key 发一个小请求

CLIProxyAPI 的 README 提到它支持 OpenAI、Gemini、Claude、Codex、Grok 兼容接口，也支持 Grok Build OAuth、多账号负载均衡、流式响应、工具调用和多模态输入。对这篇文章来说，最重要的是它能读取 xAI / Grok 的 auth 文件，然后把后端账号变成统一 API。

如果网关本身不稳定，后面导入十个 auth 文件也只是把问题放大。

## grok-build-auth 这一层做什么

项目地址：
[https://github.com/dongguatanglinux/grok-build-auth](https://github.com/dongguatanglinux/grok-build-auth)

grok-build-auth 跑的是 x.ai / Grok 公开 Web 认证链路。项目文档里给出的核心路径是：

```text
注册
  → SSO
  → Grok Build / CLI scope OAuth PKCE
  → 导出 CLIProxyAPI auth JSON
```

这里有个容易误解的点。SSO session 不是 CLIProxyAPI 能直接用的 auth 文件。必须继续完成 OAuth，拿到 `access_token` 和 `refresh_token`，再导出 `type=xai` JSON。

常见环境变量大概这些：

| 变量 | 用途 |
|---|---|
| `YESCAPTCHA_API_KEY` | Turnstile 打码 |
| `TEMPMAIL_API_KEY` | 使用 tempmail 时需要 |
| `CLOUDFLARE_API_TOKEN` | 使用 Cloudflare 邮箱助手时需要 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账户 ID |
| `CLOUDFLARE_D1_DB_ID` | Cloudflare D1 数据库 ID |
| `ALIAS_MAIL_DOMAINS` | 可控邮箱域名，多个用逗号分隔 |
| `CLIPROXYAPI_AUTH_DIR` | auth 导出目录 |
| `HTTPS_PROXY` / `HTTP_PROXY` | 代理 |

`.env`、auth JSON、邮箱 token、代理密码都算敏感信息。不要放公开仓库。私有仓库也要想清楚权限和泄露风险。

## YesCaptcha 只负责验证码

x.ai 注册过程里可能遇到 Cloudflare Turnstile。grok-build-auth 通过兼容 `createTask` 协议的打码服务处理，YesCaptcha 可以放在这里。

操作上不复杂：

1. 注册 YesCaptcha。
2. 充值少量余额。
3. 复制 API Key。
4. 写进 `.env` 或环境变量。
5. 单账号测试。

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

如果 Turnstile 连续失败，先停。检查余额、API Key、代理、站点参数和任务类型。很多失败不是打码平台贵不贵的问题，而是 IP 或请求环境已经不对了。

## 第一次怎么跑

第一次只跑一个账号。别批量。

### 1. 建好 CLIProxyAPI 的 auth 目录

确认 CLIProxyAPI 的 `auth-dir` 指向一个固定目录。建议先用测试目录，别直接动生产号池。目录权限要让 CLIProxyAPI 能读取，也要让 grok-build-auth 能写入。

### 2. 准备 grok-build-auth

项目地址：
[https://github.com/dongguatanglinux/grok-build-auth](https://github.com/dongguatanglinux/grok-build-auth)

按项目 README 安装依赖。大致会是这个顺序：

```bash
git clone https://github.com/dongguatanglinux/grok-build-auth.git
cd grok-build-auth
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

然后填写 YesCaptcha、邮箱、代理和 `CLIPROXYAPI_AUTH_DIR`。真实密钥不要写进博客、截图或公开 issue。

### 3. 先确认邮箱能收信

邮箱是这套链路里最容易被低估的一环。tempmail 适合快速试跑，自有域名邮箱更适合长期维护。无论选哪种，都要能把邮箱和 auth 文件对应起来。

后面账号失效时，你需要知道这个账号来自哪个邮箱、哪次注册、哪个代理出口。没有记录，排错会很痛苦。

### 4. 跑完整注册和 OAuth

一轮成功的结果应该包括：

- x.ai 邮箱验证码能收到
- Turnstile 能通过
- SSO session 能拿到
- Grok Build OAuth 能完成
- 本地生成 `type=xai` auth JSON
- CLIProxyAPI 能加载这个文件

中间哪一步失败，就只查那一步。不要把验证码失败、OAuth 失败、auth 加载失败混在一起处理。

### 5. 用最小请求测试

新账号导入 CLIProxyAPI 后，先发一个很小的请求。确认 Base URL、API Key、模型名和上游账号状态都对，再放进正式分组。

不要刚导入就拿大上下文请求压它。新账号是否稳定，要先看小请求和管理日志。

## 号池维护比注册更重要

号池不是 auth 文件越多越好。能知道哪个账号为什么挂掉，才有意义。

建议记录这些字段：

| 字段 | 用处 |
|---|---|
| 邮箱 | 找回、验证、定位批次 |
| 注册时间 | 判断是不是某天接口或风控变化 |
| 代理出口 | 复盘成功率 |
| YesCaptcha 状态 | 区分打码失败和后续失败 |
| auth 文件名 | 对应 CLIProxyAPI 账号 |
| 当前状态 | 可用、失效、待验证、暂停 |
| 最近错误 | 401、403、quota、refresh 失败 |

如果一批账号同时出问题，先看共同点：邮箱域名、注册时间、代理出口、验证码成功率。不要一上来逐个删 auth 文件。

## 常见坑

### Turnstile 一直不过

先查 YesCaptcha 余额和 API Key，再查代理和任务参数。连续失败时不要硬重试，同一套坏环境只会烧点数。

### 邮箱验证码收不到

检查邮箱 API、域名 DNS、收信规则和 token 权限。临时邮箱方便，但长期号池更建议用可控域名，至少方便追踪。

### SSO 有了，auth 文件没有

这很正常。SSO 不是最终产物。继续完成 Grok Build OAuth PKCE，拿到 access token 和 refresh token 后才有 CLIProxyAPI 可用的 auth JSON。

### CLIProxyAPI 看不到账号

优先查目录。`CLIPROXYAPI_AUTH_DIR` 和 CLIProxyAPI 配置里的 `auth-dir` 是否真是同一个路径？文件权限对不对？服务有没有热加载或重启？

### 客户端返回 401 或 403

先区分是客户端 API Key 错，还是上游 Grok auth 失效。用 CLIProxyAPI 管理端、日志和单账号测试来拆，不要直接把整批号判死。

## 成本怎么估算

不要只看单次 Turnstile 价格。真实成本包括打码、邮箱、代理、VPS、失败重试和人工维护。

更靠谱的算法是先跑一小批，比如 5 到 10 个自有测试账号，记录每个成功账号平均消耗多少次 Turnstile、多少次邮箱重试、多少次代理调整。这个数字比理论单价更接近你的实际成本。

YesCaptcha 注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

## FAQ

### Grok Token 号池能永久免费吗

不能这么算。就算账号本身有免费额度，打码、邮箱、代理、VPS 和维护时间也有成本。平台规则变化后，免费额度也可能消失。

### grok-build-auth 是 xAI 官方工具吗

不是。它是协议研究客户端，不是 xAI 官方 SDK。安装和参数以项目 README 为准。

### auth JSON 能不能提交到 Git

公开仓库不要提交。auth JSON、`.env`、邮箱 token、代理密码都算凭据。私有仓库也要控制访问权限。

### 能不能一开始就并发注册

不建议。先单账号跑通，再小批量测成功率。基础配置错了，并发只会放大错误。

## 最后建议

从零开始时，先跑一条最小链路：一个邮箱、一个 YesCaptcha API Key、一个 Grok 账号、一个 `type=xai` auth 文件、一次 CLIProxyAPI 小请求。

这条链路稳定后，再考虑增加账号数量。不要把“号池规模”放在“可维护性”前面。Grok Token 号池真正麻烦的地方不是注册第一批账号，而是过几天、过几周以后，你还能不能看懂每个账号为什么可用或不可用。

本文基于 2026-07-14 公开 GitHub 项目 README 和 YesCaptcha 费用资料整理。CLIProxyAPI、grok-build-auth、YesCaptcha、x.ai / Grok 的接口、价格、风控和服务条款可能随时变化，实际操作请以官方页面和项目文档为准。
