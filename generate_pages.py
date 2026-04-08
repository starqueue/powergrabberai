#!/usr/bin/env python3
"""Generate 40 PowerGrabber landing pages with identical content, different visual styles."""

import os

CONTENT = '''<nav><div class="logo">PowerGrabber</div><a href="index.html">&larr; All Designs</a></nav>
<div class="tagline-bar">LLM Security &middot; LLM Visibility &middot; LLM Observability &middot; LLM Compliance &middot; LLM Monitoring &middot; LLM Capture</div>

<section class="hero">
<h1>PowerGrabber: LLM <span>Certainty.</span></h1>
<p class="subtitle">PowerGrabber is a monitoring application for macOS, Windows, and Linux. PowerGrabber captures LLM traffic in two ways: via browser extension for browser-based AI usage such as ChatGPT, Gemini, and Claude, and directly at the API for AI applications such as Claude Code &mdash; logging everything as structured, compliance-ready data.</p>
</section>

<section class="launch-notify">
<div class="notify-box">
<h2>PowerGrabber is launching soon.</h2>
<p>Be the first to know. Enter your email and we will notify you the moment PowerGrabber is available.</p>
<form class="notify-form" onsubmit="return false;">
<input type="email" placeholder="you@company.com" class="notify-input" required>
<button type="submit" class="btn-primary notify-btn">Notify Me</button>
</form>
</div>
</section>

<section class="email-section">
<div class="email-wrap">
<div class="email-stamp">Unanswered</div>
<div class="email-card">
<div class="email-chrome"><div class="edot r"></div><div class="edot y"></div><div class="edot g"></div></div>
<div class="email-fields"><strong>From:</strong> CEO &nbsp;&nbsp; <strong>To:</strong> Executive Leadership Team &nbsp;&nbsp; <strong>Date:</strong> Today 08:14</div>
<div class="email-subject">AI/LLMs &mdash; Outstanding Questions</div>
<div class="email-body">
<div class="email-greeting">Team &mdash;</div>
<p>Who in our organisation is using AI tools &mdash; and which ones?</p>
<p>What are they putting in?</p>
<p>Are our secrets leaving the company?</p>
<p>How much are we spending on AI &mdash; and who is spending it?</p>
<p>Are we legal?</p>
<p>Are we compliant?</p>
<p>Are we secure?</p>
<p>Do we know anything?</p>
<div class="email-signoff"><strong>CEO</strong></div>
</div>
</div>
</div>
</section>

<section>
<div class="section-label">Certainty</div>
<h2>Certainty looks like this.</h2>
<div class="certainty-grid">
<div class="certainty-card">
<h3>Complete Visibility</h3>
<p><strong>You know which AI tools are in use.</strong> Every AI service accessed through the browser or at the API level is captured, identified, and logged. ChatGPT, Claude, Gemini, Claude Code, and every other LLM interaction &mdash; visible, attributed, recorded.</p>
</div>
<div class="certainty-card">
<h3>Audit Record</h3>
<p><strong>You have the record your auditor will ask for.</strong> Every interaction logged as structured, compliance-ready data. Timestamped. Searchable. Exportable. The documentation the EU AI Act, GDPR, and your own governance framework require &mdash; generated automatically, continuously, not reconstructed under pressure.</p>
</div>
<div class="certainty-card">
<h3>Policy Enforcement</h3>
<p><strong>Your AI policy has an enforcement layer.</strong> A policy without observability is a document. PowerGrabber gives your policy teeth &mdash; not by restricting what people do, but by making what they do visible.</p>
</div>
<div class="certainty-card">
<h3>Compliance Evidence</h3>
<p><strong>Your compliance team can demonstrate, not just assert.</strong> There is a significant difference between telling a regulator that AI usage is governed and showing them the capture record that proves it. PowerGrabber produces the latter.</p>
</div>
<div class="certainty-card full-width">
<h3>Full Record</h3>
<p><strong>You know exactly what is leaving your organisation through AI tools.</strong> Not approximately. Not based on assumption. A precise, structured, searchable record of every prompt, every interaction, every API call &mdash; from every endpoint, every browser, every AI application in use across your organisation.</p>
</div>
</div>
</section>

<section>
<div class="section-label">How It Works</div>
<h2>How PowerGrabber works.</h2>
<ol class="steps">
<li>Install PowerGrabber on any macOS, Windows, or Linux machine.</li>
<li>Install the PowerGrabber browser extension.</li>
<li>Everything is captured to a database.</li>
<li>The PowerGrabber dashboard gives complete visibility &mdash; who is using what, what is being sent, stats, alerts, and a full audit log.</li>
<li>For organisations that need to go further, PowerGrabber logs to databases, S3, Git, and file systems.</li>
</ol>
<div class="browsers"><span>Chrome</span><span>Firefox</span><span>Edge</span><span>Safari</span><span>Opera</span></div>
</section>

<section>
<div class="section-label">Features</div>
<h2>Features</h2>

<h3 class="feature-group-title">Capture</h3>
<ul class="feature-list">
<li>Browser-based HTTP traffic capture via webRequest API &mdash; 5 event types covering the full request lifecycle</li>
<li>API-level capture for non-browser AI tools (Claude Code, Cursor, Copilot, and others)</li>
<li>Cross-browser: Chrome, Firefox, Edge, Safari, Opera, Brave, Vivaldi, Arc</li>
<li>Single extension codebase &mdash; Manifest V3 for Chromium, Manifest V2 for Firefox</li>
<li>macOS, Windows, and Linux</li>
</ul>

<h3 class="feature-group-title">Security</h3>
<ul class="feature-list">
<li>Token-based authentication &mdash; 32-character random token, validated within 10-second window</li>
<li>Automatic sensitive header redaction &mdash; Authorization, Cookie, Set-Cookie, Proxy-Authorization, X-API-Key, WWW-Authenticate, X-CSRF-Token, X-Auth-Token</li>
<li>URL query parameter sanitization &mdash; 14 sensitive patterns automatically scrubbed</li>
<li>Rate limiting &mdash; 500 events/second per connection</li>
<li>Message size cap, connection limits, input validation</li>
<li>Self-traffic filtering &mdash; extension ignores its own WebSocket connection</li>
</ul>

<h3 class="feature-group-title">Architecture</h3>
<ul class="feature-list">
<li>Rust backend &mdash; async I/O on tokio, sub-millisecond processing</li>
<li>Real-time WebSocket streaming from extension to backend</li>
<li>Backpressure with drop counting &mdash; no blocking, no memory leaks</li>
<li>1000-event offline buffer when disconnected, with automatic replay on reconnect</li>
<li>Exponential backoff reconnection (1s to 30s)</li>
<li>No proxy, no TLS interception, no network topology changes</li>
</ul>

<h3 class="feature-group-title">Output</h3>
<ul class="feature-list">
<li>JSONL structured output (machine-readable)</li>
<li>Human-readable text output</li>
<li>SQLite storage, HAR export</li>
<li>Logging to databases, S3, Git, and file systems</li>
</ul>
</section>

<section>
<div class="section-label">OWASP AI Compliance &mdash; Coming Soon</div>
<h2>OWASP Features</h2>
<p>PowerGrabber will include built-in compliance monitoring mapped to the OWASP Top 10 for LLM Applications (2025) and the OWASP Top 10 for Agentic Applications (2026).</p>

<div class="owasp-grid">
<div class="certainty-card">
<h3>LLM02 &mdash; Sensitive Information Disclosure</h3>
<p>Detect credentials present in AI traffic. Map data flows from sensitive internal systems (healthcare, finance, HR) to AI provider endpoints. Flag API keys exposed in URL parameters. Your monitoring catches disclosure risks from HTTP metadata alone.</p>
</div>
<div class="certainty-card">
<h3>LLM03 &mdash; Supply Chain</h3>
<p>Track which domains serve AI models and artifacts. Detect outdated SDK versions from User-Agent headers. Flag traffic to unknown or unapproved AI endpoints. Know when a new AI dependency appears in your organisation.</p>
</div>
<div class="certainty-card">
<h3>LLM06 &mdash; Excessive Agency</h3>
<p>Monitor request volume per AI tool against established baselines. Detect when tools contact unexpected endpoint types or access APIs outside their normal scope. Track how many AI tools are active simultaneously across your organisation.</p>
</div>
<div class="certainty-card">
<h3>LLM10 &mdash; Unbounded Consumption</h3>
<p>Track request rates per provider. Monitor rate-limit header consumption in real time. Detect 429 rate-limit responses. Project quota exhaustion. Identify denial-of-wallet patterns &mdash; sudden spikes in expensive API calls before the invoice arrives.</p>
</div>
</div>

<p class="owasp-note">PowerGrabber will assess 9 of 20 OWASP AI items directly from HTTP metadata, provide supporting evidence for 3 more, and honestly report 8 as NOT ASSESSABLE &mdash; because knowing where your coverage ends is as valuable as knowing where it begins.</p>
</section>

<section>
<div class="section-label">Teams</div>
<h2>Built for the teams who need it.</h2>
<div class="teams-grid">
<div class="team-card"><h3>Compliance and GRC</h3><p>Continuous, automated capture of LLM interactions across the organisation. Audit-ready records without manual effort.</p></div>
<div class="team-card"><h3>Security and IT</h3><p>Complete visibility into AI tool usage across every endpoint. Shadow AI surfaced. Usage attributed. Anomalies identifiable.</p></div>
<div class="team-card"><h3>Legal and Privacy</h3><p>Documentation of AI data flows for GDPR, EU AI Act, HIPAA, and emerging AI regulatory obligations.</p></div>
<div class="team-card"><h3>Engineering and DevOps</h3><p>Full observability into LLM API usage &mdash; including developer tools like Claude Code and Cursor &mdash; for governance, cost attribution, and compliance.</p></div>
</div>
</section>

<section>
<div class="section-label">Pricing</div>
<h2>Pricing</h2>
<div class="pricing-grid">
<div class="price-card"><h3>Free</h3><div class="price">$0</div><p>Core capture. Single endpoint. CLI output.</p></div>
<div class="price-card"><h3>Pro</h3><div class="price">$19</div><div class="price-sub">/month</div><p>Advanced capture, structured logging, SQLite storage, HAR export.</p></div>
<div class="price-card"><h3>Team</h3><div class="price">$49</div><div class="price-sub">/user/month</div><p>Shared dashboard, compliance reporting, CI/CD integration.</p></div>
<div class="price-card"><h3>Enterprise</h3><div class="price">$10K+</div><div class="price-sub">/year</div><p>Multi-endpoint, SIEM integration, compliance dashboards, MDM, SSO.</p></div>
</div>
</section>

<div class="final-cta">
<h2>PowerGrabber is launching soon.</h2>
<p class="subtitle">Leave your email. We will let you know.</p>
<form class="notify-form" onsubmit="return false;">
<input type="email" placeholder="you@company.com" class="notify-input" required>
<button type="submit" class="btn-primary notify-btn">Notify Me</button>
</form>
<div class="tagline">PowerGrabber. LLM Certainty.</div>
</div>

<footer><a href="index.html">&larr; Back to all designs</a></footer>'''

