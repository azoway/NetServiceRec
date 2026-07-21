# Building a Grok token pool with CLIProxyAPI, grok-build-auth and YesCaptcha

A Grok token pool is not a magic script that bypasses xAI rules. The practical version is simpler: take Grok Build accounts you are allowed to use, export their OAuth auth files, load them into CLIProxyAPI, and give your clients one stable OpenAI-compatible endpoint.

In this setup, CLIProxyAPI is the gateway. grok-build-auth handles x.ai signup, SSO, Grok Build OAuth PKCE and `type=xai` auth export. YesCaptcha only solves the Turnstile step. It will not fix bad mailboxes, poor proxy quality, account risk, or platform policy changes.

YesCaptcha signup link:
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

## Check whether you really need a pool

If you only use the Grok web app once in a while, do not build this. The official account flow is easier.

This setup makes sense if you already run CLIProxyAPI, want to add Grok Build access, and need a cleaner way to track multiple accounts. It is also useful when your clients only want a fixed Base URL and API key instead of dealing with Grok login flows themselves.

It is a poor fit if you only use one web account, do not want to maintain mailboxes and proxies, do not want to read logs, or expect the tool to handle every failure for you. A pool still has all the boring problems: mailbox failures, expired OAuth, 401 errors, quota changes, proxy issues and account bans.

## The stack

The basic flow looks like this:

```text
Mailbox or controlled mail domain
    ↓
grok-build-auth signs up or logs in to x.ai and obtains SSO
    ↓
YesCaptcha solves Turnstile
    ↓
Grok Build OAuth PKCE completes
    ↓
A CLIProxyAPI-compatible type=xai auth JSON is exported
    ↓
CLIProxyAPI loads auth-dir and exposes one API endpoint
```

Keep the layers separate. If Turnstile fails, check YesCaptcha and the proxy. If the verification code never arrives, check the mailbox. If OAuth stops, check the grok-build-auth flow. If the client gets 401, check the auth state inside CLIProxyAPI.

## What you need

| Item | Role | Note |
|---|---|---|
| CLIProxyAPI | Public API gateway | Verify service, config and auth-dir first |
| grok-build-auth | Signup, SSO, OAuth and auth export | Python 3.9+, dependencies from requirements.txt |
| YesCaptcha API key | Turnstile solving | Start with a small balance and one test account |
| Mailbox setup | x.ai verification code | tempmail is quick, a controlled domain is better long term |
| Proxy | Stable signup and OAuth environment | Stability matters more than constant IP rotation |
| Run log | Mailbox, proxy, auth file and status | You will need this when accounts fail |

YesCaptcha uses a points model. Public pricing material commonly describes `1 RMB = 1000 points`. Simple image tasks can be very cheap. Turnstile tasks are usually higher, often around 25 to 30 points per attempt. Check the live YesCaptcha dashboard for current pricing and bonuses.

## Get CLIProxyAPI stable first

Do not start by creating accounts. Start with the gateway.

Check these points first:

- the service starts cleanly
- the config file path is correct
- `auth-dir` exists and has the right permissions
- the management API or panel can show account status
- a client can send a small test request with a known working account

CLIProxyAPI supports OpenAI, Gemini, Claude, Codex and Grok compatible interfaces. Its README also lists Grok Build OAuth, multi-account load balancing, streaming responses, tool calls and multimodal input. For this guide, the important part is simple: it can load xAI / Grok auth files and expose them through one API layer.

If the gateway is unstable, adding more auth files will only make debugging worse.

## What grok-build-auth does

