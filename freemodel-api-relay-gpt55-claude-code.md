# FreeModel 模型中转站推荐：Claude Fable 5、gpt-5.5、Claude Code 和 OpenAI 兼容 API 使用指南

如果你正在找一个能同时兼容 Claude Code、Cline、Cursor、ChatBox 和 OpenAI SDK 的模型中转站，FreeModel 可以先放进候选名单。它的定位比较明确：一边提供原生 Claude API 格式，方便 Claude Code、Cline 以及 Anthropic SDK 应用接入；另一边兼容 OpenAI 生态，常见的 Cursor、ChatBox、OpenAI SDK、ChatGPT SDK 项目都可以按 OpenAI 接口方式测试。

FreeModel 当前更适合两类人。第一类是经常折腾 AI 编程工具的人，希望一个 API 地址同时跑多个客户端；第二类是想测试 `gpt-5.5`、Claude Fable 5 这类模型的人，先用注册奖励或小额余额跑自己的真实任务，再决定是否长期充值。

注册入口：[FreeModel 注册入口](https://freemodel.dev/invite/FRE-cb3115a9)

## FreeModel 是什么

FreeModel 可以理解为一个面向开发者和 AI 工具用户的模型 API 中转站。它不是单纯给网页聊天用的站点，重点在 API 接入、模型路由、余额消费和不同客户端兼容。

从目前提供的信息看，它主要覆盖两套接口形态：

- Claude API 格式，适合 Claude Code、Cline、Anthropic SDK 相关应用
- OpenAI 兼容格式，适合 Cursor、ChatBox、OpenAI SDK、ChatGPT SDK 生态工具

这类平台的价值不在于界面多漂亮，而在于接入成本低。你拿到 API Key，配置好 `base_url` 和模型名，就可以在不同客户端里测试同一个服务。

## 注册奖励和充值逻辑

FreeModel 当前的注册激励比较直接：注册后绑定手机号可获得 10 美元余额。这个余额更适合拿来做真实测试，而不是只发一两句“你好”。建议至少测试这几类场景：

1. Claude Code 或 Cline 中的小型代码修改任务
2. Cursor、ChatBox 里的日常问答和长文本处理
3. OpenAI SDK 的 `/v1/chat/completions` 调用
4. Responses API 的多轮对话和流式输出
5. 你自己最常用的中文、英文、代码混合提示词

模型中转站最重要的是稳定性、兼容性和计费清晰度。注册送的余额刚好可以先跑一轮，不用一上来就充值。

## Claude Fable 5 已上线

按用户提供的信息，Claude Fable 5 已经在 FreeModel 上线，并且可以立即通过 API 使用。需要注意的是，Claude Fable 5 的价格是 Opus 的 2 倍，原因是模型能力更高，同时可用性更有限。

这类高价模型不建议直接拿来跑无差别闲聊。更适合用在你确实需要强模型的场景，例如复杂代码修改、长上下文分析、架构评审、难题推理或高价值内容处理。普通问答、短文本改写和轻量脚本任务，可以先用更便宜的模型测试。

## FreeModel 价格：余额充值和月付套餐不是一回事

FreeModel 的计费需要先分清两件事：余额充值和月付套餐。

余额充值是可消费余额。月付套餐是限速等级，不是余额。简单说，余额不够就充值；遇到 rate limit 就升级套餐。

## 一次性 API 余额充值

用户提供的信息里，FreeModel 的一次性充值项为 `$30 API Credits`，不同支付方式价格如下：

| 支付方式 | 地区 | 价格 |
|---|---|---|
| UPI | India | ₹99.00 |
| Card | India | ₹119.60 |
| Card | UK / International | £0.90 |
| Crypto | USDT | 1.22 USDT |

这部分是可消费余额，没有 rate limit、没有过期时间。不同地区、支付方式和结算汇率可能导致最终 checkout 价格略有变化，付款前看 FreeModel 实时页面。

## 月付套餐和限速

FreeModel 的月付套餐主要决定 rate limit，不等于购买同等金额的余额。按用户提供的信息，当前套餐如下：

| 套餐 | 英镑/月 | 约美元 | 约印度卢比 | 约人民币 |
|---|---:|---:|---:|---:|
| Pro | £5 | $6.67 | ₹664 | ¥46 |
| Pro+ | £10 | $13.35 | ₹1,329 | ¥92 |
| Max | £20 | $26.69 | ₹2,658 | ¥185 |
| Ultra | £100 | $133.45 | ₹13,289 | ¥924 |
| Power | £200 | $266.90 | ₹26,578 | ¥1,847 |

对应的 rate limit：

| 套餐 | 5 小时窗口 | 7 天窗口 |
|---|---:|---:|
| Pro | $10 / 5h | $66 / 7d |
| Pro+ | $20 / 5h | $132 / 7d |
| Max | $40 / 5h | $264 / 7d |
| Ultra | $200 / 5h | $1,320 / 7d |
| Power | $400 / 5h | $2,640 / 7d |

如果只是想确认客户端能不能连通，先用注册奖励或小额余额测试就够了。如果你已经把 FreeModel 接到 Claude Code、Cursor 或自己的 API 网关里，并且频繁碰到 rate limit，再考虑 Pro、Pro+ 或更高套餐。

## 怎么选：余额不够充值，限速不够升级

FreeModel 的选择逻辑可以压缩成两句话：

- Rate limited：升级月付套餐
- Need more balance：充值 API Credits

这点很重要。不要把月付套餐当成“买了多少余额”，也不要以为充值余额能自动提高 rate limit。长期使用前，先看自己的瓶颈到底是余额消耗还是限速窗口。

## 支持哪些接口

FreeModel 同时提到了两个常用接口：`/v1/chat/completions` 和 `/v1/responses`。这两个接口看起来相近，实际使用场景不一样。

### /v1/chat/completions

`/v1/chat/completions` 是经典的对话补全接口。它是无状态接口，每次请求都需要把完整的 `messages` 历史一起传过去。

它的优点是兼容性最好。很多工具、SDK、旧项目、脚本和网关默认都支持这个接口。你如果只是想把 FreeModel 接到 OpenAI SDK、ChatBox 或某个已有项目里，通常先从这个接口试起。

适合场景：

- OpenAI SDK 老项目迁移
- ChatBox 这类桌面客户端
- 自己写脚本调用模型
- 兼容性优先的 API 网关

### /v1/responses

`/v1/responses` 是新版 Responses 接口。它支持通过 `previous_response_id` 做有状态多轮对话，也提供更丰富的流式事件。官方描述里还提到内置文件搜索、代码解释器等工具能力。

如果你的客户端已经支持 Responses API，或者你在做更复杂的 Agent 工作流，优先测试这个接口更合适。它比传统 chat completions 更像新一代应用接口，不只是简单问答。

适合场景：

- 需要有状态多轮对话的应用
- 更复杂的 Agent 工作流
- 希望使用更丰富流式事件的客户端
- 后续可能接文件搜索、代码解释器等工具能力的项目

## Claude Code、Cline 怎么接

FreeModel 提供原生 Claude API 格式，所以对 Claude Code、Cline 这类 Anthropic API 生态工具比较友好。实际配置时，重点看三项：

- API 地址：`https://api.freemodel.dev`
- API Key：在 FreeModel 后台获取
- 模型名：按平台后台实际可用模型填写

如果工具允许自定义 Anthropic Base URL，就把地址改为 FreeModel 的 API 地址，再填入 API Key。模型名不要凭感觉写，优先复制后台或文档里给出的可用名称。

有一点容易误解：当你的工作流使用 fan-out 或 sub-agents 时，编排器可能会给不同子任务自动分配不同模型。你选择的模型处理主 agent，但子任务可能跑在其他模型上。这通常是预期行为，不一定是 FreeModel 或 Claude Code 的 bug。

## OpenAI 生态工具怎么接

OpenAI 兼容是 FreeModel 的另一个重点。Cursor、ChatBox、OpenAI SDK、ChatGPT SDK 这类工具通常都支持配置自定义 API 地址。

通用思路如下：

```text
Base URL: https://api.freemodel.dev
API Key: 在 FreeModel 后台创建
接口: /v1/chat/completions 或 /v1/responses
模型: gpt-5.5、Claude Fable 5 或后台实际支持的模型名
```

如果你的工具只支持 OpenAI Chat Completions，就先用 `/v1/chat/completions`。如果工具已经支持 Responses API，可以再测试 `/v1/responses`，尤其是多轮上下文和流式输出是否符合预期。

## Hermes Agent 配置示例

如果你用 Hermes Agent，可以按下面思路增加一个 FreeModel provider。用户提供的配置片段如下：

```toml
model_provider = "freemodel"
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
disable_response_storage = true
preferred_auth_method = "apikey"

[model_providers.freemodel]
name = "freemodel"
base_url = "https://api.freemodel.dev"
wire_api = "responses"
```

这段配置的重点有三个。`wire_api = "responses"` 表示走 Responses API，而不是传统 chat completions。`model = "gpt-5.5"` 指定默认模型。`disable_response_storage = true` 更适合不希望服务端保存响应内容的使用习惯。

API Key 仍然需要按 Hermes 当前配置方式单独放到安全位置，不建议直接写进公开文章或公开仓库。不同版本 Hermes 的配置字段可能会调整，实际以你本机 `hermes config` 和 FreeModel 后台为准。

## 413 Payload Too Large 怎么处理

如果遇到 `413 Payload Too Large`，先看请求体大小。按用户提供的 FAQ：

| 等级 | 请求体限制 |
|---|---:|
| Tier 0 | 3MB |
| Tier 1+ | 5MB |

减少 413 的办法很直接：

- 媒体文件尽量控制在 1MB 以内
- 用文件路径引用本地文件，不要把媒体直接嵌入请求体
- 长上下文拆成更小的请求
- 多轮任务尽量分阶段提交，不要一次塞完整项目和所有日志

Claude Code、Cline、Cursor 这类工具在 agent 工作流里很容易把上下文越堆越大。遇到 413 时，不要只盯着模型名，先看请求体里是否包含大文件、截图、日志或重复上下文。

## 403 ip_account_conflict 是什么

如果看到下面这种错误：

```text
403 permission_error: ip_account_conflict
This IP is already linked to another free account.
Only one free account is allowed per IP address.
```

意思是当前 IP 已经绑定过另一个免费账户。FreeModel 的免费账户规则是一个 IP 只允许一个免费账户，主要是为了防止滥用。

合规处理方式有三个：

- 升级到付费套餐，付费套餐不受免费账户 IP 限制
- 如果你在公司、宿舍、机房或共享网络下误伤，换到自己的手机网络或家庭网络
- 按官方 FAQ 使用干净网络环境，但不要用它批量创建多个免费账户

这类限制不要硬绕。中转站账户长期使用看的是稳定余额、稳定 IP 和清楚的账单，不是反复注册免费号。

## 为什么 Claude 跑几轮后变慢

Claude Code 或类似 agent 工具跑几轮后变慢，常见原因不是模型突然坏了，而是会话上下文变大了。每次消息、工具调用、文件片段和日志都会进入上下文。几轮大型任务之后，模型每次响应都要处理一大段历史，自然会慢。

处理办法很简单：开新会话。把一个会话控制在一个主题或一个任务里，任务完成后清空上下文重新开始。这样比在同一个会话里无限追加问题更稳定，也更容易控制费用。

## 适合谁使用

FreeModel 更适合下面这些用户：

- 经常使用 Claude Code、Cline、Cursor、ChatBox 的开发者
- 想用一个 API 地址接入多个 AI 客户端的人
- 想测试 `gpt-5.5`、Claude Fable 5 等模型实际表现的人
- 已经会配置 OpenAI Base URL 和 API Key 的用户
- 想先用注册奖励或小额余额验证服务质量的人

不太适合的人也很明确：

- 完全不懂 API 配置，只想网页聊天的人
- 对模型名称、接口格式、计费方式没有耐心确认的人
- 需要强 SLA、企业合同和正式技术支持的生产环境团队
- 不愿意自己测试兼容性的用户

中转站的体验很依赖具体客户端、模型、时间段和网络环境。注册送余额能解决试错成本，但不能替代自己的实测。

## 使用前建议先检查这几项

注册后不要急着把所有工具都切过去。建议按下面顺序测试：

1. 先在后台确认余额、API Key 和可用模型列表
2. 用 ChatBox 或一个简单脚本测试最基础的对话
3. 再接 Cursor、Claude Code 或 Cline
4. 分别测试中文、英文、代码任务和长上下文
5. 检查账单消耗是否符合预期
6. 确认失败请求、超时请求是否有合理提示
7. 故意跑一次接近真实工作流的任务，看 5 小时窗口和 7 天窗口是否够用

如果你要长期使用，还要重点看并发、限速、余额扣费、模型上下架通知和接口错误信息。模型中转站最怕“能用但不稳定”，所以第一次测试要尽量贴近自己的真实工作流。

## 注册入口

FreeModel 当前的核心吸引点是注册绑手机号送 10 美元余额，同时覆盖 Claude API 和 OpenAI 兼容接口，并提供 Claude Fable 5、gpt-5.5 等模型路线。

注册入口：[FreeModel 注册入口](https://freemodel.dev/invite/FRE-cb3115a9)

建议注册后先用赠送余额做小规模测试。确认 Claude Code、Cline、Cursor、ChatBox 或自己的 SDK 项目都能正常工作，再考虑充值或升级套餐。

## FAQ

### FreeModel 注册真的送 10 美元吗？

按当前提供的信息，注册并绑定手机号即可获得 10 美元余额。活动额度和规则可能调整，最终以 FreeModel 官网实时页面为准。

### Claude Fable 5 可以直接用吗？

按用户提供的信息，Claude Fable 5 已在 FreeModel 上线，可通过 API 使用。它的价格是 Opus 的 2 倍，适合高价值任务，不适合拿来跑所有轻量请求。

### 月付套餐是不是余额？

不是。FreeModel 的月付套餐是 rate limit 等级，不是可消费余额。需要更多余额时充值 API Credits，遇到 rate limit 时升级套餐。

### Pro 套餐真的有 300 美元价值吗？

按用户提供的 FAQ，Pro 的基础 7 天限额约为 `$66.67`，按 4 周计算是 `$266.68`。平台还会给活跃 Pro 用户随机赠送 credit，所以官方口径里 `$300` 是长期可期待的最低值。这个说法需要以 FreeModel 实时页面和后台规则为准。

### FreeModel 为什么会自动切换模型？

如果你的工作流用了 fan-out 或 sub-agents，编排器可能会自动给子任务分配模型。你选择的模型处理主 agent，子任务可能使用其他模型。这是预期行为，不一定是故障。

### FreeModel 能用于 Claude Code 吗？

可以按原生 Claude API 格式接入，适用于 Claude Code、Cline 和 Anthropic SDK 相关应用。实际体验取决于客户端是否支持自定义 API 地址、模型名是否匹配以及平台当前可用模型。

### Cursor 和 ChatBox 可以用吗？

可以按 OpenAI 兼容接口配置。一般需要填写 `https://api.freemodel.dev`、API Key 和模型名。如果客户端只支持旧接口，优先测试 `/v1/chat/completions`。

### /v1/chat/completions 和 /v1/responses 选哪个？

追求兼容性先选 `/v1/chat/completions`。如果你的工具支持 Responses API，并且需要有状态多轮对话、更丰富的流式事件或工具能力，再测试 `/v1/responses`。

### 413 Payload Too Large 怎么办？

Tier 0 的请求体限制是 3MB，Tier 1+ 是 5MB。减少嵌入媒体、引用文件路径、拆分长上下文，通常能避免这个错误。

### 403 ip_account_conflict 怎么办？

这个错误表示当前 IP 已经关联了另一个免费账户。优先升级付费套餐，或在合法场景下换到自己的干净网络。不要用不同网络批量注册免费账户。

### gpt-5.5 模型一定可用吗？

用户提供的配置里模型名是 `gpt-5.5`，但模型列表、可用性和价格都可能变化。配置前建议先看 FreeModel 后台实时模型列表。

## 总结

FreeModel 的卖点不是单一模型，而是接入面比较宽。Claude Code、Cline 这类 Claude API 生态工具可以用，Cursor、ChatBox、OpenAI SDK 这类 OpenAI 生态工具也能接。对经常切换 AI 编程工具的人来说，一个中转站同时覆盖两套生态，确实能少折腾不少配置。

如果你还没用过这类平台，建议先通过 [FreeModel 注册入口](https://freemodel.dev/invite/FRE-cb3115a9) 注册，绑定手机号领取 10 美元余额，然后按自己的真实场景测试接口、模型、速度、限速和扣费。确认稳定后，再考虑充值余额或升级套餐。

本文基于 2026-06-17 用户提供信息和 FreeModel 公开入口整理。余额、模型、接口能力、套餐价格、汇率和活动规则请以 FreeModel 官网实时页面为准。
