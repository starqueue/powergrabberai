# PowerGrabber Feature Analysis: OWASP AI Security + AI Coding Tool Landscape

## Date: 2026-04-08

---

## Part 1: OWASP AI Security Landscape

Three OWASP frameworks now cover AI security. PowerGrabber sits at a unique vantage point — inside the browser's network stack — where it can observe violations of all three.

### OWASP Top 10 for LLM Applications (2025 v2.0)

| ID | Name | What It Means | PowerGrabber Relevance |
|----|------|---------------|----------------------|
| LLM01 | Prompt Injection | User or external content alters LLM behavior. Direct (user crafts malicious prompt) and indirect (malicious content in files/websites processed by LLM). Multimodal injection via images. | **HIGH** — PG sees every request to LLM APIs. Can detect known injection patterns in URLs, headers, and request metadata. |
| LLM02 | Sensitive Information Disclosure | LLMs leak PII, financial data, health records, credentials, proprietary info in responses. Model inversion attacks extract training data. | **HIGH** — PG captures response headers and status codes from LLM APIs. Can flag responses that indicate large data transfers or unusual response patterns. |
| LLM03 | Supply Chain | Vulnerable pre-trained models, poisoned LoRA adapters, weak model provenance, compromised model hubs (HuggingFace). | **MEDIUM** — PG sees downloads from model hubs and package registries. Can detect pulls of known-vulnerable model artifacts. |
| LLM04 | Data and Model Poisoning | Training data manipulation introducing backdoors, biases. Split-View Poisoning, Frontrunning Poisoning, sleeper agent patterns. Malicious pickling. | **LOW** — Training happens server-side. PG could detect suspicious uploads to fine-tuning endpoints. |
| LLM05 | Improper Output Handling | LLM output passed to downstream systems without validation — XSS, SSRF, RCE, SQL injection via LLM-generated content. | **MEDIUM** — PG can detect when LLM responses are followed by suspicious downstream requests (e.g., eval endpoints, shell execution APIs). |
| LLM06 | Excessive Agency | LLM systems with too many tools, too many permissions, too little oversight. Hallucination-driven tool misuse. | **HIGH** — PG sees the entire request chain from agentic tools. Can detect excessive tool call frequency, unusual API access patterns. |
| LLM07 | System Prompt Leakage | System prompts containing API keys, credentials, internal decision rules exposed. | **MEDIUM** — PG can detect responses containing credential-like patterns in headers or redirect URLs. |
| LLM08 | Vector and Embedding Weaknesses | RAG system vulnerabilities: access control gaps, cross-tenant leaks, embedding inversion, vector store poisoning. | **MEDIUM** — PG sees traffic to vector databases (Pinecone, Weaviate, Qdrant, ChromaDB endpoints). |
| LLM09 | Misinformation | LLMs produce false/misleading content. Hallucinated legal cases, fake health advice, nonexistent code libraries. | **LOW** — Content analysis is beyond PG's current capture scope (HTTP metadata, not bodies). |
| LLM10 | Unbounded Consumption | DoS, Denial of Wallet, model extraction via API, resource-intensive queries. | **HIGH** — PG can track request frequency, detect API abuse patterns, monitor rate-limit headers for consumption tracking. |

### OWASP Top 10 for Agentic Applications (2026)

This is the most directly relevant framework. Agentic AI tools (Claude Code, Codex CLI, Gemini CLI, Cursor, Cline) are autonomous agents that make HTTP calls, execute code, and access file systems. PowerGrabber observes their network layer.

| ID | Name | What It Means | PowerGrabber Relevance |
|----|------|---------------|----------------------|
| ASI01 | Agent Goal Hijack | Attackers manipulate agent goals via instruction injection. E.g., "EchoLeak" — email payload causes Microsoft 365 Copilot to silently exfiltrate data. | **HIGH** — PG sees the resulting exfiltration requests. A hijacked agent's network behavior is visible. |
| ASI02 | Tool Misuse & Exploitation | Agents misuse legitimate tools due to excessive permissions, lack of rate limiting. Not malicious tools — overpermitted tools. | **HIGH** — PG sees every tool-triggered HTTP request. Unusual patterns (unexpected endpoints, high frequency) are detectable. |
| ASI03 | Agent Identity & Privilege Abuse | Agents operating with inherited credentials, cached tokens, delegated permissions beyond intended scope. | **HIGH** — PG sees Authorization headers (redacted values but presence detected), credential usage patterns across endpoints. |
| ASI04 | Agentic Supply Chain Compromise | Dynamic runtime composition — agents discover and integrate tools/MCP servers at runtime. Compromised tools, poisoned descriptors. GitHub MCP exploit demonstrated this. | **HIGH** — PG sees MCP server traffic, tool discovery requests, and runtime component loading. |
| ASI05 | Unexpected Code Execution | Agents execute code not intended by designers — code generation tools, dynamic eval, injection into executable contexts. AutoGPT RCE. | **MEDIUM** — PG sees the HTTP layer but not local code execution. Can detect when code execution leads to unexpected network calls. |
| ASI06 | Memory & Context Poisoning | Persistent corruption of agent memory, RAG stores, embeddings. Future reasoning biased by tainted data. | **MEDIUM** — PG can detect writes to vector databases, RAG update endpoints, and memory persistence APIs. |
| ASI07 | Insecure Inter-Agent Communication | Agent-to-agent communication lacking auth, encryption, schema validation. Spoofing, replay, MITM between agents. | **HIGH** — PG captures all HTTP traffic including inter-agent API calls. Missing auth headers and unencrypted traffic are visible. |
| ASI08 | Cascading Agent Failures | Small faults propagate across multi-agent workflows. Single agent error amplified into system-wide failure. | **MEDIUM** — PG can detect error cascades (sequences of 4xx/5xx responses across related request chains). |
| ASI09 | Human-Agent Trust Exploitation | Agents exploit anthropomorphism and authority bias. Confidently recommend risky actions, socially engineer users. | **LOW** — This is a UI/UX concern, not observable at the network layer. |
| ASI10 | Rogue Agents | Compromised or misaligned agents acting maliciously while appearing legitimate. | **HIGH** — PG sees all network behavior. A rogue agent's unauthorized API calls, data exfiltration, and unusual traffic patterns are visible at the network layer. |

### OWASP ML Security Top 10 (2023)

| ID | Name | PowerGrabber Relevance |
|----|------|----------------------|
| ML01 | Input Manipulation Attack | LOW — Server-side concern |
| ML02 | Data Poisoning Attack | LOW — Training-time concern |
| ML03 | Model Inversion Attack | MEDIUM — PG can detect repeated inference queries characteristic of model inversion |
| ML04 | Membership Inference Attack | MEDIUM — Pattern of targeted queries detectable |
| ML05 | Model Theft | HIGH — Model extraction via API is detectable (high-volume systematic queries to inference endpoints) |
| ML06 | AI Supply Chain Attacks | MEDIUM — Downloads from model hubs, ML package installs visible |
| ML07 | Transfer Learning Attack | LOW — Training-time concern |
| ML08 | Model Skewing | LOW — Training-time concern |
| ML09 | Output Integrity Attack | MEDIUM — Manipulated responses may trigger unusual downstream requests |
| ML10 | Model Poisoning | LOW — Model parameter manipulation is server-side |

---

## Part 2: AI Coding Tool Landscape — Network Behavior Analysis

PowerGrabber sits at the browser layer, but many AI coding tools also make browser-visible HTTP calls (via extensions, web UIs, or browser-based authentication). Here's what PG can observe.

### Claude Code (Anthropic)

**Known API Endpoints:**
- `api.anthropic.com` — all inference requests (prompts, code context, conversation history)
- `claude.ai` — OAuth authentication for consumer subscribers
- `platform.claude.com` — Console/API authentication
- `storage.googleapis.com` — binary downloads, auto-updater
- `downloads.claude.ai` — install scripts, version pointers

**What Goes Over the Wire:**
- Full file contents of files read by Claude
- Prompts and responses (full conversation context)
- File names, directory structures, project organization
- Telemetry: latency/reliability metrics (opt out via `DISABLE_TELEMETRY=1`)

**Security Incidents (CVEs):**
- CVE-2025-59536 (CVSS 8.7): RCE via malicious project files — arbitrary shell commands on tool initialization in untrusted directories
- CVE-2026-21852: API key exfiltration via malicious `ANTHROPIC_BASE_URL` in repo settings files
- CVE-2025-54794 (CVSS 7.7): Path restriction bypass
- CVE-2025-54795 (CVSS 8.7): Code execution via command injection
- ShadowPrompt: Chrome extension vulnerability allowing silent prompt injection from any website
- March 2026: Debugging sourcemap accidentally published to npm, exposing 512,000 lines of TypeScript

