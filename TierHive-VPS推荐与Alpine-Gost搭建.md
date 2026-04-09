# TierHive NAT VPS 推荐：新加坡最便宜的服务器 + Alpine + GOST SOCKS5

**推荐链接（通过此链接注册可支持作者）：**  
<https://tierhive.com/r/3CF119212CF2>

---

## 一、为什么写这篇

[TierHive](https://tierhive.com/r/3CF119212CF2) 是 **NAT 架构 + 按小时计费** 的 VPS 平台：没有独立公网 IPv4，通过面板做端口转发；账号侧有 **/24 私网** 与跨机房 mesh 等能力。官网提供 HAProxy、SSL、邮件中继、数据库卸载、网络盘等配套。

作者在 **新加坡节点**（底层与 **OVH** 相关，以控制台为准）使用 **最小规格：128 MB 内存 + 1 GB NVMe**，系统为 **Alpine Linux**，另加 **256 MB swap**，用 **GOST** 搭建 **SOCKS5**，长期运行稳定；折合月成本约 **0.1 美元量级**（以实际 hourly 账单为准）。

---

## 二、注册与机型选择

1. 打开：<https://tierhive.com/r/3CF119212CF2> 注册（试用政策以官网为准，常见为小额试用额度、最低充值约 $3 等）。
2. 创建 VPS 时选择：**Singapore**，镜像 **Alpine**，资源选 **128M / 1G** 或你需要的档位。
3. NAT 说明：对外服务需在面板配置 **端口转发**；若 SOCKS5 仅作出站或仅本机/隧道访问，可减少公网暴露面。

---

## 三、Alpine 基础与 256 MB Swap

### 创建固定 256 MB 的 swap 文件

与常见「Gost + 小内存 VPS」方案一致，**128 MB 内存强烈建议加 swap**，这里固定为 **256 MB**：

```sh
dd if=/dev/zero of=/swapfile bs=1M count=256 status=progress
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

可选：降低「过早换出」的倾向（按喜好调整，例如 30～60）：

```sh
echo 'vm.swappiness=40' >> /etc/sysctl.conf
sysctl -p
```

确认：

```sh
free -h
swapon --show
apk update
```

---

## 四、GOST 安装（对齐常见配置流程）

### 1. 查看架构并下载

```sh
uname -m
# x86_64 → amd64；aarch64 → arm64
```

从 [go-gost/gost Releases](https://github.com/go-gost/gost/releases) 下载对应 **linux_amd64** 或 **linux_arm64** 压缩包。以下为 **v3.2.6** 示例（若已有新版本，请把 URL 中的版本号改成 release 页上的文件名）：

```sh
cd /usr/local/bin
# x86_64
curl -fL -o gost.tgz 'https://github.com/go-gost/gost/releases/download/v3.2.6/gost_3.2.6_linux_amd64.tar.gz'
# 若 CPU 较新可选用 amd64v3 构建（不存在则退回上一行）
# curl -fL -o gost.tgz 'https://github.com/go-gost/gost/releases/download/v3.2.6/gost_3.2.6_linux_amd64v3.tar.gz'
# aarch64 示例：
# curl -fL -o gost.tgz 'https://github.com/go-gost/gost/releases/download/v3.2.6/gost_3.2.6_linux_arm64.tar.gz'

tar -xzf gost.tgz
chmod +x gost
./gost -V
```

### 2. 使用 YAML 配置（GOST v3 推荐方式）

创建配置目录与文件：

```sh
mkdir -p /etc/gost
vi /etc/gost/config.yaml
```

**示例 A：带账号密码的 SOCKS5（监听所有接口，适合 NAT 上配合面板转发端口）**

```yaml
services:
  - name: socks5
    addr: ":1080"
    handler:
      type: socks5
      auth:
        auths:
          - username: "你的用户名"
            password: "强密码请自行更换"
    listener:
      type: tcp
```

**示例 B：仅本机监听（更安全，配合 SSH -D 或 VPN 再访问）**

```yaml
services:
  - name: socks5-local
    addr: "127.0.0.1:1080"
    handler:
      type: socks5
    listener:
      type: tcp
```

前台测试（确认无报错后再做服务化）：

```sh
/usr/local/bin/gost -C /etc/gost/config.yaml
```

客户端用 `服务器IP:面板转发端口` 或 `127.0.0.1:1080`（视你的监听方式而定）连接 SOCKS5。

### 3. 使用 OpenRC 在 Alpine 上常驻（与「配置完成后交给 init」的步骤一致）

```sh
vi /etc/init.d/gost
```

写入（注意路径与配置文件一致）：

```sh
#!/sbin/openrc-run

name="gost"
description="GO Simple Tunnel"
command="/usr/local/bin/gost"
command_args="-C /etc/gost/config.yaml"
command_background="yes"
pidfile="/run/${RC_SVCNAME}.pid"

depend() {
    need net
}
```

```sh
chmod +x /etc/init.d/gost
rc-update add gost default
rc-service gost start
rc-service gost status
```

---

## 五、安全与计费提示

- **认证**：公网可达的 SOCKS5 务必 **用户名密码** 或 **仅内网/SSH 隧道**，并配合 TierHive **端口转发** 最小暴露。
- **合规**：遵守服务商 AUP 与当地法律，勿用于未授权访问或滥用。
- **计费**：按小时计费；论坛中运营方曾说明 **最短按 1 小时计费** 等规则，反复重装/调试会有成本，建议先本地验证配置再长期开机。

---

## 六、小结

- **商家**：[TierHive](https://tierhive.com/r/3CF119212CF2) — NAT、小时计费、多机房、控制面板功能较全。  
- **作者方案**：新加坡最小机 + Alpine 128MB + **256 MB swap** + GOST SOCKS5，轻量稳定、月费极低。  
- **GOST 方案结构**：安装二进制 → `/etc/gost/config.yaml` 定义 `services` → `gost -C` 前台测试 → OpenRC 后台自启

**再次附上推荐链接：**  
<https://tierhive.com/r/3CF119212CF2>
