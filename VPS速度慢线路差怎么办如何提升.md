# VPS 速度慢、线路差怎么办？从本机优化到 AKCDN IX/CCN 专线

家里的 VPS 测速不好看、晚高峰丢包、直连抖动大，不一定马上换商家。很多问题出在本机 TCP 栈、入口 IP 选路，或缺一层更稳的中转。下文按「改动小 → 改动大」排：先在 Linux 上开 BBR 和 fq，站点走 Cloudflare 时可考虑优选边缘 IP；若瓶颈在跨境入口，再用 AKCDN 的 IX/CCN 专线转发，并用社区工具 [akcdn_auto](https://github.com/azoway/akcdn_auto) 自动维护入口白名单。套餐档位、SH-HK 建规则和延迟拆分见 [AKCDN SH-HK 沪港 IX CCN 专线实测](https://obvps.com/posts/akcdn-sh-hk-ix-no-frontend-guide)；选购 AKCDN 流量包可看 [AKCDN 流量转发套餐怎么选](https://obvps.com/posts/cdn中转服务推荐akile)。

## 先判断慢在哪一段

改配置前先分清问题类型，后面才不至于把钱花在刀背上。

- **单线程下载慢、但 ping 还行**：常见是拥塞控制或带宽封顶，可先试 BBR。
- **晚高峰延迟和丢包一起抬升**：多半是运营商国际出口或绕路，单靠 VPS 内 sysctl 很难根治。
- **网站已套 Cloudflare，只有部分省份/运营商慢**：可能是本地到 Cloudflare 边缘 IP 的路由差，可尝试优选 IP（见下文）。
- **你能直连 VPS，但跨境段一直飘**：适合评估 AKCDN 一类四层转发，把入口放到更靠近你的一侧。

具体数值别靠猜。站内 [VPS 常用一键测试脚本汇总](https://obvps.com/posts/vps常用一键测试脚本工具汇总集合) 里有 bench、回程 ping、路由跟踪等入口；专线类链路更建议 tcping 监听端口，晚高峰用 MTR 看丢包，这和 [SH-HK 实测文](https://obvps.com/posts/akcdn-sh-hk-ix-no-frontend-guide) 里的建议一致。

## 启用 BBR 与 fq（本机侧、改动小）

**BBR** 是 Google 提出的拥塞控制算法，在高延迟、有一定丢包的链路上，往往比传统 cubic 更容易把带宽吃满。**fq**（Fair Queue）配合 BBR 做队列调度，减少 bufferbloat。它们只能优化「你的 VPS 怎么发 TCP」，不能改掉北京到香港绕美这类路由；对已经瓶颈在国际出口的 VPS，体感可能有限，但开起来成本低，值得先做。

内核需支持 `tcp_bbr`（多数较新的 Debian/Ubuntu 发行版在启用了相应模块后即可使用）。本站多篇 VPS 教程沿用同一套写法，核心是把默认队列设为 `fq`，并把 IPv4 TCP 拥塞控制切到 `bbr`，然后 `sysctl -p` 生效。示例（与 [德国 BGP VPS 推荐](https://obvps.com/posts/德国bgp服务器vps推荐) 文中一致）：

```bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```

OpenVZ/KVM 环境不同，有的主机商禁止改 sysctl；魔改 BBR 一类脚本在 [测试脚本汇总](https://obvps.com/posts/vps常用一键测试脚本工具汇总集合) 里有收录，是否使用自行权衡风险。改完后用同一条测速命令对比前后即可，不必指望 BBR 单独解决晚高峰跨境拥塞。

## Cloudflare 优选 IP 是什么、何时有用

站点或 API 已经接入 **Cloudflare** 时，客户端连的是 Cloudflare 的 **anycast** 边缘，而不是你源站 IP。理论上全球任一边缘都能接流量，但你家宽带到不同边缘 IP 的路由质量可能差很多：**Cloudflare 优选 IP** 指的就是，在你本地网络下，通过延迟、丢包、晚高峰稳定性等测试，挑出更合适的一两个边缘 IP，让解析或客户端配置指向它们，从而减轻「CF 开了但个别运营商仍然很慢」的情况。

这只对「流量确实经 Cloudflare」有意义；纯 VPS 端口、游戏 UDP、未走 CF 的代理链路不适用。优选需要随运营商和时间复测，没有一劳永逸的 IP 列表；具体工具、脚本和测速方法因环境而异，请以你自己验证结果为准，勿把第三方列表当成长期保证。

## 用 AKCDN 做 IX/CCN 专线转发（晚高峰与跨境入口）

当问题主要在**跨境入口**而不是 VPS 内网时，在「落地 VPS」外面加一层 **[AKCDN](https://cdn.akile.ai/?ref=48521618)** 转发，是本站经常讨论的办法。AKCDN 按流量包卖，在控制台建 **TCP/UDP 四层转发规则**：客户端连平台给的**入口节点**，平台再把流量转到你的**目标 VPS**。这样优化的是「你家 → 入口」这一段，落地机仍用你熟悉的机房。

其中 **沪港 SH-HK** 等入口把 **IX（互联网交换中心）与 CCN 专线接入** 打包进产品：上海侧由 AKCDN 承接，用户通常**不必自备国内前置机**（与要求自己买前置转发的入口不同）。根据站内 [SH-HK 实测](https://obvps.com/posts/akcdn-sh-hk-ix-no-frontend-guide) 整理：**10 元中包、20 元大包、50 元超大包** 可正常走 SH-HK；**5 元小包** 在面板里虽能选该入口，实际链路不通，属于档位与接入点分配问题，不是白名单或落地配置单独能修的。

| 套餐 | 站内整理的 SH-HK | 公开套餐参数（30 天） |
| --- | --- | --- |
| 5 元小包 | 不可用 | 200 GB，限速 200 Mbps |
| 10 元中包 | 正常 | 400 GB，限速 1000 Mbps |
| 20 元大包 | 正常 | 800 GB，限速 2000 Mbps |
| 50 元超大包 | 正常 | 2 TB，限速 5000 Mbps |

AKCDN 宣传材料常强调 **IX/CCN 专线在晚高峰仍较稳、较快**；社区用户反馈也确实有人用它缓解高峰时段抖动。但入口多为共享资源，具体晚高峰表现还取决于当地到上海入口、落地机带宽和当时负载——应视为**体验参考**，不是 SLA。想先低成本试 IX 架构、又愿意自己维护前置的，还可以对照 [低成本体验顶级 IX 线路](https://obvps.com/posts/低成本体验顶级的ix线路)（阿里云 G 口 + AKCDN + 亚太 VPS 组合），和免前置的 SH-HK 是两条路线。

使用前要过两道门槛：**档位**（SH-HK 至少 10 元档）和**入口来源白名单**（每个监听端口通常只认一个 IPv4 /32）。规则在 [AKCDN 控制台](https://cdn.akile.ai/?ref=48521618) 创建，密钥勿泄露；详细填表与排障见 [SH-HK 指南](https://obvps.com/posts/akcdn-sh-hk-ix-no-frontend-guide)。

## 在 VPS 上部署 akcdn_auto：自动更新白名单

家用宽带、4G 切 Wi-Fi 都会换**公网出口 IP**。白名单没跟上时，控制台常显示「待绑定 /32 · 转发暂停」，客户端只有连不上。每次登录面板改 IP 很烦，官方已开放 API，可对**已有规则** `PUT` 更新 `entry_whitelist`（仍只接受单个 IPv4 /32，不负责替你建规则）。

社区项目 **[akcdn_auto](https://github.com/azoway/akcdn_auto)**（**非 Akile 官方**，许可证 GPL-3.0）在一台**未被墙、能访问 `cdnapi.akile.ai` 的 Debian/Ubuntu VPS** 上当「敲门员」：

1. 按 `node_id` 拉取该节点下各规则的 `listen_port`，在 nftables 里把这些端口当成**只记录日志、直接 drop** 的传感器（端口上**没有真实服务**，客户端连上来超时或拒绝属正常）。
2. 从内核日志读出 `SRC=<客户端公网 IP>`，映射到 `rule_id`，调用官方 API 写入白名单；已是同一 IP 则跳过，并对重复敲门做短时间去重。
3. 安装入口示例（token 与 `node_id` 以你控制台为准，详见仓库 README）：

```bash
curl -fsSL https://raw.githubusercontent.com/azoway/akcdn_auto/main/run.sh \
  | bash -s -- ak_你的token 5
```

装完建议先跑 `akcdn-auto verify` 核对 token、节点与敲门端口。客户端侧常见做法：在 Clash 等内核里配一个**永远连不上的「敲门节点」**（指向 VPS 公网 IP + 敲门端口）和真实 CDN 入口节点，用 `fallback`/`urltest` 让健康检查先碰敲门节点——失败过程即完成加白，再回落到真实节点；`lazy` 类选项若阻止主动探测，敲门可能不会触发，配置细节以 README 为准。

**和 [akcdn_api](https://github.com/azoway/akcdn_api) 的区别**：后者是自托管 HTTP 小服务，同样面向改 `entry_whitelist`，带 QuanX 等示例，思路和「VPS 敲门 + 读日志」不同，维护方式自己衡量。

**何时用 akcdn_auto、何时不要指望它**

- **适合**：多个设备、**动态家庭宽带出口**，希望 IP 一变就自动写回白名单；敲门 VPS 需放行 SSH 与敲门端口的 TCP/UDP（主机商安全组也要放行）。
- **不适合或要注意**：白名单应填**客户端上网公网 IP**，不是落地机 IP。若是 [G 口前置 + AKCDN IX](https://obvps.com/posts/低成本体验顶级的ix线路) 架构，白名单往往应填**前置机访问 AKCDN 时的固定公网 IP**，而不是家里宽带——这种场景用稳定 egress，不必用敲门 VPS 追家庭 IP。CGNAT、私网段来源会被跳过；换网络（4G ↔ Wi-Fi）等于换出口，需要重新敲门。

## 怎么组合：一条可执行的优化顺序

1. **本机**：BBR + fq，复测同一脚本。
2. **站点走 CF**：在确认流量确实经 Cloudflare 的前提下，再考虑优选边缘 IP，并周期性复测。
3. **跨境 VPS/代理仍差**：确认落地 VPS 本身带宽和线路尚可后，用 **10 元及以上** AKCDN 包试 SH-HK 或其它入口；小包连通性测试见 [套餐选购文](https://obvps.com/posts/cdn中转服务推荐akile)。
4. **白名单**：固定 IP 手改控制台即可；动态家庭宽带在敲门 VPS 上装 **akcdn_auto**，按 README 配客户端 fallback。

全程别跳过实测，尤其**晚高峰**同一时段对比改前改后。

## 常见问题

### BBR 开了为什么跨境还是慢？

BBR 只调整 VPS 的发包策略。国际出口拥塞、绕路、对端限速不变的话，峰值可能略有改善，但不可能把 4837 晚高峰变成专线。跨境要动路径或入口，而不是多写几行 sysctl。

### Cloudflare 优选 IP 和 AKCDN 可以一起用吗？

可以，但作用层不同：优选针对 **HTTP/HTTPS 经 Cloudflare 代理** 的站点；AKCDN 是 **四层端口转发**，给 TCP/UDP 业务换入口。一套流量不会同时靠两种方式加速，按实际架构选其一或分层使用（例如网站走 CF，游戏/VPS 隧道走 AKCDN）。

### 为什么 SH-HK 一定要 10 元起？

站内实测记录：5 元小包分配的上海接入点目前不通，规则状态仍可能显示正常。10 元中包是能进 SH-HK 的最低档；价格与流量以 [AKCDN 购买页](https://cdn.akile.ai/?ref=48521618) 为准。

### akcdn_auto 是官方工具吗？

不是。它是 azoway 社区的 GPL-3.0 项目，通过公开 API 改白名单；可用性、安全边界（例如只改白名单、不建规则）以 [GitHub README](https://github.com/azoway/akcdn_auto) 为准，无官方 SLA。

### 晚高峰怎么验证有没有变好？

同一客户端、同一落地机，在晚高峰用 tcping 打 AKCDN 监听端口，配合 MTR 看丢包；不要用 ping 代替端口可达性（IX 段常禁 ICMP）。站内 SH-HK 文对延迟拆分和测速口径有说明，可作对照。

## 小结

**VPS 速度慢、线路差**时，先在机器上启用 **BBR 与 fq** 排除本机 TCP 因素；网站已上 **Cloudflare** 再考虑 **优选 IP**；跨境入口不稳则评估 **[AKCDN](https://cdn.akile.ai/?ref=48521618)** 的 **IX/CCN 专线转发**（如 SH-HK，**10 元及以上**档位，晚高峰表现仍须自测）。动态出口配上 **[akcdn_auto](https://github.com/azoway/akcdn_auto)** 可减轻白名单维护；G 口等固定前置架构则以稳定 egress IP 为准。更细的步骤链到 [SH-HK 实测](https://obvps.com/posts/akcdn-sh-hk-ix-no-frontend-guide)、[套餐怎么选](https://obvps.com/posts/cdn中转服务推荐akile) 与 [IX 组合方案](https://obvps.com/posts/低成本体验顶级的ix线路) 即可，不必重复整篇教程。

> 本文基于 2026-11-27 的官网公开页面、AKCDN 控制台信息及 [akcdn_auto](https://github.com/azoway/akcdn_auto) 公开 README 整理。价格、库存、套餐、各档位入口可用性与白名单策略可能随时变动，请以官网实时页面为准。