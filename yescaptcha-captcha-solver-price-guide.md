# YesCaptcha 验证码识别平台：任务类型、真实成本和接入步骤

YesCaptcha 是一个按点数扣费的验证码识别服务。1 元换 1000 点，识别失败和超时自动退点，充值没有月费也没有套餐绑定。写爬虫、跑自动注册脚本、搭号池的人，终点基本都会碰到它。

这篇不讲"验证码是什么"这种常识。重点说三件事：你遇到的验证码该选哪个任务类型，一次识别到底花多少钱，代码怎么接才不会一上手就卡在轮询上。

注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

## 先确认你要解决的是不是验证码问题

很多人第一次找打码平台，其实问题不在验证码。

页面直接 403、返回 Cloudflare 的拦截页，那是 IP 或 User-Agent 的问题，买多少点数都没用。页面能打开但抓不到数据，那是选择器和渲染时机的问题。只有在页面上真的看到了勾选框、"我是人类"按钮、九宫格图片，或者那个右下角自动打勾的小方框，才轮到打码平台出场。

这里有个高频误判。整页被 Cloudflare 拦下、显示"请稍候…正在检查您的浏览器"，那是 5 秒盾，属于另一个任务类型，返回的是 Cookie 而不是 token。把 5 秒盾的参数填进 Turnstile 的任务里，`websiteKey` 抄得再准也过不了。

## 按页面现象选任务类型

下表按"你在页面上看到什么"组织，比按产品名记更实用。

| 页面上看到什么 | 实际类型 | 任务类型 | 单价 |
|---|---|---|---|
| "我不是机器人"复选框，点开是九宫格 | reCAPTCHA v2 | `NoCaptchaTaskProxyless` | 15 点 |
| 没有复选框，点提交才弹图片 | reCAPTCHA v2 隐形版 | 同上，加 `"isInvisible": true` | 15 点 |
| 页面加载 `recaptcha/enterprise.js` | reCAPTCHA v2 企业版 | `RecaptchaV2EnterpriseTaskProxyless` | 20 点 |
| 无感验证，不弹任何东西，只要分数 | reCAPTCHA v3 | `RecaptchaV3TaskProxyless` | 20 点 |
| 九宫格加"我是人类"标题 | hCaptcha | `HCaptchaTaskProxyless` | 30 点 |
| 右下角小框"确认您是真人" | Cloudflare Turnstile | `TurnstileTaskProxyless` | 25 点 |
| 整页"请稍候…""正在检查您的浏览器" | Cloudflare 5 秒盾 | `CloudFlareTaskS2` / `CloudFlareTaskS3` | 25 / 20 点 |
| 扭曲的英文字母数字 | 图片验证码 | `ImageToTextTaskMuggle` | 2 点 |
| 只想让程序告诉你该点哪几张图 | 图像识别 | `ReCaptchaV2Classification` / `HCaptchaClassification` | 6 / 8 点 |

几个选择上的判断。

名字里带 `Proxyless` 的，是用 YesCaptcha 自己的网络去加载验证码，你不需要准备代理。名字里没有的，比如 `NoCaptchaTask`、`HCaptchaTask`、`TurnstileTask`、`CloudFlareTaskS2`，全部要你自己传 `proxyType`、`proxyAddress`、`proxyPort`。

什么时候必须用自己的代理？两种情况。目标网站对访问来源 IP 敏感，换了 IP 之后 token 直接作废。或者你拿到 token 之后，要在同一个 IP 上继续完成后续操作。这两个场景用 Proxyless 版本，成功率会明显掉。

带 `M1` 后缀的是另一条线路，参数一样，价格多数比普通版贵 5 点，hCaptcha 是例外，两个版本都是 30 点。正式跑之前同一套参数两个都试一遍，谁过率高用谁，或者干脆做成互备。reCAPTCHA v3 还有 `M1S7`、`M1S9` 两个变体，强制返回 0.7 和 0.9 的分数，30 点和 35 点一次，网站分数门槛卡得死的时候才有意义。

## YesCaptcha 一次识别多少钱

计费规则本身不复杂，但细节决定了你的实际成本。

异步类型（返回 token 的那几类）在任务创建成功时扣点，之后如果识别失败报 `ERROR_CAPTCHA_UNSOLVABLE`，或者超过 110 秒左右超时报 `ERROR_TASK_TIMEOUT`，点数自动退回。同步类型（图像识别、图片英数字）是返回结果时才扣。参数错了、余额不够、超过并发上限这类在 `createTask` 就报错的请求，一分不扣。

