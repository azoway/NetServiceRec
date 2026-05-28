# Self-Hosted API Relay Guide: Sub2API + FlowPilot + Cloudflare Temp Email + HeroSMS

> This guide walks through a practical way to build a self-hosted AI API relay on a VPS. The stack here uses [Sub2API](https://github.com/Wei-Shaw/sub2api) as the gateway and billing panel, [FlowPilot](https://github.com/QLHazyCoder/FlowPilot) for account automation and callback submission, [Cloudflare Temp Email](https://flowpilot.qlhazycoder.top/tutorial/cloudflare-temp-email-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E) for mailbox generation and code retrieval, and [HeroSMS](https://hero-sms.com/?ref=509318) for phone verification when OpenAI asks for SMS.

---

## What this stack is for

The point of a self-hosted API relay is simple: you connect multiple upstream AI accounts to one gateway, then issue your own API keys to downstream users or tools.

That gives you one place to handle:

- authentication
- account rotation
- sticky sessions
- usage metering
- user balances
- request forwarding

The full path looks like this:

```text
Upstream AI accounts -> Sub2API gateway -> your API keys -> Codex CLI / Claude Code / other clients
                         ^
                         |
              FlowPilot registers and imports accounts
                         ^
                         |
      Cloudflare Temp Email handles email codes + HeroSMS handles SMS codes
```

If you want one short summary, it is this:

- `Sub2API` runs the relay and user-facing panel
- `FlowPilot` handles account registration and panel write-back
- `Cloudflare Temp Email` reduces email friction during automation
- `HeroSMS` covers SMS verification when the upstream flow asks for a phone number

---

## Who this guide is for

This setup makes the most sense if you are:

- building a private relay for your own workflow
- running an internal team gateway
- testing a quota-distribution model around API keys
- trying to reduce manual account import work

It is probably not the right fit if you:

- only need one personal upstream account
- do not want to maintain Docker, reverse proxy, and account health
- are not comfortable handling compliance and account risk yourself

> Compliance note: Sub2API's own README explicitly warns that some use cases may violate upstream terms of service. Read the platform rules you depend on and make your own risk assessment before deploying anything in production.

---

## What you need before you start

| Item | Recommendation |
|------|----------------|
| VPS | Linux VPS on `amd64` or `arm64`, preferably with at least `2 vCPU / 4 GB RAM` |
| Network | A clean outbound IP helps with login and registration stability |
| Domain | Strongly recommended for HTTPS in front of the Sub2API panel |
| Gateway | [Sub2API](https://github.com/Wei-Shaw/sub2api) |
| Browser automation | Chrome plus [FlowPilot](https://github.com/QLHazyCoder/FlowPilot) |
| Email layer | [Cloudflare Temp Email](https://flowpilot.qlhazycoder.top/tutorial/cloudflare-temp-email-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E) |
| SMS layer | [HeroSMS](https://hero-sms.com/?ref=509318) with promo code `obvps` |
| Optional proxy | Useful if you need cleaner egress or per-account isolation |

Two practical recommendations before anything else:

1. Deploy the relay first and confirm the panel works.
2. Only then wire in email and SMS automation.

That order makes debugging much easier.

---

## Why this stack works well together

The real advantage is not just that each tool exists, but that they solve different bottlenecks cleanly.

### Sub2API handles the gateway layer

According to the official Sub2API documentation, it supports:

- multi-account management
- API key issuance
- token-level billing
- sticky session scheduling
- concurrency and rate limits
- built-in payment support

For a relay project, that means you do not need to bolt billing and request dispatch together yourself.

### FlowPilot removes a lot of the manual import work

The useful part is the `SUB2API` source mode. Instead of hand-creating every upstream account entry, FlowPilot can run through registration and authorization steps, then submit the `localhost` callback data back into Sub2API.

That is the piece that turns this from a pure panel install into a repeatable account onboarding workflow.

### Cloudflare Temp Email is better than ad-hoc inbox juggling

For one-off testing, normal mail forwarding can work. For repeated registration attempts, temporary mailbox generation plus API polling is usually far less annoying than keeping webmail tabs open and refreshing them manually.

### HeroSMS fills the phone verification gap

Some OpenAI-related registration paths still ask for phone verification. When that happens, an SMS provider with both web ordering and API support is much easier to integrate into a repeatable flow.

[HeroSMS](https://hero-sms.com/?ref=509318) fits that role well here because it supports OpenAI-related services, automation workflows, and a checkout promo code: `obvps`.

If you want a broader platform overview before buying credits, see the site article [HeroSMS Review 2026](https://obvps.com/posts/herosms-sms-activation-platform-review/).

---

## Step 1: Deploy Sub2API

[Sub2API](https://github.com/Wei-Shaw/sub2api) is the foundation of this setup, so get it stable before touching anything else.

### Recommended method: Docker Compose

The official repository provides a deployment preparation script. A quick install looks like this:

```bash
mkdir -p sub2api-deploy
cd sub2api-deploy

curl -sSL https://raw.githubusercontent.com/Wei-Shaw/sub2api/main/deploy/docker-deploy.sh | bash

docker compose up -d
docker compose logs -f sub2api
```

Based on the upstream README, the script will:

- download the compose file and environment template
- generate secrets such as `JWT_SECRET` and `POSTGRES_PASSWORD`
- create a local-directory-based deployment layout
- make backup and migration easier than a named-volume-only setup

Default panel access is:

```text
http://YOUR_SERVER_IP:8080
```

If the admin password was generated automatically, you can look it up in logs:

```bash
docker compose logs sub2api | grep "admin password"
```

### First things to configure in the panel

Once the panel opens correctly, do these first:

1. Create account groups such as `codex` or `claude`.
2. Add outbound proxies if you plan to route registration or traffic through them.
3. Generate a test user API key.
4. Confirm the dashboard, logs, and account pages all load normally.

### Reverse proxy note that matters

If you put Nginx in front of Sub2API and care about sticky sessions for clients like Codex CLI, add this in the Nginx `http` block:

```nginx
underscores_in_headers on;
```

Without it, headers that include underscores can be dropped, which can break sticky-session behavior.

### Simple mode for private use

Sub2API also documents a simpler run mode for personal or internal usage:

```bash
RUN_MODE=simple
```

For production, the upstream docs also require:

```bash
SIMPLE_MODE_CONFIRM=true
```

Use this if you do not need the full SaaS-style billing flow.

---

## Step 2: Put HTTPS in front of the panel

This is not optional if you expect to access the relay from real clients.

At minimum:

- point a domain to your VPS
- terminate TLS with Nginx or Caddy
- reverse proxy to `127.0.0.1:8080`

You do not need a complicated setup on day one, but you do want:

- valid HTTPS
- a stable panel URL
- predictable callback behavior

If you skip this and keep testing on raw IP and HTTP for too long, later debugging gets messy fast.

---

## Step 3: Configure Cloudflare Temp Email

Cloudflare Temp Email is the easiest email layer here if you want repeatable automation instead of mailbox babysitting.

### Why it is useful

Compared with manual forwarding or ordinary mailbox aliases, this approach is better for repeated runs because:

- each run can generate a fresh mailbox
- verification mail can be fetched through API polling
- you do not need to keep logging into a normal email UI

### What you need

Prepare these pieces first:

- a working Cloudflare Temp Email backend URL
- the backend `admin auth`
- optionally a site access password if your deployment has one
- the base domain used for mailbox creation
- a configured wildcard mail path if you want random subdomains

### Fields to fill inside FlowPilot

Based on the FlowPilot tutorial page, the key fields are:

| Field | What it does |
|------|---------------|
| `Temp API` | Worker/backend endpoint used for mailbox creation and mail polling |
| `Admin Auth` | Required when Cloudflare Temp Email is used as the mailbox generator |
| `Custom Auth` | Only needed if the site itself is protected by an extra access password |
| `Temp Domain` | The base domain allowed to create mailboxes |
| `Random Subdomain` | Requires backend `RANDOM_SUBDOMAIN_DOMAINS` plus Cloudflare `MX *` setup |
| `Mail Receive` | Real receiving mailbox, only relevant for forwarding-style usage |

### Recommended setup

For the cleanest automation path, use:

```text
Mailbox Generator = Cloudflare Temp Email
Mailbox Service   = Cloudflare Temp Email
```

When both sides use it, make sure both configuration paths are complete instead of filling only one half.

### Where people usually get stuck

If mailbox generation fails even though the API URL looks right, check these first:

- `Admin Auth` is correct
- the base domain is correct
- `RANDOM_SUBDOMAIN_DOMAINS` is set server-side if you enabled random subdomains
- Cloudflare DNS has the required wildcard MX setup

---

## Step 4: Prepare HeroSMS for phone verification

If your OpenAI-related flow triggers phone verification, this becomes the part that either keeps the workflow moving or blocks it completely.

### Why HeroSMS is a practical choice here

[HeroSMS](https://hero-sms.com/?ref=509318) gives you:

- a web UI for manual test runs
- an API for automation
- support for OpenAI-related services
- country selection instead of one fixed pool

There is also a site promo code:

```text
obvps
```

### Country choice tip

In practice, many users prefer to compare countries instead of assuming one market always wins. The original Chinese workflow behind this guide recommends checking Brazil first for OpenAI-related verification because it often balances price and availability well, but inventory and pass rate can change.

That means the better rule is:

- compare stock
- compare current price
- test one small batch first
- keep a backup country ready

Do not assume any one country is permanently best.

### Manual test flow

Before attempting automation, run one manual verification:

1. Create an account at [HeroSMS](https://hero-sms.com/?ref=509318).
2. Add balance and apply promo code `obvps` if available at checkout.
3. Search for the relevant service such as `OpenAI` or `ChatGPT`.
4. Pick the country with acceptable price and stock.
5. Use the rented number in the registration flow and wait for the SMS code.

### API usage

After a successful manual test, move to API mode for automation.

The standard pattern is:

```text
request number -> wait for SMS -> submit code -> release number
```

That is the mode you want before turning on FlowPilot `Auto`.

For a deeper breakdown of the platform itself, see [HeroSMS Review 2026](https://obvps.com/posts/herosms-sms-activation-platform-review/).

---

## Step 5: Install FlowPilot and connect it to Sub2API

[FlowPilot](https://github.com/QLHazyCoder/FlowPilot) is the automation glue in this stack.

### Install the extension

The normal install flow is:

1. Open `chrome://extensions/`
2. Enable Developer Mode
3. Load the unpacked FlowPilot folder
4. Open the extension sidebar

The FlowPilot tutorial also recommends reloading the extension after updates, even if you updated the local files already.

### Use `SUB2API` as the source

This is the key mode for this guide.

Inside the sidebar, choose:

```text
Source = SUB2API
```

Then fill the panel-related fields:

| Field | Example |
|------|---------|
| `SUB2API` | `https://your-domain/admin/accounts` |
| `Account / Password` | Your Sub2API admin login |
| `Group` | Usually `codex`, or your own target group |
| `Default Proxy` | Optional proxy name or ID |

### What the FlowPilot steps are doing

The practical interpretation is:

- `Step 1`: request an OAuth authorization link from Sub2API
- `Step 2` to `Step 9`: handle registration, email code retrieval, login, and authorization
- `Step 10`: submit the `localhost` callback data back to Sub2API so the upstream account record is created directly in the panel

That last step is why the stack feels integrated instead of stitched together manually.

### Recommended combination

For this stack, the most natural template is:

```text
Source             = SUB2API
Mailbox Generator  = Cloudflare Temp Email
Mailbox Service    = Cloudflare Temp Email
SMS Provider       = HeroSMS
```

### How to test before full automation

Do not jump straight into bulk mode. Use this order:

1. Run `Step 1` to `Step 4` manually and confirm email codes arrive.
2. If phone verification appears, confirm HeroSMS works for your chosen service and country.
3. Finish one complete account import.
4. Check the account record inside Sub2API.
5. Only then enable `Auto`.

This is slower at first, but it saves a lot of blind retries.

---

## Step 6: End-to-end workflow from zero to usable API key

If you want the shortest reproducible sequence, use this one.

### Phase A: Base infrastructure

1. Deploy Sub2API on your VPS.
2. Put HTTPS in front of it.
3. Confirm the admin panel works.
4. Create at least one account group such as `codex`.

### Phase B: Email and SMS layers

1. Configure Cloudflare Temp Email.
2. Test mailbox creation.
3. Test code retrieval.
4. Register and fund [HeroSMS](https://hero-sms.com/?ref=509318).
5. Complete one SMS verification manually.

### Phase C: One-account dry run

1. Set FlowPilot source to `SUB2API`.
2. Fill panel credentials and target group.
3. Fill the Cloudflare Temp Email fields.
4. Fill the HeroSMS side if your current flow needs it.
5. Run a single account from start to finish.
6. Confirm that the account appears in Sub2API with the expected status.

### Phase D: Start issuing keys

After the account import path works:

1. create or register a user in Sub2API
2. issue an API key
3. set balance, concurrency, or rate multiplier as needed
4. test an actual downstream client

For example, an Anthropic-compatible client can be pointed at your relay like this:

```bash
export ANTHROPIC_BASE_URL="https://your-domain"
export ANTHROPIC_AUTH_TOKEN="sk-your-generated-key"
```

For Codex-compatible or other OpenAI-style clients, follow the Sub2API endpoint and key format documented in the panel or upstream repository.

---

## Step 7: Day-to-day operations

Once the stack is live, the work shifts from setup to stability.

### Things worth checking regularly

- request logs
- token usage
- account health
- failed callback imports
- proxy reliability
- SMS and email success rate

### Upgrades

The normal Docker upgrade path is straightforward:

```bash
docker compose pull
docker compose up -d
```

Check the official repository changelog before major upgrades if you rely on custom behavior.

### Backups

If you deployed using the local-directory compose layout, back up the entire deployment directory, especially:

- `postgres_data`
- `redis_data`
- your compose and env files

That is much better than discovering after a failure that you only saved the container definition and not the data.

---

## Common problems and how to debug them

### The Sub2API panel does not open

Check:

- firewall rules for `8080` or your reverse-proxy port
- whether the container is healthy
- whether PostgreSQL or Redis failed to initialize

Useful command:

```bash
docker compose logs sub2api
```

### Email codes never arrive in FlowPilot

Usually this is one of:

- wrong `Temp API`
- wrong `Admin Auth`
- wrong base domain
- random subdomain enabled without proper backend or DNS support

Start by testing mailbox generation and mail retrieval separately instead of rerunning the whole registration flow.

### SMS never arrives

When that happens, do not immediately blame only the SMS provider. Check:

- selected service ID
- selected country
- current stock
- whether the order timed out
- whether the upstream site rejected the number before sending

A second country is often a faster fix than repeating the same failed order.

### Callback submission fails at the end

Check:

- the Sub2API URL entered in FlowPilot
- whether the admin session is still valid
- whether the callback data format is the expected `localhost` authorization callback

### Sticky sessions do not behave correctly

Recheck your reverse proxy and make sure:

```nginx
underscores_in_headers on;
```

is really in the active Nginx configuration.

---

## Buying and usage advice

If your goal is stable operation instead of constant tinkering, these three habits help the most:

1. Test every layer separately before combining them.
2. Keep one working baseline configuration before experimenting.
3. Scale the automation slowly instead of going straight to large batches.

For spending decisions:

- buy a small amount of SMS credit first
- verify one complete account path
- only then scale up

That approach is much cheaper than buying large credit balances before your registration flow is actually stable.

---

## FAQ

### Is this better than using a ready-made relay service?

It depends. Self-hosting gives you more control over accounts, billing, routing, and client integration. A ready-made service is easier if you do not want to handle maintenance, account health, or proxy issues yourself.

### Do I need FlowPilot if I already have upstream accounts?

Not necessarily. If your accounts are already ready to import, Sub2API may be enough. FlowPilot matters more when you want repeatable account onboarding and callback submission.

### Is Cloudflare Temp Email mandatory?

No. It is just the most convenient option in this workflow for repeated email verification tasks. If you already have a mailbox system that works reliably for automation, you can use that instead.

### Is HeroSMS required for every account?

No. It is only needed when the upstream registration path triggers phone verification. Some runs may not need it, but you should be prepared for it.

### Which part usually breaks first?

Most real-world failures show up in one of three places: mailbox configuration, SMS availability, or IP/proxy quality. The relay panel itself is often the easier part once deployed correctly.

---

## Final takeaway

If you want a workable self-hosted API relay stack, this combination is one of the more practical ones right now:

- `Sub2API` for the gateway and user panel
- `FlowPilot` for account automation and callback submission
- `Cloudflare Temp Email` for mailbox generation and verification polling
- `HeroSMS` for phone verification when needed

The best rollout order is:

```text
deploy the panel -> secure it with HTTPS -> test email -> test SMS -> run one full account -> enable automation
```

That order keeps troubleshooting manageable and gives you a clean path from first deployment to issuing your own API keys.

---

## Timing and disclaimer

- This article was organized on `2026-05-27`.
- Package availability, UI fields, prices, stock, verification rules, and promo availability may change at any time.
- Always verify current details on the official project pages before purchase or production deployment.
- This guide is for technical workflow reference only. You are responsible for using it in compliance with applicable platform rules and local laws.
