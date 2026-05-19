---
name: "Tech Watch Output"
description: "Actionable digests: what changed, why it matters, what to try."

applyTo: "**"
---

# Tech Watch Output

## Core principles

- Always prefer primary sources: official release notes, docs, RFCs, papers — not aggregator blogs.

- Every digest must answer three questions: **What changed?** → **Why does it matter?** → **What should we try?**

- Propose 1–3 concrete, time-boxed experiments (spike, benchmark, PoC) — never vague "explore this".

- Flag breaking changes, deprecations, and security advisories explicitly with a severity tag (`⚠️ Breaking`, `🔒 Security`, `📦 Deprecation`).

## Digest format

Use this structure for every tech-watch output:

```text
## [Topic] — [Version / Date]

**Source**: [URL to official release notes or changelog]

**What changed**: [2–4 sentence factual summary of the change]

**Why it matters**: [impact on our stack, DX, performance, security, or cost]

**Experiments to try**:
1. `<exact command or PoC description>` — expected outcome in ≤1 day
2. (optional) `<benchmark or integration test>` — expected outcome in ≤3 days

**Action**: [None / Monitor / Spike / Adopt / Migrate]
**Effort**: [XS / S / M / L]
**Deadline**: [date or "next sprint"]
```

## Source quality tiers

Prioritize sources in this order:

1. **Official** — GitHub releases, vendor changelogs, RFC/spec documents, CVE advisories

2. **Community authoritative** — project maintainer blog posts, conference talks with slides

3. **Secondary** — curated newsletters (e.g. TLDR, Changelog, This Week in Rust)

4. **Avoid** — anonymous aggregators, paywalled summaries without original citations

## Relevance filter

Before including an item, confirm at least one is true:

- [ ] Directly affects a technology in the current stack

- [ ] Changes a security posture or dependency risk

- [ ] Offers a measurable performance or cost improvement

- [ ] Introduces a pattern that replaces a current pain point

Discard items that are "interesting but not actionable within 90 days".

Example: well-formed digest entry
---

```text
## .NET 10 Preview 2 — 2026-02-18

**Source**: https://devblogs.microsoft.com/dotnet/dotnet-10-preview-2/

**What changed**: `Task.WhenEach` is now available in .NET 10, enabling async
iteration over tasks as they complete rather than waiting for all to finish.

**Why it matters**: Eliminates the `Task.WhenAny` loop anti-pattern in our
order-processing pipeline, reducing complexity and improving partial-failure
handling.

**Experiments to try**:
1. Replace the `Task.WhenAny` loop in `OrderDispatcher.cs` with `WhenEach` on
   a feature branch — verify behaviour parity with existing integration tests.

**Action**: Adopt (when .NET 10 GA)
**Effort**: S
**Deadline**: Q3 2026
```

---

## 🏆 Elite Section — Top 5% Tech Watch Practices

- **Maintain a living radar**: Keep a `docs/tech-radar.md` (or use Thoughtworks Radar format) with four quadrants (Adopt / Trial / Assess / Hold). Every digest item maps to a quadrant entry. Review quarterly.

- **Link watch items to backlog**: Every item with `Action: Spike` or `Action: Adopt` must have a corresponding GitHub issue created within 48 hours of the digest. No floating action items.

- **Measure adoption outcomes**: When a trialed technology is adopted, record the actual outcome vs. the expected benefit stated in the digest. Use this to calibrate future recommendations.

- **Automated feed monitoring**: Use GitHub's dependency graph + Dependabot alerts, RSS feeds for key project releases, and `nvd.nist.gov` CVE feeds — automate the ingestion so watch effort focuses on analysis, not collection.

- **Security-first triage**: CVE advisories for direct or transitive dependencies must be triaged within 24 hours of publication regardless of the normal watch cadence. Assign a severity (Critical/High/Medium/Low) and a remediation deadline immediately.

- **Cross-pollinate across domains**: The highest-value tech-watch insights come from adjacent fields (e.g. applying distributed systems patterns from the database world to frontend state management). Deliberately include one out-of-domain item per digest cycle.
