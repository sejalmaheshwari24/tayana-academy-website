#!/usr/bin/env python3
"""Week-by-week syllabi for the four Orion career tracks.

Written to the final course model (Sep 2026): every week maps to capabilities and
tools declared on that track's infographic, every week ends with something shipped,
each track carries a mid-cohort capstone before demo day.

Voice rules (CLAUDE.md): institutional, "you", concrete, no hype, no emoji,
middot separators, sentence case in body copy.

Re-runnable: replaces the block fenced by <!-- SYLLABUS --> on each track page.
"""
import re, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (week label, title, intro, [bullets], ships, is_capstone)
SYLLABI = {
'track-no-code-agent-engineer.html': dict(weeks=4, phases=[
 ('Week 1','Use cases, mapped and scored',
  'You start with the work, not the tool. Map a process your team runs every week, then score where AI actually pays.',
  ['The operator\'s model landscape — where ChatGPT, Claude and Gemini each earn their place',
   'Prompt patterns that survive real use: role, context, constraints, output format, examples',
   'Business process mapping — every step, handoff and decision written down',
   'Use-case scoring by time cost, error rate and volume'],
  'A mapped process and a scored shortlist, with one use case chosen alongside your mentor.', False),
 ('Week 2','Your first workflow, live',
  'Connect the tools your team already runs and put a real automation into production.',
  ['No-code APIs without code — triggers, actions, webhooks and authentication',
   'Choosing your platform: n8n, Make or Zapier, matched to your stack',
   'Airtable and Notion AI as the data spine underneath the workflow',
   'Testing with real data before anyone depends on it'],
  'One automated workflow running on a schedule, against live data.', False),
 ('Capstone','Mid-cohort review',
  'Your working agent goes in front of a mentor who ships automation for a living.',
  ['A walkthrough of what you built and why',
   'Failure-mode review — what happens on bad input, timeouts and duplicates',
   'A written improvement plan you carry into weeks 3 and 4'],
  'A reviewed agent and a plan to harden it.', True),
 ('Week 3','Agents that decide',
  'Move from linear automations to agents that branch, recover and know when to ask a human.',
  ['Visual agent building in Flowise and Langflow',
   'Multi-step logic — branching, retries and fallbacks',
   'Human-in-the-loop checkpoints for the decisions that need judgment',
   'Guardrails: cost limits, rate limits and safe defaults'],
  'A multi-step agent handling a real business intent, with a human checkpoint.', False),
 ('Week 4','Harden, document, hand over',
  'Make it something your team can run without you in the room. Then present it.',
  ['Edge cases, monitoring and alerting',
   'Documentation and handover so an operator can maintain it',
   'Your own AI productivity system across the tools you now run',
   'Demo day — present to mentors and hiring partners'],
  'A production agent, a handover pack and a demo-day presentation.', False),
]),

'track-pro-code-agent-engineer.html': dict(weeks=6, phases=[
 ('Week 1','Python, OOP and the engineering baseline',
  'Set the foundation the rest of the cohort is built on — properly structured code, versioned from day one.',
  ['Environment and project structure — VS Code, Git and GitHub, virtual environments',
   'Object-oriented design for agent systems: interfaces, composition, dependency injection',
   'LLM fundamentals — tokens, context windows and cost',
   'Structured output: typed, validated responses instead of parsed strings'],
  'A scaffolded repository and your first validated, typed LLM call.', False),
 ('Week 2','Tool calling and function execution',
  'An agent is only useful when it can act. This week it starts doing real work.',
  ['LangChain chains, tools and memory',
   'Designing tool schemas — arguments, validation and error paths',
   'Exploring and integrating a third-party API with Postman',
   'Retries, timeouts and graceful failure'],
  'An agent completing a real task through two or more tools.', False),
 ('Week 3','Multi-agent systems',
  'Move from one agent to a system of them — with roles, routing and recovery.',
  ['CrewAI — roles, tasks and delegation',
   'LangGraph — state machines, branching and recovery paths',
   'Orchestration patterns: supervisor, sequential and parallel',
   'Passing state safely between agents'],
  'A multi-agent workflow handling a business intent end to end.', False),
 ('Capstone','Mid-cohort review',
  'Your system is read as code and run as a product, by an engineer who does this in production.',
  ['Architecture and code review against production standards',
   'Adversarial run-through — bad inputs, loops, partial failures',
   'A prioritised hardening plan for weeks 4 to 6'],
  'A reviewed multi-agent system and a hardening plan.', True),
 ('Week 4','MCP and backend integration',
  'Connect your agents to the systems a business actually runs on.',
  ['Model Context Protocol — servers, resources and tools',
   'FastAPI: exposing agents as services with auth, rate limits and streaming',
   'Secrets, permissions and least-privilege access to internal systems',
   'Integration testing against a real backend'],
  'Your agent exposed as an API and reaching a real system through MCP.', False),
 ('Week 5','Evals, guardrails and observability',
  'Measure the thing before you trust it. This is what separates a demo from a deployment.',
  ['Building an eval harness and a regression suite',
   'Guardrails — input validation, output filters, cost and loop ceilings',
   'Tracing and structured logging across multi-agent runs',
   'Release gates: what must pass before anything ships'],
  'An eval suite your system has to pass before release.', False),
 ('Week 6','Deploy and demo day',
  'Ship it, prove the numbers, and present it to the room.',
  ['Containerising the service with Docker — environments and secrets',
   'Deployment, rollback and cost management',
   'Runbook and handover documentation',
   'Demo day — present to mentors and hiring partners'],
  'A deployed multi-agent system with its eval report and runbook.', False),
]),

'track-ai-engineer.html': dict(weeks=6, phases=[
 ('Week 1','AI product architecture and the frontier',
  'Decide what belongs in the model, the application and the database — before writing the product.',
  ['The model landscape: frontier and open-weight, LLM against SLM, cost and latency trade-offs',
   'Architecting an AI product — boundaries, state and failure behaviour',
   'Scaffolding with Next.js, Node.js or FastAPI, and a PostgreSQL schema',
   'Grounding your first response in real data'],
  'A running application shell returning its first grounded LLM response.', False),
 ('Week 2','Retrieval-augmented generation on private data',
  'The core of most AI products in production: answers grounded in your own corpus, with citations.',
  ['Chunking strategies and embedding choices',
   'Pinecone — indexes, namespaces and metadata filters',
   'Hybrid search and re-ranking for answers you can defend',
   'Citations, grounding and answering "I don\'t know" honestly'],
  'A RAG pipeline answering questions on your own data, with citations.', False),
 ('Week 3','Agents and tool use inside the product',
  'Retrieval alone is not a product. This week the interface and the intelligence meet.',
  ['LangChain tools operating inside a full-stack application',
   'Streaming responses, optimistic UI and error states in React',
   'Session and conversation state in PostgreSQL',
   'The product loop: input, retrieval, action, response'],
  'Your product\'s core loop, working end to end.', False),
 ('Capstone','Mid-cohort review',
  'Your product is used, not described — a mentor runs it the way a user would.',
  ['Live walkthrough and architecture review',
   'Usability and failure review under real inputs',
   'A prioritised plan for evaluation, deployment and hardening'],
  'A reviewed product loop and a plan to production.', True),
 ('Week 4','Model evaluation and red-teaming',
  'Know what your system gets wrong, and how it can be misused, before your users find out.',
  ['Building an eval set — offline and online evaluation',
   'Red-teaming: prompt injection, data leakage and jailbreaks',
   'Regression gates on every change',
   'Measuring quality against a baseline you can publish'],
  'An eval harness and a documented security pass on your product.', False),
 ('Week 5','Deploy and observe',
  'From working locally to running for other people, at a cost you can defend.',
  ['Docker, environments and secrets management',
   'Latency, caching and cost control — moving to an SLM where it pays',
   'Observability: tracing, logging and user feedback capture',
   'Rate limits, abuse handling and graceful degradation'],
  'Your product deployed, instrumented and measured.', False),
 ('Week 6','Production hardening and demo day',
  'Close the gaps, write it up, and present the system to the room.',
  ['Load behaviour and failure modes under pressure',
   'Architecture write-up and runbook',
   'Portfolio packaging — what a hiring team needs to see',
   'Demo day — present to mentors and hiring partners'],
  'A deployed AI product with its architecture write-up.', False),
]),

'track-ml-engineer.html': dict(weeks=6, phases=[
 ('Week 1','Problem framing, statistics and data pipelines',
  'Most model failures are framing failures. You start by defining what "good" means and building a set you can trust.',
  ['Framing: what to predict, what to optimise, and the baseline to beat',
   'NumPy and Pandas — cleaning, joins and the leakage traps that invalidate results',
   'Statistics that matter in practice: distributions, sampling and significance',
   'Splitting data honestly — train, validation and test'],
  'A clean, documented training set and a stated success metric.', False),
 ('Week 2','Feature engineering and classical machine learning',
  'Beat a sensible baseline with methods you can explain, before reaching for anything deeper.',
  ['Scikit-learn pipelines, cross-validation and hyperparameter search',
   'Feature engineering — encoding, scaling and selection',
   'Choosing the metric that matches the business question',
   'Reading a confusion matrix like an operator, not a statistician'],
  'A trained baseline model that beats a naive benchmark, with results you can defend.', False),
 ('Week 3','Deep learning across vision and language',
  'Apply deep learning where it earns its cost — and learn to tell when it does not.',
  ['Training loops and transfer learning in TensorFlow or PyTorch',
   'Computer vision task patterns — classification, detection, segmentation',
   'Natural language processing with Hugging Face models',
   'Error analysis: when to fix the data instead of the architecture'],
  'A trained deep-learning model with a documented error analysis.', False),
 ('Capstone','Mid-cohort review',
  'Your model is reviewed against the brief you wrote in week 1 — including whether it should exist.',
  ['Results review against the stated success metric',
   'Data, leakage and reproducibility audit',
   'A prioritised plan for tracking, serving and monitoring'],
  'A reviewed model and a plan to production.', True),
 ('Week 4','Experiment tracking and model management',
  'Make every result reproducible and every model accountable.',
  ['MLflow — runs, parameters, artifacts and the model registry',
   'Versioning data alongside models',
   'Comparing experiments honestly',
   'Model cards: documenting intended use and known limits'],
  'Your experiments tracked and your best model registered with a model card.', False),
 ('Week 5','Serving and MLOps',
  'A model that nothing can call is not a system. This week it goes behind an endpoint.',
  ['Containerising with Docker for reproducible serving',
   'Batch and real-time serving paths',
   'Monitoring drift, data quality and performance decay',
   'Retraining loops and rollback'],
  'Your model served behind an endpoint, with monitoring in place.', False),
 ('Week 6','End-to-end system and demo day',
  'Prove the whole pipeline holds, from raw data to a monitored prediction.',
  ['Cost, scale and failure modes end to end',
   'Portfolio packaging — what a hiring team needs to see',
   'Runbook and handover documentation',
   'Demo day — present to mentors and hiring partners'],
  'An end-to-end ML system with its model card and runbook.', False),
]),
}

