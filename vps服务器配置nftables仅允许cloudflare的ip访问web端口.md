# 使用nftables配置VPS仅允许Cloudflare IP访问Web端口的完整指南

## 简介
在当今的网络安全环境中，保护您的VPS服务器免受恶意攻击至关重要。本文将详细介绍如何使用nftables防火墙规则，仅允许来自Cloudflare的IP地址访问您的Web服务端口，从而显著提升服务器的安全性。

## 前提条件
- 运行Linux的VPS服务器（如Ubuntu、Debian等）
- root或sudo权限
- 基本的命令行操作知识
- 已经配置了Cloudflare作为您的CDN服务

## 快速部署方法

### 1. 安装必要组件
首先需要安装curl和nftables：
```bash
apt update && apt install curl nftables -y
```

### 2. 部署防火墙规则
运行以下命令来部署预配置的nftables规则：
```bash
bash <(curl -s https://raw.githubusercontent.com/azoway/across/main/nftables/nft-cloudflare.sh)
```

## 配置说明
默认配置包含以下特性：
- ✅ 允许任意IP访问SSH端口（默认22端口）
- ✅ 仅允许Cloudflare的IPv4地址访问Web端口（默认80和443端口）
- ✅ 限制ICMP（ping）请求速率，防止DoS攻击
- ✅ 自动加载最新的Cloudflare IP地址列表

## 自定义配置
如需自定义配置，您可以：
1. 访问[nftables cloudflare脚本](https://github.com/azoway/across/blob/main/nftables/nft-cloudflare.sh)
2. 根据需求修改以下内容：
   - 允许访问的特定IP地址
   - 自定义端口规则
   - 调整访问限制策略

## 重要参考
- Cloudflare IP地址范围官方列表：https://www.cloudflare.com/ips/
- 本配置仅包含IPv4地址，如需IPv6支持请相应修改规则

## 故障排除
如果遇到问题，请检查：
1. nftables服务状态
2. 防火墙规则是否正确加载
3. 确保您的服务器可以访问Cloudflare的IP列表

## 安全提示
- 定期更新您的防火墙规则
- 监控服务器访问日志
- 保持系统和软件包更新

## 结语
通过以上配置，您的服务器将只接受来自Cloudflare的Web流量，显著提升安全性。建议定期检查和更新规则，确保持续的安全保护。