**Permission Model:** Three-tier (deny → ask → allow). OS-level sandboxing: bubblewrap (Linux), seatbelt (macOS). Network forced through proxy. MCP server integration for extended tool access.

### OpenAI Codex CLI

**Known API Endpoints:**
- OpenAI API inference endpoints (model-specific)
- Network disabled by default in sandbox mode
- SOCKS5 proxy with policy enforcement

**Architecture:** Runs in isolated cloud containers (Codex Cloud) or local with bubblewrap/seatbelt sandboxing. Two phases: setup (network on for dependency install) then agent (network off by default).

**Approval Modes:** Auto (read/edit/command in workspace), Read-only (browse only), Full Access (unrestricted).

### Google Gemini CLI

**Known API Endpoints:**
- `generativelanguage.googleapis.com` — Gemini API
- Google Cloud Vertex AI endpoints
- Authentication: `x-goog-api-key` header or Application Default Credentials

**Security Incidents (Critical):**
- June-July 2025: Command injection + prompt injection vulnerabilities allowing silent data exfiltration of API keys, access tokens, proprietary code. Attack vector: opening an untrusted repository. Fixed v0.1.14.

**No default sandbox.** Google displays persistent red warning if sandboxing not enabled. Optional Docker/Podman/Seatbelt sandboxing.

### Cursor

**Known API Endpoints:**
- `api2.cursor.sh` — primary API requests
- `api5.cursor.sh` — agent requests
- `api3.cursor.sh`, `api4.cursor.sh` — Tab completion
- `repo42.cursor.sh` — codebase indexing
- Forwards to: OpenAI, Anthropic, Fireworks, xAI (zero-data-retention agreements)

**What Goes Over the Wire:** Recently viewed files, conversation history, code snippets. Codebase indexing uploads file hashes and changed files. Privacy Mode (`x-ghost-mode`) deletes code after each request.

**Security Incident:** CVE-2025-54136: RCE via MCP server "swap attack" — authorization bound to plugin name rather than content hash.

### Windsurf (Codeium)

**Known API Endpoints:**
- `server.codeium.com` — API requests
- `inference.codeium.com` — model inference
- `unleash.codeium.com` — feature flags
- Subprocessors: OpenAI, Anthropic, Google Vertex, xAI, Fireworks

**What Goes Over the Wire:** Autocomplete requests on every keystroke with code context. Cascade (agent) requests per instruction and tool call. "No single request contains entire codebases."

### GitHub Copilot

**Known API Endpoints:**
- `copilot-proxy.githubusercontent.com` — suggestions
- `api.githubcopilot.com` — coding agent inference
- `copilot-telemetry.githubusercontent.com/telemetry` — usage telemetry
- `collector.github.com/*` — analytics

**Cloud Agent:** Runs in cloud with firewall. Extensive package manager allowlist. Container registry access.

### Cline / Aider / Continue

**Architecture:** Open-source, bring-your-own-key. Requests go directly to configured provider (Anthropic, OpenAI, Google, or local models via Ollama). No centralized server. Zero server-side components.

**Critical Observation:** These tools have full filesystem access including `.env` files. `.gitignore` prevents commits but not reads. The recommended mitigation is zero-disk secrets (remote vault injection at runtime).

---

## Part 3: Feature Set for PowerGrabber

The weak ideas from the original 20 have been removed. What remains are features that PowerGrabber can genuinely deliver from HTTP metadata (URLs, headers, status codes, timing) without request/response body access. The OWASP Compliance Scorecard has been expanded into a detailed, practical section because this is what enterprise clients actually ask for.

### Feature 1: LLM API Endpoint Detection & Classification Engine

**Foundation feature — everything else depends on this.**

Build a detection engine that automatically identifies and classifies HTTP requests to known LLM API endpoints. Maintain a registry of:

- **OpenAI:** `api.openai.com/v1/chat/completions`, `/v1/embeddings`, `/v1/images/generations`, `/v1/audio/*`
- **Anthropic:** `api.anthropic.com/v1/messages`, `/v1/complete`
- **Google:** `generativelanguage.googleapis.com/v1beta/models/*`, Vertex AI endpoints
- **Cohere:** `api.cohere.ai/v1/generate`, `/v1/embed`, `/v1/rerank`
- **Mistral:** `api.mistral.ai/v1/chat/completions`
- **HuggingFace:** `api-inference.huggingface.co/models/*`
- **Groq:** `api.groq.com/openai/v1/*`
- **Together AI:** `api.together.xyz/v1/*`
- **Perplexity:** `api.perplexity.ai/chat/completions`
- **Fireworks:** `api.fireworks.ai/inference/v1/*`

Each request tagged with: provider name, endpoint type (chat, embedding, image, audio, moderation), model identifier (from URL path where visible), timestamp, originating tab, request/response status.

**Implementation:** Pattern matching on URL + known path structures. Configurable provider registry in TOML/JSON. New events emitted with enriched metadata.

---

### Feature 2: AI Coding Tool Traffic Fingerprinting

Detect and attribute traffic from specific AI coding tools based on their known network signatures:

| Tool | Fingerprint |
|------|------------|
| Claude Code | `api.anthropic.com` + specific User-Agent patterns + `downloads.claude.ai` |
| Cursor | `api2.cursor.sh`, `api3.cursor.sh`, `api5.cursor.sh`, `repo42.cursor.sh` |
| Windsurf | `server.codeium.com`, `inference.codeium.com` |
| GitHub Copilot | `copilot-proxy.githubusercontent.com`, `api.githubcopilot.com` |
| Gemini CLI | `generativelanguage.googleapis.com` + specific path patterns |
| Codex CLI | OpenAI API + specific User-Agent |
| Cline/Aider/Continue | Direct provider API calls + distinctive request patterns |

Emit `tool_detected` events with: tool name, tool version (from headers where available), provider being used, session duration, request count.

This gives organizations a complete inventory of which AI coding tools are in active use — addressing the "shadow AI developer tools" problem.

---

### Feature 3: AI API Cost Estimation Engine

Estimate per-request and aggregate costs using response headers that major providers include:

- **OpenAI:** `x-ratelimit-remaining-tokens`, `x-ratelimit-limit-tokens`
- **Anthropic:** `x-ratelimit-*` headers, `anthropic-ratelimit-*` headers
- **Google:** Response metadata includes token counts

Maintain a pricing table (configurable, user-updateable) mapping provider + model + token count to dollar cost. Track:

- Cost per request (estimated from token delta between consecutive rate-limit headers)
- Cost per provider per hour/day/month
- Cost per originating tab/domain
- Running total across all providers
- Budget threshold alerts (configurable)

Output: Running cost ticker in text mode, detailed cost breakdown in JSON mode. Alert events when thresholds exceeded.

---

### Feature 4: Shadow AI Discovery

Automated reporting of unauthorized AI service usage. Maintain a configurable allowlist of approved AI services and endpoints. Flag any AI API traffic not on the list.

```
SHADOW AI DISCOVERY REPORT — 2026-04-08
========================================
Approved services:   OpenAI, Anthropic (api.anthropic.com)
Unapproved detected: Cohere (api.cohere.ai) — 47 requests
                     Mistral (api.mistral.ai) — 12 requests
                     HuggingFace (api-inference.huggingface.co) — 3 requests
First seen:          Cohere at 09:14:22 from tab "Internal Dashboard"
```

Configurable via a policy file defining approved/denied providers. Denial emits alert events. Supports both allowlist (only approved) and denylist (block specific) modes.

---

### Feature 5: AI Data Flow Mapping

Build a directed graph of data flows between browser tabs/origins and AI endpoints:

```
Tab: "Internal CRM"
  → api.openai.com/v1/chat/completions (247 requests)
  → api.anthropic.com/v1/messages (12 requests)

Tab: "GitHub - private-repo"
  → copilot-proxy.githubusercontent.com (1,843 requests)
  → api.anthropic.com/v1/messages (89 requests)
  → api2.cursor.sh (234 requests)

Tab: "Patient Records System"
  → api.openai.com/v1/chat/completions (3 requests) ← ALERT: Healthcare origin → AI API
```

