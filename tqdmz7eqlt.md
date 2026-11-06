# vps服务器必备命令和软件

> 这篇文章围绕「vps服务器必备命令和软件」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

## 常用命令

以下信息为公开套餐与经验整理，具体价格和库存请以下单页实时展示为准。

1. **ssh连接**：通过SSH连接到你的vps服务器，使用以下命令（Windows用户需要使用[Mobaxterm](https://mobaxterm.mobatek.net/)或[Putty](https://www.putty.org/)等工具）。

```
ssh -p [端口号] [用户名]@[服务器IP地址]
```

2. **文件传输**：使用SCP命令可以将本地文件传输到vps服务器上或者将vps服务器上的文件传输到本地。

```
// 本地文件上传到服务器
scp -P [端口号] [本地文件路径] [用户名]@[服务器IP地址]:[服务器目标路径]

// 服务器文件下载到本地
scp -P [端口号] [用户名]@[服务器IP地址]:[服务器文件路径] [本地目标路径]
```

3. **软件安装**：使用apt-get可以安装各种软件包。

```
sudo apt-get install [软件包名称]
```

4. **关闭和重启服务器**：使用以下命令来关闭或重启vps服务器。

```
sudo shutdown -h now // 关闭服务器
sudo shutdown -r now // 重启服务器
```

5. **系统信息查询**：可以使用以下命令查询服务器的系统信息。

```
uname -a // 查看操作系统信息
free -m // 查看内存使用情况
df -h // 查看磁盘使用情况
top // 查看进程使用情况
```

## 常用软件

1. **Web服务器**：Apache和Nginx是两个最常见的Web服务器。使用以下命令来安装它们。

```
sudo apt-get install apache2 // 安装Apache
sudo apt-get install nginx // 安装Nginx
```

2. **数据库**：MySQL和PostgreSQL是两个最常用的关系型数据库。使用以下命令来安装它们。

```
sudo apt-get install mysql-server // 安装MySQL
sudo apt-get install postgresql // 安装PostgreSQL
```

3. **版本控制工具**：Git是最常用的版本控制工具。使用以下命令来安装它。

```
sudo apt-get install git
```

以上是一些常用的vps服务器命令和软件，希望能够帮助你更好地管理和使用自己的服务器。当然，还有很多其他的命令和软件，需要根据自己的需求进行安装和学习。

## 相关阅读

- [gost下载安装配置vps进行端口转发中转加速](https://obvps.com/posts/gost下载安装配置vps进行端口转发中转加速)
- [AkileCloud US VPS Detailed Review: 4837 Optimized Line + Native IP + Streaming …](https://obvps.com/posts/akilecloud-us-vps-review-4837-optimized-line-native-ip-streaming)
- [AkileCloud 越南胡志明 VNPT NAT VPS 上新：年付 ¥158.88，动态 IPv4 + 独立 IPv6](https://obvps.com/posts/akilecloud-vnpt-nat-starter-vietnam-vps)
