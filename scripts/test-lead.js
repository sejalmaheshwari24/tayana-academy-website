// Exercise api/lead.js directly: validation, honeypot, unconfigured, success.
// Run: node scripts/test-lead.js   (no framework, no network — fetch is stubbed)
const fn = require('../api/lead.js');
function mkRes() {
  const r = { code: 0, body: null, headers: {} };
  r.setHeader = (k,v)=>{ r.headers[k]=v; };
  r.status = c => { r.code = c; return r; };
  r.json = b => { r.body = b; return r; };
  r.end = () => r;
  return r;
}
const call = async (body, env={}) => {
  const saved = {...process.env};
  Object.assign(process.env, env);
  const res = mkRes();
  await fn({ method:'POST', body }, res);
  process.env = saved;
  return res;
};
(async () => {
  let r;
  r = await call({form:'contact', name:'A', email:'a@b.com'});
  console.log('unconfigured        ->', r.code, JSON.stringify(r.body));

  // fake webhook
  global.fetch = async () => ({ ok:true, text: async()=> '' });
  r = await call({form:'contact', name:'A', email:'a@b.com'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('valid contact       ->', r.code, JSON.stringify(r.body));

  r = await call({form:'contact', email:'a@b.com'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('missing name        ->', r.code, JSON.stringify(r.body));

  r = await call({form:'contact', name:'A', email:'not-an-email'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('bad email           ->', r.code, JSON.stringify(r.body));

  r = await call({form:'evil', email:'a@b.com'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('unknown form        ->', r.code, JSON.stringify(r.body));

  r = await call({form:'contact', name:'A', email:'a@b.com', company_website:'bot'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('honeypot filled     ->', r.code, JSON.stringify(r.body));

  // capture payload
  let sent=null;
  global.fetch = async (u,o) => { sent = JSON.parse(o.body); return { ok:true, text: async()=>'' }; };
  await call({form:'team-pilot', email:'x@y.com', company:'Acme', team_size:'11–20 people', page:'/for-teams.html'},
             {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('payload             ->', JSON.stringify(sent));

  global.fetch = async () => ({ ok:false, status:500, text: async()=>'boom' });
  r = await call({form:'newsletter', email:'a@b.com'}, {LEAD_WEBHOOK_URL:'https://example.test/h'});
  console.log('webhook 500         ->', r.code, JSON.stringify(r.body));
})();
