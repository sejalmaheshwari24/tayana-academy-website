#!/usr/bin/env python3
"""Inject the final Orion role model into the four track pages.

Content source: the four course infographics (Sep 2026), transcribed into TRACKS below.
Re-runnable: each generated block is fenced with <!-- ROLE:… --> markers and replaced in place.
"""
import re, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- small inline icon set, keyed by keyword found in the label -------------
ICON = {
 'code':   '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/>',
 'brain':  '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M8 10h8"/>',
 'net':    '<circle cx="6" cy="7" r="2.5"/><circle cx="18" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 9l3.5 6.5M16.5 9L13 15.5"/>',
 'cloud':  '<path d="M6 18h11a4 4 0 000-8 6 6 0 00-11.7 1.8A3.5 3.5 0 006 18z"/>',
 'chart':  '<path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/>',
 'doc':    '<path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9z"/><path d="M14 3v6h6"/>',
 'gear':   '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
 'shield': '<path d="M12 3l8 3.5v5c0 4.5-3.4 8.6-8 9.5-4.6-.9-8-5-8-9.5v-5z"/>',
 'db':     '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
 'bot':    '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4"/><circle cx="9" cy="14" r="1.2"/><circle cx="15" cy="14" r="1.2"/>',
 'eye':    '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'zap':    '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
}
KEYMAP = [
 ('python','code'),('programming','code'),('oop','code'),('object-orient','code'),
 ('api','net'),('backend','db'),('database','db'),('vector','db'),('postgres','db'),('sql','db'),
 ('agent','bot'),('multi-agent','net'),('mcp','net'),('context protocol','net'),('tool calling','gear'),
 ('llm','brain'),('slm','brain'),('machine learning','brain'),('deep learning','brain'),('model','brain'),
 ('nlp','doc'),('natural language','doc'),('prompt','doc'),('content','doc'),('document','doc'),
 ('vision','eye'),('image','eye'),
 ('deploy','cloud'),('mlops','cloud'),('production','cloud'),('scalable','cloud'),('infrastructure','cloud'),
 ('evaluat','chart'),('statistic','chart'),('feature','chart'),('predictive','chart'),('analy','chart'),
 ('workflow','gear'),('automat','gear'),('process','gear'),('orchestrat','gear'),('integration','gear'),
 ('full stack','code'),('full-stack','code'),('retrieval','db'),('rag','db'),('search','db'),
 ('architecture','shield'),('assistant','bot'),('chatbot','bot'),('recommendation','chart'),
 ('productivity','zap'),('use case','zap'),('design','gear'),('pipeline','cloud'),('service','net'),
]
def icon_for(label):
    l = label.lower()
    for key, ic in KEYMAP:
        if key in l:
            return ICON[ic]
    return ICON['zap']