# 40 different style definitions
# Each is: (style_name, font_import, css)
STYLES = [
# 1 - Radar Dark (Orbitron, red)
("Radar Dark", "Orbitron:wght@400;700;900&family=Inter:wght@300;400;600", """
body{font-family:'Inter',sans-serif;background:#0a0a0f;color:#c8c8d0}
nav{padding:24px 48px;border-bottom:1px solid rgba(233,69,96,0.15);display:flex;justify-content:space-between;align-items:center}
.logo{font-family:'Orbitron',monospace;font-weight:900;font-size:1.2rem;color:#e94560;letter-spacing:4px;text-transform:uppercase}
nav a{color:#666;text-decoration:none;font-size:.85rem}
.tagline-bar{text-align:center;padding:14px;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:#555;border-bottom:1px solid rgba(233,69,96,0.08)}
.hero{min-height:70vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 24px}
.hero h1{font-family:'Orbitron',monospace;font-size:clamp(2.5rem,6vw,5rem);font-weight:900;color:#fff;text-transform:uppercase;letter-spacing:2px;margin-bottom:16px}
.hero h1 span{color:#e94560}
.subtitle{font-size:1.05rem;max-width:700px;line-height:1.8;color:#888;margin-bottom:40px}
.cta-group{display:flex;gap:16px;flex-wrap:wrap;justify-content:center}
.btn-primary{background:#e94560;color:#fff;padding:14px 36px;font-family:'Orbitron',monospace;font-size:.75rem;letter-spacing:3px;text-transform:uppercase;border:none;text-decoration:none;transition:all .3s}
.btn-primary:hover{background:#ff6b81;box-shadow:0 0 30px rgba(233,69,96,0.4)}
.btn-ghost{background:transparent;color:#e94560;padding:14px 36px;font-family:'Orbitron',monospace;font-size:.75rem;letter-spacing:3px;text-transform:uppercase;border:1px solid #e94560;text-decoration:none;transition:all .3s}
.btn-ghost:hover{background:rgba(233,69,96,0.1)}
section{max-width:860px;margin:0 auto;padding:70px 32px}
.section-label{font-family:'Orbitron',monospace;font-size:.65rem;letter-spacing:4px;text-transform:uppercase;color:#e94560;margin-bottom:14px}
h2{font-family:'Orbitron',monospace;font-size:clamp(1.2rem,2.5vw,1.8rem);color:#fff;margin-bottom:20px}
p,li{font-size:.95rem;line-height:1.8;color:#888;margin-bottom:14px}
strong{color:#fff}
.questions{list-style:none;padding:0}.questions li{padding:12px 0;border-bottom:1px solid rgba(233,69,96,0.1);color:#c8c8d0}
.certainty-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.certainty-card{background:rgba(233,69,96,0.03);border:1px solid rgba(233,69,96,0.12);padding:24px;transition:all .3s}
.certainty-card:hover{border-color:#e94560;background:rgba(233,69,96,0.06)}
.certainty-card h3{font-family:'Orbitron',monospace;font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#e94560;margin-bottom:10px}
.certainty-card p{margin-bottom:0;font-size:.9rem}
.full-width{grid-column:span 2}
.steps{counter-reset:step;list-style:none;padding:0}.steps li{counter-increment:step;padding:14px 0;border-bottom:1px solid rgba(233,69,96,0.08)}
.steps li::before{content:counter(step)'.';font-family:'Orbitron',monospace;color:#e94560;font-weight:700;margin-right:12px}
.browsers{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin-top:20px}.browsers span{color:#666;font-size:.85rem}
.teams-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.team-card{border-left:3px solid #e94560;padding:18px 22px;background:rgba(233,69,96,0.02)}
.team-card h3{color:#e94560;font-size:.8rem;font-weight:600;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px}
.team-card p{margin-bottom:0;font-size:.9rem}
.pricing-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.price-card{background:rgba(233,69,96,0.03);border:1px solid rgba(233,69,96,0.12);padding:22px 18px;text-align:center;transition:all .3s}
.price-card:hover{border-color:#e94560}
.price-card h3{font-family:'Orbitron',monospace;font-size:.65rem;letter-spacing:2px;color:#e94560;margin-bottom:8px;text-transform:uppercase}
.price{font-family:'Orbitron',monospace;font-size:1.4rem;color:#fff;margin-bottom:4px}
.price-sub{font-size:.75rem;color:#666}
.price-card p{font-size:.8rem;color:#888;margin:10px 0 0}
.final-cta{text-align:center;padding:80px 32px;border-top:1px solid rgba(233,69,96,0.1);margin-top:40px}
.final-cta h2{margin-bottom:8px}
.final-cta .cta-group{margin-top:24px}
.tagline{color:#e94560;font-family:'Orbitron',monospace;font-size:.75rem;letter-spacing:4px;margin-top:24px;text-transform:uppercase}
footer{text-align:center;padding:40px;border-top:1px solid rgba(233,69,96,0.1);color:#444;font-size:.85rem}
footer a{color:#e94560;text-decoration:none}
@media(max-width:768px){nav{padding:16px 20px}.certainty-grid,.teams-grid{grid-template-columns:1fr}.full-width{grid-column:span 1}.pricing-grid{grid-template-columns:1fr 1fr}}
"""),

# 2 - Clean SaaS (Inter, blue on white)
("Clean SaaS", "Inter:wght@300;400;500;600;700", """
body{font-family:'Inter',sans-serif;background:#fff;color:#334155}
nav{padding:20px 48px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:700;font-size:1.1rem;color:#2563eb}
nav a{color:#2563eb;text-decoration:none;font-size:.85rem}
.tagline-bar{text-align:center;padding:12px;font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#94a3b8;background:#f8fafc;border-bottom:1px solid #e2e8f0}
.hero{min-height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 24px}
.hero h1{font-size:clamp(2.5rem,5vw,4rem);font-weight:700;color:#0f172a;margin-bottom:16px}
.hero h1 span{color:#2563eb}
.subtitle{font-size:1.1rem;max-width:660px;line-height:1.8;color:#64748b;margin-bottom:40px}
.cta-group{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.btn-primary{background:#2563eb;color:#fff;padding:12px 32px;border-radius:8px;font-weight:600;font-size:.9rem;text-decoration:none;transition:all .3s;border:none}
.btn-primary:hover{background:#1d4ed8;box-shadow:0 4px 16px rgba(37,99,235,0.3)}
.btn-ghost{background:#fff;color:#2563eb;padding:12px 32px;border-radius:8px;font-weight:600;font-size:.9rem;text-decoration:none;border:1px solid #bfdbfe;transition:all .3s}
.btn-ghost:hover{background:#eff6ff}
section{max-width:820px;margin:0 auto;padding:64px 32px}
.section-label{font-size:.7rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#2563eb;margin-bottom:12px}
h2{font-size:1.6rem;font-weight:700;color:#0f172a;margin-bottom:20px}
p,li{font-size:.95rem;line-height:1.8;color:#64748b;margin-bottom:14px}
strong{color:#0f172a}
.questions{list-style:none;padding:0}.questions li{padding:14px 0;border-bottom:1px solid #f1f5f9;color:#334155;font-size:1.05rem}
.certainty-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.certainty-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;transition:all .3s}
.certainty-card:hover{border-color:#93c5fd;box-shadow:0 4px 16px rgba(0,0,0,0.04)}
.certainty-card h3{font-size:.8rem;font-weight:600;color:#2563eb;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.certainty-card p{margin-bottom:0;font-size:.9rem}
.full-width{grid-column:span 2}
.steps{counter-reset:step;list-style:none;padding:0}.steps li{counter-increment:step;padding:14px 0;border-bottom:1px solid #f1f5f9}
.steps li::before{content:counter(step)'.';color:#2563eb;font-weight:700;margin-right:12px}
.browsers{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:20px}.browsers span{color:#94a3b8;font-size:.85rem;background:#f1f5f9;padding:4px 12px;border-radius:6px}
.teams-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.team-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:22px}
.team-card h3{color:#2563eb;font-size:.85rem;font-weight:600;margin-bottom:6px}
.team-card p{margin-bottom:0;font-size:.9rem}
.pricing-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.price-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px 16px;text-align:center;transition:all .3s}
.price-card:hover{border-color:#2563eb;box-shadow:0 4px 12px rgba(0,0,0,0.04)}
.price-card h3{font-size:.7rem;font-weight:600;color:#2563eb;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.price{font-size:1.6rem;font-weight:700;color:#0f172a;margin-bottom:4px}
.price-sub{font-size:.75rem;color:#94a3b8}
.price-card p{font-size:.8rem;color:#64748b;margin:10px 0 0}
.final-cta{text-align:center;padding:80px 32px;border-top:1px solid #e2e8f0;margin-top:40px;background:#f8fafc}
.final-cta h2{margin-bottom:8px}
.final-cta .cta-group{margin-top:24px}
.tagline{color:#2563eb;font-size:.8rem;font-weight:600;letter-spacing:3px;margin-top:24px;text-transform:uppercase}
footer{text-align:center;padding:40px;border-top:1px solid #e2e8f0;color:#94a3b8;font-size:.85rem}
footer a{color:#2563eb;text-decoration:none}
@media(max-width:768px){nav{padding:16px 20px}.certainty-grid,.teams-grid{grid-template-columns:1fr}.full-width{grid-column:span 1}.pricing-grid{grid-template-columns:1fr 1fr}}
"""),

# 3 - Dark Enterprise (DM Sans, muted blue-gray)
("Dark Enterprise", "DM+Sans:wght@400;500;600;700", """
body{font-family:'DM Sans',sans-serif;background:#0b0f19;color:#94a3b8}
nav{padding:20px 48px;border-bottom:1px solid #1e293b;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:700;font-size:1.1rem;color:#e2e8f0;letter-spacing:1px}
nav a{color:#64748b;text-decoration:none;font-size:.85rem}
.tagline-bar{text-align:center;padding:12px;font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#475569;border-bottom:1px solid #1e293b}
.hero{min-height:70vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 24px}
.hero h1{font-size:clamp(2.5rem,5.5vw,4.5rem);font-weight:700;color:#f1f5f9;margin-bottom:16px}
.hero h1 span{background:linear-gradient(135deg,#60a5fa,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.subtitle{font-size:1.05rem;max-width:680px;line-height:1.8;color:#64748b;margin-bottom:40px}
.cta-group{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.btn-primary{background:#3b82f6;color:#fff;padding:12px 32px;border-radius:6px;font-weight:600;font-size:.9rem;text-decoration:none;transition:all .3s;border:none}
.btn-primary:hover{background:#2563eb;box-shadow:0 4px 20px rgba(59,130,246,0.3)}
.btn-ghost{background:transparent;color:#94a3b8;padding:12px 32px;border-radius:6px;font-weight:600;font-size:.9rem;text-decoration:none;border:1px solid #334155;transition:all .3s}
.btn-ghost:hover{border-color:#64748b;color:#e2e8f0}
section{max-width:840px;margin:0 auto;padding:64px 32px}
.section-label{font-size:.7rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#60a5fa;margin-bottom:12px}
h2{font-size:1.6rem;font-weight:700;color:#f1f5f9;margin-bottom:20px}
p,li{font-size:.95rem;line-height:1.8;color:#94a3b8;margin-bottom:14px}
strong{color:#e2e8f0}
.questions{list-style:none;padding:0}.questions li{padding:14px 0;border-bottom:1px solid #1e293b;color:#cbd5e1}
.certainty-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.certainty-card{background:rgba(30,41,59,0.5);border:1px solid #1e293b;border-radius:8px;padding:24px;transition:all .3s}
.certainty-card:hover{border-color:#3b82f6}
.certainty-card h3{font-size:.8rem;font-weight:600;color:#60a5fa;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.certainty-card p{margin-bottom:0;font-size:.9rem}
.full-width{grid-column:span 2}
.steps{counter-reset:step;list-style:none;padding:0}.steps li{counter-increment:step;padding:14px 0;border-bottom:1px solid #1e293b}
.steps li::before{content:counter(step)'.';color:#60a5fa;font-weight:700;margin-right:12px}
.browsers{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:20px}.browsers span{color:#64748b;font-size:.85rem;background:#1e293b;padding:4px 12px;border-radius:4px}
.teams-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.team-card{background:rgba(30,41,59,0.5);border:1px solid #1e293b;border-radius:8px;padding:22px}
.team-card h3{color:#60a5fa;font-size:.85rem;font-weight:600;margin-bottom:6px}
.team-card p{margin-bottom:0;font-size:.9rem}
.pricing-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.price-card{background:rgba(30,41,59,0.5);border:1px solid #1e293b;border-radius:8px;padding:22px 16px;text-align:center;transition:all .3s}
.price-card:hover{border-color:#3b82f6}
.price-card h3{font-size:.7rem;font-weight:600;color:#60a5fa;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.price{font-size:1.5rem;font-weight:700;color:#f1f5f9;margin-bottom:4px}
.price-sub{font-size:.75rem;color:#64748b}
.price-card p{font-size:.8rem;color:#94a3b8;margin:10px 0 0}
.final-cta{text-align:center;padding:80px 32px;border-top:1px solid #1e293b;margin-top:40px}
.final-cta h2{margin-bottom:8px}
.final-cta .cta-group{margin-top:24px}
.tagline{color:#60a5fa;font-size:.8rem;font-weight:600;letter-spacing:3px;margin-top:24px;text-transform:uppercase}
footer{text-align:center;padding:40px;border-top:1px solid #1e293b;color:#475569;font-size:.85rem}
footer a{color:#60a5fa;text-decoration:none}
@media(max-width:768px){nav{padding:16px 20px}.certainty-grid,.teams-grid{grid-template-columns:1fr}.full-width{grid-column:span 1}.pricing-grid{grid-template-columns:1fr 1fr}}
"""),
]