Map which internal applications/domains send data to which AI providers. Flag sensitive origins (healthcare, financial, HR systems) sending traffic to AI endpoints. This is the core data flow visibility that compliance teams need.

---

### Feature 6: AI Traffic Policy Engine

Configurable rule engine for AI traffic governance:

```toml
# policy.toml

[[rules]]
name = "block-unapproved-providers"
action = "alert"  # alert | log | block (future)
match = { provider = "!openai,!anthropic" }
message = "Unapproved AI provider detected"

[[rules]]
name = "rate-limit-alert"
action = "alert"
match = { provider = "*", requests_per_minute = ">100" }
message = "Excessive AI API call rate"

[[rules]]
name = "healthcare-origin-block"
action = "alert"
match = { tab_url_contains = "patient|medical|health", endpoint_type = "llm" }
message = "Healthcare application sending data to LLM API"

[[rules]]
name = "after-hours-alert"
action = "alert"
match = { provider = "*", time_range = "18:00-08:00" }
message = "AI API usage outside business hours"

[[rules]]
name = "new-tool-alert"
action = "alert"
match = { coding_tool = "first_seen" }
message = "New AI coding tool detected"
```

Rules evaluated against every captured event. Matching rules emit structured alert events.

---

### Feature 7: Credential Exposure Detection in AI Context

Enhance the existing redaction system to also detect and alert (not just redact) credential patterns visible in URLs and headers:

- API keys in query parameters: `sk-proj-*`, `sk-ant-*`, `AIza*`, `ghp_*`, `gho_*`, `github_pat_*`
- OAuth tokens in URLs: `access_token=*`, `code=*`, `state=*`
- Bearer tokens in non-standard headers
- Multiple distinct API keys used to the same provider (credential sharing/sprawl)
- Expired/rotated credentials (detected via 401 responses after previously successful auth)

Alert events include: credential type detected, provider, originating tab, timestamp. Values always redacted — alert on presence, not content.

---

### Feature 8: AI Model Inventory & Drift Tracker

Automatically build and maintain an inventory of AI models in use:

- Extract model identifiers from URL paths (e.g., `/v1/models/gpt-4o`, `/v1beta/models/gemini-2.0-flash`)
- Track model usage over time: which models are being used, when they first appeared, when they were last used
- Detect model changes: an application that was using GPT-4o suddenly switching to a different model
- Flag deprecated models (maintain a list of known deprecated model IDs)
- Detect shadow model usage: models being accessed that aren't on the approved list

Output: Model inventory report with provider, model ID, first seen date, last seen date, request count, originating tabs/domains.

---

### Feature 9: Real-Time AI Security Dashboard Protocol

Define a structured event protocol for real-time dashboard consumption. Instead of just JSONL to stdout, emit enriched security events over a secondary WebSocket for dashboard consumption:

```json
{"type": "ai_request", "provider": "openai", "model": "gpt-4o", "endpoint_type": "chat", "tab_url": "...", "cost_estimate": 0.003}
{"type": "ai_response", "provider": "openai", "status": 200, "ratelimit_remaining": 456, "tokens_used": 1234}
{"type": "tool_detected", "tool": "cursor", "version": "0.48.1", "provider": "anthropic"}
{"type": "shadow_ai_alert", "provider": "cohere", "tab_url": "Internal CRM", "severity": "warning"}
{"type": "policy_violation", "rule": "healthcare-origin-block", "tab_url": "Patient Records", "endpoint": "api.openai.com"}
{"type": "cost_threshold", "provider": "openai", "daily_total": 147.32, "threshold": 100.00}
{"type": "model_drift", "provider": "anthropic", "old_model": "claude-3.5-sonnet", "new_model": "claude-4-opus"}
```

This protocol enables building web dashboards, Grafana panels, SIEM integrations, Slack alerts, and custom monitoring pipelines. The Rust backend would expose a second WebSocket endpoint (configurable, separate auth token) that emits these enriched events.

---

### Feature 10: OWASP AI Compliance Scorecard

This is the feature that enterprise clients will ask for by name. The rest of this section is dedicated to making it practical and honest — mapping each OWASP item to what PowerGrabber can actually detect, what evidence it produces, and what score it can legitimately assign.

#### The Principle: Score What You Can See

PowerGrabber captures HTTP metadata: URLs, headers (with sensitive values redacted but presence detected), status codes, timing, tab context, and request/response lifecycle events. It does NOT capture request or response bodies.

This means PowerGrabber can provide genuine compliance evidence for some OWASP items, partial evidence for others, and no meaningful evidence for a few. The scorecard must be honest about this. A score of "NOT ASSESSABLE — requires code review" is more valuable to a compliance team than a fabricated "PASS" based on insufficient data.

#### Scoring Model

Each OWASP item gets one of five statuses:

| Status | Meaning |
|--------|---------|
| **PASS** | PowerGrabber has positive evidence that the risk is being managed. Specific, observable criteria met. |
| **WARNING** | PowerGrabber has detected activity that may indicate a problem. Requires human investigation. |
| **FAIL** | PowerGrabber has detected clear evidence of a violation. Specific, observable criteria breached. |
| **MONITORING** | PowerGrabber is actively tracking this risk but has no findings yet. Baseline being established. |
| **NOT ASSESSABLE** | This risk cannot be meaningfully assessed from HTTP metadata. Requires other controls (code review, architecture audit, access control audit). Stating this clearly is itself valuable to the compliance team — it tells them where to focus other efforts. |

---

#### OWASP Top 10 for LLM Applications (2025) — Item-by-Item Scorecard

##### LLM01: Prompt Injection — NOT ASSESSABLE (with caveats)

**Why PowerGrabber can't score this:** Prompt injection is a content-level attack — it happens inside request and response bodies that PowerGrabber doesn't capture. You can't detect a malicious prompt from a URL and a set of headers.

**What PowerGrabber CAN provide as supporting evidence:**
- **Indirect injection surface area:** Count how many distinct external data sources (websites, APIs) feed into tabs that also make LLM API calls. A tab that loads content from 47 external domains and then sends it to ChatGPT has a larger indirect injection surface than one that loads from 2.
- **Injection attack aftermath:** If a prompt injection succeeds in causing an agent to exfiltrate data, PowerGrabber sees the exfiltration request — an unexpected outbound call to an unusual endpoint immediately following an LLM response.

**Scorecard output:**
```
LLM01 Prompt Injection:  NOT ASSESSABLE — requires content inspection
  Supporting data:
  - 12 tabs observed with mixed external content + LLM API calls (indirect injection surface)
  - 0 suspicious post-LLM outbound requests detected (no observed exfiltration)
  Recommendation: Deploy content-level prompt injection scanning at the application layer
```

##### LLM02: Sensitive Information Disclosure — WARNING/PASS

**What PowerGrabber can genuinely detect:**
- **Credential presence in AI traffic:** Authorization headers, API keys, cookies present on requests to LLM endpoints (values redacted, but presence is the finding). If someone's browser is sending cookies to `api.openai.com`, that's a configuration problem regardless of the cookie's content.
- **Sensitive origin → AI endpoint data flows:** Requests from healthcare systems (`*.hospital.org`), financial systems (`*.bank.com`), HR systems to AI API endpoints. The fact that data is flowing from a sensitive system to an AI provider is itself a disclosure risk finding — you don't need to see the body to know it's a problem.
- **Large response transfers:** Unusually large `Content-Length` values on AI API responses may indicate bulk data extraction (though this is circumstantial).
- **Credential patterns in URLs:** Tokens, API keys, session IDs in query parameters of AI API requests (the existing redaction system already detects these).

**Scoring criteria:**
- PASS: No credentials detected in AI traffic, no sensitive-origin → AI flows, no unusual response sizes
- WARNING: Credentials detected in AI traffic OR sensitive-origin → AI flows detected
- FAIL: API keys in URL query parameters to AI endpoints (clear exposure)

**Scorecard output:**
```
LLM02 Sensitive Information Disclosure:  WARNING
  Findings:
  - 3 requests to api.openai.com included Cookie header (should not be present for API calls)
  - Tab "Patient Records" (*.hospital.org) made 3 requests to api.openai.com
  - 0 API keys detected in URL query parameters
  Actions: Investigate Cookie headers on API calls. Review Patient Records → OpenAI data flow.
```

##### LLM03: Supply Chain — PASS/WARNING

