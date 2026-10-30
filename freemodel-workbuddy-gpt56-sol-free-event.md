# FreeModel 限时活动：WorkBuddy 配置 gpt-5.6-sol 免费使用

如果你在用 WorkBuddy，又想低成本试 `gpt-5.6-sol`，FreeModel 这次限时活动可以直接上手。活动重点不是再介绍一个聊天网页，而是把 FreeModel 的 `work` 接口接到 WorkBuddy 自定义模型里，用 `gpt-5.6-sol` 跑真实对话和编程任务。

按当前提供的信息，注册后完成首次 `15` 元充值即可参与。接口地址、模型名和 API Key 都写得很明确，配置大约 3 分钟。活动是否仍开放、免费额度和充值门槛以 FreeModel 实时页面为准。

注册入口：[FreeModel 注册入口](https://agentrouter.org/register?aff=Vnpm)

另一个值得关注的免费 AI API 网关是 AgentRouter，同样支持 Claude Code、Cline、Cursor 等工具，当前有邀请加码 $150 和高频额度补给活动：[AgentRouter 注册入口](https://agentrouter.org/register?aff=Vnpm)

配置文档：[FreeModel WorkBuddy 配置说明](https://freemodel.dev/dashboard/docs#workbuddy)

## 先说结论

这次活动适合已经会装 AI 客户端、愿意填 Base URL 和 API Key 的人。你注册 FreeModel，完成首次 `15` 元充值，创建 API Key，再把下面三项填进 WorkBuddy 自定义模型：

| 项目 | 配置值 |
|---|---|
| 接口地址 | `https://work.freemodel.dev/v1/chat/completions` |
| API Key | 在 FreeModel API 密钥页面创建 |
| 模型名称 | `gpt-5.6-sol` |

如果你只想打开网页随便聊几句，不想碰客户端配置，这篇文章的路径对你没那么友好。如果你本来就在用 WorkBuddy、Claude Code、Codex 这类工具，这次活动的价值更直接：用较小的首次充值门槛，验证 `gpt-5.6-sol` 在自己工作流里是否够稳、够快、够好用。

FreeModel 的通用接入、Claude Code、OpenAI 兼容接口和套餐逻辑，可以继续看站内这篇：[FreeModel 模型中转站推荐](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code/)。本文只聚焦 WorkBuddy 和这次 `gpt-5.6-sol` 限时活动。

## 活动信息摘要

| 项目 | 信息 |
|---|---|
| 活动内容 | WorkBuddy 配置 `gpt-5.6-sol` 免费使用 |
| 平台 | FreeModel |
| 客户端 | WorkBuddy（macOS / Windows） |
| 接口地址 | `https://work.freemodel.dev/v1/chat/completions` |
| 模型名 | `gpt-5.6-sol` |
| 使用门槛 | 注册后完成首次 `15` 元充值 |
| 配置时间 | 约 3 分钟 |
| 官方文档 | FreeModel Dashboard Docs 的 WorkBuddy 小节 |

有两点要先看清。第一，免费使用是限时活动，不是保证长期免费。第二，首次 `15` 元充值是当前参与门槛，不是模型永久价格说明。活动规则、余额到账、模型可用性和限速都可能调整，付款和接入前以官网和控制台为准。

## FreeModel 和 WorkBuddy 分别解决什么

FreeModel 是模型 API 中转入口。它的价值在 API 地址、密钥、模型列表、余额和客户端兼容，不是单纯给网页闲聊。站内旧文已经写过它同时覆盖 Claude API 格式和 OpenAI 兼容格式，适合 Claude Code、Cline、Cursor、ChatBox 和 OpenAI SDK 项目。

WorkBuddy 是桌面端 AI 客户端。这次活动的关键路径是：FreeModel 提供 `work` 接口和 `gpt-5.6-sol` 模型，WorkBuddy 通过“自定义模型”把请求打到 FreeModel。对用户来说，日常还是在 WorkBuddy 里对话，背后换成 FreeModel 的接口。

`gpt-5.6-sol` 本身是 GPT-5.6 系列里偏旗舰的路线，公开资料里多把它放在编码、知识工作、长任务协作这类场景。FreeModel 活动里的模型名是 `gpt-5.6-sol`，实际能力、延迟、上下文和计费规则仍以 FreeModel 后台和实时响应为准，不要把公开评测直接当成这个中转接口的承诺。

## 适合谁，不适合谁

更适合这些人：

- 已经在用 WorkBuddy，想接自定义模型
- 想低成本测试 `gpt-5.6-sol` 真实表现
- 会创建 API Key，会填接口地址和模型名
- 主要场景是编程辅助、文档处理、多轮对话、工具链任务
- 愿意先小额充值验证，再决定是否扩大使用

不太适合这些人：

- 只想网页聊天，不想装桌面客户端
- 不愿意完成首次充值门槛
- 对模型名、接口路径、密钥权限没有耐心核对
- 需要企业合同、强 SLA 和专属支持的生产环境
- 把“限时免费”理解成长期零成本服务的用户

## WorkBuddy 配置步骤

### 1. 注册并完成首次充值

先通过 [FreeModel 注册入口](https://agentrouter.org/register?aff=Vnpm) 注册账号。按当前活动说明，注册后完成首次 `15` 元充值，才能使用这次 WorkBuddy 免费配置路径。

注册后先检查三件事：

1. 账号余额是否到账
2. API 密钥页面能否创建 Key
3. 文档页是否仍有 WorkBuddy 配置说明

如果控制台没有显示 `gpt-5.6-sol`、`work` 接口或活动入口，先以实时页面为准，不要硬套旧截图。

### 2. 安装 WorkBuddy

WorkBuddy 支持 macOS 和 Windows。按你自己的系统去官方安装指南安装，装完先确认客户端能正常启动。

这一步不需要先接 FreeModel。先把客户端装稳，再配置自定义模型，排错会更简单。

### 3. 创建 FreeModel API Key

进入 FreeModel 的 API 密钥页面，创建一个新 Key。Key 只用于客户端调用，不要发到公开群、截图或仓库。

建议单独为 WorkBuddy 建一个 Key。如果后面还要接 Claude Code、Codex 或其他工具，分开密钥更方便排查权限和用量。

### 4. 在 WorkBuddy 配置自定义模型

启动 WorkBuddy，在对话界面底部找到模型切换入口，点击「+ 配置自定义模型」。然后按下面填写：

```text
接口地址: https://work.freemodel.dev/v1/chat/completions
API Key: 你在 FreeModel 创建的密钥
模型名称: gpt-5.6-sol
```

注意接口域名是 `work.freemodel.dev`，不是普通 `api.freemodel.dev`。这次活动明确给的是 WorkBuddy 用的 `work` 接口，路径也固定到 `/v1/chat/completions`。

模型名请原样填写 `gpt-5.6-sol`。少写、多写、大小写不一致，都可能导致客户端显示模型不存在或请求失败。

### 5. 切换模型并做第一轮测试

保存自定义模型后，在 WorkBuddy 里切换到 `gpt-5.6-sol`，先跑一轮小任务：

1. 普通中文问答，确认连通
2. 一段代码解释或小范围改写，确认编码场景可用
3. 多轮追问，确认上下文是否正常
4. 回到 FreeModel 后台看用量或余额变化

如果客户端报 401，优先检查 API Key。如果报模型不存在，优先检查模型名和活动是否仍生效。如果超时或连接失败，再看网络、接口地址和 FreeModel 服务状态。

## 配置时容易踩的坑

| 问题 | 常见原因 | 处理建议 |
|---|---|---|
| 连不上 | 接口地址写错 | 确认是 `https://work.freemodel.dev/v1/chat/completions` |
| 401 / 鉴权失败 | API Key 错误、未创建或未复制完整 | 重新创建并完整粘贴 Key |
| 模型不可用 | 模型名写错，或活动已结束 | 核对 `gpt-5.6-sol`，并查看控制台实时模型列表 |
| 能注册但不能用 | 未完成首次 `15` 元充值 | 先完成活动要求的充值门槛 |
| 客户端无响应 | WorkBuddy 未保存自定义模型，或仍停在旧模型 | 重新切换到刚配置的自定义模型 |
| 扣费看不清 | 把限时免费理解成永远不计费 | 以控制台余额、用量和活动页规则为准 |

还有一个容易混的点：FreeModel 旧文里常见的通用 API 地址是 `https://api.freemodel.dev`，适合 Claude Code、Cursor、ChatBox 这类通用接入。这次 WorkBuddy 活动单独给了 `https://work.freemodel.dev/v1/chat/completions`。两套地址不要混填。

## 建议怎么测，才算真的试过

不要只发一句“你好”就判断模型好坏。更有参考价值的测试包括：

1. 让模型解释一段你正在改的代码
2. 让它按你的仓库风格补一个小函数或修一个明确 bug
3. 给它一份需求说明，让它拆步骤
4. 连续多轮追问，看会不会丢上下文
5. 故意给错误模型名或错误 Key，看报错是否清楚

如果这些都正常，再考虑把更多日常对话或编程任务切过去。限时免费或低门槛试用不代表可以立刻替换主工作流，先验证稳定性、延迟和账单可见性更稳妥。

## 和 FreeModel 通用接入怎么配合

如果你只想在 WorkBuddy 里试 `gpt-5.6-sol`，按本文配置就够了。

如果你还想把 FreeModel 接到 Claude Code、Codex、Cursor、ChatBox 或自己的 SDK 项目，继续参考：

- [FreeModel 模型中转站推荐（中文）](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code/)
- [FreeModel review in English](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code-en/)

通用接入通常看 Base URL、API Key、模型名、`/v1/chat/completions` 或 `/v1/responses` 兼容性。WorkBuddy 这次活动则更明确：固定 `work` 接口 + `gpt-5.6-sol`。

## 注册入口

想试这次活动，按这个顺序最省事：

1. 打开 [FreeModel 注册入口](https://agentrouter.org/register?aff=Vnpm)
2. 完成注册和首次 `15` 元充值
3. 创建 API Key
4. 安装 WorkBuddy 并配置自定义模型
5. 用小任务验证 `gpt-5.6-sol`

官方配置说明：[FreeModel WorkBuddy 配置说明](https://freemodel.dev/dashboard/docs#workbuddy)

## FAQ

### 这次活动是完全免费吗？

按当前提供的信息，活动内容是 WorkBuddy 配置 `gpt-5.6-sol` 免费使用，但需要注册后完成首次 `15` 元充值。免费范围、持续时间和后续计费以 FreeModel 实时页面为准。

### 接口地址应该填哪一个？

WorkBuddy 这次活动填 `https://work.freemodel.dev/v1/chat/completions`。不要和通用 `api.freemodel.dev` 地址混用。

### 模型名怎么写？

模型名填写 `gpt-5.6-sol`。配置前最好再看一眼 FreeModel 控制台或文档，确认名称没有变更。

### 不会用 WorkBuddy 可以吗？

可以先按系统安装 WorkBuddy，再按自定义模型流程接入。如果你完全不想碰桌面客户端和 API 配置，这条活动路径就不太适合。

### 首次 15 元充值后还能退吗？

公开素材没有给出退款细则。付款前以 FreeModel 充值页、服务条款和客服说明为准。

### 这个活动适合长期主力使用吗？

它更适合先验证 `gpt-5.6-sol` 和 WorkBuddy 组合是否符合你的习惯。长期是否继续用，要看活动结束后的价格、限速、稳定性和账单是否清楚。

## 总结

FreeModel 这次限时活动的切入点很具体：WorkBuddy + `gpt-5.6-sol` + `work.freemodel.dev` 接口。对已经在用 AI 编程客户端的人，配置成本不高；注册后完成首次 `15` 元充值，填好接口、Key 和模型名，就能开始小范围实测。

如果你准备试，先从 [FreeModel 注册入口](https://agentrouter.org/register?aff=Vnpm) 进入，完成充值和 API Key 创建，再按 WorkBuddy 自定义模型流程接入。确认连通、延迟、上下文和用量都正常后，再决定要不要把更多任务切过去。

本文基于 2026-07-27 用户提供的活动信息和 FreeModel 公开入口整理。活动规则、免费额度、首次充值门槛、模型可用性和接口地址请以 FreeModel 官网实时页面为准。
