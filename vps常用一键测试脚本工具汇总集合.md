# VPS常用一键测试脚本工具汇总集合

> 这篇文章围绕「VPS常用一键测试脚本工具汇总集合」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

#### Bench.sh
来自秋水逸冰的Bench.sh脚本，可以查看 Linux 系统信息，以及网络带宽及硬盘读写速率测试。
使用方法：
`wget -qO- bench.sh | bash`

#### UnixBench
来自秋水逸冰的UnixBench一键脚本。
UnixBench是一个类unix系`（Unix，BSD，Linux）`统下的性能测试工具，一个开源工具，被广泛用与测试linux系统主机的性能。主要测试项目有：系统调用、读写、进程、图形化测试、2D、3D、管道、运算、C库等系统基准性能提供测试数据。
使用方法：
```bash
wget --no-check-certificate https://github.com/teddysun/across/raw/master/unixbench.sh
chmod +x unixbench.sh
./unixbench.sh
```

#### SuperBench.sh
主要可用于获取基本硬件信息、CPU跑分测试、硬盘IO速度、国内网络测速等。
使用方法：
`wget -qO- git.io/superbench.sh | bash`

#### ZBench
一个一键检测服务器基本性能的脚本
测试完之后呢，会在 /root / 下面生成一个 report.html 的文件。
使用方法：
`wget https://raw.githubusercontent.com/FunctionClub/ZBench/master/ZBench-CN.sh && chmod +x ZBench-CN.sh && bash ZBench-CN.sh`

#### mPing.sh
mPing回程测试，可以测试回程PING检测。
`wget https://raw.githubusercontent.com/helloxz/mping/master/mping.sh && chmod +x mping.sh && bash mping.sh`

#### 锐速破解全功能版
91yun的锐速破解版linux一键自动安装包
安装方法：
`wget -N --no-check-certificate https://github.com/91yun/serverspeeder/raw/master/serverspeeder.sh && bash serverspeeder.sh`
卸载方法：
`chattr -i /serverspeeder/etc/apx* && /serverspeeder/bin/serverSpeeder.sh uninstall -f`

#### 锐速破解版linux一键自动安装包
锐速 serverSpeeder
安装方法：
```bash
wget --no-check-certificate -qO /tmp/appex.sh "https://raw.githubusercontent.com/0oVicero0/serverSpeeder_Install/master/appex.sh" && bash /tmp/appex.sh 'install'
```
卸载方法：
```bash
wget --no-check-certificate -qO /tmp/appex.sh "https://raw.githubusercontent.com/0oVicero0/serverSpeeder_Install/master/appex.sh" && bash /tmp/appex.sh 'uninstall'
```

#### 魔改BBR
安装方法：
KVM版
```bash
wget https://raw.githubusercontent.com/tcp-nanqinlang/general/master/General/CentOS/bash/tcp_nanqinlang-1.3.2.sh && chmod +x ./tcp_nanqinlang-1.3.2.sh && bash ./tcp_nanqinlang-1.3.2.sh
```
OpenVZ版
`curl https://raw.githubusercontent.com/mixool/script/master/rinetd.sh | bash`

#### PING速度测试
1、`http://ping.chinaz.com/`

2、`http://www.webkaka.com/Ping.aspx`

Ping工具可以检测到较多国内和国外节点的PING速度，在一定程度上PING速度也是比较重要的，可以看到服务器的丢包情况，以及速度。比如我们在选择美国VPS主机的时候，一般能在200速度之内算是不错的。

#### 路由节点跟踪
1、`http://www.webkaka.com/Tracert.aspx`

2、`https://www.ipip.net/traceroute.php`

路由跟踪测试还是有必要的，我们可以看到服务器IP节点的走向。我们在选择服务器机房的时候，不能只看地理位置，同样的线路走向有很大的区别。  

#### 大家可以用OB推荐的廉价月付的virmach的各个节点VPS测试以作测试:  
> [Virmach最新优惠 VPS 1美元起售](https://billing.virmach.com/aff.php?aff=2385&gid=18)  
> [Test IP & Looking Glass Locations](https://billing.virmach.com/aff.php?aff=2385&http://lg.virmach.com/)
