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

## Part 3: 20 Feature Ideas for PowerGrabber

These features leverage PowerGrabber's unique position — inside the browser network stack — to address OWASP AI security risks and provide visibility into the AI coding tool ecosystem.

### Idea 1: LLM API Endpoint Detection & Classification Engine

**OWASP Coverage:** LLM10 (Unbounded Consumption), ASI02 (Tool Misuse)

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

### Idea 2: AI Coding Tool Traffic Fingerprinting

**OWASP Coverage:** ASI10 (Rogue Agents), ASI03 (Agent Identity)

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

### Idea 3: AI API Cost Estimation Engine

**OWASP Coverage:** LLM10 (Unbounded Consumption / Denial of Wallet)

Estimate per-request and aggregate costs using response headers that major providers include:

- **OpenAI:** `x-ratelimit-remaining-tokens`, `x-ratelimit-limit-tokens`, response body token usage (where visible)
- **Anthropic:** `x-ratelimit-*` headers, `anthropic-ratelimit-*` headers
- **Google:** Response metadata includes token counts

Maintain a pricing table (configurable, user-updateable) mapping provider + model + token count to dollar cost. Track:

- Cost per request (estimated)
- Cost per provider per hour/day/month
- Cost per originating tab/domain
- Running total across all providers
- Budget threshold alerts (configurable)

Output: Running cost ticker in text mode, detailed cost breakdown in JSON mode. Alert events when thresholds exceeded.

---

### Idea 4: Shadow AI Discovery Report

**OWASP Coverage:** LLM06 (Excessive Agency), ASI02 (Tool Misuse)

Automated reporting of unauthorized AI service usage. Maintain a configurable allowlist of approved AI services and endpoints. Flag any AI API traffic not on the list.

Report format:
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

### Idea 5: Agentic Request Chain Tracing

**OWASP Coverage:** ASI01 (Goal Hijack), ASI02 (Tool Misuse), ASI08 (Cascading Failures)

Track sequences of requests that form agentic tool-use chains. When an AI coding tool makes an API call that triggers a response, then makes follow-up calls to other APIs, this forms a chain. Detect and log:

- **Chain start:** Initial request to LLM API
- **Chain links:** Subsequent requests triggered within a time window from the same tab/origin
- **Chain depth:** How many sequential API calls in the chain
- **Chain breadth:** How many distinct endpoints contacted
- **Anomaly detection:** Chains that are unusually long, contact unexpected endpoints, or show error cascades

Example chain: Claude Code → `api.anthropic.com` → (tool call) → `api.github.com` → (tool call) → `registry.npmjs.org` → (tool call) → `api.anthropic.com`

This maps the actual tool-use behavior of agentic systems, making OWASP ASI02 (Tool Misuse) and ASI08 (Cascading Failures) visible.

---

### Idea 6: MCP Server Traffic Monitor

**OWASP Coverage:** ASI04 (Agentic Supply Chain Compromise)

Model Context Protocol (MCP) servers are the connection point between AI assistants and external tools/APIs/data. OWASP has published specific guidance on securing MCP servers. PowerGrabber can:

- Detect HTTP-based MCP server traffic (MCP uses HTTP+SSE or stdio transports)
- Log which MCP servers are being contacted
- Track tool discovery requests (MCP `tools/list` calls)
- Monitor for MCP server "swap attacks" (CVE-2025-54136 pattern — tool descriptions changing between authorization and execution)
- Flag MCP traffic to unknown/unauthorized servers

Maintain a registry of known MCP server endpoints. Alert on first-seen MCP servers. Log all tool invocations through MCP.

---

### Idea 7: Rate Limit & Quota Dashboard

**OWASP Coverage:** LLM10 (Unbounded Consumption)

Extract and track rate-limit headers from LLM API responses:

```
x-ratelimit-limit-requests: 10000
x-ratelimit-remaining-requests: 9456
x-ratelimit-limit-tokens: 2000000
x-ratelimit-remaining-tokens: 1834211
x-ratelimit-reset-requests: 6ms
x-ratelimit-reset-tokens: 234ms
retry-after: 2
```

Track per provider:
- Current request/token consumption rate
- Remaining quota percentage
- Time to quota reset
- 429 (rate limited) response frequency
- Projected exhaustion time at current rate

Alert when: remaining quota drops below configurable threshold, 429 responses exceed threshold, consumption rate spikes suddenly.

---

### Idea 8: Model Extraction Attack Detection

**OWASP Coverage:** ML05 (Model Theft), LLM10 (Unbounded Consumption)

Detect patterns characteristic of model extraction attacks:

- **High-volume systematic queries:** Unusually high request rate to a single inference endpoint with minimal variation
- **Distillation patterns:** Requests that appear to be systematically probing the model's decision boundary
- **Embedding extraction:** High volume of embedding requests with synthetic inputs
- **API scraping:** Requests with incrementing or systematically varied parameters

Detection heuristics:
- Request rate to single model endpoint exceeds N/minute (configurable)
- Request patterns show low entropy in varied parameters
- Same model endpoint hit from multiple tabs in parallel
- Request volume dramatically exceeds normal usage baseline

