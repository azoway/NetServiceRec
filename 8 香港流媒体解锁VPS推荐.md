香港VPS支持Netflix/Disney+/Youtube/ChatGPT/Abema/DMM等流媒体解锁  
Hongkong vps servers support unlocking streaming services such as Netflix, Disney+, YouTube, ChatGPT, Abema, and DMM.  
HKLite接入NTT/PCCW/EIE等网络，国际互联优秀，内置AKILE DNS香港内网解锁流媒体解锁，支持Netflix/Disney+/Youtube/ChatGPT/MytvSuper等流媒体解锁

个人使用推荐以下三款：  

```
HKLite-One
CPU 1核 ｜ 内存 1024 M
硬盘 5 GB ｜ 带宽 5000M
1000G/月 ｜ 超出限速共享10Mbps
重置流量 ¥7.00
IPv4 1个 ｜ IPv6 1个
¥9.99/月
```

下单链接：https://akile.io/shop/server?type=traffic&areaId=3&nodeId=1&planId=819&aff_code=a1e2817f-c626-4f0b-b7ba-afce0951a583

```
HKPRO-Starter
CPU 1核 ｜ 内存 1024 M
硬盘 20 GB ｜ 带宽 50M
500G/月 ｜ 超出限速共享10Mbps
重置流量 ¥35.00
IPv4 1个 ｜ IPv6 0个
¥44.99/月
```

下单链接：https://akile.io/shop/server?type=traffic&areaId=3&nodeId=3&planId=815&aff_code=a1e2817f-c626-4f0b-b7ba-afce0951a583

```
HKPlus-Starter
CPU 1核 ｜ 内存 1024 M
硬盘 20 GB ｜ 带宽 500M
500G/月 ｜ 超出限速共享10Mbps
重置流量 ¥40.00
IPv4 1个 ｜ IPv6 0个
¥53.74/月
```

下单链接：https://akile.io/shop/server?type=traffic&areaId=3&nodeId=5&planId=831&aff_code=a1e2817f-c626-4f0b-b7ba-afce0951a583  

购买VPS后设置DNS解锁：  
Default: 154.83.83.83  
HK: 154.83.83.84  
JP: 154.83.83.85   
TW: 154.83.83.86  
SG: 154.83.83.87  
US: 154.83.83.88  
UK: 154.83.83.89  
DE: 154.83.83.90  
默认可使用154.83.83.83  
如需更改为其他地区的Netflix/Disney等可选择其他DNS  

快捷设置dns  
```bash
cp /etc/resolv.conf /etc/resolv.conf.bak && echo "nameserver 154.83.83.83" > /etc/resolv.conf
```

【流媒体解锁情况一键脚本】
 注意脚本结果仅供参考 以实际为准
```bash
bash <(curl -L -s https://github.com/1-stream/RegionRestrictionCheck/raw/main/check.sh) -M 4