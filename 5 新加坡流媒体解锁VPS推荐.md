新加坡VPS支持Netflix/Disney+/Youtube/ChatGPT/Abema/DMM等流媒体解锁
Singapore vps servers support unlocking streaming services such as Netflix, Disney+, YouTube, ChatGPT, Abema, and DMM.

个人使用推荐以下2款：  
```
SGLite-Mini
CPU 1核 ｜ 内存 1024 M
硬盘 5 GB ｜ 带宽 1000M
1000G/月 ｜ 超出限速共享10Mbps
重置流量 ¥19.99
IPv4 1个 ｜ IPv6 1个
¥24.99/月
```

下单链接：https://akile.io/shop/server?type=traffic&areaId=7&nodeId=18&planId=892&aff_code=a1e2817f-c626-4f0b-b7ba-afce0951a583

```
SGLite-Starter
CPU 1核 ｜ 内存 1024 M
硬盘 10 GB ｜ 带宽 1000M
3000G/月 ｜ 超出限速共享10Mbps
重置流量 ¥36.00
IPv4 1个 ｜ IPv6 1个
¥43.74/月
```

下单链接：https://akile.io/shop/server?type=traffic&areaId=7&nodeId=18&planId=887&aff_code=a1e2817f-c626-4f0b-b7ba-afce0951a583

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
```
