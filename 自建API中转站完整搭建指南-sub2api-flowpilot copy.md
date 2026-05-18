# 自建 API 中转站完整搭建指南：Sub2API + FlowPilot + 接码

> 本文介绍如何在一台 VPS 上自建 **AI API 中转站**：用 [Sub2API](https://github.com/Wei-Shaw/sub2api/blob/main/README_CN.md) 做配额分发与计费面板，用 [FlowPilot](https://github.com/QLHazyCoder/FlowPilot) 批量完成 OpenAI / Codex 账号注册并回写面板，邮箱推荐 **Cloudflare Temp Email**，手机验证推荐 **HeroSMS**（OpenAI 注册建议巴西号码 + API 自动化）。配套图文教程见 [FlowPilot 官方教程站](https://flowpilot.qlhazycoder.top/tutorial/)。

---

## 这套方案能做什么

自建 API 中转站的核心目标，是把多个上游 AI 订阅账号（OAuth 或 API Key）统一接入一个网关，再向终端用户分发 **API Key**，由平台完成鉴权、计费、负载均衡和请求转发。

整条链路可以概括为：

```
上游订阅账号 → Sub2API 网关 → 你的 API Key → Claude Code / Codex CLI / 其他客户端
                    ↑
         FlowPilot 自动注册并导入账号
                    ↑
    Cloudflare Temp Email（邮箱） + HeroSMS（短信）
```

**Sub2API** 负责「跑起来、管起来、算清楚」；**FlowPilot** 负责「把号注册好并塞进面板」；**Cloudflare Temp Email** 和 **HeroSMS** 分别解决邮箱验证与手机验证。

---

## 你需要准备什么

| 类别 | 建议 |
|------|------|
| 服务器 | Linux VPS（amd64 / arm64），建议 2C4G 及以上；海外机房更利于访问 OpenAI |
| 域名 | 用于 HTTPS 反代 Sub2API 面板（生产环境务必上 TLS） |
| 面板 | [Sub2API](https://github.com/Wei-Shaw/sub2api)（Go + PostgreSQL + Redis） |
| 自动化 | Chrome + [FlowPilot](https://github.com/QLHazyCoder/FlowPilot) 扩展 |
| 邮箱 | [Cloudflare Temp Email](https://flowpilot.qlhazycoder.top/tutorial/cloudflare-temp-email-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)（Worker 部署） |
| 接码 | [HeroSMS](https://hero-sms.com/?ref=509318)（OpenAI 建议巴西号 + API） |
| 代理（可选） | 干净 IP，降低注册与登录风控；FlowPilot 教程中也覆盖节点检测与代理配置 |

> **合规提示**：使用 Sub2API、批量注册 OpenAI 账号可能涉及上游服务条款与当地法律。本文仅供技术学习与正当业务场景参考，请自行评估风险，作者与站点不承担因违规使用导致的封号、封禁或其他损失。

---

## 一、部署 Sub2API 中转面板

[Sub2API](https://github.com/Wei-Shaw/sub2api/blob/main/README_CN.md) 是开源的 **AI API 网关平台**，支持多账号管理、API Key 分发、Token 级计费、并发与速率限制、内置支付等。官方演示：[demo.sub2api.org](https://demo.sub2api.org/)。

### 1.1 推荐：Docker Compose 一键部署

前置：已安装 Docker 20.10+ 与 Docker Compose v2+。

```bash
mkdir -p sub2api-deploy && cd sub2api-deploy

curl -sSL https://raw.githubusercontent.com/Wei-Shaw/sub2api/main/deploy/docker-deploy.sh | bash

docker compose up -d
docker compose logs -f sub2api
```

脚本会下载 `docker-compose.local.yml`、生成 `.env`（含 `JWT_SECRET`、`POSTGRES_PASSWORD` 等），数据落在本地目录，便于备份迁移。

首次访问：`http://你的服务器IP:8080`，按向导完成 PostgreSQL、Redis、管理员账号配置。若密码为自动生成，可在日志中查找：

```bash
docker compose logs sub2api | grep "admin password"
```

### 1.2 生产环境：Nginx 反代注意事项

若通过 Nginx 反代 Sub2API，且搭配 Codex CLI 使用粘性会话，需在 `http` 块加入：

```nginx
underscores_in_headers on;
```

Nginx 默认会丢弃带下划线的请求头（如 `session_id`），会导致多账号粘性会话失效。

### 1.3 面板里建议先完成的配置

1. **创建分组**：例如 `codex`、`claude`，与 FlowPilot 侧「分组名」保持一致。  
2. **配置代理（可选）**：在管理后台添加出站代理，供 OAuth 注册与 API 调用使用。  
3. **生成用户 API Key**：给 Claude Code、Codex CLI 等客户端使用。  
4. **（可选）简易模式**：个人自用可设 `RUN_MODE=simple` 跳过 SaaS 计费（生产需 `SIMPLE_MODE_CONFIRM=true`）。

升级：管理后台左上角「检测更新」，或执行 `docker compose pull && docker compose up -d`。

更完整的脚本安装、源码编译、安全项（URL 白名单、CORS、Turnstile 等）见 [Sub2API 中文 README](https://github.com/Wei-Shaw/sub2api/blob/main/README_CN.md)。

---

## 二、配置 Cloudflare Temp Email（推荐）

相比 DuckDuckGo 别名或手动维护 QQ/163 转发，**Cloudflare Temp Email** 更适合批量注册：每次生成独立临时邮箱，验证码由 Worker 接收，FlowPilot 通过 API 轮询，无需反复登录网页邮箱。

### 2.1 部署 Temp Email 后端

若尚未部署，可参考社区教程（FlowPilot 文档引用）：[linux.do 相关主题](https://linux.do/t/topic/316819)。

你需要准备：

- 一个已接入 Cloudflare 的域名  
- 部署好的 **Cloudflare Temp Email Worker** 地址，例如 `https://your-worker-domain`  
- 后端 `admin auth`（以及站点若启用了访问密码，则还有 `custom auth`）

### 2.2 FlowPilot 中的填写项

在 FlowPilot 侧边栏（详见 [Cloudflare Temp Email 使用说明](https://flowpilot.qlhazycoder.top/tutorial/cloudflare-temp-email-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)）：

| 配置项 | 说明 |
|--------|------|
| **Temp API** | Worker 地址，邮箱生成/收信都依赖此项 |
| **Admin Auth** | 对应后端 `admin auth`；仅作「邮箱生成」时必填 |
| **Custom Auth** | 仅站点额外设了访问密码时填写 |
| **Temp 域名** | 允许创建邮箱的基础域名（不是随机子域） |
| **随机子域** | 需后端配置 `RANDOM_SUBDOMAIN_DOMAINS`，且 DNS 已设 `MX *` |
| **邮件接收** | 作「邮箱服务」时填写真实收件邮箱（一般可留空，以 API 收信为主） |

**推荐组合**：`邮箱生成 = Cloudflare Temp Email`，`邮箱服务 = Cloudflare Temp Email`，两边字段都配齐后，Step 4 / Step 8 可全自动拉取注册码与登录码。

### 2.3 与 Cloudflare Email Routing 的区别

FlowPilot 也支持「Cloudflare 域名 + QQ/163 转发」模式（本地随机前缀 `@你的域名`）。该方式需在 Cloudflare 后台配置 Catch-all 转发，适合已有 Email Routing 的用户。

**批量自动化更省心的是 Temp Email Worker 方案**，不依赖网页邮箱登录态，也更少被邮箱服务商风控。

---

## 三、HeroSMS 接码：OpenAI 注册建议

OpenAI / ChatGPT 注册流程中，部分节点会要求**手机号验证**。推荐使用国际接码平台 **HeroSMS** 完成 **AI 接码**，并与 FlowPilot 的短信 Helper / API 对接。

- **官网**：[https://hero-sms.com/?ref=509318](https://hero-sms.com/?ref=509318)  
- **促销码**：`obvps`（充值约 15% 折扣，以官网为准）  
- **能力**：180+ 国家、网页 + API、兼容 SMS-Activate 类流程  

### 3.1 为什么 OpenAI 建议用巴西号码

经验上，OpenAI 注册对**巴西**等拉美号段的成功率与单价往往更均衡：

- 平台展示 OpenAI / ChatGPT 类服务起步价约 **$0.01–0.05**（随国家与库存浮动）  
- 在 HeroSMS 下单页选择服务 **OpenAI** 或 **ChatGPT**，国家选 **Brazil（巴西）**  
- 对比多国库存与价格后，优先选「库存充足 + 单价低」的组合  

> 接码无法保证 100% 成功，最终结果还取决于 IP 环境、浏览器指纹、注册频率等。请控制并发，避免短时间大量失败重试。

### 3.2 网页手动接码（适合试跑）

1. 注册 [HeroSMS](https://hero-sms.com/?ref=509318) 并充值（结账填 `obvps`）  
2. 搜索服务 **OpenAI**，国家选 **巴西**  
3. 复制虚拟号码到 OpenAI 验证页，在订单页等待短信  
4. 填入 6 位验证码完成验证  

### 3.3 API 自动化（适合 FlowPilot 批量）

HeroSMS 提供开发者 API，适合：

- FlowPilot 内置 HeroSMS 短信能力（见 [FlowPilot 教程总览](https://flowpilot.qlhazycoder.top/tutorial/)）  
- 自有脚本：取号 → 轮询短信 → 释放号码  

API 密钥与文档在登录后的开发者中心获取。批量场景下 **API 单价通常低于反复手动下单**，且便于与 Auto 多轮注册联动。

---

## 四、安装 FlowPilot 并对接 Sub2API

[FlowPilot](https://github.com/QLHazyCoder/FlowPilot) 是 Chrome 扩展，用于批量跑通 **ChatGPT OAuth 注册/登录**，并在 Step 10 将 `localhost` 回调提交回管理面板。

### 4.1 安装扩展

1. 打开 `chrome://extensions/`，开启「开发者模式」  
2. 「加载已解压的扩展程序」，选择 FlowPilot 项目目录  
3. 打开扩展侧边栏  

建议从 [Releases](https://github.com/QLHazyCoder/FlowPilot/releases) 下载最新打包版本，或 `git pull` 后重新加载。更新方法见 [FlowPilot 教程 · 更新扩展](https://flowpilot.qlhazycoder.top/tutorial/)。

### 4.2 来源选择：SUB2API（核心）

在侧边栏将 **来源** 设为 `SUB2API`，填写：

| 字段 | 说明 |
|------|------|
| **SUB2API** | 后台账号管理页地址，例如 `https://你的域名/admin/accounts` |
| **账号 / 密码** | Sub2API 管理员登录信息 |
| **分组** | 目标 OpenAI 分组，留空默认 `codex` |
| **默认代理** | 可选，填代理名称或 ID；留空则不附带 `proxy_id` |

流程要点：

- **Step 1**：在 Sub2API 后台生成 OAuth 授权链接  
- **Step 2–9**：自动注册、收邮箱验证码、登录、OAuth 同意  
- **Step 10**：将 `localhost` 回调中的 `code` / `state` 提交回 Sub2API，**直接创建 OpenAI 账号记录**  

这比旧版 CPA 面板方案更贴合 Sub2API 原生 API，无需适配第三方 DOM。

### 4.3 推荐配置模板（Sub2API + Temp Email + HeroSMS）

```
来源：SUB2API
邮箱生成：Cloudflare Temp Email
邮箱服务：Cloudflare Temp Email
Mail：（按你接码/收信方案，短信用 HeroSMS 时在扩展内配置对应 Provider）
```

操作顺序建议：

1. 先 **单步** 跑通 Step 1 → Step 4（确认邮箱验证码能收到）  
2. 若出现手机号验证，确认 HeroSMS 巴西号 + API 正常  
3. 再开右上角 **Auto** 多轮批量  

FlowPilot 支持 Auto 多轮、中途 Stop、账号记录面板；遇到 `max_check_attempts` 多为 Cloudflare 风控，需换 IP 或等待 15–30 分钟后再试。

### 4.4 其他来源（了解即可）

- **CPA**：传统 CPA 管理面板 OAuth 页  
- **Codex2API**：协议直连 `/api/admin/oauth/*`  

本文以 **Sub2API** 为主线，与上文部署章节一致。

更细的步骤说明、Hotmail/2925 号池、PayPal 绑卡等扩展能力，请查阅 [FlowPilot 各种配置使用教程](https://flowpilot.qlhazycoder.top/tutorial/)。

---

## 五、端到端操作流程

下面是一条可复现的「从零到出 Key」路径：

### 阶段 A：基础设施（约 30–60 分钟）

1. VPS 安装 Docker，部署 Sub2API，记录管理员账号  
2. 域名 + Nginx/Caddy 配置 HTTPS，反代到 `8080`（记得 `underscores_in_headers`）  
3. 部署 Cloudflare Temp Email Worker，记下 API 地址与 Admin Auth  
4. 注册 HeroSMS，充值并保存 API Key；试一单巴西 OpenAI 号码确认可用  

### 阶段 B：面板与代理（约 15 分钟）

1. 登录 Sub2API，创建分组 `codex`（或自定名称）  
2. 添加出站代理（如有），在 FlowPilot「默认代理」中填写  
3. 创建测试用户，生成一条 API Key 备用  

### 阶段 C：单账号试跑（约 10–20 分钟）

1. FlowPilot：`来源 = SUB2API`，填面板地址与管理员账号  
2. 配齐 Cloudflare Temp Email 各项  
3. 配置 HeroSMS（网页或 API）  
4. 单步执行 Step 1–4，确认注册邮件验证码成功  
5. 若触发手机验证，用巴西号码完成  
6. 跑完 Step 10，在 Sub2API 后台确认账号已入库且 OAuth 状态正常  

### 阶段 D：批量与交付

1. 设置 Auto 轮数与步间随机延迟，避免过快触发风控  
2. 批量完成后，在 Sub2API 为用户分发 API Key、设置余额与并发  
3. 客户端示例（Claude Code）：

```bash
export ANTHROPIC_BASE_URL="https://你的域名"
export ANTHROPIC_AUTH_TOKEN="sk-你在面板生成的Key"
```

Codex / 其他兼容客户端按 Sub2API 文档配置 Base URL 与 Key 即可。

---

## 六、客户端接入与日常运维

### 6.1 给用户分发 Key

在 Sub2API 管理后台：

- 用户注册 / 管理员创建用户  
- 为用户生成 API Key（前缀默认 `sk-`）  
- 配置余额、并发、速率倍率  

### 6.2 监控与升级

- 查看请求日志、Token 用量、账号健康状态  
- 定期 `docker compose pull && docker compose up -d` 或面板内一键升级  
- 备份 `sub2api-deploy` 整个目录（含 `postgres_data`、`redis_data`）  

### 6.3 简易自用模式

仅个人或内网团队使用时，可启用 Sub2API **简易模式**（`RUN_MODE=simple`），隐藏 SaaS 计费相关界面，降低运维复杂度。

---

## 七、常见问题

**Q：Sub2API 启动后无法访问？**  
检查防火墙是否放行 `8080`（或反代端口）、容器是否 healthy、`docker compose logs sub2api` 是否有数据库连接错误。

**Q：FlowPilot Step 4 一直收不到验证码？**  
核对 Temp API、Admin Auth、Temp 域名；随机子域需 DNS `MX *` 与后端 `RANDOM_SUBDOMAIN_DOMAINS`。先用 API 或后台手动发一封测试邮件。

**Q：OpenAI 要求手机号，HeroSMS 没收到短信？**  
换巴西以外的备用国家试单；检查订单是否超时释放；API 模式确认 service ID 与国家代码正确。

**Q：Step 10 提交回调失败？**  
确认 Sub2API 地址、管理员 session 有效；回调 URL 必须是 `http(s)://localhost:<port>/auth/callback?code=...&state=...` 格式。

**Q：Codex CLI 粘性会话不生效？**  
检查 Nginx 是否开启 `underscores_in_headers on`。

**Q：是否违反 OpenAI / Anthropic 条款？**  
Sub2API README 已声明可能违反上游 ToS，请自行阅读协议并承担风险。

---

## 八、工具与链接汇总

| 工具 | 链接 |
|------|------|
| Sub2API 项目 | [GitHub · README_CN](https://github.com/Wei-Shaw/sub2api/blob/main/README_CN.md) |
| Sub2API 在线演示 | [demo.sub2api.org](https://demo.sub2api.org/) |
| FlowPilot 项目 | [GitHub · QLHazyCoder/FlowPilot](https://github.com/QLHazyCoder/FlowPilot) |
| FlowPilot 教程站 | [flowpilot.qlhazycoder.top/tutorial](https://flowpilot.qlhazycoder.top/tutorial/) |
| Cloudflare Temp Email 教程 | [FlowPilot · Temp Email](https://flowpilot.qlhazycoder.top/tutorial/cloudflare-temp-email-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E) |
| HeroSMS 接码 | [hero-sms.com](https://hero-sms.com/?ref=509318)（促销码 `obvps`） |

---

## 总结

自建 API 中转站并不神秘：**Sub2API** 解决网关与计费，**FlowPilot** 解决账号批量入库，**Cloudflare Temp Email** 解决邮箱验证，**HeroSMS（巴西号 + API）** 解决 OpenAI 手机验证。按「先部署面板 → 再配邮箱与接码 → 单号试跑 → Auto 批量」的顺序推进，大多数卡点都出在邮箱 API 或接码国家选择上，逐项排查即可。

部署与自动化前，请再次确认使用场景符合各平台服务条款与当地法规；技术栈再完善，也无法替代合规使用。

---

## 选购与免责说明

- Sub2API、HeroSMS 的价格、功能与活动以各官网实时信息为准。  
- 本文为技术流程整理与经验分享，不构成任何商业承诺或成功率保证。  
- 请理性选购接码与服务器资源，勿将本方案用于欺诈、滥发或其他违法行为。