**What PowerGrabber can detect:**
- **Model source tracking:** Which domains are serving AI models and model artifacts. Are models being downloaded from official sources (huggingface.co, official provider CDNs) or from unknown mirrors/registries?
- **AI SDK and library versions:** User-Agent headers and URL paths often contain SDK version identifiers. Outdated SDK versions may contain known vulnerabilities.
- **New/unexpected AI dependencies:** First-time traffic to a previously unseen AI-related endpoint or model hub.

**Scoring criteria:**
- PASS: All AI traffic goes to known, approved provider endpoints. No traffic to unknown model sources.
- WARNING: Traffic detected to new/unrecognised AI endpoints. Outdated SDK version detected in User-Agent.
- FAIL: Traffic to known-compromised endpoints (if a threat intelligence feed is integrated).

**Scorecard output:**
```
LLM03 Supply Chain:  PASS
  Evidence:
  - All AI API traffic to 3 approved providers (OpenAI, Anthropic, Google)
  - No traffic to unofficial model registries or unknown AI endpoints
  - SDK versions: openai-python/1.52.0 (current), anthropic-sdk/0.40.0 (current)
  - 0 first-seen AI endpoints this reporting period
```

##### LLM04: Data and Model Poisoning — NOT ASSESSABLE

**Why:** Data poisoning happens at training time on the provider's infrastructure. PowerGrabber has zero visibility into this. Scoring it would be dishonest.

**What PowerGrabber CAN note:**
- Whether the organisation is uploading data to fine-tuning endpoints (detectable via URL patterns like `/v1/fine_tuning/jobs` on OpenAI). This doesn't detect poisoning but establishes that fine-tuning is happening, which is a prerequisite for the risk.

**Scorecard output:**
```
LLM04 Data and Model Poisoning:  NOT ASSESSABLE — training-time risk, not observable from browser
  Supporting data:
  - 0 requests to fine-tuning endpoints detected (fine-tuning not in use via browser)
  Recommendation: If fine-tuning is used, implement data validation pipelines at the training layer
```

##### LLM05: Improper Output Handling — NOT ASSESSABLE (with supporting data)

**Why PowerGrabber can't score this directly:** Whether an application validates LLM output before executing it is an application architecture question, not observable from HTTP metadata.

**What PowerGrabber CAN detect as circumstantial evidence:**
- Temporal patterns: LLM API response followed within milliseconds by requests to execution-like endpoints (package registries, cloud APIs, internal services). This is suggestive but not conclusive — a developer might independently install a package right after asking an LLM about it.

**Scorecard output:**
```
LLM05 Improper Output Handling:  NOT ASSESSABLE — requires application code review
  Supporting data:
  - 14 instances of LLM response followed by package registry request within 5 seconds
    (may indicate automated pipeline, may be coincidence — requires investigation)
  Recommendation: Audit applications that consume LLM output for input validation controls
```

##### LLM06: Excessive Agency — WARNING/PASS

**This is one of PowerGrabber's strongest OWASP items.** Excessive agency manifests directly as network behaviour: an AI agent making too many API calls, contacting too many distinct endpoints, or accessing resources beyond its intended scope.

**What PowerGrabber can detect:**
- **Request volume per tool per session:** Claude Code making 2,000 API calls in an hour vs its 30-day average of 400/hour
- **Endpoint diversity per tool:** A coding tool that normally contacts 2 APIs suddenly contacting 8 distinct endpoints
- **Function breadth:** An AI tool calling both chat and embedding and image and audio endpoints when it should only be calling chat
- **Tool count per browser:** How many distinct AI tools are active simultaneously (tool sprawl = permission sprawl)

**Scoring criteria:**
- PASS: All AI tools operating within established baselines for volume and endpoint diversity
- WARNING: Any tool exceeding 2x its baseline request volume OR contacting unexpected endpoint types
- FAIL: Tool contacting endpoints completely outside its normal pattern (potential goal hijack manifesting as excessive agency)

**Scorecard output:**
```
LLM06 Excessive Agency:  WARNING
  Findings:
  - Cursor: 847 requests in last hour (baseline: 320/hr) — 2.6x normal
  - Cursor: contacted api.openai.com/v1/images/generations (never seen before from this tool)
  - Claude Code: operating within baseline (134 requests/hr, baseline: 150/hr)
  - 4 distinct AI coding tools active simultaneously (Cursor, Copilot, Claude Code, Windsurf)
  Action: Investigate Cursor request spike and image generation endpoint access
```

##### LLM07: System Prompt Leakage — NOT ASSESSABLE

**Why:** System prompt leakage is a content-level issue. The leaked prompt is in the response body. PowerGrabber can't see response bodies.

**Scorecard output:**
```
LLM07 System Prompt Leakage:  NOT ASSESSABLE — requires response content inspection
  Recommendation: Implement output filtering at the application layer to detect system prompt patterns in responses
```

##### LLM08: Vector and Embedding Weaknesses — MONITORING (limited)

**What PowerGrabber can detect:**
- Traffic to known vector database cloud services (Pinecone, Weaviate, Qdrant, ChromaDB, Milvus/Zilliz)
- Whether embedding endpoints are being called (OpenAI `/v1/embeddings`, Cohere `/v1/embed`)
- Whether these are correlated (embedding call followed by vector DB write)

**Limitations:** PowerGrabber can tell you that vector databases are in use and how much traffic they get. It cannot assess access control configuration, cross-tenant isolation, or embedding inversion risk — those require infrastructure auditing.

**Scoring criteria:**
- MONITORING: Vector DB traffic detected, establishing usage baseline
- WARNING: Vector DB write traffic from unexpected origins

**Scorecard output:**
```
LLM08 Vector and Embedding Weaknesses:  MONITORING
  Observations:
  - Traffic to *.pinecone.io detected: 234 requests (estimated 180 reads, 54 writes based on HTTP method)
  - OpenAI /v1/embeddings called 89 times, correlated with Pinecone writes
  - All vector DB traffic from expected origins (Internal Search Service tab)
  Recommendation: Audit Pinecone access controls and tenant isolation independently
```

##### LLM09: Misinformation — NOT ASSESSABLE

**Why:** Misinformation is entirely a content quality problem. PowerGrabber sees that a request to an LLM API returned status 200. It has no idea whether the response contained accurate information.

**Scorecard output:**
```
LLM09 Misinformation:  NOT ASSESSABLE — content quality issue, not observable from HTTP metadata
  Recommendation: Implement human review processes and fact-checking workflows for LLM-generated content
```

##### LLM10: Unbounded Consumption — PASS/WARNING/FAIL

**This is PowerGrabber's single best OWASP item.** Every indicator of unbounded consumption is directly visible in HTTP metadata.

**What PowerGrabber can detect:**
- **Request rate per provider:** Requests per minute/hour/day, trend vs baseline
- **Rate limit consumption:** `x-ratelimit-remaining-*` headers showing quota depletion rate
- **429 responses:** Rate limit hits — the provider is telling you consumption is too high
- **Projected quota exhaustion:** At current consumption rate, when will the rate limit be fully consumed?
- **Denial of Wallet indicators:** Sudden spike in API calls, especially to expensive endpoints (image generation, large models)
- **Anomalous patterns:** Single tab generating orders of magnitude more requests than normal

**Scoring criteria:**
- PASS: All providers below 70% rate limit consumption, no 429s in reporting period, request rates within 1.5x baseline
- WARNING: Any provider above 70% rate limit consumption OR 429 responses detected OR request rate above 2x baseline
- FAIL: Any provider above 90% rate limit consumption OR 429 rate exceeds 5% of requests OR sudden 10x spike in request volume

**Scorecard output:**
```
LLM10 Unbounded Consumption:  FAIL
  Findings:
  - OpenAI: 94% of token rate limit consumed (1,882,000 / 2,000,000)
  - OpenAI: 23 rate-limited (429) responses in last hour (4.8% of requests)
  - Anthropic: 67% of rate limit consumed (normal range)
  - Request volume spike: +340% on OpenAI in last 2 hours vs 24h average
  - Source of spike: Cursor (api2.cursor.sh) — 1,200 requests in 2 hours from "Project Refactor" tab
  Action: IMMEDIATE — investigate Cursor runaway usage. Consider pausing or rate-limiting Cursor access.
  Cost impact: Estimated $34.50 excess spend from spike (above daily baseline)
```

---

#### OWASP Top 10 for Agentic Applications (2026) — Item-by-Item Scorecard

##### ASI01: Agent Goal Hijack — WARNING/PASS (by observable consequence)

