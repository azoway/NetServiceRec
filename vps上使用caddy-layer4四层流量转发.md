# vps上使用caddy layer4四层流量转发

> 这篇文章围绕「vps上使用caddy layer4四层流量转发」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

  
* 服务器分配端口较少时,以此节约端口
* 商家限制安装代理软件,使用caddy可能会降低一定的风险  
* 可以配置转发到开启Cloudflare的CDN域名,相比iptables转发,没有盗用风险
* 可搭建naiveproxy

<!--more-->

以下教程在debian 64上测试,仅供参考:
#### dpkg安装caddy服务
```bash
trap 'rm -f "$TMPFILE"' EXIT; TMPFILE=$(mktemp) || exit 1
caddyURL="$(wget -qO-  https://api.github.com/repos/caddyserver/caddy/releases | grep -E "browser_download_url.*linux_amd64\.deb" | cut -f4 -d\" | head -n1)"
wget -O $TMPFILE $caddyURL && dpkg -i $TMPFILE

#### 替换有layer4插件的caddy文件版本
https://github.com/lxhao61/integrated-examples/releases
```

#### 按需修改/etc/caddy/Caddyfile.json文件
```json
{
	"admin": {"disabled": true},
	"apps": {
		"layer4": {
			"servers": {
				"example0": {
					"listen": [":20143"],
					"routes": [
						{
							"match": [{"tls": {"sni": ["example1.com"]}}],
							"handle": [
								{
									"handler": "proxy",
									"upstreams": [{"dial": ["example1.com:443"]}]
								}
							]
						},
						{
							"match": [{"tls": {"sni": ["example2.com"]}}],
							"handle": [
								{
									"handler": "proxy",
									"upstreams": [{"dial": ["example2.com:443"]}]
								}
							]
						}
					]
				}
			}
		}
	}
}
```

#### 启动服务
systemctl enable caddy && systemctl restart caddy && sleep 3 && systemctl status caddy

#### 参考
* https://github.com/azoway/across/tree/main/caddy

## 📌 选购说明

以下信息为公开套餐与经验整理，具体价格和库存请以下单页实时展示为准。

- 套餐与价格可能随商家活动调整，请以下单页实时信息为准。
- 本文仅做信息整理与经验分享，请按自身需求理性选购。