---

### Idea 9: OWASP AI Compliance Scorecard

**OWASP Coverage:** All LLM01-LLM10, ASI01-ASI10

Generate a compliance scorecard based on observed traffic patterns:

```
OWASP AI COMPLIANCE SCORECARD
==============================
LLM01 Prompt Injection:      MONITORING — 0 suspicious patterns detected
LLM02 Sensitive Disclosure:   WARNING — 3 large response transfers to unknown AI endpoints
LLM03 Supply Chain:           PASS — all model downloads from approved sources
LLM06 Excessive Agency:       WARNING — Cursor made 847 API calls in 1 hour
LLM10 Unbounded Consumption:  FAIL — 2 providers at >90% rate limit
ASI02 Tool Misuse:            WARNING — Claude Code contacted 12 unique APIs in one session
ASI04 Supply Chain:           MONITORING — 2 new MCP servers detected this week
ASI07 Inter-Agent Comms:      PASS — all agent traffic uses TLS
```

Score calculated from: observed traffic patterns, header analysis, endpoint inventory, rate limit status, anomaly counts. Exportable as JSON for SIEM integration.

---

### Idea 10: AI Data Flow Mapping

**OWASP Coverage:** LLM02 (Sensitive Disclosure), ASI01 (Goal Hijack)

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

### Idea 11: Vector Database & RAG Traffic Monitor

**OWASP Coverage:** LLM08 (Vector and Embedding Weaknesses), ASI06 (Memory Poisoning)

Detect and monitor traffic to vector databases and RAG infrastructure:

**Known Endpoints:**
- Pinecone: `*.pinecone.io`
- Weaviate: `*.weaviate.network`, `*.semi.technology`
- Qdrant: `*.qdrant.io`, Qdrant Cloud endpoints
- ChromaDB: Chroma Cloud endpoints
- Milvus: Zilliz Cloud endpoints
- Supabase pgvector: `*.supabase.co` with vector-specific paths

Track:
- Which vector databases are in use
- Upsert (write) vs query (read) ratio — high writes from unexpected sources may indicate poisoning
- Cross-origin access patterns — which applications read/write to which vector stores
- Embedding API calls (OpenAI `/v1/embeddings`, Cohere `/v1/embed`) correlated with vector DB writes

---

### Idea 12: AI Traffic Policy Engine

**OWASP Coverage:** LLM06 (Excessive Agency), ASI02 (Tool Misuse)

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

### Idea 13: Credential Exposure Detection in AI Context

**OWASP Coverage:** LLM02 (Sensitive Disclosure), LLM07 (System Prompt Leakage), ASI03 (Privilege Abuse)

Enhance the existing redaction system to also detect and alert (not just redact) credential patterns visible in URLs and headers:

- API keys in query parameters: `sk-proj-*`, `sk-ant-*`, `AIza*`, `ghp_*`, `gho_*`, `github_pat_*`
- OAuth tokens in URLs: `access_token=*`, `code=*`, `state=*`
- Bearer tokens in non-standard headers
- Multiple distinct API keys used to the same provider (credential sharing/sprawl)
- Expired/rotated credentials (detected via 401 responses after previously successful auth)

Alert events include: credential type detected, provider, originating tab, timestamp. Values always redacted — alert on presence, not content.

---

### Idea 14: AI Extension Update & Integrity Monitor

**OWASP Coverage:** LLM03 (Supply Chain), ASI04 (Agentic Supply Chain)

Monitor browser extension update traffic and integrity:

- Detect extension update checks to Chrome Web Store, Firefox AMO, Edge Add-ons
- Log version changes for AI-related extensions (Copilot, Cursor, Cline, etc.)
- Flag extensions making unexpected API calls post-update
- Detect new extensions being installed that request AI-related permissions
- Track `chrome-extension://` and `moz-extension://` origin traffic patterns

The ShadowPrompt attack on Claude Code's Chrome extension demonstrated that compromised extensions can inject prompts silently. Monitoring extension network behavior detects this class of attack.

---

### Idea 15: Multi-Agent Communication Auditor

**OWASP Coverage:** ASI07 (Insecure Inter-Agent Communication), ASI08 (Cascading Failures)

In multi-agent architectures, agents communicate via HTTP APIs. Detect and audit:

- **Unencrypted inter-agent traffic:** HTTP (not HTTPS) between agent endpoints
- **Missing authentication:** Agent-to-agent requests without Authorization headers
- **Replay patterns:** Identical request payloads sent repeatedly (potential replay attack)
- **Agent-in-the-middle indicators:** Requests routed through unexpected intermediaries
- **Error cascades:** Sequence of 4xx/5xx responses across multiple agent endpoints within a time window

Log all inter-agent communication with: source agent identifier, destination agent, auth present (yes/no), encryption (TLS/plain), response status, latency.

---

### Idea 16: AI Session Forensics Recorder

**OWASP Coverage:** ASI01 (Goal Hijack), ASI10 (Rogue Agents)

