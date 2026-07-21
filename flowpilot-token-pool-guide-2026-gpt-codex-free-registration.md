# FlowPilot token pool guide 2026: GPT, Codex and free registration

If you use GPT, Codex, Claude Code or OpenAI-compatible clients every day, one account is often not enough for a serious workflow. A single upstream account can hit rate limits, lose OAuth status, return 401 errors, or stop working at the worst moment. Manually registering accounts, collecting email codes, handling phone verification and importing sessions into a gateway gets old fast.

This guide explains a cleaner way to manage that work: use FlowPilot to help with account onboarding, email verification, OAuth authorization and platform write-back, then manage the resulting accounts through a gateway such as Sub2API, CPA, SUB2API or Codex2API.

The goal here is not to bypass platform rules. The goal is to make legally owned accounts, subscriptions and API access easier to track, rotate and troubleshoot.

When a registration flow asks for SMS verification, you can use HeroSMS:
[HeroSMS registration link](https://hero-sms.com/?ref=509318)

## What FlowPilot does

FlowPilot is a Chrome side panel extension maintained by QLHazyCoder:
[https://github.com/QLHazyCoder/FlowPilot](https://github.com/QLHazyCoder/FlowPilot)

According to the project README, FlowPilot is built for ChatGPT / OpenAI account registration, verification codes, OAuth, Plus payment paths, account importing, retry handling and local run records. It is not just a one-click userscript. It is closer to an account onboarding cockpit.

The project currently covers these areas:

- ChatGPT / OpenAI registration and OAuth flows
- CPA, SUB2API and Codex2API source modes
- a separate Kiro flow
- email verification, login verification and email binding codes
- Hotmail, 2925, QQ Mail, 163 Mail, iCloud, Cloud Mail and other mailbox options
- Cloudflare Temp Email, custom mailbox pools and custom mailbox service pools
- SMS verification providers
- IP proxy management, retry control, execution ranges and account run history

In simple terms, FlowPilot helps you prepare an account, complete the authorization path and write the result back to your account management platform.

## Who should use this setup

This setup is useful if you are:

- building a private GPT or Codex API gateway
- managing multiple OpenAI or ChatGPT upstream accounts
- testing Codex CLI or Claude Code against your own relay
- trying to reduce manual OAuth callback and account import work
- tracking account status, failures and verification history

It is not the best fit if you:

- only use one personal ChatGPT account
- do not want to maintain a VPS, proxy, mailbox and gateway
- expect a tool to bypass platform terms
- cannot handle account risk, failed verification or payment issues

If your usage is light, the official account path is simpler. FlowPilot makes more sense when you already have an operational reason to manage multiple legitimate accounts.

## Compliance comes first

An account pool can be used in a reasonable way or in a risky way.

A reasonable use case is managing your own accounts, team accounts, test accounts or paid subscriptions through a consistent gateway. You know what each account is for, how it was registered, which mailbox belongs to it and which client uses it.

A risky use case is mass free registration, resale of unclear account sources, spam, or attempts to evade platform restrictions. OpenAI, ChatGPT, Codex, Kiro, PayPal, Google and similar platforms all have their own terms of service.

This article does not provide instructions for bypassing risk controls or abusing free registration. It focuses on infrastructure, preparation, troubleshooting and clean account governance.

## Recommended architecture

A practical token pool stack looks like this:

```text
Legitimate upstream GPT / Codex accounts
        ↓
FlowPilot handles registration, verification, OAuth and write-back
        ↓
Sub2API / CPA / SUB2API / Codex2API manages accounts and API keys
        ↓
Your clients: Codex CLI, Claude Code, OpenAI-compatible apps
```

Each layer has a job.

FlowPilot handles browser-side onboarding. The gateway handles groups, API keys, quotas, logs and account status. The mailbox layer receives email codes. HeroSMS covers phone verification when the platform asks for a mobile number.

This separation makes debugging much easier. If email codes fail, check the mailbox layer. If SMS fails, check the SMS provider, country and stock. If OAuth fails, check the callback and gateway URL. If requests return 401, check the imported account state.

## Preparation checklist

Before running your first account, prepare the basics.

| Item | Recommendation |
|---|---|
| Browser | Chrome or Chromium with developer mode enabled |
| FlowPilot | Latest version from GitHub or the official FlowPilot tutorial site |
| Gateway | Sub2API, CPA, SUB2API or Codex2API, depending on your target |
| Email | Cloudflare Temp Email, custom mailbox pool, Hotmail, iCloud or similar |
| SMS | HeroSMS for projects that require phone verification |
| Proxy | Stable and clean IP, not a constantly changing exit node |
| Records | Keep email, phone source, platform, group, status and failure reason |

HeroSMS link:
[https://hero-sms.com/?ref=509318](https://hero-sms.com/?ref=509318)

For the first run, do not start with a large batch. Use one mailbox, one phone number if needed, one IP and one account. Prove the path first.

## Installing FlowPilot

The official README gives a simple setup path:

1. Open `chrome://extensions/`.
2. Enable developer mode.
3. Click "Load unpacked".
4. Select the FlowPilot project directory.
5. Open the extension side panel.
6. Choose your flow and source.
7. Fill in mailbox, verification, Plus payment or platform parameters.
8. Run the first few steps manually before using Auto.

Do not rush this part. Many failures come from basic configuration mistakes: wrong Temp API, wrong Admin Auth, wrong gateway admin URL, proxy not actually applied, or no balance in the SMS account.

## Choosing a source: SUB2API, CPA, Codex2API or Kiro

FlowPilot supports several source modes.

### SUB2API

SUB2API is a good fit when your goal is to import accounts into a Sub2API gateway. You prepare the admin URL, admin credentials, target group and optional proxy. After OAuth, the account can be written back to the gateway and used through your own API keys.

For Codex CLI, Claude Code and OpenAI-compatible clients, this is usually the cleanest path.

### CPA

CPA is for traditional OAuth-based panel workflows. It can also import the current ChatGPT session into CPA in Plus mode.

### Codex2API

Codex2API keeps the OAuth path and does not currently support direct Plus session import. It is relevant if your stack is specifically built around Codex-style access.

### Kiro

Kiro has its own flow. The README describes Builder ID registration, desktop authorization and `kiro.rs` upload steps. It should be treated separately from OpenAI Plus or general GPT account flows.

Pick the source based on where the account needs to end up. The destination platform matters more than the label.

## Email verification options

FlowPilot supports webmail polling, API mailbox polling and local helper reading. The official materials mention Hotmail, 2925, QQ Mail, 163 Mail, 126 Mail, iCloud, Cloud Mail, YYDS Mail, Cloudflare Temp Email and custom mailbox pools.

For automation, Cloudflare Temp Email is often easier than juggling ordinary inboxes. It can generate mailboxes and let FlowPilot poll messages through an API.

Whatever you choose, the mailbox layer needs to satisfy three conditions:

- it receives GPT / OpenAI / Codex-related emails reliably
- FlowPilot can poll or read the code
- each account can be traced back to its mailbox

Do not mix mailbox sources casually. Account recovery and failure analysis become painful when the mailbox source is unclear.

## SMS verification with HeroSMS

Some AI-related registration paths may ask for a phone number. For those cases, HeroSMS can be used as the SMS activation provider.

HeroSMS registration link:
[https://hero-sms.com/?ref=509318](https://hero-sms.com/?ref=509318)

A sensible test flow is:

1. Register a HeroSMS account and add balance.
2. Search for OpenAI, ChatGPT or the target service.
3. Choose a country with enough stock and a reasonable price.
4. Run one manual SMS order first.
5. Only consider API automation after the manual test works.

SMS activation is not a guarantee. Success still depends on the target platform, number quality, IP reputation, browser state and registration behavior. If one run fails, do not blindly retry the same environment ten times.

For more details on HeroSMS, see the OBVPS review:
[HeroSMS SMS activation platform review](https://obvps.com/posts/herosms-sms-activation-platform-review/)

## Proxy and IP environment

FlowPilot includes an IP Proxy module. The project documentation describes it as a way to configure proxy takeover inside the extension and show current proxy, current exit IP and diagnostic status.

The practical advice is simple: stable is better than noisy.

Registration, OAuth, Plus payment and login verification flows do not like sudden environment changes. A clean, stable IP is usually better than a fast-changing proxy pool.

Before running Auto, check these points:

- the browser page actually uses the configured proxy
- the exit region is consistent with your account and phone verification choice
- the proxy does not disconnect halfway through OAuth or verification
- FlowPilot's proxy status card does not show takeover failure

If the proxy is not really applied, stop and fix it. Continuing the run only creates more bad records.

## First-run workflow

Use a small, controlled run before thinking about a pool.

### Step 1: Verify the gateway

Log in to Sub2API, CPA or Codex2API first. Confirm that the admin panel opens, groups exist and a test API key can be created.

### Step 2: Verify mailbox code retrieval

Configure Cloudflare Temp Email or your mailbox pool. Run only up to the email code step and make sure FlowPilot can read the code.

### Step 3: Verify SMS if required

If the platform asks for phone verification, test HeroSMS manually first. Confirm the selected service and country can receive the code.

### Step 4: Complete OAuth and write-back

After authorization, check the gateway. The account should appear in the correct group with a healthy OAuth state.

### Step 5: Test from a real client

Send a small request from Codex CLI, Claude Code or another OpenAI-compatible client. Only expand the pool after this works.

## Maintaining account pool health

A healthy token pool is not just a large list of accounts. You need a usable record for each account.

Track at least these fields:

| Field | Why it matters |
|---|---|
| Email | Recovery and verification history |
| Phone source | SMS success rate analysis |
| Registration date | Batch-level troubleshooting |
| Source | SUB2API, CPA, Codex2API or Kiro |
| Group | Separate GPT, Codex and testing accounts |
| Status | Healthy, pending verification, failed, paused |
| Failure reason | Email, SMS, OAuth, proxy, payment or write-back |

FlowPilot's run history and local helper snapshots reduce manual work, but you still need periodic review. Watch for 401, 403, expired login, expired subscription and repeated verification failures.

## FAQ

### Can FlowPilot create free GPT or Codex accounts

FlowPilot can assist the registration and authorization flow. Whether free registration is available depends on the target platform's current policy. Treat "free registration" as account creation, not a promise of free long-term usage.

### Does HeroSMS guarantee OpenAI verification success

No. HeroSMS provides phone numbers and SMS retrieval. Final success depends on the platform, number country, stock, IP quality and registration behavior.

### Should I configure proxy first or mailbox first

Start with the gateway and mailbox. Proxy helps stability, but it does not fix a broken Temp API, wrong admin URL or missing SMS balance.

### Should I use Auto immediately

No. Run the first account manually. Auto is for repeating a known-good workflow, not discovering what is broken.

### Can GPT and Codex accounts share one pool

You can store them in one platform, but use separate groups. GPT, Codex, Kiro and API relay use cases fail for different reasons, and separate groups make troubleshooting easier.

## Final notes

In 2026, token freedom is mostly an operations problem. You need clean account records, stable mailbox handling, a working SMS layer, a predictable proxy setup and a gateway that tells you which account failed and why.

FlowPilot is useful because it reduces browser-side repetitive work. Sub2API, CPA, SUB2API or Codex2API handle the gateway layer. Cloudflare Temp Email handles email codes. HeroSMS handles phone verification when a registration project requires it.

Start with one account and one complete path. Once that works, scale carefully.

This article is based on public FlowPilot README, official tutorial index and GitHub project materials available in 2026. Platform rules, prices, phone number stock and FlowPilot features can change, so always check the official pages and terms before using the setup.
