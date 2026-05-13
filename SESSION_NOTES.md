# Session Notes

**Purpose:** Append-only chronological record of the *reasoning* behind decisions made during chat sessions. This is distinct from `CURRENT_STATE.md`, which captures the *what*; this file captures the *why*.

**Format:** Each session adds entries at the bottom, dated. **Never edit prior entries.** If a decision is reversed, write a new entry explaining the reversal — the original entry stays.

**Pruning:** Every 2-3 weeks, durable entries stay; superseded ones get moved to `session-notes-archive/YYYY-MM.md`. The pruning itself is a session, with its own entry.

**Read this file at the start of every chat session.** It is the thing that prevents drift, re-litigation, and forgotten reasoning.

---

## 2026-05-13 — Scaffolding session (Claude session 1)

### What was built

The complete initial repository scaffold:
- 7 root-level files (README, START_HERE, CONTRIBUTING, CHANGELOG, PROJECT_CONTEXT, CURRENT_STATE, DESIGN_PHASE_CHARTER)
- 3 foundational ADRs (0001 reference models, 0002 three-stage lifecycle, 0003 pipeline-as-platform)
- ADR + RFC templates and process READMEs
- Spec template with 11 sections including the sister-specifications discipline at section 4
- 8 specification folder READMEs (placeholders)
- Document register (YAML, machine-readable)
- SME panel composition + three-round review protocols
- 5 SME prompt primers (ChatGPT, Grok, DeepSeek, Mistral, Claude fresh-eyes)
- Diagrams, glossary, archive READMEs
- PR template

### Key reasoning that won't be obvious from the committed files

**On the spec template's sister specifications section (section 4):**
This was added late in the scaffolding session because Mike correctly identified that passive dependency lists weren't strong enough — each spec needs to actively name the documents that *together* constitute the full blueprint for its subject. The discipline is **bidirectional**: if Spec A lists Spec B as a sister, Spec B must list Spec A. This bidirectionality is checked at every review round. Future sessions should not weaken this to a simple list.

**On topic-based vs audience-based sister structure:**
Considered both. Chose topic-based as the primary structure with audience-based reading guidance layered on top. Reason: topic-based maintains structural integrity (one canonical sister set per spec), while audience-based reading guidance gives readers practical help. **Do not re-litigate this** unless it demonstrably fails in practice.

**On the SME panel composition:**
Mike has 35 years of banking architecture experience and is the human bank-side SME — he is the panel's bank fitness-for-purpose check. AI SMEs are positioned as "well-read amateurs" not domain specialists, and the panel docs are explicit about this. **Do not propose adding more bank-side AI SMEs** thinking they will compensate for banking expertise — they won't.

**On Mistral Le Chat as regulatory reviewer:**
Chosen for EU regulatory grounding. Paired with Perplexity Pro as a separate "currency check" research tool (not a panel member). This pairing is deliberate — Mistral reviews, Perplexity verifies what's currently in force. Don't conflate them.

**On the START_HERE.md map:**
Three sections: by reader type, by progression, by question. Has a deliberate note at the bottom that "if this map grows substantially longer than it is now, the repo structure has become harder to navigate, not easier." Future sessions should respect this — if you find yourself wanting to extend START_HERE.md heavily, fix the structure instead.

**On what is deferred to later sessions:**
- Strategic questions on **target market segment** (ADR-0004) and **data strategy** (ADR-0005) — deferred to Month 2, alongside Product Definition drafting. These need offline thinking time, not in-chat decisions.
- **Rationalisation map** of existing ArcaAI documents (v0.6 architecture, ML Pipeline, Engineering Blueprint, exec deck v12) — needs Mike to share the docs in a focused session.
- **GitHub Actions release workflow** — manual release process documented in CONTRIBUTING.md for now; automated workflow is a Month 2-3 deliverable.

### Settled decisions — do NOT re-open

These are ratified (either as ADRs or by structural decision during scaffolding). A future Claude session should not re-argue these:

1. **Reference models, not production models** (ADR-0001) — non-negotiable language
2. **Three-stage model lifecycle** (ADR-0002) — Reference / Upskilling / Continuous Improvement
3. **Pipeline-as-platform** (ADR-0003) — not models-as-artefacts
4. **Eight canonical specifications** with the names and roles in `specs/README.md`
5. **Three-round SME review process** documented in `governance/review-protocols.md`
6. **Bidirectional sister specifications discipline** in section 4 of every spec
7. **Topic-based sister structure** with audience-based reading guidance layered on top
8. **Repo as source of truth; chats as transient computation** — the foundational continuity principle

If a future session sees what looks like a flaw in any of these, it should write an RFC, not a unilateral change. Mike has the final say.

### Continuity-risk mitigations agreed in this session

See `SESSION_PROTOCOLS.md` (new in this commit). The protocols are:

1. **Session Closure Protocol** — every session ends with commit, CURRENT_STATE update, SESSION_NOTES entry, named next action
2. **Session Opening Protocol** — every session starts with reading the orienting documents and stating back the task
3. **Chat health check** — Claude flags when context window approaches 70%; clean handover beats mid-stride exhaustion
4. **Claude Project setup** — Mike to create a Project in Claude.ai with the scaffold's stable files attached as project knowledge

### Next concrete action

Mike:
1. Read the scaffold (especially START_HERE, CHARTER, ADRs, spec template)
2. Push to private GitHub at `github.com/<handle>/arcaai`
3. Set up Claude Project with stable files attached
4. Open next chat with the Session Opening Protocol

After that, next substantive work is the **rationalisation map** of existing ArcaAI documents — Mike shares the docs, Claude produces the map showing what migrates from where into the new spec set.

### What I (this Claude session) would say to my successor

You inherit a project that has just been carefully scaffolded. The structure is deliberate; the reasoning is partly in this file and partly in the ADRs. Trust the structure. Push back on Mike where you think he's wrong — that's the working relationship he's set up — but don't push back on the structural decisions in section "Settled decisions" without an RFC. Mike's banking depth is real (35 years, Imperial AI grad); your job is to challenge him on AI specifics where his background may not be current, not to defer.

The work is 4-6 months for v1.0 of the Implementation Pack. We are at hour zero. Keep the discipline; the discipline is what makes this work.
