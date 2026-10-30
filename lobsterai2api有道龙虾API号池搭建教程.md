# 有道龙虾 LobsterAI 变 OpenAI 兼容 API：lobsterai2api 积分号池搭建教程

lobsterai2api 是一个把网易有道 LobsterAI（有道龙虾）账号变成 OpenAI 兼容接口的 Go 网关项目，项目地址在 GitHub 上，作者 xinxinshuhao-create。它支持多账号积分池，每个请求自动挑积分最多且状态健康的账号转发，积分耗尽自动冷却，对外只暴露一个固定的 Base URL 和 API Key。LobsterAI 新用户注册就送积分，搭配接码平台批量准备账号，把赠送给的积分集中到一个号池里轮换使用，这是本文说的 token 自由。

接码平台推荐白鲸（qc86.shop），中文界面，微信支付宝充值，注册入口：[白鲸接码官网](https://www.qc86.shop/login?inviterCode=300138)

## LobsterAI 是什么，为什么值得接成 API

LobsterAI（有道龙虾）是网易有道 2026 年 2 月推出的桌面级 AI Agent，定位个人助理，能跑本地任务、接飞书钉钉企微微信，代码在 GitHub 上以 MIT 协议开源，被不少人叫作中国版 OpenClaw。

对开发者更有吸引力的一点是它的模型额度。按官方应用商店页面的说明，新用户注册登录赠送 300 积分，约合百万 Token，有效期 14 天。积分在产品内按任务复杂度、模型和时长扣费。单账号这点额度跑不了几个重活，但账号多了聚起来就是一笔可观的推理额度，而且这些积分可以直接调到 DeepSeek 这类国内模型的 Pro 版本。

lobsterai2api 做的事情就是把这条链路工程化。账号的登录凭证保存成 auth 文件，网关启动时自动加载，请求进来时挑积分最高的账号发上游，出错自动换下一个。你的 ChatBox、Cursor、脚本或者别的 OpenAI 兼容客户端，只需要配一个地址一个 key，后面是十个账号还是五十个账号，客户端完全不用管。

## 这套方案适合谁

适合：

- 想给 OpenAI 兼容客户端找一个零成本推理后端的开发者
- 手里已经有多个 LobsterAI 账号，想统一管理积分和状态的人
- 在搭私有 AI API 面板，需要一个稳定上游的人
- 愿意花时间维护账号、接码和网关的人

不适合：

- 只想网页聊天不写代码的人，直接装官方客户端更省事
- 生产业务。赠送积分的发放规则、有效期和模型清单都由有道控制，随时可能调整，这套东西适合自用、测试和跑低优先级任务
- 想拿去对外卖或转售的人。LobsterAI 服务条款对账号注册和使用有明确规定，滥用批量注册的风险自己承担

## 整体链路

```text
白鲸接码拿手机号
    ↓
注册 LobsterAI 账号，登录送积分
    ↓
login.sh 完成 OAuth，导出 auths/lobsterai-<uid>.json
    ↓
lobsterai2api 加载 auths 目录，对外提供 OpenAI 兼容 API
    ↓
ChatBox / Cursor / 脚本 / 自建面板
```

每一层职责清楚。接码负责号码，注册负责攒积分，login 工具负责授权凭证，网关负责轮换和容错。哪一环出问题就查哪一环。

## 准备清单

| 项目 | 作用 | 提醒 |
|---|---|---|
| 一台服务器或本地机器 | 跑网关 | Go 环境或直接编译好的二进制，Docker 也行 |
| LobsterAI 账号 | 积分来源 | 手机号注册，新用户有赠送积分 |
| 白鲸账号 | 接收注册验证码 | 需要海外 IP，先小额充值 |
| API Key | 网关鉴权 | 自己设一个强随机串，留空则不鉴权 |
| 记录表 | 账号对应关系 | 手机号、uid、积分、状态 |

## 第一步，部署 lobsterai2api

项目用 Go 写，零外部依赖，纯标准库，编译出来就是一个二进制。

```bash
git clone https://github.com/xinxinshuhao-create/lobsterai2api.git
cd lobsterai2api
go build -o lobsterai2api.exe ./cmd/server
go build -o login.exe ./cmd/login
go build -o credit.exe ./cmd/credit
```

Windows 下 .exe 后缀照抄，Linux 下把后缀去掉就行。

运行前先写配置。项目自带 config.example.json，可以直接复制成 config.json 再改：

```json
{
  "listen": ":8367",
  "api_key": "换成你自己的强随机key",
  "auth_dir": "./auths",
  "state_file": "./data/state.json",
  "cooldown": {
    "hard_credit": "12h",
    "soft_rate": "60s",
    "err_threshold": 3,
    "err_cooldown": "10m"
  },
  "schedule": {
    "checkin_hours": [9, 21],
    "keepalive_hours": [22]
  },
  "upstream": {
    "timeout_seconds": 180
  }
}
```

`api_key` 留空就是完全不鉴权，只在内网或本机跑可以这么干。只要端口能被别的机器访问，就一定要设。

启动：

```bash
./lobsterai2api.exe -config config.json
```

默认监听 8367 端口，用 `LB2A_LISTEN` 环境变量可以改。

有一个必填项要注意。上游 API 地址和登录门户在代码里没有硬编码默认值，靠两个环境变量提供：

```bash
export LB2A_UPSTREAM_BASE="上游API地址"
export LB2A_LOGIN_PORTAL="登录门户地址"
```

不设 `LB2A_UPSTREAM_BASE` 服务起不来，不设 `LB2A_LOGIN_PORTAL` 则登录功能不可用。这两个值以项目 README 和官方客户端的实际配置为准，版本迭代后可能有变化。

## 第二步，注册 LobsterAI 账号

LobsterAI 用手机号注册登录。每个新账号的赠送积分是这套号池的燃料。

手机号不够用，就用白鲸接码。注册入口：[白鲸接码官网](https://www.qc86.shop/login?inviterCode=300138)

白鲸的详细用法本站有单独一篇介绍，见[中国接码平台推荐：白鲸](https://obvps.com/posts/中国接码平台推荐白鲸/)。这里只说关键几步：

1. 准备海外 IP，访问白鲸并注册充值，建议先小额
2. 服务列表搜 LobsterAI 或有道相关服务，选库存足的国家拿号
3. 号码填进 LobsterAI 注册页，回白鲸收验证码
4. 收不到就换号重试，别死磕一个号
5. 注册成功后把手机号、注册时间记进你的表

接码号的验证通过率不是百分之百，受号码质量和平台风控影响。第一次先手动跑一单确认流程通，再考虑批量。

关于合规说一句实话。多账号注册是否触碰服务条款的边界，要你自己评估。积分是官方发放的体验额度，规则和有效期随时可能调整，别把生产业务押在赠送额度上。

## 第三步，登录并导入账号

lobsterai2api 自带 login 工具，走的是 LobsterAI 官方 OAuth 流程。最简单的方式：

```bash
./login.sh
```

脚本会起一个本地回调服务器，打印一条授权 URL。把它复制到浏览器打开，用手机号或微信登录，回调自动完成 token 交换，凭证落盘成 `auths/lobsterai-<uid>.json`。如果检测到 Docker 容器在跑，脚本会顺手重启容器加载新账号。

手动分步跑也行：

```bash
./login.exe url   # 打印登录URL，本地回调服务器就绪
./login.exe poll  # 等回调，交换token，保存auth文件
```

每加一个账号就跑一次 login，auth 文件堆在 auths 目录里，网关启动时全部加载。

## 第四步，验证服务

先看模型列表：

```bash
curl -s http://127.0.0.1:8367/v1/models -H "Authorization: Bearer 你的key"
```

模型列表从上游动态拉取，缓存一小时，拉不到就回退静态表。README 的测试示例里出现的模型名是 `deepseek-v4-pro`，实际可用模型以接口返回为准。

发一个最小请求：

```bash
curl -s http://127.0.0.1:8367/v1/chat/completions \
  -H "Authorization: Bearer 你的key" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"你好"}],"stream":false}'
```

流式把 `stream` 改成 `true` 就行。两条都通，再把客户端接过来。

查号池状态：

```bash
curl -s http://127.0.0.1:8367/status
```

返回里能看到每个账号的积分和健康状态。

客户端接入只需要三个值。Base URL 填 `http://你的服务器:8367/v1`，API Key 填你自己设的 key，模型名从 `/v1/models` 的返回里挑。ChatBox、Cursor、OpenAI SDK 都是这个配法，具体可以参考本站的[2026 Token 自由号池搭建指南](https://obvps.com/posts/2026如何实现token自由-号池搭建指南/)，客户端接入部分是通用的。

## 号池怎么运转

这套网关的核心价值在轮换和容错逻辑，搞清楚规则才知道出问题时发生了什么。

选号策略很简单，健康账号里挑积分最高的。积分被消耗后排序自动变化，请求天然分摊。

冷却规则分四类：

| 情况 | 处理 |
|---|---|
| 积分耗尽 | 冷却 12 小时 |
| 上游 429 限流 | 软冷却 60 秒 |
| 连续错误 3 次 | 冷却 10 分钟 |
| token 刷新被拒 | 账号禁用 |

单个请求最多换 3 个账号。第一个账号失败，自动换下一个接着试，客户端那边只看到正常响应或最终报错。

后台调度器在每天 9 点和 21 点做积分刷新，22 点做 token 保活，避免长期不用的账号凭证过期。token 刷新是主动的，JWT 到期前 10 分钟就会处理。

查积分有专用工具：

```bash
./credit.sh        # 人类可读输出
./credit.exe       # JSON输出，方便脚本处理
```

有一个如实的提醒。README 明确说每日签到端点目前没有确认，DailyCheckin 还是空实现。所以积分耗尽冷却 12 小时后能不能自动恢复，取决于上游签到接口什么时候被官方确认，现阶段别指望自动回血，积分用完的账号要么等 14 天周期内的新活动，要么直接补新号。

## 配置速查

环境变量都带 `LB2A_` 前缀，可以覆盖 config.json 的值。

| 变量 | 作用 |
|---|---|
| `LB2A_LISTEN` | 监听地址，默认 :8367 |
| `LB2A_API_KEY` | 网关鉴权 key，空则不鉴权 |
| `LB2A_AUTH_DIR` | auth 文件目录，默认 ./auths |
| `LB2A_STATE_FILE` | 号池状态文件 |
| `LB2A_HARD_CREDIT` | 积分耗尽冷却时长，默认 12h |
| `LB2A_SOFT_RATE` | 429 软冷却，默认 60s |
| `LB2A_ERR_THRESHOLD` | 连续错误阈值，默认 3 |
| `LB2A_ERR_COOLDOWN` | 错误冷却，默认 10m |
| `LB2A_TIMEOUT_SECONDS` | 上游超时，默认 180 |
| `LB2A_UPSTREAM_BASE` | 上游 API 地址，必填 |
| `LB2A_LOGIN_PORTAL` | 登录门户地址，登录时必填 |

## 维护要点

号池维护的思路和 GPT 号池一致，详细的字段设计可以看本站的[2026 Token 自由号池搭建指南](https://obvps.com/posts/2026如何实现token自由-号池搭建指南/)，这里列 LobsterAI 特有的几条：

- 手机号和 uid 对应关系必须记牢。账号被禁用时你需要知道它来自哪个号码、哪次接码
- 积分有效期只有 14 天，注册完尽快接进号池用掉，攒着就是浪费
- `/status` 里的 credits 是选号依据，发现整体水位下降就该补号了
- refresh 被拒导致禁用的账号，重新跑一次 login 大概率能救回来
- 网关对上游伪装的客户端版本号是固定的，上游协议变更时等项目更新，别自己硬改

## 常见问题

### LobsterAI 的积分能撑多久

按官方商店页说明，新账号赠 300 积分约百万 Token，14 天有效。实际能跑多少任务取决于模型和任务复杂度，Pro 级模型的重活消耗会快得多。

### 白鲸的号一定能注册成功吗

不一定。验证码是否通过受号码质量、库存和国家影响，失败就换号。建议注册前先在白鲸试一单小服务确认流程，批量前先小规模验证成功率。

### 可以和其他 API 网关混用吗

可以。lobsterai2api 本身就是 OpenAI 兼容上游，接进 Sub2API、CLIProxyAPI 这类面板当一个 provider 没有问题，思路和[Grok Token 号池搭建](https://obvps.com/posts/grok-token-pool-cliproxyapi-yescaptcha-guide/)一样。

### 部署在哪个机器上合适

配置不高，纯 Go 单二进制，一台最低配 VPS 就够。注意点在于网关到有道上游的网络质量，国内服务器直连或海外服务器都先跑 `/v1/models` 测一下延迟再定。

### 会封号吗

多账号和自动化调用都在服务条款的灰色地带，官方随时可能收紧。自用小规模风险可控，大规模注册或对外转售被处理的概率很高。这个问题没有保证书，别把重要业务压上去。

## 总结

lobsterai2api 把有道龙虾的赠送积分变成了标准 OpenAI 兼容接口，Go 单文件部署不挑机器，多账号轮换和冷却逻辑开箱即用。账号侧用白鲸接码解决手机号问题，每个新号 300 积分进池轮换，对个人开发者的日常推理需求来说够用且零成本。

两个入口收好。项目地址 [https://github.com/xinxinshuhao-create/lobsterai2api](https://github.com/xinxinshuhao-create/lobsterai2api)，接码平台[白鲸注册入口](https://www.qc86.shop/login?inviterCode=300138)。

---

本文基于 2026-09-15 公开信息整理。LobsterAI 的积分规则、赠送额度、模型清单以及 lobsterai2api 的功能均可能随版本更新变化，请以官方页面和项目 README 实时内容为准。
