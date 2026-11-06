# Debian使用caddy2搭建Typecho网站

> 这篇文章围绕「Debian使用caddy2搭建Typecho网站」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

#### Typecho安装和数据的备份迁移
* 数据备份和迁移： 使用了tar和lrzsz来处理/var/www/typecho/usr目录下的所有文件

* 安装运行必须的php相关代码： 
`apt install php-cgi php-fpm php-curl php-gd php-mbstring php-xml php-sqlite3 sqlite3 -y`
* 安装typecho网站文件相关代码如下

```bash
    wget -O /tmp/typecho.tar.gz https://github.com/typecho/typecho/releases/download/v1.1-17.10.30-release/1.1.17.10.30.-release.tar.gz
    [[ ! -d "/var/www/typecho" ]] && mkdir -p /var/www/typecho || rm -rf /var/www/typecho/*
    tar zxvf /tmp/typecho.tar.gz -C /var/www/typecho/ && mv /var/www/typecho/build/* /var/www/typecho
    rm -rf /tmp/typecho.tar.gz /var/www/typecho/build
    chmod -Rf 755 /var/www/typecho/* 
    chown www-data:www-data -R /var/www/typecho/* 
```
  
#### 安装caddy2并使用cloudflare的DNS和CDN服务
安装caddy2:
```bash
    apt update && apt install apt-transport-https ca-certificates -y
    rm -rf /etc/apt/sources.list.d/caddy-fury.list
    echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" | tee -a /etc/apt/sources.list.d/caddy-fury.list
    apt update && apt install caddy -y
```
替换默认caddy2文件为包含cloudflare.dns的模块的版本
```bash
    curl "https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fcaddy-dns%2Fcloudflare" --output /usr/bin/caddy
    chmod +x /usr/bin/caddy
```
配置/etc/caddy/Caddyfile,注意版本号php7.3-fpm不同的话使用`ls /run/php/`查看
```bash
    obvps.com

    root * /var/www/typecho
    encode zstd gzip
    file_server

    tls {
    dns cloudflare cloudflare-api-key
    }

    php_fastcgi unix//run/php/php7.3-fpm.sock
```
运行相关服务：`systemctl restart php7.3-fpm && systemctl restart caddy`
  
#### TIPS:
* 如需要使用nftables作为防火墙，只允许ssh+http+https三个端口以及其它一些设置:`bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/nftables/nft.sh)`
* cloudflare-api-key非全局值，需单独创建一个值且具有如下二条权限:`Zone|Zone|Read && Zone|DNS|Edit`