也就是说，失败不花钱，但失败会烧时间。批量跑的时候真正拖慢你的是重试和排队，不是点数。

按 1 元 = 1000 点折算：

| 任务 | 点数 | 折合每千次 |
|---|---:|---:|
| 图片英数字 | 2 | 约 2 元 |
| reCAPTCHA v2 token | 15 | 约 15 元 |
| Turnstile token | 25 | 约 25 元 |
| hCaptcha token | 30 | 约 30 元 |

一个号池项目注册 200 个账号，每次注册吃一次 Turnstile，成本是 5 元左右的点数。这个数字通常远小于代理、邮箱域名和你能省下的人工时间。真正该算的是成功率：如果通过率只有五成，你会花掉两倍的任务量，还要赔上重试的时间。

余额有个硬门槛，必须大于 10 点才能创建任务，不够直接返回 `ERROR_ZERO_BALANCE`。

充值支持微信、支付宝、PayPal、加密货币（Cryptomus，走 BTC / ETH / USDT）、对公转账。累计充值到门槛自动升 VIP，之后每次充值按等级比例额外赠点，最高 VIP 10，累计 48000 元，赠送 40%。

| 等级 | 累计充值 | 每次充值赠送 |
|---|---|---:|
| VIP 1 | 10 元 | 2% |
| VIP 2 | 100 元 | 5% |
| VIP 3 | 500 元 | 8% |
| VIP 4 | 1000 元 | 10% |
| VIP 5 | 2000 元 | 15% |
| VIP 6 | 3000 元 | 20% |
| VIP 7 | 6000 元 | 25% |
| VIP 8 | 12000 元 | 30% |
| VIP 9 | 24000 元 | 35% |
| VIP 10 | 48000 元 | 40% |

累计制，不要求一次充完。第一次直接充 1000 元，这次就按 VIP 4 的 10% 送。用邀请链接注册的账号会直接拿到一个初始 VIP 等级，规则是邀请人等级减 1，最低 VIP 1、最高 VIP 6，具体以后台显示为准。

注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

第一次不要充太多。先把链路跑通，确认你的场景通过率能接受，再决定充多少。

## 接入：先查余额，再测一张图

API 只有两个节点，接口和参数完全一样：

- 国际节点 `https://api.yescaptcha.com`
- 国内节点 `https://cn.yescaptcha.com`

服务器在中国大陆的走 cn，其他地区走国际节点。所有方法都是 HTTPS POST JSON，`clientKey` 放在请求体里鉴权。有一个坑必须记住：在哪个节点创建的任务，就只能到哪个节点查结果，混用会一直查不到。

先确认密钥能用。`getBalance` 不扣点：

```bash
curl -s https://api.yescaptcha.com/getBalance \
  -H 'Content-Type: application/json' \
  -d '{"clientKey": "YOUR_CLIENT_KEY"}'
```

返回 `{"errorId": 0, "balance": 12345, ...}` 就通了。返回 `ERROR_KEY_DOES_NOT_EXIST` 说明密钥复制不全。

下面是一个能直接跑的完整脚本。它处理了同步和异步两种返回方式、超时、失败重试和并发限流，任务类型和参数从命令行传。

