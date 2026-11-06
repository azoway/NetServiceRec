# debian安装配置nftables端口转发

> 这篇文章围绕「debian安装配置nftables端口转发」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

<!--more-->

###### 卸载iptables，安装启用nftables
`apt purge iptables -y`
`apt install nftables -y; systemctl enable nftables; systemctl restart nftables`

###### 创建转发规则/etc/nft.diy文件，文件每行为一个转发规则，支持端口段第一个为本地端口，第二个为远程域名或IP，第三个为远程端口,以下内容请按需修改
cat <<EOF > /etc/nft.diy
20103/bing.com/443
20104-20108/1.1.1.1/443
30000-30108/www.example.com/30000-30108
EOF

###### 执行脚本，配置端口转发
`bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/nftables/nft-nat.sh)`

###### 使用定时任务执行更新规则,如每二小时执行一次：
```bash
wget --no-check-certificate -O /opt/nft-nat.sh https://raw.githubusercontent.com/azoway/across/main/nftables/nft-nat.sh
chmod 755 /opt/nft-nat.sh
(crontab -l ; echo "0 */2 * * * /opt/nft-nat.sh") | crontab -
```

## 相关阅读

- [使用nftables配置VPS仅允许Cloudflare IP访问Web端口的完整指南](https://obvps.com/posts/vps服务器配置nftables仅允许cloudflare的ip访问web端口)
- [Debian使用caddy2搭建Typecho网站](https://obvps.com/posts/debian使用caddy2搭建typecho网站)
- [gost下载安装配置vps进行端口转发中转加速](https://obvps.com/posts/gost下载安装配置vps进行端口转发中转加速)
