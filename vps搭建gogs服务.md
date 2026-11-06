# vps搭建gogs服务

> 这篇文章围绕「vps搭建gogs服务」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

甲骨文arm服务器，已有docker-compose服务，记录为主 

#### 配置caddy
```bash
wget -O caddy.deb https://github.com/caddyserver/caddy/releases/download/v2.4.6/caddy_2.4.6_linux_arm64.deb
dpkg -i caddy.deb
cat <<EOF >/etc/caddy/Caddyfile
ex.com {
  reverse_proxy 127.0.0.1:10880
}
EOF
systemctl restart caddy
systemctl status caddy
```

#### 配置gogs
```bash
docker rm -f gogs
rm -rf /var/gogs
mkdir -p /var/gogs
docker run -d --restart always --name=gogs -p 22:22 -p 127.0.0.1:10880:3000 -v /var/gogs:/data gogs/gogs
```

#### 使用
```bash
ssh-keygen
git clone git@ex.com:username/examples.git
```

## 相关阅读

- [VPS搭建聚合图床程序收集和推荐](https://obvps.com/posts/vps搭建聚合图床程序收集和推荐)
- [VPS搭建OneDrive网盘程序推荐](https://obvps.com/posts/vps搭建onedrive网盘程序推荐)
- [gost下载安装配置vps进行端口转发中转加速](https://obvps.com/posts/gost下载安装配置vps进行端口转发中转加速)