```python
# Python 3.9+ | 依赖: pip install requests
# 运行: YESCAPTCHA_CLIENT_KEY=你的key python solve.py turnstile https://example.com/login 0x4AAAAAAA_SITE_KEY

import os
import sys
import time

import requests

CLIENT_KEY = os.environ["YESCAPTCHA_CLIENT_KEY"]
REGION = os.environ.get("YESCAPTCHA_REGION", "intl")

ENDPOINTS = {
    "intl": "https://api.yescaptcha.com",
    "cn": "https://cn.yescaptcha.com",
}
BASE = ENDPOINTS[REGION]

# 任务类型映射，用哪个填哪个
TASK_TYPES = {
    "turnstile": "TurnstileTaskProxyless",
    "recaptcha_v2": "NoCaptchaTaskProxyless",
    "hcaptcha": "HCaptchaTaskProxyless",
}


def call(method, payload):
    body = {"clientKey": CLIENT_KEY}
    body.update(payload)
    resp = requests.post(f"{BASE}/{method}", json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_balance():
    return call("getBalance", {}).get("balance")


def solve(task_type, website_url, website_key, timeout=180, interval=5):
    created = call("createTask", {
        "task": {
            "type": task_type,
            "websiteURL": website_url,
            "websiteKey": website_key,
        }
    })

    if created.get("errorId") != 0:
        raise RuntimeError(
            f"createTask 失败: {created.get('errorCode')} {created.get('errorDescription')}"
        )

    # 同步类型（图片识别、图像分类）在这里就直接有结果了
    if "solution" in created:
        return created["solution"]

    task_id = created["taskId"]
    deadline = time.time() + timeout

    while time.time() < deadline:
        time.sleep(interval)
        result = call("getTaskResult", {"taskId": task_id})

        if result.get("errorId") != 0:
            raise RuntimeError(
                f"getTaskResult 失败: {result.get('errorCode')} {result.get('errorDescription')}"
            )

        status = result.get("status")
        if status == "ready":
            return result["solution"]
        # status == "processing" 时继续等，不要改参数重发

    # 超时：任务会由平台判定并退点，本地直接放弃这一次
    raise TimeoutError(f"taskId {task_id} 在 {timeout} 秒内没有返回结果")


def solve_with_fallback(task_type, website_url, website_key, fallbacks=()):
    """主类型失败时按顺序换备用线路，每次都重新建任务。"""
    candidates = [task_type, *fallbacks]
    last_error = None

    for candidate in candidates:
        try:
            return candidate, solve(candidate, website_url, website_key)
        except (RuntimeError, TimeoutError) as exc:
            # 并发超限不要立刻重试，先让已发出的请求回来
            if "ERROR_THREADS_MAXIMUM" in str(exc):
                time.sleep(2)
            last_error = exc

    raise RuntimeError(f"全部任务类型均失败，最后一个错误: {last_error}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in TASK_TYPES:
        print("用法: solve.py <turnstile|recaptcha_v2|hcaptcha> <页面URL> <sitekey>")
        sys.exit(1)

    kind, url, sitekey = sys.argv[1], sys.argv[2], sys.argv[3]
    task_type = TASK_TYPES[kind]

    print("余额:", get_balance(), "点")

    fallbacks = {
        "turnstile": ["TurnstileTaskProxylessM1"],
        "recaptcha_v2": ["RecaptchaV2TaskProxyless"],
        "hcaptcha": ["HCaptchaTaskProxylessM1"],
    }[kind]

    used, solution = solve_with_fallback(task_type, url, sitekey, fallbacks)
    print("任务类型:", used)
    print("token:", solution.get("token"))
    # 返回里带了 userAgent 时，提交 token 必须用它，否则大概率被判定为无效
    print("userAgent:", solution.get("userAgent"))
```

跑 Turnstile 时，`websiteKey` 就是页面里 `turnstile.render` 那个 `sitekey`，一般以 `0x` 开头。绝大多数情况传 `websiteURL` 和 `websiteKey` 就够了。如果确定这两个都对还是过不了，再看网页调用时有没有传 `action` 和 `cData`，有的话原样填进 `pageAction` 和 `data`。这两个字段是最后手段，不是默认要填。

## 不会写代码的那条路

YesCaptcha 还有一个浏览器插件，叫 YesCaptcha 人机助手，Chrome 和 Firefox 都有，插件本身免费，识别时按用到的 API 从同一个账户余额扣点。

装上之后在插件图标里填 `clientKey`，遇到 reCAPTCHA v2、hCaptcha、FunCaptcha、AWS WAF 的图片题会自动识别并点。普通字符验证码不带自动识别，需要在图片上右键"标记为验证码"、在输入框上右键"输入验证码"，插件识别后帮你填进去。

适合的人群很明确：用比特浏览器、AdsPower 这类指纹浏览器做多账号操作，或者跑 Kiwi Browser 的手机场景。不适合的也很明确：插件靠 DOM 定位，网站改版就失效，不是所有站都能过，批量无人值守也不该指望它。

## 几个会浪费钱和时间的地方

**两个节点混用。** 在 `api.yescaptcha.com` 建的任务，去 `cn.yescaptcha.com` 查 `getTaskResult`，永远查不到结果，一直等到超时。全局统一一个 BASE，别在代码里散着写域名。

**token 拿到不当场用。** token 是一次性的。reCAPTCHA 的有效期大约 120 秒，实操上拿到之后 60 秒内就得提交。中途去跑别的逻辑，token 就废了，白扣点。

