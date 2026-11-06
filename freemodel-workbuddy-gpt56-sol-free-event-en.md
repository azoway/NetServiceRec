# FreeModel limited offer: use gpt-5.6-sol free in WorkBuddy

If you already use WorkBuddy and want a low-friction way to try `gpt-5.6-sol`, FreeModel's current limited offer is worth a look. The point of this promo is practical setup, not another browser chat page. You connect FreeModel's `work` endpoint as a custom model in WorkBuddy, then run real chat and coding tasks on `gpt-5.6-sol`.

Based on the provided campaign details, new users need to complete a first top-up of `15 CNY` after registration before they can use this path. The endpoint, model name, and API key flow are all clear, and setup takes about three minutes. Whether the free offer is still live, and what the exact free quota covers, should always be checked on FreeModel's live pages.

Signup link: [FreeModel registration](https://agentrouter.org/register?aff=Vnpm)

Another free AI API gateway worth checking is AgentRouter, which also supports Claude Code, Cline, Cursor, and similar tools. It currently offers a $150 referral boost and high-frequency quota refill campaign: [AgentRouter signup](https://agentrouter.org/register?aff=Vnpm)

Setup docs: [FreeModel WorkBuddy docs](https://freemodel.dev/dashboard/docs#workbuddy)

## Bottom line first

This offer is a good fit if you can install a desktop AI client and fill in a base URL, API key, and model name. After you register on FreeModel and complete the first `15 CNY` top-up, create an API key and add these three fields in WorkBuddy:

| Field | Value |
|---|---|
| Endpoint | `https://work.freemodel.dev/v1/chat/completions` |
| API Key | Create it on FreeModel's API key page |
| Model name | `gpt-5.6-sol` |

If you only want a no-config browser chatbot, this path is not ideal. If you already live in WorkBuddy, Claude Code, Codex, or similar tools, the value is clearer: pay a small first top-up, then check whether `gpt-5.6-sol` is stable and useful in your own workflow.

For FreeModel's broader Claude Code, OpenAI-compatible, and plan notes, see the existing English guide: [FreeModel API relay review](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code-en/). This article stays focused on WorkBuddy and the current `gpt-5.6-sol` offer.

## Offer summary

| Item | Details |
|---|---|
| Offer | Configure WorkBuddy to use `gpt-5.6-sol` for free |
| Platform | FreeModel |
| Client | WorkBuddy on macOS / Windows |
| Endpoint | `https://work.freemodel.dev/v1/chat/completions` |
| Model name | `gpt-5.6-sol` |
| Entry requirement | First top-up of `15 CNY` after registration |
| Setup time | About 3 minutes |
| Official docs | WorkBuddy section in FreeModel Dashboard Docs |

Two caveats matter immediately. First, free usage is a limited-time campaign, not a permanent promise. Second, the first `15 CNY` top-up is the current entry requirement, not a full long-term price card for the model. Campaign rules, balance, model availability, and rate limits can change, so verify them before you pay or switch daily work over.

## What FreeModel and WorkBuddy each do

FreeModel is an API relay entry point. Its value is in endpoints, keys, model lists, balance, and client compatibility. It is not mainly a casual web chat product. Earlier OBVPS coverage already noted that FreeModel can cover Claude-style and OpenAI-compatible workflows for tools such as Claude Code, Cline, Cursor, ChatBox, and OpenAI SDK projects.

WorkBuddy is a desktop AI client. In this campaign, FreeModel exposes a `work` endpoint and the `gpt-5.6-sol` model name, while WorkBuddy sends requests through its custom model settings. Day to day, you still chat inside WorkBuddy. The backend becomes FreeModel.

Public coverage of GPT-5.6 often positions Sol as a stronger coding and knowledge-work option in the family. That context is useful for choosing tasks, but FreeModel's live model behavior, latency, context window, and billing still need to be checked in the FreeModel console and real responses. Do not treat third-party reviews as guarantees for this relay endpoint.

## Who it fits and who it does not

Better fit for:

- People already using WorkBuddy who want a custom model
- Users who want a low-cost first test of `gpt-5.6-sol`
- Anyone comfortable creating an API key and filling endpoint fields
- Coding assistance, document work, multi-turn chat, and tool-chain tasks
- Users willing to top up a small amount first and expand only after validation

Poor fit for:

- Users who only want browser chat and refuse desktop setup
- Users who do not want to complete the first top-up requirement
- Anyone unwilling to check model names, endpoint paths, and key permissions
- Production teams that need enterprise contracts and hard SLAs
- Anyone treating "limited free usage" as a permanent free service

## WorkBuddy setup steps

### 1. Register and complete the first top-up

Start with the [FreeModel registration link](https://agentrouter.org/register?aff=Vnpm). Based on the current campaign notes, complete the first `15 CNY` top-up after signup before using this free WorkBuddy path.

After registration, check three things:

1. Whether balance has been credited
2. Whether you can create a key on the API key page
3. Whether the WorkBuddy docs section is still present

If the console does not show `gpt-5.6-sol`, the `work` endpoint, or the campaign entry, trust the live page over older screenshots.

### 2. Install WorkBuddy

WorkBuddy supports macOS and Windows. Install it from the official guide for your OS, then make sure the app launches cleanly.

You do not need FreeModel connected for this step. Get the client working first, then add the custom model. That order makes debugging much easier.

### 3. Create a FreeModel API key

Open FreeModel's API key page and create a new key. Keep it private. Do not paste it into public chats, screenshots, or repositories.

A separate key for WorkBuddy is a good idea. If you later connect Claude Code, Codex, or other clients, separate keys make permission and usage checks simpler.

### 4. Add a custom model in WorkBuddy

Launch WorkBuddy, open the model switcher at the bottom of the chat UI, and choose `+` to configure a custom model. Fill in:

```text
Endpoint: https://work.freemodel.dev/v1/chat/completions
API Key: the key you created in FreeModel
Model name: gpt-5.6-sol
```

Note the host carefully: `work.freemodel.dev`, not the general `api.freemodel.dev`. This campaign specifically documents the WorkBuddy `work` endpoint and the `/v1/chat/completions` path.

Use the model name exactly as `gpt-5.6-sol`. Extra characters, missing characters, or case changes can produce "model not found" or failed requests.

### 5. Switch models and run a first test

Save the custom model, switch WorkBuddy to `gpt-5.6-sol`, then run a small checklist:

1. A normal short chat to confirm connectivity
2. A code explanation or small rewrite to check coding quality
3. A multi-turn follow-up to check context handling
4. A look at FreeModel usage or balance after the requests

If you get 401 errors, check the API key first. If the model is unavailable, re-check the model name and whether the campaign is still active. For timeouts or connection failures, inspect the network path, endpoint spelling, and FreeModel service status.

## Common setup mistakes

| Issue | Likely cause | What to check |
|---|---|---|
| Cannot connect | Wrong endpoint | Confirm `https://work.freemodel.dev/v1/chat/completions` |
| 401 / auth failure | Bad, incomplete, or missing API key | Recreate the key and paste it fully |
| Model unavailable | Wrong model name or ended campaign | Use `gpt-5.6-sol` and check the live model list |
| Registered but blocked | First `15 CNY` top-up not completed | Complete the campaign's entry top-up |
| No response in client | Custom model not saved, or still on the old model | Switch explicitly to the new custom model |
| Confusing billing | Treating limited free usage as forever free | Trust console balance, usage, and campaign rules |

One mix-up is especially common. FreeModel's general API host in older guides is often `https://api.freemodel.dev` for Claude Code, Cursor, ChatBox, and similar clients. This WorkBuddy offer uses `https://work.freemodel.dev/v1/chat/completions`. Do not blend the two.

## How to test it properly

A single "hello" message is a weak test. More useful checks include:

1. Ask the model to explain code you are actively editing
2. Ask for a small function or a clearly scoped bug fix in your style
3. Give it a short requirements note and ask for an implementation plan
4. Follow up across several turns to see whether context holds
5. Intentionally send a wrong model name or key once to confirm error messages are readable

If those checks look good, move more daily chat or coding work over. Limited free access is still a trial path. Validate stability, latency, and billing visibility before replacing your main workflow.

## How this fits FreeModel's broader setup

If you only want `gpt-5.6-sol` inside WorkBuddy, the steps above are enough.

If you also want FreeModel on Claude Code, Codex, Cursor, ChatBox, or your own SDK project, use these existing guides:

- [FreeModel Chinese guide](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code/)
- [FreeModel English guide](https://obvps.com/posts/freemodel-api-relay-gpt55-claude-code-en/)

General FreeModel setup usually revolves around base URL, API key, model name, and whether the client wants `/v1/chat/completions` or `/v1/responses`. This WorkBuddy campaign is narrower: fixed `work` endpoint plus `gpt-5.6-sol`.

## Signup path

The cleanest order is:

1. Open the [FreeModel registration link](https://agentrouter.org/register?aff=Vnpm)
2. Complete registration and the first `15 CNY` top-up
3. Create an API key
4. Install WorkBuddy and add the custom model
5. Validate `gpt-5.6-sol` with small real tasks

Official setup notes: [FreeModel WorkBuddy docs](https://freemodel.dev/dashboard/docs#workbuddy)

## FAQ

### Is this campaign completely free?

Based on the provided details, the offer is free usage of `gpt-5.6-sol` in WorkBuddy after you complete a first top-up of `15 CNY`. Free scope, duration, and later billing should be checked on FreeModel's live pages.

### Which endpoint should I use?

For this WorkBuddy offer, use `https://work.freemodel.dev/v1/chat/completions`. Do not mix it with the general `api.freemodel.dev` host.

### What exact model name should I enter?

Enter `gpt-5.6-sol`. Before saving, double-check FreeModel's console or docs in case the published name changes.

### Can I use this without WorkBuddy?

This article is specifically about the WorkBuddy path. FreeModel may support other clients, but the endpoint and steps here are for WorkBuddy custom models.

### Is the first 15 CNY top-up refundable?

The provided campaign notes do not include refund terms. Check FreeModel's top-up page, terms, and support before paying.

### Is this ready to become a daily main model?

Treat it as a validation path first. Long-term use depends on post-campaign pricing, rate limits, stability, and whether billing remains easy to audit.

## Final take

FreeModel's current offer is specific and useful: WorkBuddy + `gpt-5.6-sol` + the `work.freemodel.dev` endpoint. For people already comfortable with AI coding clients, setup cost is low. Register, complete the first `15 CNY` top-up, fill in the endpoint, key, and model name, then run a few real tasks.

If you want to try it, start at the [FreeModel registration link](https://agentrouter.org/register?aff=Vnpm), create an API key, and follow the WorkBuddy custom model flow. Only expand usage after connectivity, latency, context handling, and usage reporting look acceptable.

This article is based on campaign details provided on 2026-07-27 and FreeModel's public entry pages. Campaign rules, free quota, first top-up requirements, model availability, and endpoints should be verified on FreeModel's live site.
