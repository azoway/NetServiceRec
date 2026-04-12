# DMIT 洛杉矶 CN2 GIA / 9929 与日本东京 VPS 补货：三款 TINY 参数与购买链接

DMIT 在美西和日本一直有面向大陆方向的 KVM 套餐，洛杉矶常见分 Pro（电信 CN2 GIA 为主的三网组合）和 EB（电联走 AS9929、移动侧 CMIN2 等），东京 Pro 则多标为 CTGNet 与 CN2 GIA 一类表述。近段 IPv4 和硬件成本压力下，部分机型曾下架或砍掉季付，这次补货的 LAX.AN4.Pro.TINY、LAX.AN4.EB.TINY 和 TYO.AS3.Pro.TINY 属于门槛较低、线路标注相对清楚的档位，适合先买来用，后面有更合适再迁。下文价格与库存以官网订单页为准；测速请用官方 Looking Glass，别只看白天一次 ping。

## DMIT 几条线路在说什么

电信国际里 CN2 GIA（常对应 AS4809 一类路径）晚高峰往往比随机直连干净，丢包和抖动容易好看一些。联通侧 AS9929 常被称作精品网出口方向，联通用户命中概率高。CMIN2 则是移动国际里偏精品的表述，有的套餐 IPv4 和 IPv6 策略不一致，DMIT 这几款里 IPv6 单独标 CMIN2 的要看自己终端是否走 v6。东京 AS3 Pro 写的 CTGNet + CN2 GIA，本质还是「对大陆出口有挑选」的那类东京机，具体到你家宽带仍以实测为准。

## 补货背景

IP 紧张、硬件涨价是整个圈子都在喊的事，DMIT 也缩过在售型号和付款周期，部分套餐不再给季付只留月付或年付是常态。要的是大陆方向稳定、能接受单价，就按年付或月付锁一台；指着等历史低价再入手，短期内不现实。

## 三款 TINY 对比表

| 套餐 | 机房 | 线路（按官方文案归纳） | 配置 | 流量 / 带宽 | 价位 |
| --- | --- | --- | --- | --- | --- |
| LAX.AN4.Pro.TINY | 洛杉矶 Pro | 三网 CN2 GIA；IPv6 为 CMIN2 | 1C / 2G / 20G SSD | 1TB / 1Gbps | 88 USD/年 |
| LAX.AN4.EB.TINY | 洛杉矶 EB | 电信、联通 9929；移动 CMIN2；IPv6 为 CMIN2 | 1C / 2G / 20G SSD | 1.5TB / 1Gbps | 88 USD/年 |
| TYO.AS3.Pro.TINY | 东京 Pro | 三网 CTGNet CN2 GIA | 1C / 1G / 20G SSD | 500GB / 1Gbps | 21.9 USD/月 |

EB 那台流量比同价 Pro TINY 多 500GB，联通用户可优先看 EB；电信老 CN2 GIA 党更常盯 Pro。东京这台只有 1G 内存、500G 流量，只适合轻代理或低负载，别当下载机。

### LAX.AN4.Pro.TINY

洛杉矶，三网 CN2 GIA，IPv6 标 CMIN2。1 核 2G，20G SSD，1TB 流量，端口 1Gbps，年付 88 美元。

Looking Glass：https://lg.dmit.sh/?server=lax-pro

[购买 LAX.AN4.Pro.TINY](https://www.dmit.io/aff.php?aff=11524&pid=237)

### LAX.AN4.EB.TINY

洛杉矶，电信/联通 9929，移动 CMIN2，IPv6 同标 CMIN2。1 核 2G，20G SSD，1.5TB 流量，1Gbps，年付 88 美元。

Looking Glass：https://lg.dmit.sh/?server=lax-eb

[购买 LAX.AN4.EB.TINY](https://www.dmit.io/aff.php?aff=11524&pid=245)

### TYO.AS3.Pro.TINY

东京，三网 CTGNet CN2 GIA。1 核 1G，20G SSD，500GB 流量，1Gbps，月付 21.9 美元。

Looking Glass：https://lg.dmit.sh/?server=tyo-pro

[购买 TYO.AS3.Pro.TINY](https://www.dmit.io/aff.php?aff=11524&pid=138)

## Looking Glass 怎么用才有参考价值

先选和自己手机卡或家里宽带同一运营商的测速文件，晚上八九点再跑一轮。LG 只能证明机房到你当前网络的大致质量，流媒体解锁、游戏 UDP 之类还得本机实装再试。

---

下单前核对官网显示的库存、条款和计费周期。