Record complete AI interaction sessions for forensic analysis:

- Group related requests into "sessions" based on tab, time window, and provider
- Each session records: start/end time, total requests, providers contacted, endpoints hit, error count, rate limit events, credential detections, policy violations
- Sessions exportable as structured JSONL for SIEM ingestion or standalone analysis
- Bookmark/tag sessions for investigation
- Compare session patterns: "this Claude Code session contacted 3x more unique endpoints than the 30-day average"

For incident response: when a security event occurs, the session log provides a complete timeline of what the AI agent did at the network layer.

---

### Idea 17: Prompt-to-Execution Pipeline Monitor

**OWASP Coverage:** LLM05 (Improper Output Handling), ASI05 (Unexpected Code Execution)

Detect when LLM API responses are followed by execution-like activity:

**Pattern:** Request to LLM API → Response received → Within N seconds, request to:
- Package registry (npmjs.org, pypi.org, crates.io) — LLM suggested installing a package
- GitHub API (creating repos, pushing code, opening issues) — LLM-driven automation
- Cloud provider APIs (AWS, GCP, Azure) — LLM-directed infrastructure changes
- Internal APIs — LLM output being passed to downstream systems

**Detection:** Temporal correlation between LLM response events and subsequent requests to known execution targets. Alert when the gap is suspiciously short (automated pipeline) or when the execution target is sensitive.

This detects the OWASP LLM05 scenario where LLM output flows directly into execution without human review.

---

### Idea 18: AI Model Inventory & Drift Tracker

**OWASP Coverage:** LLM03 (Supply Chain), ASI04 (Agentic Supply Chain)

Automatically build and maintain an inventory of AI models in use:

- Extract model identifiers from URL paths (e.g., `/v1/models/gpt-4o`, `/v1beta/models/gemini-2.0-flash`)
- Track model usage over time: which models are being used, when they first appeared, when they were last used
- Detect model changes: an application that was using GPT-4o suddenly switching to a different model
- Flag deprecated models (maintain a list of known deprecated model IDs)
- Detect shadow model usage: models being accessed that aren't on the approved list

Output: Model inventory report with provider, model ID, first seen date, last seen date, request count, originating tabs/domains.

---

### Idea 19: AI Supply Chain Download Monitor

**OWASP Coverage:** LLM03 (Supply Chain), ML06 (AI Supply Chain Attacks), ASI04 (Agentic Supply Chain)

Monitor downloads from AI model hubs and ML package registries:

**Known Sources:**
- HuggingFace: `huggingface.co/api/models/*`, `cdn-lfs.huggingface.co/*`
- PyPI (ML packages): `pypi.org`, `files.pythonhosted.org` — track downloads of torch, transformers, tensorflow, langchain, llamaindex, etc.
- npm (AI packages): `registry.npmjs.org` — track openai, @anthropic-ai/sdk, langchain, etc.
- Docker Hub: `registry-1.docker.io` — ML model containers
- ONNX Model Zoo, TensorFlow Hub, PyTorch Hub

Track:
- What's being downloaded (package names, model names where visible in URL)
- Version information
- Download size (from Content-Length headers)
- First-time downloads vs updates
- Downloads from unofficial/forked registries

Flag: Downloads of known-vulnerable model versions, downloads from non-standard registries, unusually large downloads.

---

### Idea 20: Real-Time AI Security Dashboard Protocol

**OWASP Coverage:** All

Define a structured event protocol for real-time dashboard consumption. Instead of just JSONL to stdout, emit enriched security events over a secondary WebSocket for dashboard consumption:

**Event Types:**
```json
{"type": "ai_request", "provider": "openai", "model": "gpt-4o", "endpoint_type": "chat", "tab_url": "...", "cost_estimate": 0.003}
{"type": "ai_response", "provider": "openai", "status": 200, "ratelimit_remaining": 456, "tokens_used": 1234}
{"type": "tool_detected", "tool": "cursor", "version": "0.48.1", "provider": "anthropic"}
{"type": "shadow_ai_alert", "provider": "cohere", "tab_url": "Internal CRM", "severity": "warning"}
{"type": "policy_violation", "rule": "healthcare-origin-block", "tab_url": "Patient Records", "endpoint": "api.openai.com"}
{"type": "cost_threshold", "provider": "openai", "daily_total": 147.32, "threshold": 100.00}
{"type": "chain_anomaly", "chain_depth": 12, "unique_endpoints": 8, "duration_ms": 34000}
{"type": "model_drift", "provider": "anthropic", "old_model": "claude-3.5-sonnet", "new_model": "claude-4-opus"}
{"type": "mcp_server_detected", "server": "github-mcp.example.com", "first_seen": true}
{"type": "supply_chain_download", "source": "huggingface", "artifact": "meta-llama/Llama-3.1-8B", "size_mb": 4800}
```

This protocol enables building web dashboards, Grafana panels, SIEM integrations, Slack alerts, and custom monitoring pipelines. The Rust backend would expose a second WebSocket endpoint (configurable, separate auth token) that emits these enriched events.

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