Project page:
[https://github.com/dongguatanglinux/grok-build-auth](https://github.com/dongguatanglinux/grok-build-auth)

grok-build-auth reproduces the public x.ai / Grok web authentication chain. The path is roughly:

```text
signup
  → SSO
  → Grok Build / CLI scope OAuth PKCE
  → CLIProxyAPI auth JSON export
```

One detail matters: an SSO session is not enough for CLIProxyAPI. The flow must continue through Grok Build OAuth. After it gets `access_token` and `refresh_token`, it can export a `type=xai` JSON file that CLIProxyAPI can load.

Common environment variables include:

| Variable | Purpose |
|---|---|
| `YESCAPTCHA_API_KEY` | Turnstile solving |
| `TEMPMAIL_API_KEY` | needed for tempmail mode |
| `CLOUDFLARE_API_TOKEN` | needed for Cloudflare mail helper mode |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |
| `CLOUDFLARE_D1_DB_ID` | Cloudflare D1 database ID |
| `ALIAS_MAIL_DOMAINS` | controlled mail domains, comma separated |
| `CLIPROXYAPI_AUTH_DIR` | export directory for auth files |
| `HTTPS_PROXY` / `HTTP_PROXY` | proxy settings |

Do not publish `.env`, auth JSON files, mailbox tokens or proxy passwords. The auth file is a credential. If it leaks, someone may be able to use your account quota.

## Where YesCaptcha fits

x.ai signup may require Cloudflare Turnstile. grok-build-auth can use a captcha service compatible with the `createTask` protocol, and YesCaptcha is one option.

A safe first run looks like this:

1. Register a YesCaptcha account.
2. Add a small balance.
3. Copy the API key.
4. Put it in `.env` or an environment variable.
5. Test with one account only.

YesCaptcha signup link:
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

If Turnstile keeps failing, stop and inspect the setup. Check balance, API key, task type, proxy and site parameters. Repeating the same bad environment usually just burns points.

## First run workflow

Run one account first. Batch mode comes later.

### 1. Create the auth directory

Make sure CLIProxyAPI and grok-build-auth agree on the same auth directory. For the first test, use a separate directory instead of your production pool. Check permissions before running the flow.

### 2. Prepare grok-build-auth

Project page:
[https://github.com/dongguatanglinux/grok-build-auth](https://github.com/dongguatanglinux/grok-build-auth)

Follow the project README. The setup usually looks like this:

```bash
git clone https://github.com/dongguatanglinux/grok-build-auth.git
cd grok-build-auth
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then fill in YesCaptcha, mailbox, proxy and `CLIPROXYAPI_AUTH_DIR`. Do not paste real secrets into screenshots, blog comments or public issues.

### 3. Verify the mailbox first

The mailbox layer is easy to underestimate. tempmail is good for a quick test. A controlled domain is usually better if you plan to keep the pool for a while.

Record which mailbox produced which auth file. Later, when an account fails, that mapping will save time.

### 4. Complete signup and OAuth

A clean run should produce these results:

- x.ai verification email arrives
- Turnstile is solved
- SSO session is obtained
- Grok Build OAuth completes
- a `type=xai` auth JSON is written locally
- CLIProxyAPI loads the file

When something fails, isolate the failed step. Do not treat captcha failure, mailbox failure, OAuth failure and auth loading failure as the same problem.

### 5. Send a small client request

After import, send a tiny request through CLIProxyAPI. Confirm Base URL, API key, model name and upstream account state before putting the account into a normal group.

Do not stress test a fresh account with large context immediately. First check the small request and the gateway logs.

## Maintaining the pool

A useful pool is not the one with the most auth files. It is the one you can debug.

Track at least these fields:

| Field | Why it matters |
|---|---|
| Mailbox | recovery, verification and batch tracing |
| Signup time | helps identify policy or endpoint changes |
| Proxy exit | useful for success-rate review |
| YesCaptcha status | separates captcha failure from later failures |
| Auth filename | maps to the CLIProxyAPI account |
| Current state | active, expired, pending, paused |
| Last error | 401, 403, quota, refresh failure |

If a batch fails together, look for shared causes: domain, signup date, proxy exit, captcha success rate. Do not start by deleting files one by one.

## Common failure points

### Turnstile keeps failing

Check the YesCaptcha balance and API key first. Then check proxy and task parameters. If the same setup fails repeatedly, do not keep retrying.

### Verification email never arrives

Check the mailbox API, DNS, mail routing and token permissions. tempmail is convenient, but a controlled mail domain is easier to trace over time.

### SSO works but there is no auth file

That is expected if OAuth has not completed. SSO is not the final artifact. The flow still needs Grok Build OAuth PKCE and token exchange before it can export a CLIProxyAPI auth JSON.

### CLIProxyAPI cannot see the account

Check the directory first. Does `CLIPROXYAPI_AUTH_DIR` match CLIProxyAPI `auth-dir`? Are permissions correct? Did the gateway hot reload, or does it need a restart?

### Client gets 401 or 403

Separate client auth from upstream auth. The client API key may be wrong, or the Grok auth may be expired. Use the management panel, logs and a single-account test before judging the whole pool.

## Cost estimate

Do not estimate cost only from the Turnstile price. Real cost includes captcha attempts, mailbox setup, proxy, VPS time, retries and maintenance.

The useful number is cost per successful account. Run 5 to 10 authorized test accounts, record captcha attempts, mail retries and proxy changes, then calculate the average. That number is more useful than the advertised per-task price.

YesCaptcha signup link:
[https://yescaptcha.com/i/zWdD7S](https://yescaptcha.com/i/zWdD7S)

## FAQ

### Can a Grok token pool be free forever?

No. Even if an account has free quota, captcha, mailbox, proxy, VPS and maintenance time still cost something. Platform rules can also change.

### Is grok-build-auth an official xAI tool?

No. It is a protocol research client, not an official xAI SDK. Use the project README for setup and configuration details.

### Can I commit auth JSON files to Git?

Do not commit them to a public repository. Auth JSON files, `.env`, mailbox tokens and proxy passwords are credentials. If you use a private repository, restrict access carefully.

### Should I start with concurrent signup?

No. Start with one account. Then run a small batch and measure success rate. Concurrency only amplifies bad configuration.

## Final advice

Start with the smallest working chain: one mailbox, one YesCaptcha API key, one Grok account, one `type=xai` auth file and one small CLIProxyAPI request.

After that works, add accounts slowly. Do not put pool size ahead of maintainability. The hard part is not creating the first few auth files. The hard part is understanding, a week later, why each account is working or broken.

This article is based on public GitHub README material and YesCaptcha pricing notes checked on 2026-07-14. CLIProxyAPI, grok-build-auth, YesCaptcha and x.ai / Grok behavior may change. Check the live project documentation and service terms before running anything important.