# Now define remaining 37 styles more concisely using a generator pattern
def make_style(bg, text, accent, accent2, card_bg, border, font_heading, font_body, radius="8px", heading_transform="", logo_style=""):
    ht = f"text-transform:{heading_transform};" if heading_transform else ""
    ls = f"font-family:'{font_heading}',sans-serif;" if logo_style == "" else logo_style
    return f"""
body{{font-family:'{font_body}',sans-serif;background:{bg};color:{text}}}
nav{{padding:20px 48px;border-bottom:1px solid {border};display:flex;justify-content:space-between;align-items:center}}
.logo{{font-weight:700;font-size:1.1rem;color:{accent};{ls}}}
nav a{{color:{accent};text-decoration:none;font-size:.85rem}}
.tagline-bar{{text-align:center;padding:12px;font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:{text};opacity:.5;border-bottom:1px solid {border}}}
.hero{{min-height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px 24px}}
.hero h1{{font-family:'{font_heading}',sans-serif;font-size:clamp(2.5rem,5vw,4rem);font-weight:700;color:{accent2};margin-bottom:16px;{ht}}}
.hero h1 span{{color:{accent}}}
.subtitle{{font-size:1.05rem;max-width:660px;line-height:1.8;color:{text};margin-bottom:40px}}
.cta-group{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}}
.btn-primary{{background:{accent};color:{bg};padding:12px 32px;border-radius:{radius};font-weight:600;font-size:.9rem;text-decoration:none;transition:all .3s;border:none}}
.btn-primary:hover{{opacity:.85;box-shadow:0 4px 16px {accent}33}}
.btn-ghost{{background:transparent;color:{accent};padding:12px 32px;border-radius:{radius};font-weight:600;font-size:.9rem;text-decoration:none;border:1px solid {accent};transition:all .3s}}
.btn-ghost:hover{{background:{accent}11}}
section{{max-width:840px;margin:0 auto;padding:64px 32px}}
.section-label{{font-size:.7rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{accent};margin-bottom:12px}}
h2{{font-family:'{font_heading}',sans-serif;font-size:1.6rem;font-weight:700;color:{accent2};margin-bottom:20px;{ht}}}
p,li{{font-size:.95rem;line-height:1.8;color:{text};margin-bottom:14px}}
strong{{color:{accent2}}}
.questions{{list-style:none;padding:0}}.questions li{{padding:14px 0;border-bottom:1px solid {border};color:{accent2};font-size:1.05rem}}
.certainty-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}}
.certainty-card{{background:{card_bg};border:1px solid {border};border-radius:{radius};padding:24px;transition:all .3s}}
.certainty-card:hover{{border-color:{accent}}}
.certainty-card h3{{font-size:.8rem;font-weight:600;color:{accent};margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}}
.certainty-card p{{margin-bottom:0;font-size:.9rem}}
.full-width{{grid-column:span 2}}
.steps{{counter-reset:step;list-style:none;padding:0}}.steps li{{counter-increment:step;padding:14px 0;border-bottom:1px solid {border}}}
.steps li::before{{content:counter(step)'.';color:{accent};font-weight:700;margin-right:12px}}
.browsers{{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:20px}}.browsers span{{color:{text};font-size:.85rem}}
.teams-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.team-card{{background:{card_bg};border:1px solid {border};border-radius:{radius};padding:22px}}
.team-card h3{{color:{accent};font-size:.85rem;font-weight:600;margin-bottom:6px}}
.team-card p{{margin-bottom:0;font-size:.9rem}}
.pricing-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}}
.price-card{{background:{card_bg};border:1px solid {border};border-radius:{radius};padding:22px 16px;text-align:center;transition:all .3s}}
.price-card:hover{{border-color:{accent}}}
.price-card h3{{font-size:.7rem;font-weight:600;color:{accent};margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}}
.price{{font-size:1.5rem;font-weight:700;color:{accent2};margin-bottom:4px}}
.price-sub{{font-size:.75rem;color:{text};opacity:.6}}
.price-card p{{font-size:.8rem;color:{text};margin:10px 0 0}}
.launch-notify{{padding:0 32px}}
.notify-box{{max-width:600px;margin:0 auto;text-align:center;background:{card_bg};border:1px solid {accent};border-radius:{radius};padding:40px 32px}}
.notify-box h2{{margin-bottom:8px}}
.notify-box p{{margin-bottom:20px}}
.notify-form{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}
.notify-input{{padding:12px 16px;border:1px solid {border};border-radius:{radius};background:{bg};color:{accent2};font-size:.9rem;min-width:260px;font-family:inherit}}
.notify-input::placeholder{{color:{text};opacity:.5}}
.notify-btn{{cursor:pointer;white-space:nowrap}}
.feature-group-title{{font-size:.95rem;font-weight:600;color:{accent};margin:28px 0 12px;text-transform:uppercase;letter-spacing:1px}}
.feature-list{{list-style:none;padding:0}}.feature-list li{{padding:10px 0;border-bottom:1px solid {border};font-size:.9rem;line-height:1.6}}
.feature-list li::before{{content:"\\2713\\0020";color:{accent};font-weight:700}}
.owasp-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}}
.owasp-note{{margin-top:20px;font-size:.85rem;font-style:italic;opacity:.7}}
.final-cta{{text-align:center;padding:80px 32px;border-top:1px solid {border};margin-top:40px}}
.final-cta h2{{margin-bottom:8px}}
.final-cta .notify-form{{margin-top:24px}}
.tagline{{color:{accent};font-size:.8rem;font-weight:600;letter-spacing:3px;margin-top:24px;text-transform:uppercase}}
footer{{text-align:center;padding:40px;border-top:1px solid {border};color:{text};opacity:.5;font-size:.85rem}}
footer a{{color:{accent};text-decoration:none}}
@media(max-width:768px){{nav{{padding:16px 20px}}.certainty-grid,.teams-grid,.owasp-grid{{grid-template-columns:1fr}}.full-width{{grid-column:span 1}}.pricing-grid{{grid-template-columns:1fr 1fr}}.notify-form{{flex-direction:column}}.notify-input{{min-width:auto;width:100%}}}}
"""

