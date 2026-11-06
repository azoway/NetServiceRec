# vps使用gist上传代码

> 这篇文章围绕「vps使用gist上传代码」整理了可直接落地的步骤，适合按顺序操作并逐项验证结果。

<!--more-->

以下教程适用于debian:
1. 在[github](https://github.com/settings/tokens/new)申请MY_TOKEN,勾选gist权限
2. `apt install gist -y`
3. `umask 0077 && echo MY_TOKEN > ~/.gist`
4.  gist-paste命令使用方式:
```bash
Usage: gist-paste [-o|-c|-e] [-p] [-s] [-R] [-d DESC] [-u URL]
                          [--skip-empty] [-P] [-f NAME|-t EXT]* FILE*
       gist-paste --login
       gist-paste [-l|-r]

        --login                      Authenticate gist on this computer.
    -f, --filename [NAME.EXTENSION]  Sets the filename and syntax type.
    -t, --type [EXTENSION]           Sets the file extension and syntax type.
    -p, --private                    Makes your gist private.
        --no-private
    -d, --description DESCRIPTION    Adds a description to your gist.
    -s, --shorten                    Shorten the gist URL using git.io.
    -u, --update [ URL | ID ]        Update an existing gist.
    -c, --copy                       Copy the resulting URL to the clipboard
    -e, --embed                      Copy the embed code for the gist to the clipboard
    -o, --open                       Open the resulting URL in a browser
        --no-open
        --skip-empty                 Skip gisting empty files
    -P, --paste                      Paste from the clipboard to gist
    -R, --raw                        Display raw URL of the new gist
    -l, --list [USER]                List all gists for user
    -r, --read ID [FILENAME]         Read a gist and print out the contents
        --delete [ URL | ID ]        Delete a gist
    -h, --help                       Show this message.
    -v, --version                    Print the version.
```

## 相关阅读

- [gost下载安装配置vps进行端口转发中转加速](https://obvps.com/posts/gost下载安装配置vps进行端口转发中转加速)
- [AkileCloud US VPS Detailed Review: 4837 Optimized Line + Native IP + Streaming …](https://obvps.com/posts/akilecloud-us-vps-review-4837-optimized-line-native-ip-streaming)
- [AkileCloud 越南胡志明 VNPT NAT VPS 上新：年付 ¥158.88，动态 IPv4 + 独立 IPv6](https://obvps.com/posts/akilecloud-vnpt-nat-starter-vietnam-vps)
