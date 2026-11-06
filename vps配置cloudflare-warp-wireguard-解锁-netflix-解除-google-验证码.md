# vps配置cloudflare warp wireguard 解锁 netflix 解除 google 验证码

> 这篇文章围绕「vps配置cloudflare warp wireguard 解锁 netflix 解除 google 验证码」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

#### 一. cloudflare warp 注册，此步骤可跳过
* 访问 https://warp.plus/EmoCb 可以下载注册安装获取LICENSE_KEY给之后VPS上使用
* 如果你还需要warp+流量可以参考[这个脚本](https://github.com/mixool/across/tree/master/wireguard),实际上免费版无限流量对于解锁NF和解除google验证码效果和warp+效果是一样的

#### 二. [ViRb3/wgcf](https://github.com/ViRb3/wgcf) 生成配置
```bash
wget -O /usr/bin/wgcf https://github.com/ViRb3/wgcf/releases/download/v2.2.2/wgcf_2.2.2_linux_amd64
chmod +x /usr/bin/wgcf
wgcf register
wgcf generate
```
* 文件wgcf-profile.conf内有二行代码，如果需要IPv6就删除`AllowedIPs = 0.0.0.0/0`，需要IPv4就删除`AllowedIPs = ::/0`,解锁一般都是使用IPv6,即删除`AllowedIPs = 0.0.0.0/0`这一行
`sed -i "s/AllowedIPs = 0.0.0.0\/0//" wgcf-profile.conf`

#### 三. wireguard 安装
* 可以参考安装cloud内核并开启bbr的脚本来安装较新的内核
`bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/kvmbbr/bbr.sh) cloud`
* 内核支持，安装就很简单了
```bash
apt update
apt install wireguard resolvconf -y
```
* 把上一步生成的配置内容导入到/etc/wireguard目录下
`cat  wgcf-profile.conf >/etc/wireguard/wgcf.conf`
* 关闭 `wg-quick down wgcf`
* 启动 `wg-quick up wgcf`
* 状态 `wg`

#### 四. 配置ray路由规则
* 参考并编辑/usr/local/etc/xray/config.json配置文件部分内容如下，主要是二条directv6，之后重启服务即可
```json
"outbounds": 
	[
		{"protocol": "freedom","tag": "direct","settings": {}},
		{"protocol": "freedom","tag": "directv6","settings": {"domainStrategy": "UseIPv6"}}
	],

	"routing": 
	{
		"rules": 
		[
			{"type": "field","outboundTag": "directv6","domain": ["geosite:netflix","geosite:google"]}
		]
	}
```