# Define all 40 styles: (name, google_font_query, css)
ALL_STYLES = [
    STYLES[0],  # 1
    STYLES[1],  # 2
    STYLES[2],  # 3
    # 4 - Editorial serif
    ("Editorial Serif", "Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600", make_style("#f9f7f3","#57534e","#b45309","#1c1917","#fff","#e7e5e4","Playfair Display","Source Sans 3","4px")),
    # 5 - Purple gradient
    ("Purple Gradient", "DM+Sans:wght@400;500;700", make_style("#0f0a1a","#a78bfa","#8b5cf6","#f5f3ff","rgba(139,92,246,0.05)","rgba(139,92,246,0.15)","DM Sans","DM Sans","12px")),
    # 6 - Teal minimal
    ("Teal Minimal", "Inter:wght@300;400;600;700", make_style("#f0fdfa","#475569","#0d9488","#0f172a","#fff","#ccfbf1","Inter","Inter","10px")),
    # 7 - Terminal green
    ("Terminal Green", "Share+Tech+Mono&family=Fira+Code:wght@400", make_style("#000","#00cc33","#00ff41","#00ff41","rgba(0,255,65,0.03)","#003300","Share Tech Mono","Share Tech Mono","0px","uppercase")),
    # 8 - Indigo space
    ("Indigo Space", "Outfit:wght@300;400;600;700;800", make_style("#020617","#cbd5e1","#818cf8","#f8fafc","rgba(99,102,241,0.04)","rgba(99,102,241,0.12)","Outfit","Outfit","16px")),
    # 9 - Orange racing
    ("Orange Racing", "Barlow:wght@300;400;600;700;900", make_style("#0c0a09","#a8a29e","#f97316","#fafaf9","#1c1917","#292524","Barlow","Barlow","4px")),
    # 10 - Open source teal (light)
    ("Open Teal", "Literata:wght@400;600;700;900&family=Inter:wght@400;500;600", make_style("#f0fdfa","#334155","#0d9488","#0f172a","#fff","#e2e8f0","Literata","Inter","12px")),
    # 11 - GitHub dark
    ("GitHub Dark", "JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600", make_style("#0d1117","#c9d1d9","#58a6ff","#f0f6fc","#161b22","#30363d","JetBrains Mono","Inter","6px")),
    # 12 - Finance light
    ("Finance Light", "Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700", make_style("#fafafa","#1a1a2e","#4f46e5","#0f172a","#fff","#e5e7eb","Inter","Inter","8px")),
    # 13 - Navy formal
    ("Navy Formal", "Playfair+Display:wght@400;700;900&family=Inter:wght@400;500;600", make_style("#fff","#475569","#1e293b","#0f172a","#f8fafc","#e2e8f0","Playfair Display","Inter","4px")),
    # 14 - Clinical blue
    ("Clinical Blue", "Source+Sans+3:wght@300;400;600;700", make_style("#fafafa","#475569","#0ea5e9","#0f172a","#fff","#e0f2fe","Source Sans 3","Source Sans 3","8px")),
    # 15 - Incident red
    ("Incident Red", "Barlow:wght@400;600;700;900", make_style("#0f0f0f","#a8a29e","#ef4444","#fafaf9","rgba(239,68,68,0.04)","rgba(239,68,68,0.15)","Barlow","Barlow","4px")),
    # 16 - Catalogue teal
    ("Catalogue Teal", "Outfit:wght@300;400;600;700", make_style("#f0fdfa","#475569","#0d9488","#0f172a","#fff","#ccfbf1","Outfit","Outfit","12px")),
    # 17 - Forensic amber
    ("Forensic Amber", "Space+Grotesk:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600", make_style("#111827","#9ca3af","#f59e0b","#f9fafb","rgba(245,158,11,0.04)","rgba(245,158,11,0.15)","Space Grotesk","IBM Plex Sans","6px")),
    # 18 - Blueprint cyan
    ("Blueprint Cyan", "Fira+Code:wght@400;500&family=Inter:wght@400;500;600", make_style("#0c1222","#94a3b8","#22d3ee","#f1f5f9","rgba(34,211,238,0.04)","rgba(34,211,238,0.12)","Fira Code","Inter","4px")),
    # 19 - Executive black
    ("Executive Black", "Outfit:wght@300;400;600;700;800", make_style("#000","#a1a1aa","#fff","#fff","rgba(255,255,255,0.03)","#333","Outfit","Outfit","0px")),
    # 20 - EU regulatory
    ("EU Regulatory", "Libre+Baskerville:wght@400;700&family=Inter:wght@400;500;600", make_style("#fff","#475569","#003399","#1e293b","#f8fafc","#dbeafe","Libre Baskerville","Inter","4px")),
    # 21 - Green architecture
    ("Green Architecture", "IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600", make_style("#0a0e17","#94a3b8","#10b981","#f1f5f9","rgba(16,185,129,0.04)","rgba(16,185,129,0.12)","IBM Plex Mono","IBM Plex Sans","6px")),
    # 22 - SOC red alert
    ("SOC Alert", "JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600", make_style("#0d1117","#c9d1d9","#f85149","#f0f6fc","rgba(248,81,73,0.04)","rgba(248,81,73,0.12)","JetBrains Mono","Inter","6px")),
    # 23 - Team colours
    ("Team Colours", "DM+Sans:wght@400;500;600;700", make_style("#fafafa","#475569","#7c3aed","#1e293b","#fff","#e2e8f0","DM Sans","DM Sans","12px")),
    # 24 - Monitor cyan
    ("Monitor Cyan", "Fira+Code:wght@400;500&family=Inter:wght@400;500;600", make_style("#111827","#94a3b8","#06b6d4","#f1f5f9","rgba(6,182,212,0.04)","rgba(6,182,212,0.12)","Fira Code","Inter","6px")),
    # 25 - Violet identity
    ("Violet Identity", "Space+Grotesk:wght@400;600;700", make_style("#0f172a","#a78bfa","#8b5cf6","#f5f3ff","rgba(139,92,246,0.04)","rgba(139,92,246,0.12)","Space Grotesk","Space Grotesk","8px")),
    # 26 - Cloud orange
    ("Cloud Orange", "Barlow:wght@400;600;700", make_style("#1a0a00","#d6d3d1","#f97316","#fafaf9","rgba(249,115,22,0.04)","rgba(249,115,22,0.12)","Barlow","Barlow","6px")),
    # 27 - Audit formal
    ("Audit Formal", "Lora:wght@400;600;700&family=Inter:wght@400;500;600", make_style("#fff","#475569","#1e293b","#0f172a","#f8fafc","#e2e8f0","Lora","Inter","4px")),
    # 28 - Attack surface red
    ("Attack Surface", "Share+Tech+Mono&family=Inter:wght@400;500;600", make_style("#0a0a0a","#a8a29e","#dc2626","#fafaf9","rgba(220,38,38,0.04)","rgba(220,38,38,0.12)","Share Tech Mono","Inter","4px")),
    # 29 - Budget amber (light)
    ("Budget Amber", "Inter:wght@300;400;500;600;700", make_style("#f8fafc","#475569","#d97706","#1c1917","#fff","#fde68a","Inter","Inter","10px")),
    # 30 - Honest monochrome
    ("Honest Monochrome", "Inter:wght@400;500;600;700", make_style("#fff","#555","#000","#000","#fafafa","#ddd","Inter","Inter","0px")),
    # 31 - Stripe clean
    ("Stripe Clean", "Inter:wght@300;400;500;600;700", make_style("#fff","#425466","#635bff","#0a2540","#f6f9fc","#e3e8ee","Inter","Inter","8px")),
    # 32 - Vercel dark
    ("Vercel Dark", "Inter:wght@300;400;500;600;700", make_style("#000","#888","#fff","#fafafa","#111","#333","Inter","Inter","8px")),
    # 33 - Notion editorial
    ("Notion Editorial", "Georgia,serif&family=Inter:wght@400;500;600", make_style("#fff","#37352f","#37352f","#37352f","#f7f6f3","#e9e5e0","Georgia","Inter","3px")),
    # 34 - Warm terracotta
    ("Warm Terracotta", "Libre+Baskerville:wght@400;700&family=Inter:wght@400;500;600", make_style("#faf8f5","#57534e","#c2410c","#1c1917","#fff","#e7e5e4","Libre Baskerville","Inter","6px")),
    # 35 - Brutalist mono
    ("Brutalist Mono", "Space+Grotesk:wght@400;600;700", make_style("#fff","#111","#111","#000","#f5f5f5","#000","Space Grotesk","Space Grotesk","0px","uppercase")),
    # 36 - Gradient mesh
    ("Gradient Mesh", "Syne:wght@400;600;700;800", make_style("#0a0a0f","#cbd5e1","#a78bfa","#f8fafc","rgba(167,139,250,0.04)","rgba(167,139,250,0.12)","Syne","Syne","16px")),
    # 37 - Docs style
    ("Documentation", "JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600", make_style("#fff","#334155","#0369a1","#0f172a","#f8fafc","#e2e8f0","Inter","Inter","6px")),
    # 38 - Warm cream
    ("Warm Cream", "Libre+Baskerville:wght@400;700&family=Inter:wght@400;500;600", make_style("#faf8f5","#57534e","#92400e","#292524","#fff","#e7e5e4","Libre Baskerville","Inter","6px")),
    # 39 - Split navy
    ("Split Navy", "DM+Sans:wght@400;500;600;700", make_style("#fff","#475569","#1e40af","#0f172a","#f8fafc","#dbeafe","DM Sans","DM Sans","8px")),
    # 40 - Glass dark
    ("Glassmorphism", "Inter:wght@300;400;500;600;700", make_style("#0f172a","#cbd5e1","#60a5fa","#f1f5f9","rgba(255,255,255,0.05)","rgba(255,255,255,0.1)","Inter","Inter","16px")),
]