**并发超限后死循环重试。** 平台按账号、按任务类型限制同时处理中的任务数，超了返回 `ERROR_THREADS_MAXIMUM`，响应里带 `limit` 字段告诉你当前上限。这类请求不扣点，也不计入自动暂停，但立即循环重发只会继续报错。正确做法是控制"同时在等结果的请求数"，用信号量或固定大小线程池，收到错误后等已有请求回来再发。

**错误刷得太密。** 同一个 `clientKey` 一分钟内出现 100 次错误，账号会被暂停创建任务 5 分钟，返回 `ERROR_IP_BLOCKED_5MIN`。参数类错误（`ERROR_TASK_ABSENT`、`ERROR_TASK_NOT_SUPPORTED`、`ERROR_REQUEST_FORMATS`）都算在内。上线前先单线程跑通，别拿生产并发去试错。

**拿到 token 却被目标站拒绝。** 这种情况按成功计费，因为平台无法知道网站的判定结果。原因通常在环境不在识别：IP 和注册时不一致、User-Agent 没对上、浏览器指纹太假、行为轨迹不像人。可以换成自带代理的任务类型并在提交时走同一个代理，或者干脆改用图像识别，让程序告诉你在真浏览器里点哪几张图。

**图像识别点错了。** 只有 5 类支持上报返点：`FunCaptchaClassification`、`HCaptchaClassification`、`ReCaptchaV2Classification`、`AwsClassification`、`bCaptchaClassification`。要在任务创建后 1 小时内调 `report`，同一个任务只算一次，大约 24 小时后结算。结算时会和同期、同题的其他用户比较，上报失败率明显高于水平的，按同期失败率返还，不是报了就全退。返回 token 的类型上报不返点。

## 它在整条链路里的位置

打码只解决"过验证码"这一环。邮箱能不能收到验证码、代理 IP 干不干净、账号注册后能活多久，这些都不在它的责任范围内。把打码当成万能药的项目，最后都栽在后面几环上。

站内已经把两条常见链路写完了，需要的话直接看：

- Grok Token 号池：CLIProxyAPI 加 grok-build-auth，用 Turnstile 打码：[https://obvps.com/posts/grok-token-pool-cliproxyapi-yescaptcha-guide/](https://obvps.com/posts/grok-token-pool-cliproxyapi-yescaptcha-guide/)
- NVIDIA Build 的 `nvapi` 批量注册，用 hCaptcha 打码：[https://obvps.com/posts/nvidia-build-apikey-register-somanyapikeys-yescaptcha/](https://obvps.com/posts/nvidia-build-apikey-register-somanyapikeys-yescaptcha/)

这两篇里的打码环节都是同一个账户，一个 `clientKey` 可以在多个程序、多个浏览器里同时用，共享余额和并发额度。

## 常见问题

### 识别失败扣钱吗

不扣。识别失败（`ERROR_CAPTCHA_UNSOLVABLE`）和超时（`ERROR_TASK_TIMEOUT`）的任务自动退点，创建任务时就报错的请求也不扣。只有拿到了 token 但目标网站不接受的情况按成功计费。

### 是人工打码还是机器识别

机器识别，基于机器学习模型。所以速度是秒级到几十秒级，不是等人工接单。

### 识别一次要多久

异步任务通常几秒到几十秒，最长约 110 秒，少数类型会到 180 到 220 秒。超时自动退点。图像识别和图片英数字是同步的，一次请求直接返回。

### 国内服务器该用哪个节点

`cn.yescaptcha.com`。国际节点从大陆访问会有延迟和掉线，成功率和速度都差一截。

### 用打码平台会导致目标网站封号吗

平台只返回识别结果，不接触你在目标网站上的账号。封不封号由目标网站自己的规则判定，跟用不用打码没有直接因果。但自动化注册、批量操作本身在多数平台的服务条款里是不允许的，这部分风险得自己评估。

## 怎么开始

想先确认服务能用，最省的做法是注册后充最小的额度，用 `getBalance` 确认到账，再跑一次 `ImageToTextTaskMuggle` 识别一张图。这个类型 2 点一次、同步返回、不依赖任何第三方网站，是验证账户和代码是否正常的成本最低的测试。

确认链路通了，再换成你实际要处理的验证码类型，单线程跑十次，记下成功率和平均耗时。通过率低于七成的话，先别扩量，去查 IP 和参数，不要用充值和并发去掩盖环境问题。

注册入口：
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

本文基于 2026-10-28 的 YesCaptcha 官方文档、后台公开价格页和任务类型页整理。任务类型、价格、赠送比例、并发额度和节点地址都可能调整，充值前请以后台和官方文档的实时页面为准。
