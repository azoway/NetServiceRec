# oracle甲骨文免费vps重装系统

> 这篇文章围绕「oracle甲骨文免费vps重装系统」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

  
#### 1. 为了区分,把待重装的VPS称为实例B。首先通过新建付费实例A，来获得一个正常的引导卷
* 新建实例的时候可以使用cloud-init来设置root账号密码登录：

```bash
#!/bin/bash
echo root:qwerasdfzxcv |sudo chpasswd root
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config;
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config;
sudo reboot
```

* 登录实例A后，可以使用萌咔DD脚本更换VPS系统: https://obvps.com/2020/06/04/moeos.html
2020/10/21更新： DD时遇到interfaces错误先执行：`sudo apt-get autoremove --purge ifupdown; sudo apt-get install ifupdown` 

#### 2. 进入B实例面板，停止实例B（非终止！！！）后，分离实例B的引导卷。登录实例A，选择附加B的引导卷。这步按照给出的iscsi命令在A机器上执行
* 成功挂载后。A实例执行命令 fdisk -l 会有2个卷： /dev/sda && /dev/sdb

#### 3. 在A实例上执行dd或者fv命令重写B引导卷： `dd if=/dev/sda of=/dev/sdb` 或者 `pv < /dev/sda > /dev/sdb`
* 推荐使用pv，速度较快，有进度条

#### 4. 重写B引导卷成功后，在A实例面板分离B引导卷，并重新挂载到B实例，成功启动B实例后即可用A的登录信息登录B实例

#### 5. 终止付费的A实例,注意选中同时删除A引导卷,避免扣费

#### Tips:
参考内容： 
* https://dxz.plus/posts/oracle/
* https://www.hostloc.com/thread-725006-1-1.html
