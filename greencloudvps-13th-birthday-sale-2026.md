# 绿云 GreenCloudVPS 13 周年庆：2222 / 1313 套餐与活动规则整理

绿云 GreenCloudVPS 的 13 周年庆活动页已经上线，官方窗口是 `2026-10-26` 到 `2026-10-31`（UTC+0），北京时间大约对应 10 月 26 日到 11 月 1 日上午。页面分类名是 `13th Birthday Sale`，套餐会分批上架、卖完再补。

整理时活动页上比较明确的两组是：`2222` 年付 `$22`，以及 `1313` 三年付 `$123`。预算紧、先要一台能用的，看 2222；想要更大内存和三年周期，看 1313。日本 SoftBank / IIJ、新加坡、香港通常比美加欧更抢手，库存经常显示 `0 Available`。

活动页写明了三件事：这批套餐不支持退款，下单前先测 IP，未付款订单 30 分钟取消。还没账号的人，最好先注册，别等补货时卡在结账页。

## 绿云周年庆活动入口

- [绿云 13 周年庆活动入口](https://greencloudvps.com/billing/aff.php?aff=5899)
- [绿云机房测试 IP](https://greencloudvps.com/data-centers.php)
- [提前注册入口](https://greencloudvps.com/billing/aff.php?aff=5899&pid=1799)

进官网后，商店分类选 `13th Birthday Sale`。如果没跳到周年庆页，先打开 [绿云官网](https://greencloudvps.com/billing/aff.php?aff=5899)，再进这个分类。

绿云注册通常要走一遍下单流程：随便选套餐进结账页，把账号建好就行，不用付款。上面的注册入口就是干这个的。

## 官方还有哪些福利

除了活动页闪购，官方周年庆公告里还有几项：

活动期内合格账单累计满 `$500`，可返 `13%` 到账户余额。充值余额、未付款账单一般不算。标准 Windows VPS 买或续 12 个月，符合条件的可以再送 6 个月；促销折扣机通常不参加。实付达到约 `$50` 的订单还能抽生日转盘，每人最多 5 次，用余额抵扣通常不计。

小单别按“一定有返现”去算账。`$22` 的 2222 主要价值在机器本身，不在返现和转盘。

## 绿云 2222 套餐：年付 $22

`2222` 是这次最容易上手的低价档。常见配置是 `2GB` 内存、`22GB` NVMe、`2` 核 EPYC、`1 IPv4 + IPv6`、`10Gbps` 端口，Linux + VirtFusion，年付 `$22`。

页面上出现过的节点包括 SG DC1、SG DC2、Canada、Chicago IL2、JP SoftBank、JP IIJ、Hong Kong DC2 等。亚洲节点流量常见约 `750GB`，部分北美节点能到 `2222GB`。

不少 2222 产品说明写了：选三年付时，可以申请内存+流量翻倍，或硬盘+流量翻倍，需要开 ticket 自选。能不能翻倍，以你下单那一款的产品描述为准，别默认所有数字机都行。

如果你只是要一台长期挂轻量服务的年付机，先看 2222，比直接上 1313 更稳妥。

## 绿云 1313 套餐：三年付 $123

`1313` 是今年周年庆新增的数字档，整理时价格是 `$123 / 三年付`，折合约 `$41/年`。统一配置大约是 `13GB` 内存、`113GB` NVMe 4.0 RAID-10、`6` 核 fair-share EPYC Milan、`10Gbps` 端口，多数带 1 次免费 Backup/Snapshot。

| 套餐 | 机房 | 流量 |
|---|---|---|
| 1313 CAN | Toronto, ON | 12TB |
| 1313 DE | Frankfurt, DE | 12TB |
| 1313 IL2 | Chicago, IL DC2 | 12TB |
| 1313 MO | Kansas City, MO | 12TB |
| 1313 NY | Buffalo, NY | 12TB |
| 1313 NYC2 | Staten Island, NY | 12TB |
| 1313 SJC | San Jose, CA | 12TB |
| 1313 TX | Dallas, TX | 12TB |
| 1313 UK | Coventry, UK | 12TB |
| 1313 JP Softbank | Tokyo SoftBank | 3333GB |
| 1313 JP IIJ | Tokyo IIJ | 3333GB |
| 1313 HK DC2 | Hong Kong DC2 | 3333GB |
| 1313 SG DC1 | Singapore DC1 | 3333GB |
| 1313 SG DC2 | Singapore DC2 | 3333GB |

美加欧流量普遍 `12TB`，日新港常见 `3333GB`。内存和磁盘都比 2222 宽裕不少，适合长期放面板、监控、轻量站、备用节点。三年一次付清，买错机房会比较难受，尤其这批活动机不退款。

页面之后还可能补 `6666`、`8888`、`9999`、`1010`、`1111`、`1212` 等经典数字机，以及 Budget / Storage 相关优惠。配置和库存变化很快，以下单页为准。

## 机房怎么选，买前盯什么

普通建站、海外业务、备用机，美加欧都可以，优先选你熟悉且还有货的。更看亚洲访问的，JP SoftBank、JP IIJ、SG、HK 更常被盯，软银和 IIJ 通常最先空。

如果你真正要的是大陆优化线路，别把周年庆闪购默认当成 Gen2 或 CN Premium。那条产品线单独看站内的 [绿云 CN Premium Optimized 服务器推荐](https://obvps.com/posts/绿云cn-premium-optimized服务器推荐/)，以及 [新加坡 CN Premium Optimized Mini](https://obvps.com/posts/绿云新加坡cn-premium-optimized-mini补货推荐/)。

绿云 CPU 限制一向偏严，高占用业务要自己掂量。活动机无退款，只想短测几天的人更适合月付或别处短周期机器。未付款订单 30 分钟取消，乱开单占不住库存。下单前用官方 [测试 IP 页](https://greencloudvps.com/data-centers.php) 自己测一轮，尤其是日本、新加坡、香港。

站内之前整理过 [GreenCloudVPS 2026 独立日促销](https://obvps.com/posts/greencloudvps-2026-independence-day-sale/)。那次更偏三年付常规机和大盘存储，这次周年庆更偏数字系列闪购和一周活动福利。

## 怎么下单

1. 打开 [绿云官网](https://greencloudvps.com/billing/aff.php?aff=5899) 登录，没有账号就先注册
2. 进入 `13th Birthday Sale`
3. 测目标机房 IP
4. 核对套餐名、机房、流量、付款周期，以及有没有写三年付可翻倍
5. 确认无退款后下单，30 分钟内付款
6. 如果产品说明支持翻倍，付款后按页面要求开 ticket 选择

预算优先看 `2222`。内存和三年付更重要，再看 `1313`。机房测不通就别硬买。

## FAQ

### 绿云 13 周年庆什么时候结束？

官方写的是 `2026-10-26` 至 `2026-10-31`（UTC+0）。单个套餐可能提前售罄，页面也会继续补货。

### 绿云周年庆有日本 SoftBank 吗？

活动页出现过 `2222 JP Softbank` 和 `1313 JP Softbank`，但库存经常是 0。能不能买到，只能看实时补货。

### 绿云 2222 三年付能翻倍吗？

部分 2222 产品说明写了三年付可申请内存+流量或硬盘+流量翻倍，并要求开 ticket。以你下单那一款的描述为准。

### 绿云周年庆套餐适合大陆访问吗？

多数是普通国际节点，不是 CN Premium Optimized。要大陆优化，优先看 [绿云 CN Premium Optimized 推荐](https://obvps.com/posts/绿云cn-premium-optimized服务器推荐/)。

### 没账号怎么抢绿云周年庆？

先走 [注册入口](https://greencloudvps.com/billing/aff.php?aff=5899&pid=1799) 建好账号，再盯活动页。补货时再临时注册，很容易卡在验证和结账信息上。

## 怎么选更合适

只想先有一台年付机，优先 `2222`。确定要三年付和大内存，再盯 `1313`。日本软银、IIJ 和亚洲节点要边测边抢；大陆优化需求请走开 CN Premium，不要和周年庆闪购混为一谈。

本文基于 2026-10-26 绿云官方周年庆公告与活动页整理。价格、库存、配置和规则请以下单页实时显示为准。
