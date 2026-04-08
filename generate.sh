#!/bin/bash
# Generate all 40 pages with the same content, different styles
# Usage: bash generate.sh

CONTENT='<nav><div class="logo">PowerGrabber</div><a href="index.html">&larr; All Designs</a></nav>
<div class="tagline-bar">LLM Security &middot; LLM Visibility &middot; LLM Observability &middot; LLM Compliance &middot; LLM Monitoring &middot; LLM Capture</div>

<section class="hero">
<h1>LLM <span>Certainty.</span></h1>
<p class="subtitle">PowerGrabber is a monitoring application for macOS, Windows, and Linux. PowerGrabber captures LLM traffic in two ways: via browser extension for browser-based AI usage such as ChatGPT, Gemini, and Claude, and directly at the API for AI applications such as Claude Code &mdash; logging everything as structured, compliance-ready data.</p>
<div class="cta-group">
<a href="#" class="btn-primary">Download Free</a>
<a href="#" class="btn-ghost">Talk to us about Enterprise</a>
</div>
</section>

<section>
<div class="section-label">The Questions</div>
<ul class="questions">
<li>Who in our organisation is using AI tools &mdash; and which ones?</li>
<li>What are they putting in?</li>
<li>Are our secrets leaving the company?</li>
<li>How much are we spending on AI &mdash; and who is spending it?</li>
<li>Are we legal?</li>
<li>Are we compliant?</li>
<li>Are we secure?</li>
<li>Do we have records?</li>
</ul>
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
<h2>Download PowerGrabber &mdash; Free</h2>
<div class="cta-group">
<a href="#" class="btn-primary">Download Free</a>
<a href="#" class="btn-ghost">Talk to us about Enterprise</a>
</div>
<div class="tagline">PowerGrabber. LLM Certainty.</div>
</div>

<footer><a href="index.html">&larr; Back to all designs</a></footer>'

echo "Generating pages..."
echo "Content template ready."
