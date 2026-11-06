# gost下载安装配置vps进行端口转发中转加速

> 这篇文章围绕「gost下载安装配置vps进行端口转发中转加速」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

GOST从2.1版本开始增加了对端口转发的支持

###### 获取最新版本gost下载地址：
`URL="$(wget -qO- https://api.github.com/repos/ginuerzh/gost/releases/latest | grep -E "browser_download_url.*gost-linux-amd64" | cut -f4 -d\")"`
###### 删除之前gost旧版:
`rm -rf /usr/bin/gost`
###### 下载最新版本gost并解压，下载成功赋予执行权限：
`wget -O - $URL | gzip -d > /usr/bin/gost && chmod +x /usr/bin/gost`
###### 运行gost，进行端口转发中转加速，比如将中转机的12345端口tcp转发到落地端的54321端口,假设落地VPS的IP是1.1.1.1：
`/usr/bin/gost -L=tcp://:12345/1.1.1.1:54321`
###### 创建gost.service文件：
```bash
cat <<EOF > /etc/systemd/system/gost.service
[Unit]
Description=gost
[Service]
ExecStart=/usr/bin/gost -L=tcp://:12345/1.1.1.1:54321
Restart=always
User=root
[Install]
WantedBy=multi-user.target
EOF
```
###### 启用gost.service,使用systemctl配置gost开机自启：
`systemctl enable gost.service && systemctl daemon-reload && systemctl restart gost.service && systemctl status gost`
  
#### 当然以上步骤可以直接使用一键脚本命令，之前的步骤都可以略过：
`bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/gost/gost.sh) -L=tcp://:12345/1.1.1.1:54321`

## 📌 选购说明

以下信息为公开套餐与经验整理，具体价格和库存请以下单页实时展示为准。

- 套餐与价格可能随商家活动调整，请以下单页实时信息为准。
- 本文仅做信息整理与经验分享，请按自身需求理性选购。

## 相关阅读

- [TierHive NAT VPS 推荐：新加坡最便宜的服务器 + Alpine + GOST SOCKS5](https://obvps.com/posts/tierhive-vps推荐与alpine-gost搭建)
- [德国BGP服务器VPS推荐 - 高速稳定德国服务器 | 2025年最新配置指南](https://obvps.com/posts/德国bgp服务器vps推荐)
- [使用nftables配置VPS仅允许Cloudflare IP访问Web端口的完整指南](https://obvps.com/posts/vps服务器配置nftables仅允许cloudflare的ip访问web端口)