SHARED_CSS = """
.launch-notify{padding:0 32px}
.notify-box{max-width:600px;margin:0 auto;text-align:center;padding:40px 32px;border-radius:8px}
.notify-form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.notify-input{padding:12px 16px;border-radius:6px;font-size:.9rem;min-width:260px;font-family:inherit;outline:none}
.notify-input:focus{outline:2px solid currentColor}
.notify-btn{cursor:pointer;white-space:nowrap}
.feature-group-title{font-size:.95rem;font-weight:600;margin:28px 0 12px;text-transform:uppercase;letter-spacing:1px}
.feature-list{list-style:none;padding:0}.feature-list li{padding:10px 0;font-size:.9rem;line-height:1.6}
.owasp-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.owasp-note{margin-top:20px;font-size:.85rem;font-style:italic;opacity:.7}
.final-cta .notify-form{margin-top:24px}
.email-section{display:flex;justify-content:center;padding:40px 32px}
.email-wrap{position:relative;max-width:560px;width:100%}
.email-stamp{position:absolute;bottom:28px;right:28px;border:2px solid rgba(200,16,46,0.55);color:rgba(200,16,46,0.55);font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;padding:5px 10px;transform:rotate(-14deg);font-family:monospace;pointer-events:none;z-index:10}
.email-card{width:100%;background:#fff;border-radius:8px;overflow:hidden;border:1px solid #e0ddd8;transform:rotate(1deg)}
.email-chrome{background:#f5f5f5;border-bottom:1px solid #e0ddd8;padding:10px 16px;display:flex;align-items:center;gap:8px}
.edot{width:10px;height:10px;border-radius:50%}
.edot.r{background:#ff5f57}.edot.y{background:#ffbd2e}.edot.g{background:#28c840}
.email-fields{padding:16px 20px 12px;border-bottom:1px solid #f0f0f0;font-size:13px;line-height:2;color:#888}
.email-fields strong{color:#222;font-weight:500}
.email-subject{padding:12px 20px;border-bottom:1px solid #f0f0f0;font-size:15px;font-weight:600;color:#111}
.email-body{padding:20px;font-size:14px;line-height:1.7;color:#222}
.email-greeting{margin-bottom:16px;color:#555}
.email-body p{padding:7px 0;border-bottom:1px solid #f5f5f5;color:#222}
.email-body p:last-of-type{border-bottom:none;font-weight:600;font-size:15px;color:#111;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:2px;text-decoration-color:#c8102e;padding-top:12px}
.email-signoff{margin-top:20px;color:#888;font-size:13px;line-height:1.8}
.email-signoff strong{color:#222;font-weight:500}
@media(max-width:768px){.owasp-grid{grid-template-columns:1fr}.notify-form{flex-direction:column}.notify-input{min-width:auto;width:100%}}
"""

def generate_page(num, name, font_query, css):
    # Clean up font query for google fonts URL
    font_url = f"https://fonts.googleapis.com/css2?family={font_query}&display=swap"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PowerGrabber — LLM Certainty ({name})</title>
<style>
@import url('{font_url}');
*{{margin:0;padding:0;box-sizing:border-box}}
{css}
{SHARED_CSS}
</style>
</head>
<body>
{CONTENT}
</body>
</html>"""

    filepath = f"page{num}.html"
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"  Generated {filepath} — {name}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Generating {len(ALL_STYLES)} pages...")
    for i, (name, font, css) in enumerate(ALL_STYLES, 1):
        generate_page(i, name, font, css)
    print(f"\nDone. {len(ALL_STYLES)} pages generated.")
