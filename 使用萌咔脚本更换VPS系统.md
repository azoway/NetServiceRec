# 萌咖脚本VPS一键重装系统教程 2025版 (Debian/Ubuntu/CentOS 全系统支持)

> 本教程提供一键重装 VPS 系统的完整指南，支持 Debian/Ubuntu/CentOS 系统，可自定义密码和国内外镜像源，适用于阿里云、腾讯云、AWS、GCP、Azure 等各类服务器。

## 功能特点

- ✨ 支持 Debian、Ubuntu、CentOS 等主流 Linux 发行版
- 🚀 一键快速重装，无需进入控制面板
- 🔧 支持自定义 root 密码和网络配置
- 🌐 内置国内外主流镜像源
- 💡 支持 32/64 位系统选择
- 🛡️ 支持自定义 IP、网关、子网掩码

## 使用场景

- 🔄 需要更换 VPS 操作系统版本
- 🎯 控制面板不支持特定系统版本
- ⚡ 需要快速重装系统
- 🔒 需要更安全的系统配置
- 📦 需要使用特定软件包源

## 重装命令

### 1. 海外服务器通用版本
```bash
bash <(curl -s https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh) -d 12 -v 64 -p 'MyPassword123..' -a
```

### 2. 国内服务器推荐版本

#### 2.1 阿里云源（推荐国内阿里云服务器使用）
```bash
bash <(curl -s https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh) -d 12 -v 64 -p 'MyPassword123..' -a --mirror 'http://mirrors.aliyun.com/debian/'
```

#### 2.2 腾讯云源（推荐国内腾讯云服务器使用）
```bash
bash <(curl -s https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh) -d 12 -v 64 -p 'MyPassword123..' -a --mirror 'http://mirrors.cloud.tencent.com/debian/'
```

#### 2.3 网易163源（推荐国内其他服务器使用）
```bash
bash <(curl -s https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh) -d 12 -v 64 -p 'MyPassword123..' -a --mirror 'http://mirrors.163.com/debian/'
```

### 3. 高级配置（自定义网络设置）
```bash
bash <(curl -s https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh) -d 12 -v 64 -p 'MyPassword123..' -a --mirror 'http://mirrors.163.com/debian/' --ip-addr 192.168.1.34 --ip-gate 192.168.1.1 --ip-mask 255.255.255.0
```

## 参数详解

| 参数 | 说明 | 示例 |
|------|------|------|
| `-d` | 指定系统版本 | `-d 12` 安装 Debian 12 |
| `-u` | 指定 Ubuntu 版本 | `-u 20.04` 安装 Ubuntu 20.04 |
| `-c` | 指定 CentOS 版本 | `-c 7` 安装 CentOS 7 |
| `-v` | 系统位数 | `-v 64` 使用64位系统 |
| `-p` | root 密码 | `-p 'MyPassword123..'` |
| `-a` | 自动安装模式 | `-a` |
| `--mirror` | 指定镜像源 | `--mirror 'http://mirrors.aliyun.com/debian/'` |
| `--ip-addr` | 指定 IP 地址 | `--ip-addr 192.168.1.34` |
| `--ip-gate` | 指定默认网关 | `--ip-gate 192.168.1.1` |
| `--ip-mask` | 指定子网掩码 | `--ip-mask 255.255.255.0` |

## 常见问题解决

### 1. 网络配置问题
如果遇到 interfaces 错误，请依次执行：
```bash
sudo apt-get update
sudo apt-get autoremove --purge ifupdown
sudo apt-get install ifupdown
```

### 2. 脚本下载失败
如果遇到脚本下载失败，可以尝试：
```bash
wget --no-check-certificate -qO InstallNET.sh 'https://raw.githubusercontent.com/MoeClub/Note/refs/heads/master/InstallNET.sh' && bash InstallNET.sh -d 12 -v 64 -p 'MyPassword123..' -a
```

## 安全建议

1. 🔐 密码设置
   - 使用至少12位的强密码
   - 包含大小写字母、数字和特殊字符
   - 避免使用常见词组和个人信息

2. 🛡️ 安装后操作
   - 立即修改默认 root 密码
   - 更新系统至最新版本
   - 配置防火墙规则
   - 禁用不需要的服务

3. 💾 数据安全
   - 执行重装前备份重要数据
   - 记录当前系统配置信息
   - 保存重要的系统文件

## 兼容性说明

- ✅ 支持大部分主流 VPS 提供商
- ✅ 支持 KVM、XEN、VMware 等虚拟化平台
- ✅ 支持 DHCP 和静态 IP 配置
- ⚠️ 部分 OpenVZ 架构可能不支持

## 更新日志

- 2025