def svg(paths, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'

# --- logo files present on disk (Phase 4) ----------------------------------
LOGO_DIR = os.path.join(SITE, 'assets', 'logos')
HAVE = {f[:-4] for f in os.listdir(LOGO_DIR)} if os.path.isdir(LOGO_DIR) else set()
LOGO_KEY = {
 'Python':'python','NumPy':'numpy','Pandas':'pandas','Scikit-learn':'scikit-learn',
 'TensorFlow':'tensorflow','PyTorch':'pytorch','MLflow':'mlflow','Hugging Face':'huggingface',
 'Docker':'docker','React':'react','Next.js':'nextjs','Node.js':'nodejs','FastAPI':'fastapi',
 'PostgreSQL':'postgresql','LangChain':'langchain','OpenAI':'openai','Postman':'postman',
 'Git &amp; GitHub':'github','ChatGPT':'openai','Claude':'claude','Gemini':'gemini',
 'n8n':'n8n','Make':'make','Zapier':'zapier','Airtable':'airtable','Notion AI':'notion',
 'VS Code':'vscode','CrewAI':'crewai','LangGraph':'langgraph','Flowise':'flowise','Langflow':'langflow',
 'Pinecone':'pinecone.png',   # raster: only an official PNG mark exists
}
def tool_chip(name):
    key = LOGO_KEY.get(name)
    if key:
        fname = key if key.endswith('.png') else key + '.svg'
        if os.path.isfile(os.path.join(LOGO_DIR, fname)):
            return f'<span class="tool-chip"><img src="assets/logos/{fname}" alt="" aria-hidden="true" loading="lazy" width="19" height="19">{name}</span>'
    return f'<span class="tool-chip no-mark">{name}</span>'

# --- THE CONTENT MODEL (transcribed from the four infographics) ------------
TRACKS = {
 'track-no-code-agent-engineer.html': dict(
  name='No-Code Agent Engineers',
  triad='Job-ready. Tool-powered. Business-focused.',
  entry='AI Foundation + Career Assessment',
  desc='Our No-Code Agent Engineers are trained to design, build and automate intelligent solutions that streamline operations, save time and drive measurable business impact — without writing traditional code.',
  cap_label='Skills our engineers bring',
  caps=['Prompt Engineering','AI Workflow Design','AI Agent Design','Process Automation',
        'Business Process Mapping','AI Use Case Identification','No-Code APIs','AI Productivity'],
  tools=['ChatGPT','Claude','Gemini','n8n','Make','Zapier','Flowise','Langflow','Airtable','Notion AI'],
  tool_note='Engineers are hands-on with these platforms and can integrate them to build end-to-end solutions.',
  deliver_label='What our engineers deliver',
  delivers=['AI Chatbots','Workflow Automations','Business Process Automation','Manual Work Eliminated',
            'Improved Accuracy','Operational Efficiency','Rapid Internal Tools'],
  hire=[('Faster Deployment','Deliver solutions quickly with pre-built components and automation expertise.'),
        ('Cost-Effective','Reduce development costs and dependency on specialised engineering resources.'),
        ('Boost Productivity','Automate repetitive tasks and workflows to improve team efficiency.'),
        ('Measurable Impact','Drive measurable results with intelligent, scalable automation solutions.'),
        ('Flexible &amp; Adaptable','Adapt to evolving business needs and integrate with existing tools seamlessly.')],
  profile='No-Code AI Agent Engineer | Workflow Automation | Prompt Engineering | n8n | Make | ChatGPT'),

 'track-pro-code-agent-engineer.html': dict(
  name='Pro-Code Agent Engineers',
  triad='Job-ready. Engineering-focused. Enterprise-ready.',
  entry='Python Assessment / Python Foundation',
  desc='Pro-Code Agent Engineers are trained to design, develop and deploy production-ready AI agents and intelligent automation systems using modern AI frameworks and software engineering best practices. With expertise in Python, agent architectures, backend development and LLM orchestration, they build scalable AI solutions that integrate seamlessly into enterprise environments.',
  cap_label='Core technical capabilities',
  caps=['Python Programming','Object-Oriented Programming (OOP)','API Development &amp; Integration',
        'AI Agent Architecture','Multi-Agent Systems','Model Context Protocol (MCP)',
        'Tool Calling &amp; Function Execution','LLM &amp; AI Integrations','Backend Development'],
  tools=['Python','VS Code','Git &amp; GitHub','LangChain','CrewAI','LangGraph','FastAPI','Docker','Postman'],
  tool_note='They are trained to build, test, deploy and maintain production-grade AI applications using industry-standard development workflows and enterprise tooling.',
  deliver_label='Enterprise AI solutions they can deliver',
  delivers=['Autonomous AI Agents','Enterprise AI Assistants','Multi-Agent Systems','AI Workflow Orchestration',
            'Backend AI Services &amp; APIs','LLM-powered Enterprise Applications','Intelligent Process Automation'],
  hire=[('Build Production-Ready AI','Develop production AI systems that integrate seamlessly into existing technology stacks.'),
        ('Accelerate AI Product Development','Reduce development timelines with engineers skilled in modern AI frameworks and backend technologies.'),
        ('Automate Complex Processes','Design intelligent agents capable of executing multi-step workflows across enterprise systems.'),
        ('Integrate Into Infrastructure','Leverage APIs, backend services and modern orchestration frameworks to deploy inside existing systems.'),
        ('Scale With Confidence','Build secure, maintainable and scalable AI applications using industry-standard engineering practices.')],
  profile='AI Agent Engineer | Python | LangChain | CrewAI | LangGraph | MCP | FastAPI'),

 'track-ai-engineer.html': dict(
  name='AI Engineer',
  triad='Full-stack. AI-native. Production-ready.',
  entry='Full Stack Assessment / Full Stack Foundation',
  desc='AI Engineers are trained to build end-to-end AI applications that integrate retrieval, large language models and modern web technologies. They design intelligent systems, develop robust backends, create seamless user experiences and deploy scalable AI products in production environments.',
  cap_label='Technical expertise',
  caps=['Full Stack Development','Retrieval-Augmented Generation (RAG)','LLM &amp; SLM Applications',
        'Vector Databases','AI Product Architecture','Model Evaluation','AI Deployment','Production AI Systems'],
  tools=['React','Next.js','Node.js','FastAPI','PostgreSQL','Pinecone','LangChain','OpenAI','Docker'],
  tool_note='Engineers are skilled in building, integrating and deploying AI solutions using industry-leading frameworks and cloud-native tools.',
  deliver_label='Enterprise AI solutions they can deliver',
  delivers=['RAG-Powered Applications','LLM-Powered Applications','Intelligent AI Assistants','Vector Search Solutions',
            'AI Product Development','AI APIs &amp; Backend Services','Scalable Production AI Systems'],
  hire=[('Build End-to-End AI Products','Design, develop and deploy full-stack AI applications from data retrieval to production.'),
        ('Leverage Modern Tech Stack','Skilled in the latest frameworks, LLM tools and cloud-native technologies.'),
        ('Deliver Intelligent Experiences','Create AI-driven features and applications that enhance user experience and drive adoption.'),
        ('Deploy Scalable Solutions','Build secure, reliable and scalable AI systems ready for enterprise use.'),
        ('Accelerate Time to Market','Reduce development cycles with engineers who understand both AI and full-stack development.')],
  profile='AI Engineer | RAG | LLM Applications | Full Stack AI | LangChain | Vector DBs | React'),

 'track-ml-engineer.html': dict(
  name='Machine Learning Engineers',
  triad='Data-driven. Model-centric. Impactful.',
  entry='Python Assessment / Python Foundation',
  desc='Machine Learning Engineers are trained to design, develop and deploy scalable ML and deep learning solutions. They combine strong foundations in statistics, algorithms and engineering to build intelligent systems that solve real-world problems and create measurable business value.',
  cap_label='Core technical capabilities',
  caps=['Python Programming &amp; Statistics','Machine Learning','Deep Learning','Feature Engineering',
        'Model Training &amp; Evaluation','Computer Vision','Natural Language Processing (NLP)','MLOps &amp; Model Deployment'],
  tools=['Python','NumPy','Pandas','Scikit-learn','TensorFlow','PyTorch','MLflow','Hugging Face','Docker'],
  tool_note='Engineers are proficient in building, training, tracking and deploying ML models using modern MLOps practices and industry-standard tools.',
  deliver_label='Enterprise ML solutions they can deliver',
  delivers=['Predictive Models','Computer Vision Applications','NLP &amp; Language Intelligence','Recommendation Systems',
            'End-to-End ML Pipelines','MLOps &amp; Model Deployment','Scalable Production ML Systems'],
  hire=[('Solve Real-World Problems','Build data-driven solutions that address complex business challenges and drive measurable impact.'),
        ('Make Better Decisions','Transform data into accurate predictions and insights that improve business outcomes.'),
        ('Automate &amp; Optimise Processes','Leverage ML to automate manual work, optimise operations and reduce costs.'),
        ('Deploy at Scale','Deliver production-ready ML models with robust pipelines, monitoring and MLOps best practices.'),
        ('Future-Proof Your Business','Build intelligent systems that adapt, learn and create long-term competitive advantage.')],
  profile='Machine Learning Engineer | Python | TensorFlow | PyTorch | MLOps | Deep Learning | NLP | CV'),
}

# --- section builders ------------------------------------------------------
def role_section(d):
    caps = '\n        '.join(
        f'<li>{svg(icon_for(c))}{c}</li>' for c in d['caps'])
    tools = '\n        '.join(tool_chip(t) for t in d['tools'])
    return f'''<!-- ROLE:DEFINITION -->
<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="role-triad">
      <span class="rt-words">{d['triad']}</span>
      <span class="role-entry">{svg('<path d="M12 3l8 3.5v5c0 4.5-3.4 8.6-8 9.5-4.6-.9-8-5-8-9.5v-5z"/><path d="M9 12l2 2 4-4"/>')}Entry · {d['entry']}</span>
    </div>
    <p class="section-lede" style="text-align:left;margin-left:0">{d['desc']}</p>
    <div class="road-grid" style="margin-top:38px;align-items:start">
      <div>
        <p class="eyebrow" style="text-align:left;margin-left:0">{d['cap_label']}</p>
        <ul class="cap-list" style="margin-top:16px">
        {caps}
        </ul>
      </div>
      <div>
        <p class="eyebrow" style="text-align:left;margin-left:0">Technologies &amp; tools</p>
        <div class="tool-wall">
        {tools}
        </div>
        <p class="tool-note">{d['tool_note']}</p>
      </div>
    </div>
  </div>
</section>
<!-- /ROLE:DEFINITION -->'''

def value_section(d):
    delivers = '\n      '.join(
        f'<div class="deliver reveal"><span class="dv-ico">{svg(icon_for(x))}</span><span class="dv-t">{x}</span></div>'
        for x in d['delivers'])
    hires = '\n      '.join(
        f'<div class="wh reveal"><div class="wh-n">0{i+1}</div><div class="wh-t">{t}</div><div class="wh-d">{s}</div></div>'
        for i, (t, s) in enumerate(d['hire']))
    prof = d['profile'].replace(' | ', '</b> | <b>', 1)
    return f'''<!-- ROLE:VALUE -->
<section class="section">
  <div class="wrap">
    <p class="eyebrow">{d['deliver_label']}</p>
    <h2 class="section-q">What they <span class="em">ship for you.</span></h2>
    <div class="deliver-row">
      {delivers}
    </div>
  </div>
</section>

<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <p class="eyebrow">For employers</p>
    <h2 class="section-q">Why hire <span class="em">{d['name']}?</span></h2>
    <div class="why-hire">
      {hires}
    </div>
    <div class="profile-line">
      <span class="pl-lab">Sample professional profile</span>
      <span class="pl-val"><b>{prof}</b></span>
    </div>
    <div style="display:flex;gap:12px;margin-top:26px;flex-wrap:wrap">
      <a href="hire-talent.html" class="btn btn-primary">Hire from this track <span aria-hidden="true">&#8594;</span></a>
      <a href="contact.html" class="btn btn-ghost">Talk to admissions</a>
    </div>
  </div>
</section>
<!-- /ROLE:VALUE -->'''

# --- injection -------------------------------------------------------------
def inject(path, block, marker, after_pattern=None, before_pattern=None):
    p = os.path.join(SITE, path)
    s = open(p, encoding='utf-8').read()
    fence = re.compile(rf'<!-- {marker} -->.*?<!-- /{marker} -->', re.S)
    if fence.search(s):                       # re-run: replace in place
        s = fence.sub(block, s, count=1)
    elif after_pattern:
        m = re.search(after_pattern, s, re.S)
        if not m: raise SystemExit(f'anchor not found in {path}: {after_pattern}')
        s = s[:m.end()] + '\n\n' + block + s[m.end():]
    else:
        m = re.search(before_pattern, s, re.S)
        if not m: raise SystemExit(f'anchor not found in {path}: {before_pattern}')
        s = s[:m.start()] + block + '\n\n' + s[m.start():]
    open(p, 'w', encoding='utf-8').write(s)

for path, d in TRACKS.items():
    # role definition goes right after the hero block (</div> closing .wrap after .td-hero)
    inject(path, role_section(d), 'ROLE:DEFINITION',
           after_pattern=r'<aside class="enroll".*?</aside>\s*</div>\s*</div>')
    # employer value goes before the "Keep building" related-tracks rail
    inject(path, value_section(d), 'ROLE:VALUE',
           before_pattern=r'<section class="section">\s*<div class="wrap">\s*<p class="eyebrow"[^>]*>Related Builders tracks')
    print(f'✓ {path}')
print('\nrole sections injected into 4 track pages')