CHEV = ('<svg class="acc-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>')

def build(track):
    d = SYLLABI[track]
    items = []
    for i, (wk, title, intro, bullets, ships, cap) in enumerate(d['phases']):
        cls = 'acc-item' if i == 0 else 'acc-item collapsed'
        if cap: cls += ' syl-cap'
        blist = ''.join(f'<li>{b}</li>' for b in bullets)
        items.append(
          f'<div class="{cls}"><button class="acc-q"><span class="syl-wk">{wk}</span>{title}{CHEV}</button>'
          f'<div class="acc-body"><p>{intro}</p><ul class="syl-list">{blist}</ul>'
          f'<p class="syl-ships"><b>You ship:</b> {ships}</p></div></div>')
    accordions = '\n        '.join(items)

    rows = [(wk if wk != 'Capstone' else 'Mid-cohort review', title)
            for wk, title, *_ in d['phases']]
    n = len(rows)
    bars = []
    for i, (wk, title) in enumerate(rows):
        left = round(i * 100 / n); right = round(100 - (i + 1) * 100 / n)
        cls = ' final' if i == n - 1 else (' brass' if 'review' in wk.lower() else '')
        bars.append(f'<tr><td>{title}</td><td colspan="{d["weeks"]}">'
                    f'<span class="gantt-bar{cls}" style="left:{max(left,1)}%;right:{max(right,1)}%"></span></td></tr>')
    ths = ''.join(f'<th>W{i+1}</th>' for i in range(d['weeks']))

    return f'''<!-- SYLLABUS -->
<section class="section" id="curriculum" style="background:var(--paper)">
  <div class="wrap">
    <p class="eyebrow">The curriculum</p>
    <h2 class="section-q">Week by week, <span class="em">project-first.</span></h2>
    <p class="section-lede">Every week ends with something shipped and reviewed. There is a mid-cohort capstone before demo day, so nothing reaches the final week untested.</p>
    <div class="road-grid" style="margin-top:40px;align-items:start">
      <div>
        {accordions}
      </div>
      <div class="gantt-wrap reveal">
        <div class="gantt">
          <div class="gantt-head"><h3>{d['weeks']} weeks at a glance</h3><p>Live cohort · 24 seats · reviewed weekly by working operators.</p></div>
          <table class="gantt-table">
            <thead><tr><th>Phase</th>{ths}</tr></thead>
            <tbody>
              {chr(10).join('              ' + b for b in bars).strip()}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- /SYLLABUS -->'''

if __name__ == '__main__':
    for track in SYLLABI:
        p = os.path.join(SITE, track)
        s = open(p, encoding='utf-8').read()
        block = build(track)
        fence = re.compile(r'<!-- SYLLABUS -->.*?<!-- /SYLLABUS -->', re.S)
        if fence.search(s):
            s = fence.sub(block, s, count=1)
        else:
            # replace the original template curriculum section
            old = re.search(r'<section class="section"[^>]*>\s*<div class="wrap">\s*'
                            r'<p class="eyebrow">The curriculum</p>.*?</section>', s, re.S)
            if not old: raise SystemExit(f'curriculum section not found in {track}')
            s = s[:old.start()] + block + s[old.end():]
        open(p, 'w', encoding='utf-8').write(s)
        print(f'✓ {track} — {len(SYLLABI[track]["phases"])} phases')
    print('\nsyllabi written')
