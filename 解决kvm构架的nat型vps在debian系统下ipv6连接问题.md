# 解决KVM构架的NAT型VPS在Debian系统下IPV6连接问题

> 这篇文章围绕「解决KVM构架的NAT型VPS在Debian系统下IPV6连接问题」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

但是OB在使用过程中发现用商家的Debian模板装好的系统IPv6不能使用。由于NAT型的低廉VPS无技术支持，只好自己想办法解决问题了。经过多次尝试后，OB终于在对比其它商家NAT型VPS的网络配置文件，修改`/etc/network/interfaces`文件后重启系统，成功启用IPv6，以下是修改前后的文件内容，以供参考：  
  
#### 修改前，执行命令：`cat /etc/network/interfaces`
```bash
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet static
address 172.36.0.29
netmask 255.255.255.0

gateway 172.36.0.1
iface eth0 inet6 static
	address 2406:3280:C:0b0d:0cf0:0c0f:0d0e:0001
	netmask 64

	gateway 2406:4380:F::1
```  

#### 修改后，执行命令：`cat /etc/network/interfaces`
```bash
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0

iface eth0 inet static
address 172.36.0.29
netmask 255.255.255.0
gateway 172.36.0.1

iface eth0 inet6 static
    address 2406:3280:C:0b0d:0cf0:0c0f:0d0e:0001
    netmask 64

    post-up /sbin/ip -f inet6 route add 2406:4380:F::1 dev eth0
    post-up /sbin/ip -f inet6 route add default via 2406:4380:F::1
    pre-down /sbin/ip -f inet6 route del 2406:4380:F::1 dev eth0
    pre-down /sbin/ip -f inet6 route del default via 2406:4380:F::1
```
#### 通过对比发现：
主要即是替换`iface eth0 inet6 static`配置中`gateway`的原本值为具体命令。
> `gateway 2406:4380:F::1 >> post-up .....`  
具体的各项值得按照VPS分配到的地址来配置，上例中的值也是OB随机设置的，在网络上不要随意暴露自己的VPS网络地址，能有效的减少VPS受到各种攻击的可能性。