**What PowerGrabber can detect:** Not the hijack itself (that's a prompt-level event), but the **consequences** of a successful hijack:
- Agent making requests to unexpected endpoints (data exfiltration to attacker-controlled servers)
- Agent making requests to internal APIs it doesn't normally access
- Sudden change in an agent's traffic pattern (different endpoints, different methods, different volume)

**Scoring criteria:**
- PASS: All observed agent traffic matches established baselines for endpoints and patterns
- WARNING: Agent traffic to first-seen or unexpected endpoints detected

**Scorecard output:**
```
ASI01 Agent Goal Hijack:  PASS
  Evidence:
  - All agent traffic to expected endpoints (no first-seen external domains)
  - Claude Code: 100% of traffic to api.anthropic.com and api.github.com (normal)
  - Cursor: 100% of traffic to api2.cursor.sh and api.openai.com (normal)
  - No outbound requests to suspicious or unrecognised domains from agent processes
```

##### ASI02: Tool Misuse & Exploitation — WARNING/PASS

**Excellent fit for PowerGrabber.** Tool misuse = tools doing more than they should, and that manifests as network behaviour.

**What PowerGrabber can detect:**
- **Endpoint diversity per agent:** An agent that normally uses 2 APIs now using 7
- **HTTP method escalation:** An agent that normally only does GET requests now doing POST/PUT/DELETE
- **Volume per tool type:** An embedding tool suddenly making chat completions calls
- **Cross-boundary access:** A coding tool accessing cloud infrastructure APIs (AWS, GCP, Azure console endpoints)

**Scoring criteria:**
- PASS: All tools operating within their expected endpoint sets and methods
- WARNING: Any tool accessing endpoint types outside its normal pattern
- FAIL: Tool accessing sensitive infrastructure APIs (cloud consoles, admin panels, internal services) that it has never accessed before

**Scorecard output:**
```
ASI02 Tool Misuse & Exploitation:  WARNING
  Findings:
  - Claude Code: accessed registry.npmjs.org 47 times (normal — package management)
  - Claude Code: accessed console.aws.amazon.com 2 times (UNEXPECTED — never seen before)
  - Cursor: operating within normal endpoint set
  Action: Investigate Claude Code accessing AWS console. May indicate tool operating beyond intended scope.
```

##### ASI03: Agent Identity & Privilege Abuse — WARNING/PASS

**What PowerGrabber can detect:**
- **Credential presence on agent traffic:** Does the agent's traffic carry Authorization headers? To which endpoints?
- **Credential reuse across endpoints:** Same authorization pattern (by header structure, not value) used across many different APIs suggests an overprivileged credential
- **Multiple agents, same credential pattern:** Different tools sending traffic with the same credential prefix pattern to the same provider (shared API key — privilege boundary violation)
- **401/403 responses:** Agent trying to access something it's not authorised for (may indicate permission probing or stale credentials)

**Scoring criteria:**
- PASS: Each agent uses credentials only for its expected provider. No cross-agent credential sharing detected. No 401/403 errors suggesting permission probing.
- WARNING: Credential sharing detected between agents OR 401/403 responses from unexpected endpoints
- FAIL: Agent sending credentials to endpoints outside its expected scope

**Scorecard output:**
```
ASI03 Agent Identity & Privilege Abuse:  WARNING
  Findings:
  - OpenAI API key prefix sk-proj-a... used by BOTH Cursor and Claude Code
    (credential sharing — same key used by 2 different tools, 2 different trust boundaries)
  - Copilot: using dedicated credential (copilot-proxy auth, expected pattern)
  - 0 unexpected 401/403 responses (no permission probing detected)
  Action: Issue separate API keys for Cursor and Claude Code to establish tool-level accountability
```

##### ASI04: Agentic Supply Chain Compromise — MONITORING/WARNING

**What PowerGrabber can detect (limited to HTTP-transport MCP):**
- Traffic to MCP servers using HTTP+SSE transport (many MCP servers use stdio, which PowerGrabber can't see — this is an honest limitation)
- First-seen MCP server endpoints
- HTTP-based tool discovery requests
- Downloads of agent plugins, extensions, or configuration from external sources

**Limitations:** Most MCP servers use stdio transport (local process communication), not HTTP. PowerGrabber only sees the HTTP-transported ones. This is a significant gap for this OWASP item.

**Scoring criteria:**
- MONITORING: Tracking all agent-related HTTP traffic for baseline establishment
- WARNING: New/unrecognised HTTP endpoints accessed by agent tools

**Scorecard output:**
```
ASI04 Agentic Supply Chain Compromise:  MONITORING
  Observations:
  - 0 HTTP-based MCP server connections detected (agents may use stdio transport — not visible)
  - No new agent-related endpoints detected this period
  Limitation: PowerGrabber cannot observe stdio-based MCP servers or local tool integrations.
  Recommendation: Audit MCP server configurations and tool manifests through infrastructure review.
```

##### ASI05: Unexpected Code Execution — NOT ASSESSABLE (with supporting data)

**Why:** Code execution is a local system event. PowerGrabber sees network traffic, not process execution.

**What PowerGrabber CAN provide:**
- Evidence that code execution may have resulted in network activity: agent process making HTTP requests to endpoints it doesn't normally access (the network consequence of unexpected code execution)
- Package installation requests (npmjs.org, pypi.org, crates.io) that may indicate LLM-suggested code being installed and run

**Scorecard output:**
```
ASI05 Unexpected Code Execution:  NOT ASSESSABLE — local execution not visible at network layer
  Supporting data:
  - 23 package registry requests from agent processes (expected for coding tools)
  - 0 unexpected outbound connections from agent processes
  Recommendation: Monitor agent system calls via OS-level auditing (auditd, eBPF) for code execution visibility
```

##### ASI06: Memory & Context Poisoning — NOT ASSESSABLE (with supporting data)

**Why:** Memory poisoning is a data integrity problem inside the agent's storage. PowerGrabber can't inspect what's stored.

**What PowerGrabber CAN detect:**
- Write traffic to vector databases / RAG stores from unexpected sources (potential poisoning vector)
- Volume of writes vs reads to memory endpoints (unusual write-heavy patterns may indicate bulk poisoning)

**Scorecard output:**
```
ASI06 Memory & Context Poisoning:  NOT ASSESSABLE — data integrity issue, not observable from HTTP metadata
  Supporting data:
  - Pinecone write traffic: 54 requests, all from expected origin (Internal Search Service)
  - No unexpected sources writing to vector stores
  Recommendation: Implement input validation on RAG pipeline writes. Audit vector store access controls.
```

##### ASI07: Insecure Inter-Agent Communication — PASS/FAIL (for HTTP-based comms)

**What PowerGrabber can detect for HTTP-based inter-agent communication:**
- **Encryption:** Is the traffic HTTPS or plain HTTP? (URL scheme check)
- **Authentication presence:** Does inter-agent traffic carry Authorization headers?
- **Certificate issues:** Status codes or error patterns indicating TLS problems

**Limitations:** Most inter-agent communication in current frameworks (LangGraph, CrewAI, AutoGen) happens in-process via function calls, not via HTTP. PowerGrabber only scores what goes over the network.

**Scoring criteria:**
- PASS: All observed agent HTTP traffic uses HTTPS with Authorization headers present
- WARNING: HTTPS but no Authorization headers on inter-service calls
- FAIL: Any plain HTTP traffic between agent endpoints

**Scorecard output:**
```
ASI07 Insecure Inter-Agent Communication:  PASS
  Evidence:
  - All agent HTTP traffic uses HTTPS (0 plain HTTP requests detected)
  - Authorization headers present on 100% of agent API calls
  Limitation: In-process agent communication (function calls, message queues) not visible. This score covers HTTP-based communication only.
```

##### ASI08: Cascading Agent Failures — MONITORING/WARNING

**What PowerGrabber can detect:**
- **Error cascades:** Sequence of 4xx/5xx responses across multiple endpoints within a short time window
- **Retry storms:** Same endpoint hit repeatedly with error responses (agent retrying a failed operation)
- **Correlated failures:** Multiple agents hitting errors simultaneously (shared dependency failure)

**Scoring criteria:**
- MONITORING: Baseline error rates established, no cascades detected
- WARNING: 3+ consecutive errors across 2+ endpoints within 60 seconds from the same agent
- FAIL: Error rate exceeds 20% of requests across all agent traffic for 5+ minutes

**Scorecard output:**
```
ASI08 Cascading Agent Failures:  MONITORING
  Observations:
  - Agent error rate: 1.2% (within normal range)
  - Longest error sequence: 2 consecutive 500 responses to api.openai.com (normal transient failure)
  - No multi-endpoint error cascades detected
```

##### ASI09: Human-Agent Trust Exploitation — NOT ASSESSABLE

**Why:** This is a human psychology and UI/UX issue. Whether a user blindly trusts an agent's recommendation is not observable from network traffic.

**Scorecard output:**
```
ASI09 Human-Agent Trust Exploitation:  NOT ASSESSABLE — human behavior issue, not observable from network traffic
  Recommendation: Implement mandatory human review gates for high-impact agent actions (financial, infrastructure, data deletion)
```

##### ASI10: Rogue Agents — PASS/WARNING

**What PowerGrabber can detect:** Rogue behaviour manifests as abnormal network patterns. An agent that has been compromised or has drifted from its intended behaviour will make different network calls than a healthy one.

**What PowerGrabber can detect:**
- **New endpoint access:** Agent contacting domains/APIs it has never accessed before
- **Data exfiltration patterns:** Outbound requests to unusual external services, especially those that accept arbitrary data (paste sites, file sharing, attacker-controlled endpoints)
- **Volume anomalies:** Sudden spike in agent traffic volume
- **Timing anomalies:** Agent making requests at unusual times (midnight batch operations from a coding tool that's normally used 9-5)
- **Method anomalies:** Agent switching from read-heavy (GET) to write-heavy (POST/PUT/DELETE) patterns

**Scoring criteria:**
- PASS: All agent traffic matches established baselines across all dimensions (endpoints, volume, timing, methods)
- WARNING: Any single dimension deviating significantly from baseline
- FAIL: Multiple dimensions deviating simultaneously (strong indicator of compromised agent)

**Scorecard output:**
```
ASI10 Rogue Agents:  PASS
  Evidence:
  - All agents operating within established baselines
  - Endpoint sets: stable (no new domains)
  - Volume: within 1.5x of 7-day moving average
  - Timing: all activity within business hours
  - Methods: GET/POST ratio stable
  - 0 requests to known exfiltration targets (paste sites, file sharing services, suspicious domains)
```

---

#### Full Scorecard Summary Example

```
╔══════════════════════════════════════════════════════════════════════════╗
║            POWERGRABBER — OWASP AI COMPLIANCE SCORECARD                ║
║            Reporting period: 2026-04-01 to 2026-04-08                  ║
║            Browser instances monitored: 47                              ║
║            Total AI API requests observed: 34,521                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  OWASP TOP 10 FOR LLM APPLICATIONS (2025)                             ║
║  ─────────────────────────────────────────                             ║
║  LLM01  Prompt Injection              NOT ASSESSABLE  (content-level)  ║
║  LLM02  Sensitive Info Disclosure      ⚠ WARNING      (3 findings)     ║
║  LLM03  Supply Chain                   ✓ PASS         (all approved)   ║
║  LLM04  Data and Model Poisoning       NOT ASSESSABLE  (training-time) ║
║  LLM05  Improper Output Handling       NOT ASSESSABLE  (code review)   ║
║  LLM06  Excessive Agency               ⚠ WARNING      (1 finding)     ║
║  LLM07  System Prompt Leakage          NOT ASSESSABLE  (content-level) ║
║  LLM08  Vector/Embedding Weaknesses    MONITORING      (baseline)      ║
║  LLM09  Misinformation                 NOT ASSESSABLE  (content-level) ║
║  LLM10  Unbounded Consumption          ✗ FAIL         (2 findings)    ║
║                                                                        ║
║  Assessable: 4/10 | Findings: 6 | Actions required: 3                 ║
║                                                                        ║
║  OWASP TOP 10 FOR AGENTIC APPLICATIONS (2026)                         ║
║  ─────────────────────────────────────────────                         ║
║  ASI01  Agent Goal Hijack              ✓ PASS         (normal traffic) ║
║  ASI02  Tool Misuse & Exploitation     ⚠ WARNING      (1 finding)     ║
║  ASI03  Agent Identity & Privilege     ⚠ WARNING      (key sharing)   ║
║  ASI04  Agentic Supply Chain           MONITORING      (limited vis.)  ║
║  ASI05  Unexpected Code Execution      NOT ASSESSABLE  (local exec)    ║
║  ASI06  Memory & Context Poisoning     NOT ASSESSABLE  (data integrity)║
║  ASI07  Insecure Inter-Agent Comms     ✓ PASS         (HTTPS + auth)  ║
║  ASI08  Cascading Agent Failures       MONITORING      (baseline)      ║
║  ASI09  Human-Agent Trust Exploit.     NOT ASSESSABLE  (human behavior)║
║  ASI10  Rogue Agents                   ✓ PASS         (normal baselin)║
║                                                                        ║
║  Assessable: 5/10 | Findings: 2 | Actions required: 2                 ║
║                                                                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║  OVERALL: 9/20 items assessable from HTTP metadata                     ║
║  PASS: 5  |  WARNING: 4  |  FAIL: 1  |  NOT ASSESSABLE: 8             ║
║  MONITORING: 2                                                         ║
║                                                                        ║
║  TOP ACTIONS:                                                          ║
║  1. CRITICAL: Investigate OpenAI rate limit exhaustion (LLM10)         ║
║  2. HIGH: Investigate Cursor → AWS console access (ASI02)              ║
║  3. HIGH: Issue separate API keys per tool (ASI03)                     ║
║  4. MEDIUM: Investigate Patient Records → OpenAI data flow (LLM02)    ║
║  5. MEDIUM: Investigate Cursor request volume spike (LLM06)            ║
╚══════════════════════════════════════════════════════════════════════════╝
```

#### Why Clients Want This

1. **Board and executive reporting.** "We scored 5 PASS, 4 WARNING, 1 FAIL across the OWASP AI Top 10" is a sentence a CISO can say to a board. It converts technical monitoring into governance language.

2. **Audit evidence.** When an auditor asks "how do you manage AI risks per OWASP guidance?", the scorecard is a structured, timestamped answer with specific evidence for each item. The NOT ASSESSABLE items are equally valuable — they tell the auditor exactly which risks need other controls.

3. **Prioritised action.** The scorecard doesn't just report status — it ranks the actions needed. "Fix the rate limit problem first, then investigate the AWS access" gives the security team a priority queue, not a wall of alerts.

4. **Trend tracking.** Run the scorecard weekly. "We went from 2 FAILs to 1 FAIL to 0 FAILs over 3 weeks" is measurable progress.

5. **Gap analysis.** The 8 NOT ASSESSABLE items are a precise map of where PowerGrabber's coverage ends and other tools need to begin. This is more valuable than pretending to cover everything — it builds trust and drives complementary tool purchases.

#### Export Formats

- **JSON:** Machine-readable scorecard for SIEM/dashboard ingestion
- **Markdown/HTML:** Human-readable report for email/Confluence/SharePoint distribution
- **CSV:** Per-item scores with finding counts for spreadsheet analysis
- **SARIF:** Static Analysis Results Interchange Format for integration with code security platforms (treating OWASP items as "rules" and findings as "results")

---

## Part 4: Organisation-Wide AI Usage, Account Tracking & Expense Management

This section addresses a problem that is distinct from security: **financial and operational governance of AI usage across an organisation.** Security tells you whether AI usage is dangerous. This tells you who's using what, how much it costs, and whether the organisation is getting value for money.

PowerGrabber is uniquely positioned to provide this because it sits at the browser layer — where the actual API calls happen. Unlike provider dashboards (which show usage per API key, not per person or team), PowerGrabber can attribute usage to specific browsers, tabs, applications, and time periods.

### The Problem

Organisations have no single pane of glass for AI spend. The reality looks like this:

- **Engineering** has an OpenAI API key billed to a shared credit card. Three teams use it. Nobody knows which team generates which costs.
- **Marketing** uses ChatGPT Plus subscriptions (per-seat). Some people also use the API directly via Zapier integrations. The API spend is invisible.
- **Data Science** uses Anthropic via AWS Bedrock, Google via Vertex AI, and HuggingFace inference endpoints. Three different billing systems.
- **Individual developers** use Claude Code, Cursor, Copilot, and Windsurf — each with different subscription models. Some use personal API keys expensed to the company. Some use the company's shared keys.
- **Customer-facing products** make LLM API calls from browser-based frontends. The cost per customer interaction is unknown.

The CFO asks "how much are we spending on AI?" and the honest answer is "we don't know, and we can't find out without checking 8 different dashboards, 4 credit cards, and asking every team lead."

### What PowerGrabber Can Capture (Without Request Bodies)

From HTTP headers and URLs alone, PowerGrabber can extract:

**From Request Headers:**
- `Authorization: Bearer sk-proj-*` → OpenAI project key (project identified by key prefix pattern, value redacted)
- `x-api-key: sk-ant-*` → Anthropic key
- `Authorization: Bearer gsk_*` → Groq key
- Custom headers identifying the calling application or SDK version
- `User-Agent` — identifies which client library, SDK, or tool made the call

**From Response Headers (the gold mine for cost tracking):**

OpenAI returns:
```
x-ratelimit-limit-requests: 10000
x-ratelimit-remaining-requests: 9234
x-ratelimit-limit-tokens: 2000000
x-ratelimit-remaining-tokens: 1823456
x-ratelimit-reset-requests: 6ms
x-ratelimit-reset-tokens: 234ms
openai-organization: org-abc123
openai-processing-ms: 1245
openai-version: 2020-10-01
x-request-id: req_abc123
```

Anthropic returns:
```
x-ratelimit-limit-requests: 4000
x-ratelimit-remaining-requests: 3891
x-ratelimit-limit-tokens: 400000
x-ratelimit-remaining-tokens: 389234
anthropic-ratelimit-tokens-remaining: 389234
request-id: req_abc123
```

Google returns:
```
x-goog-api-client: genai-js/0.x.x
x-request-id: abc123
```

**From URLs:**
- Model identifier: `/v1/chat/completions` with model in query params or path for some providers
- Endpoint type: chat, embeddings, images, audio, moderation, fine-tuning
- API version

**From Response Status Codes:**
- `200` — successful (billable) request
- `429` — rate limited (not billed, but indicates capacity pressure)
- `401/403` — authentication failure (credential issue)
- `500/502/503` — provider error (not billed)

### Feature: AI Usage Analytics Engine

#### 4.1 Per-Provider Usage Tracking

Track every AI API call with:

```
{
  "timestamp": "2026-04-08T14:23:01.442Z",
  "provider": "openai",
  "endpoint_type": "chat",
  "model": "gpt-4o",           // extracted from URL path where visible
  "status": 200,
  "billable": true,
  "tab_url": "cursor://workspace/project-x",
  "tab_title": "Cursor - project-x",
  "tool": "cursor",             // detected AI coding tool
  "ratelimit_remaining_tokens": 1823456,
  "ratelimit_limit_tokens": 2000000,
  "processing_ms": 1245,        // from openai-processing-ms header
  "org_id": "org-abc123",       // from openai-organization header
  "request_id": "req_abc123"
}
```

Aggregation periods: per-minute, per-hour, per-day, per-week, per-month.

Breakdowns by:
- Provider (OpenAI, Anthropic, Google, Cohere, Mistral, etc.)
- Endpoint type (chat, embedding, image, audio, moderation)
- Model (where detectable from URL)
- Originating tool (Cursor, Copilot, Claude Code, browser web UI, custom app)
- Originating application/tab (which internal app or website)
- Time of day / day of week
- Success rate (2xx vs 4xx vs 5xx)

#### 4.2 Token Consumption Tracking

The key insight: **you don't need request bodies to track token consumption.** Rate-limit headers tell you remaining tokens, and the delta between consecutive responses gives you tokens consumed per request.

**Method:**

1. On each response from an AI provider, record `ratelimit_remaining_tokens`
2. On the next response to the same provider (same rate-limit bucket), compute: `tokens_used = previous_remaining - current_remaining`
3. If `current_remaining > previous_remaining`, a rate-limit window reset occurred — flag it and start a new tracking window

This gives approximate per-request token usage without reading request/response bodies.

**Limitations (be honest about them):**
- Only works when rate-limit headers are present (most major providers include them)
- Shared API keys mean multiple consumers affect the same counter — token deltas may include other users' consumption
- Rate-limit window resets introduce gaps
- Some providers use separate token pools for input vs output tokens — headers may not distinguish

**Accuracy:** Good enough for trend analysis, budget alerts, and team-level attribution. Not accurate enough for per-request billing reconciliation. Should be presented as "estimated" with appropriate caveats.

#### 4.3 Cost Estimation

Maintain a configurable pricing table:

```toml
# pricing.toml — user-editable, ships with defaults

[openai]
"gpt-4o"           = { input_per_1k = 0.0025, output_per_1k = 0.01 }
"gpt-4o-mini"      = { input_per_1k = 0.00015, output_per_1k = 0.0006 }
"gpt-4.1"          = { input_per_1k = 0.002, output_per_1k = 0.008 }
"o3"               = { input_per_1k = 0.01, output_per_1k = 0.04 }
"text-embedding-3-small" = { input_per_1k = 0.00002 }
"text-embedding-3-large" = { input_per_1k = 0.00013 }

[anthropic]
"claude-sonnet-4-6" = { input_per_1k = 0.003, output_per_1k = 0.015 }
"claude-opus-4-6"   = { input_per_1k = 0.015, output_per_1k = 0.075 }
"claude-haiku-4-5"  = { input_per_1k = 0.0008, output_per_1k = 0.004 }

[google]
"gemini-2.5-pro"    = { input_per_1k = 0.00125, output_per_1k = 0.01 }
"gemini-2.5-flash"  = { input_per_1k = 0.00015, output_per_1k = 0.0006 }

# Users add their own providers/models here
```

Cost = estimated_tokens * price_per_token. Displayed as running totals with configurable alert thresholds.

**Cost reports:**

```
AI SPEND REPORT — 2026-04-08
=============================
Provider       Requests   Est. Tokens   Est. Cost    Trend
─────────────────────────────────────────────────────────────
OpenAI            2,847    4,123,000     $48.32       ▲ +23% vs yesterday
Anthropic         1,203    1,890,000     $31.45       ▼ -8%
Google              456      234,000      $1.12       ● stable
Cohere               89       45,000      $0.34       ▲ new this week
─────────────────────────────────────────────────────────────
TOTAL             4,595    6,292,000     $81.23

Top consumers by source:
  Cursor (api2.cursor.sh)         $34.10  (42%)
  ChatGPT web UI                  $22.40  (28%)
  Claude Code (api.anthropic.com) $18.90  (23%)
  Internal CRM AI features         $5.83   (7%)

Budget status: $81.23 / $200.00 daily limit (41%)
```

#### 4.4 Account & API Key Tracking

PowerGrabber redacts credential values but can still track credential **patterns** and **metadata**:

- **Distinct key count:** How many different API keys are being used per provider (based on key prefix patterns — `sk-proj-` vs `sk-ant-` — without storing the actual key)
- **Organisation ID tracking:** OpenAI's `openai-organization` response header identifies which org account is being billed
- **Key rotation detection:** When a previously-seen key prefix pattern stops appearing and a new one starts
- **Shared key detection:** Same provider being called from multiple distinct tools/tabs simultaneously (suggests shared API key)
- **Personal vs corporate key heuristic:** API calls from `chat.openai.com` or `claude.ai` (web UI) likely use personal accounts. API calls from coding tools or internal apps likely use corporate keys.

**Account inventory report:**

```
API KEY INVENTORY (by observable pattern)
==========================================
OpenAI:
  - Key pattern: sk-proj-a... (org: org-abc123)
    Sources: Cursor, Internal CRM
    Last seen: 2026-04-08 14:23:01
    Daily request avg: 1,200

  - Key pattern: sk-proj-x... (org: org-xyz789)
    Sources: ChatGPT web UI
    Last seen: 2026-04-08 13:45:22
    Daily request avg: 340
    NOTE: Different org ID — possible personal account

Anthropic:
  - Key pattern: sk-ant-api03-...
    Sources: Claude Code, Internal search tool
    Last seen: 2026-04-08 14:22:58
    Daily request avg: 890

  - 3 requests via claude.ai web UI (session-based, no API key visible)
    NOTE: Personal Claude accounts in use
```

#### 4.5 Team & Department Attribution

PowerGrabber can't directly know which team a browser belongs to. But it can be configured with attribution rules:

```toml
# attribution.toml

[[teams]]
name = "Engineering"
match_tab_urls = ["github.com", "gitlab.com", "cursor://", "vscode://"]
match_tools = ["cursor", "copilot", "claude-code", "windsurf"]

[[teams]]
name = "Marketing"
match_tab_urls = ["hubspot.com", "mailchimp.com", "canva.com"]

[[teams]]
name = "Data Science"
match_tab_urls = ["jupyter", "colab.research.google.com", "databricks.com"]
match_providers_via = ["bedrock", "vertex"]

[[teams]]
name = "Product"
match_tab_urls = ["linear.app", "figma.com", "notion.so"]

[[teams]]
name = "Customer-Facing"
match_tab_urls = ["app.ourcompany.com", "dashboard.ourcompany.com"]
```

This is heuristic-based and imperfect. But "Engineering spent ~$48/day on AI and Marketing spent ~$12/day" is infinitely more useful than "we have no idea."

For more accurate attribution, PowerGrabber could accept an external identity signal — e.g., the browser extension popup could include a "Team" dropdown that tags all traffic from that browser instance.

#### 4.6 Organisation-Wide Rollup

When PowerGrabber is deployed across multiple browsers (the intended enterprise scenario), the backend aggregates all traffic into a single view:

```
ORGANISATION AI USAGE — WEEKLY ROLLUP
Week of 2026-04-01
==========================================

Total AI API requests:    34,521
Total estimated tokens:   52,340,000
Total estimated cost:     $623.45
Active browser instances: 47
Active AI providers:      5
Active AI models:         12
Active coding tools:      4

Provider breakdown:
  OpenAI:     $312.10 (50.1%) — 18,234 requests
  Anthropic:  $198.40 (31.8%) — 11,203 requests
  Google:      $67.30 (10.8%) —  3,456 requests
  Cohere:      $34.20  (5.5%) —  1,204 requests
  Mistral:     $11.45  (1.8%) —    424 requests

Team breakdown:
  Engineering: $398.20 (63.9%)
  Data Science: $112.30 (18.0%)
  Marketing:    $56.40  (9.0%)
  Product:      $34.10  (5.5%)
  Unattributed: $22.45  (3.6%)

Trend: ▲ +18% vs previous week
Alert: Engineering spend increased 34% — primarily Cursor usage (+2,100 requests)
Alert: 3 new API keys detected this week (possible credential sprawl)
Alert: 89 requests to unapproved provider (Cohere) from Data Science team
```

#### 4.7 Budget Enforcement & Alerts

Configurable budget thresholds:

```toml
# budgets.toml

[global]
daily_limit = 200.00
weekly_limit = 1000.00
monthly_limit = 4000.00
alert_at = [50, 75, 90, 100]  # percentage thresholds

[per_provider.openai]
daily_limit = 120.00
alert_at = [75, 100]

[per_team.engineering]
daily_limit = 150.00
weekly_limit = 700.00

[per_team.marketing]
daily_limit = 30.00
alert_at = [80, 100]
```

Alert events emitted when thresholds crossed:

```json
{"type": "budget_alert", "scope": "global", "period": "daily", "current": 182.30, "limit": 200.00, "percent": 91, "severity": "warning"}
{"type": "budget_alert", "scope": "team:marketing", "period": "daily", "current": 30.50, "limit": 30.00, "percent": 102, "severity": "critical"}
```

#### 4.8 Subscription vs API Usage Tracking

Distinguish between:

- **Web UI usage** (ChatGPT, Claude.ai, Gemini web) — identified by tab URL. These are typically covered by per-seat subscriptions, not API billing. Still valuable to track for productivity analysis and data flow governance, but don't directly cost per-request.

- **API usage** (direct API calls from tools, extensions, internal apps) — identified by API endpoint URLs. These are billed per-token. This is where cost tracking matters.

- **Coding tool usage** (Cursor, Copilot, Windsurf) — mixed model. Subscription covers the tool, but some tools also make direct API calls billed to the user's key. PowerGrabber can distinguish between calls to the tool's own backend (e.g., `api2.cursor.sh`) and calls to the raw provider API (e.g., `api.openai.com`).

#### 4.9 Usage Anomaly Detection

Flag unusual patterns:

- **Spike detection:** Daily request count exceeds 2x the 7-day moving average
- **New provider:** First-ever request to a previously unseen AI provider
- **New model:** First-ever request to a previously unseen model
- **Off-hours usage:** Significant AI API traffic outside configured business hours
- **Single-tab surge:** One browser tab generating an unusual volume of AI requests (possible automation or runaway loop)
- **Credential sprawl:** Number of distinct API key patterns increasing over time

#### 4.10 Data Export for Finance

Export formats designed for finance teams, not engineers:

- **CSV:** Date, Provider, Team, Request Count, Estimated Tokens, Estimated Cost — importable into Excel/Google Sheets
- **JSONL:** Structured events for data warehouse ingestion
- **Monthly summary PDF** (future): Generated report with charts, suitable for attaching to expense reports or board decks

**Integration points:**
- Webhook on budget threshold: POST to Slack, PagerDuty, or custom endpoint
- Periodic report delivery: daily/weekly/monthly summaries to configured email (via external integration)
- SIEM integration: all events available on the dashboard WebSocket protocol (#20)

### What This Section Does NOT Cover (Honest Limitations)

1. **Per-request exact token counts** — without reading request/response bodies, token counts are estimated from rate-limit header deltas. This is directionally accurate but not precise.

2. **Prompt content analysis** — PowerGrabber captures HTTP metadata, not bodies. It cannot tell you what was asked or what the AI responded. This is by design (privacy), but it means usage tracking is quantitative (how much), not qualitative (what).

3. **Individual user attribution** — PowerGrabber runs per-browser. In a shared computer environment, it can't distinguish users. In a one-person-per-machine environment (standard corporate), the browser instance is a reasonable proxy for the individual.

4. **Exact cost reconciliation** — estimated costs will not match provider invoices exactly. Token estimation from headers is approximate. The goal is directional accuracy (within 20-30%) and trend visibility, not accounting-grade precision. The output should always be labelled "estimated."

5. **Subscription costs** — PowerGrabber can count web UI visits to ChatGPT or Claude.ai, but it cannot determine subscription tier or per-seat pricing. Subscription cost tracking requires data from the billing system, not the browser.

---

## Summary: Feature Priority Matrix

| # | Feature | OWASP Coverage | Implementation Complexity | Value |
|---|---------|---------------|--------------------------|-------|
| 1 | LLM API Endpoint Detection | LLM10, ASI02 | Low | Critical |
| 2 | AI Coding Tool Fingerprinting | ASI10, ASI03 | Low | High |
| 3 | AI API Cost Estimation | LLM10 | Medium | High |
| 4 | Shadow AI Discovery | LLM06, ASI02 | Low | Critical |
| 5 | Agentic Request Chain Tracing | ASI01, ASI02, ASI08 | High | High |
| 6 | MCP Server Traffic Monitor | ASI04 | Medium | High |
| 7 | Rate Limit & Quota Dashboard | LLM10 | Low | Medium |
| 8 | Model Extraction Detection | ML05, LLM10 | Medium | Medium |
| 9 | OWASP AI Compliance Scorecard | All | High | Critical |
| 10 | AI Data Flow Mapping | LLM02, ASI01 | Medium | Critical |
| 11 | Vector DB & RAG Monitor | LLM08, ASI06 | Medium | Medium |
| 12 | AI Traffic Policy Engine | LLM06, ASI02 | High | Critical |
| 13 | Credential Exposure Detection | LLM02, LLM07, ASI03 | Low | High |
| 14 | Extension Update Monitor | LLM03, ASI04 | Medium | Medium |
| 15 | Multi-Agent Comm Auditor | ASI07, ASI08 | Medium | High |
| 16 | AI Session Forensics | ASI01, ASI10 | Medium | High |
| 17 | Prompt-to-Execution Monitor | LLM05, ASI05 | High | High |
| 18 | Model Inventory & Drift | LLM03, ASI04 | Low | Medium |
| 19 | Supply Chain Download Monitor | LLM03, ML06, ASI04 | Medium | High |
| 20 | Real-Time Dashboard Protocol | All | Medium | Critical |

**Recommended Build Order (highest impact, lowest complexity first):**
1. LLM API Endpoint Detection (#1) — foundation for everything else
2. Shadow AI Discovery (#4) — immediate enterprise value
3. AI Coding Tool Fingerprinting (#2) — developer-facing value
4. Credential Exposure Detection (#13) — security quick win
5. AI Traffic Policy Engine (#12) — governance framework
6. Real-Time Dashboard Protocol (#20) — enables all downstream integrations
