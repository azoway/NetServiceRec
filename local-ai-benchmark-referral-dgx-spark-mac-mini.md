# local.ai：独立本地 AI 基准测试平台 + 推荐活动赢 DGX Spark 和 Mac Mini

local.ai 是 EXO Labs 做的一个独立本地 AI 基准测试网站，目标是把各种开源大模型在不同消费级硬件、量化方案和推理框架下的真实跑分数据集中展示出来。目前处于早期访问阶段，正在搞推荐活动，排名第 1 的用户可以同时拿走 NVIDIA DGX Spark 和 M4 Pro Mac Mini 24GB，前 10 名每人一台 M4 Pro Mac Mini 24GB。

注册入口：[local.ai 早期访问注册](https://local.ai/groker/invite)

## local.ai 是什么

EXO Labs 是开源分布式推理框架 exo 的开发团队，之前因为用多台 Mac 互连跑 DeepSeek V3 671B 和 Qwen3 235B 出了圈。local.ai 是他们的新项目，定位很明确：给本地 AI 提供独立、透明的性能基准数据。

官网原话是 "How AI really runs on your own hardware"，核心卖点是提供来自真实 agent 工作负载的数据，覆盖每种模型、每种量化、每种硬件和每种推理框架，让你在买硬件之前就知道能拿到什么性能。

网站目前规划了这几个主要板块：

- **Hardware** — 不同 GPU、CPU、Mac 芯片的跑分对比
- **Models** — 各种开源大模型的性能数据
- **Energy** — 能耗表现
- **Wall** — 早期用户留言墙，早期访问结束后会打印出来裱在 EXO 旧金山办公室

这个项目解决的痛点很实际。现在想在自己机器上跑大模型，最大的信息缺口不是"这个模型好不好"，而是"我这个配置到底能跑多少 token/s"。社区里的散落数据要么测试条件不一致，要么过时了，要么只测了特定量化。local.ai 想把这些做成一站式查询。

## 背后的 EXO Labs 和 exo 框架

EXO Labs 的核心项目 exo 是一个开源分布式推理框架，可以把多台设备组合成一个 AI 集群。它不要求所有设备都是同一种 GPU，Mac、Linux 桌面、甚至树莓派都能混着用，exo 自动把推理任务分配到可用设备上。

在 Apple Silicon 上，exo 支持 Thunderbolt 5 的 RDMA，GPU 之间直接传内存数据，不用经过 CPU 中转。Jeff Geerling 的测试显示，4 台 M3 Ultra Mac Studio 组合跑 Qwen3 235B（8-bit）能到约 32 tokens/s，跑 DeepSeek V3.1 671B（8-bit）能到约 32.5 tokens/s。

local.ai 的跑分数据来源跟 exo 的实际使用场景直接相关，这也是它和其他基准测试站的区别——数据来自真实的分布式推理工作负载，而不是单机实验室条件。

## 早期访问和推荐活动

local.ai 目前处于早期访问（Early Access）阶段，需要通过 Hugging Face 账号登录才能使用完整功能。注册流程比较简单，用 Hugging Face OAuth 登录，选一个 local.ai 用户名就行。

现在的推荐活动规则：

- **第 1 名**：同时获得 NVIDIA DGX Spark 和 M4 Pro Mac Mini 24GB
- **前 10 名**：每人一台 M4 Pro Mac Mini 24GB
- **有效推荐定义**：被推荐人使用你的推荐链接注册并完成用户名认领
- 无需购买任何东西
- 排名是临时的，最终规则（时间、资格、地区、验证方式、平局处理）在活动正式开放前会公布

DGX Spark 由 NVIDIA 提供。这是一台面向本地 AI 开发的工作站，配备 128GB 统一内存，适合跑 20B 以上规模的大模型和微调任务，Sebastian Raschka 等研究者已经公开过使用体验。

M4 Pro Mac Mini 24GB 是目前本地 AI 入门性价比很高的选择，Apple Silicon 的统一内存架构在跑量化模型时效率不错，Ollama、LM Studio、MLX 等工具链也成熟。

注册入口：[local.ai 早期访问注册](https://local.ai/groker/invite)

## 当前排行榜情况

从推荐排行榜看，竞争已经比较激烈。排名第 1 的 Mia 有 902 个有效推荐，第 2 名 0xSero 有 308 个，第 3 名 V2EX 有 199 个。前 10 名的门槛目前在 36 个有效推荐左右，第 10 名之外就失去了 Mac Mini 资格线。

排名第 11 以下的人数不少，推荐数从 33 到 7 个不等。想冲前 10 的话，至少需要 37 个以上的有效推荐才有机会，而想拿双设备大奖则需要 900+ 的推荐量。

需要注意的是，排行榜标注了 "Standings are provisional"（排名暂定），最终资格验证规则还没完全确定，不排除后续会有反作弊清理。

## 适合谁注册

- **在折腾本地 AI 的人** — 买硬件之前想看真实跑分数据的，local.ai 的数据来自 agent 工作负载，比纯实验室条件更接近实际使用
- **用 exo 框架的人** — 跑分数据直接关联 exo 的分布式推理场景
- **关注 Apple Silicon 做 AI 的人** — Mac Mini、Mac Studio 在本地 AI 场景下的表现数据是 EXO Labs 的强项
- **想拿免费硬件的人** — 推荐活动不花钱，前 10 名拿 Mac Mini，第 1 名拿双设备

如果你已经在用 NVIDIA Build API Key 或者 Grok Token 号池这类方案，本地 AI 基准数据对硬件选型也有参考价值。可以参考站内的 [NVIDIA Build API Key 批量注册与管理](https://obvps.com/posts/nvidia-build-apikey-register-somanyapikeys-yescaptcha/) 和 [Grok Token 号池搭建指南](https://obvps.com/posts/grok-token-pool-cliproxyapi-yescaptcha-guide/)。

## 怎么参与

1. 打开 [local.ai 注册入口](https://local.ai/groker/invite)
2. 用 Hugging Face 账号登录（只请求 profile 权限，不会访问你的仓库）
3. 认领一个 local.ai 用户名
4. 拿到你自己的推荐链接，分享给其他人
5. 被推荐人通过你的链接注册并完成用户名认领后，算一个有效推荐

注册只需要 Hugging Face 账号和个人用户名，不用付费，不用填信用卡。推荐链接的格式是 `local.ai/你的用户名/invite`。

## FAQ

**local.ai 现在能看跑分数据吗？**

目前还在早期访问阶段，Hardware、Models 等页面需要登录后才能查看完整内容。网站标注了 "Coming soon"，完整数据在正式上线后开放。

**推荐活动什么时候结束？**

官方还没有公布具体的截止时间。规则页面说明排名是临时的，最终的时间、资格、地区限制和验证方式会在活动正式开放前公布。

**DGX Spark 是什么？**

NVIDIA DGX Spark 是一台紧凑型 AI 工作站，配备 128GB 统一内存，支持 CUDA，适合本地大模型推理和微调。Sebastian Raschka 在博客中分享过用它跑 gpt-oss-20B 和更大模型的体验。

**有效推荐怎么算？**

被推荐人通过你的推荐链接注册 local.ai 并完成用户名认领，才算一个有效推荐。只点链接不注册不算。

**需要买什么东西吗？**

不需要。活动规则明确写了 "No purchase necessary"，注册和推荐都不花钱。

---

本文基于 2026 年 8 月 local.ai 官网公开页面整理。活动规则、排名和奖励以官网实时页面为准。
