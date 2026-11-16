"""Client hub + one bespoke 'world' page per client. Facts come only from the current HMG site."""
# Python 3.8+ compatibility: literals used inside f-strings
_Q1 = " class=\"on\""
import html as H

UP = 'https://www.harrismediallc.com/wp-content/uploads/'
e = lambda s: H.escape(str(s), quote=True)
ARR = '<span aria-hidden="true">→</span>'

# slug, name, world name, category, logo, accent (roster hover bg), ink (text on accent), next-bg, short line
CLIENTS = [
    dict(slug='right-for-america', name='Right for America PAC', world='BROADCAST', cat='presidential', tag='PRO-TRUMP SUPER PAC · 2024',
         logo=UP + '2024/12/Pro-Trump.png', c='#C1121F', ink='#fff', bg='linear-gradient(120deg,#07122B,#1A3270 60%,#C1121F)'),
    dict(slug='netanyahu-likud', name='Benjamin Netanyahu', world='THE CHATBOT', cat='international', tag='PRIME MINISTER · ISRAEL',
         logo=UP + '2024/12/Benjamin-Natanyahu.png', c='#0038B8', ink='#fff', bg='linear-gradient(120deg,#071A4D,#0038B8)'),
    dict(slug='nh-senate-republicans', name='NH Senate Republicans', world='TARGET LOCK', cat='state', tag='STATE LEGISLATIVE · NEW HAMPSHIRE',
         logo=UP + '2024/12/NH-SEANET.png', c='#C6F432', ink='#0E1A12', bg='linear-gradient(120deg,#0E1A12,#1D3526 60%,#4C6B1A)'),
    dict(slug='francis-suarez', name='Francis Suarez', world='MIAMI NEON', cat='presidential', tag='SOS AMERICA PAC · AAPC 2024',
         logo=UP + '2024/12/Mayor-Francis-Suarez.png', c='#FF2E88', ink='#fff', bg='linear-gradient(120deg,#12002B,#2B0050 50%,#FF2E88)'),
    dict(slug='rand-paul', name='Rand Paul', world='INTERNET ARMY', cat='federal', tag='U.S. SENATE · PRESIDENT 2016',
         logo=UP + '2024/12/Rand-Paul-1.png', c='#39FF14', ink='#020A02', bg='linear-gradient(120deg,#020A02,#062806 60%,#0B4A0B)'),
    dict(slug='ted-cruz', name='Ted Cruz', world='THE UNDERDOG', cat='federal', tag='U.S. SENATE · TEXAS',
         logo=UP + '2025/01/Ted-Cruz.png', c='#EFE9DD', ink='#1A1714', bg='linear-gradient(120deg,#1A1714,#4A3F33 60%,#B3261E)'),
    dict(slug='rick-scott', name='Rick Scott', world='DARK HORSE', cat='federal', tag='GOVERNOR · U.S. SENATE · FLORIDA',
         logo=UP + '2025/01/Rick-Scot.png', c='#F28C28', ink='#062A2A', bg='linear-gradient(120deg,#062A2A,#0B4747 60%,#F28C28)'),
    dict(slug='mike-huckabee', name='Mike Huckabee', world='FROM AN ASTERISK', cat='presidential', tag='PRESIDENTIAL · 2008',
         logo=UP + '2024/12/Mike-Huckabee-1.png', c='#C8102E', ink='#fff', bg='linear-gradient(120deg,#22303C,#3B4B59 60%,#C8102E)'),
    dict(slug='maine-gop', name='Maine GOP', world='THE LIGHTHOUSE', cat='state', tag='STATE PARTY · NEW ENGLAND',
         logo=UP + '2024/12/MEGOP.png', c='#F6D776', ink='#0A1B2E', bg='linear-gradient(120deg,#081525,#163B5C)'),
    dict(slug='linda-mcmahon', name='Linda McMahon', world='SPOTLIGHT', cat='state', tag='STATEWIDE · CONNECTICUT',
         logo=UP + '2024/12/Linda.png', c='#FFD666', ink='#050505', bg='linear-gradient(120deg,#050505,#2A2108 60%,#8A6A12)'),
    dict(slug='vhha', name='Virginia Hospital & Healthcare Association', world='VITAL SIGNS', cat='advocacy', tag='HEALTHCARE ADVOCACY · VIRGINIA',
         logo=UP + '2024/12/Likud.png', c='#0E7C86', ink='#fff', bg='linear-gradient(120deg,#062B2F,#0E7C86)'),
    dict(slug='txoga', name='TXOGA', world='PRESSURE', cat='advocacy', tag='TEXAS OIL & GAS ASSOCIATION',
         logo=UP + '2024/12/TXOGA.png', c='#FFB000', ink='#121212', bg='linear-gradient(120deg,#121212,#3A2A05 60%,#FFB000)'),
    dict(slug='dan-patrick', name='Dan Patrick', world='LONE STAR', cat='state', tag='LIEUTENANT GOVERNOR · TEXAS',
         logo=UP + '2025/01/Dan-Patrick.png', c='#BF0A30', ink='#fff', bg='linear-gradient(120deg,#002868,#0E1B3D 55%,#BF0A30)'),
    dict(slug='sarah-palin', name='Sarah Palin', world='FRONTIER', cat='federal', tag='ALASKA · CONSERVATIVE ICON',
         logo=UP + '2025/01/Sarah-Palin.png', c='#2EFFAA', ink='#04111C', bg='linear-gradient(120deg,#020812,#0E2E43 50%,#1B6B5A)'),
    dict(slug='doug-collins', name='Doug Collins', world='ROLL TAPE', cat='federal', tag='GEORGIA',
         logo=UP + '2024/12/Doug.png', c='#FF9E5E', ink='#111', bg='linear-gradient(120deg,#111,#3A2414 60%,#FF9E5E)'),
]
BY = {c['slug']: c for c in CLIENTS}

STAR = '<svg viewBox="0 0 100 100" aria-hidden="true"><polygon points="50,4 61,38 97,38 68,59 79,93 50,72 21,93 32,59 3,38 39,38" fill="none" stroke="#E63946" stroke-width="1.2"/><polygon points="50,18 58,42 84,42 63,57 71,82 50,67 29,82 37,57 16,42 42,42" fill="rgba(230,57,70,.15)" stroke="#fff" stroke-width=".6"/></svg>'
LONESTAR = '<svg viewBox="0 0 100 100" aria-hidden="true"><polygon points="50,4 61,38 97,38 68,59 79,93 50,72 21,93 32,59 3,38 39,38" fill="#F4F1EA"/></svg>'


def crumbs(c, color='inherit'):
    return (f'<div class="w-crumbs" style="color:{color}"><a href="index.html">HOME</a><span>/</span>'
            f'<a href="clients.html">OUR CLIENTS</a><span>/</span><span>{e(c["name"]).upper()}</span></div>')


def proof(href, label, extra=''):
    return f'<a class="w-btn" href="{href}" target="_blank" rel="noopener">{label} {ARR}</a>{extra}'


# ----------------------------------------------------------------------------- worlds
def w_rfa(c):
    return f'''<section class="w-hero"><div class="stars"></div><div class="bigstar">{STAR}</div>
<div class="wrap">{crumbs(c)}<span class="onair"><i></i>ON AIR · 2024</span>
<h1 class="w-title"><span>RIGHT</span><span class="o">FOR</span><span class="r">AMERICA</span></h1>
<p class="w-lede">The pro-Trump Super PAC whose digital operation HMG ran in the 2024 Presidential cycle — one of the largest spenders on Google and Meta in the entire race.</p>
<div style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap">{proof("https://drive.google.com/file/d/1DRznd864uxirOjhMIlt_bQx2MmH1bvbb/view?usp=sharing", "VIEW THE CASE")}</div></div></section>
<div class="stripes" aria-hidden="true"></div>
<section class="w-sec"><div class="wrap">
<span class="w-kicker" style="color:#E63946">THE AD WAR · 2024 PRESIDENTIAL CYCLE</span>
<h2 class="w-h2">AMONG THE LARGEST<br>SPENDERS ON</h2>
<div class="w-two" style="align-items:stretch">
  <div class="plat" data-reveal><div class="p">GOOGLE</div><div class="meter"><i></i></div><div class="w-note">Search · YouTube · Display</div></div>
  <div class="plat" data-reveal><div class="p">META</div><div class="meter"><i></i></div><div class="w-note">Facebook · Instagram</div></div>
</div>
<p class="w-p" style="margin-top:34px;max-width:70ch">Vincent Harris and the HMG team ran the full digital operation for the Florida-based Right for America PAC — strategy, creative and paid media at presidential scale.</p>
</div></section>'''


def w_likud(c):
    msgs = [('bot', 'Hi! Thanks for supporting Likud. Ready to help get out the vote today?'), ('me', 'Yes — what can I do?'),
            ('bot', 'Great. I can connect you to call fellow voters right now. Should I start?'), ('me', 'Start 📞'),
            ('bot', 'Connecting you… Thank you! Every call counts.')]
    chat = ''.join(f'<div class="msg {k}">{e(t)}</div>' for k, t in msgs)
    return f'''<section class="w-hero"><div class="wrap w-two">
<div>{crumbs(c, '#BFD3FF')}<span class="w-kicker" style="color:#8FB4FF">LIKUD NATIONAL LIBERAL PARTY · ISRAEL</span>
<h1 class="w-title">THE<br>CHAT<span style="color:#8FB4FF">BOT</span></h1>
<p class="w-lede" style="color:#DCE6FF">The first-ever AI-generated and AI-operated chatbot in presidential political history — built by HMG for Prime Minister Benjamin Netanyahu’s Likud party.</p>
<div style="margin-top:30px">{proof("https://drive.google.com/file/d/1Log_w9TUS4wNAAxe7hSFDu8CaUQPsNws/view", "VIEW THE CASE")}</div></div>
<div><div class="phone"><div class="screen" data-chat><div class="bar"><span class="av">AI</span><div><b>LIKUD BOT</b><small>● online · AI-operated</small></div></div>{chat}<div class="typing" style="display:none"><i></i><i></i><i></i></div></div></div><div class="w-note" style="text-align:right;color:#BFD3FF">Illustrative interface</div></div>
</div></section>
<section class="w-sec"><div class="wrap">
<span class="w-kicker" style="color:#0038B8">VOTERS MOBILIZED TO CALL</span>
<h2 class="w-h2"><span data-count="16999">0</span> VOTERS.<br>TWO CHANNELS.</h2>
<div class="split" data-reveal><div class="tg">TELEGRAM · 8,323</div><div class="fb">FACEBOOK · 8,676</div></div>
<div class="w-facts" style="margin-top:22px">
  <div class="w-fact" data-reveal><div class="n"><span data-count="8323">0</span></div><div class="l">voters calling via Telegram</div></div>
  <div class="w-fact" data-reveal><div class="n"><span data-count="8676">0</span></div><div class="l">voters calling via Facebook</div></div>
  <div class="w-fact" data-reveal><div class="n">#1</div><div class="l">first AI-operated campaign chatbot</div></div>
</div></div></section>
<section class="w-sec" style="background:#E8EEF9"><div class="wrap">
<span class="w-kicker" style="color:#0038B8">HEAD OF STATE · TWO VICTORIES</span>
<h2 class="w-h2">ON THE GROUND IN ISRAEL</h2>
<div class="yr"><div data-reveal><b>2015</b>Successful election cycle for the Prime Minister</div><div data-reveal><b>2022</b>Successful election cycle for the Prime Minister</div></div>
<p class="w-p" style="margin-top:28px;max-width:70ch">Vincent Harris spent extensive time in Israel in both the 2015 and 2022 successful election cycles for Benjamin Netanyahu. HMG has run digital operations twice for the Prime Minister’s successful elections — part of head-of-state work that also spans France, Spain and Albania.</p>
</div></section>'''


def w_nh(c):
    return f'''<section class="w-hero"><div class="topo"></div><div class="wrap w-two">
<div>{crumbs(c, '#C6F432')}<span class="w-kicker" style="color:#C6F432">STATE LEGISLATIVE · 2025 AWARD</span>
<h1 class="w-title">TARGET<br><em>LOCKED.</em></h1>
<p class="w-lede">Best Use of Online Targeting for a State Legislative Campaign. HMG’s digital strategy helped expand the New Hampshire Senate Republican caucus to a supermajority over three election cycles.</p>
<div class="coords">43.2081° N · 71.5376° W — CONCORD, NH</div>
<div style="margin-top:28px">{proof("https://drive.google.com/file/d/1rbmmw1RVOGBLwLtVTHeE2lj_E0LmBBru/view", "VIEW THE CASE")}</div></div>
<div class="radar" aria-hidden="true"><div class="h"></div><span class="blip" style="left:62%;top:30%"></span><span class="blip" style="left:30%;top:62%;animation-delay:.6s"></span><span class="blip" style="left:70%;top:72%;animation-delay:1.2s"></span><span class="lock"></span></div>
</div></section>
<section class="w-sec"><div class="wrap w-two">
<div><span class="w-kicker" style="color:#C6F432">THREE CYCLES</span><h2 class="w-h2">FROM MAJORITY TO SUPERMAJORITY</h2>
<p class="w-p">Cycle after cycle, precise online targeting found the voters that decide state senate seats — and the caucus kept growing until it reached a supermajority.</p>
<p class="w-p">HMG has also worked in New Hampshire on multiple presidential campaigns, including for Mike Huckabee, Rick Perry, Newt Gingrich, Rand Paul and Francis Suarez.</p></div>
<div class="cycles" data-reveal><div class="cyc c1">CYCLE 01</div><div class="cyc c2">CYCLE 02</div><div class="cyc c3">SUPERMAJORITY</div></div>
</div></section>
<section class="w-sec" style="padding-top:0"><div class="wrap"><div class="award" data-reveal>
<span class="w-kicker" style="color:#C6F432">AWARD · 2025</span><h2 class="w-h2" style="margin-bottom:0">BEST USE OF ONLINE TARGETING<br>FOR A STATE LEGISLATIVE CAMPAIGN</h2>
</div></div></section>'''


def w_sos(c):
    palm = '<svg viewBox="0 0 100 160" class="palm" style="left:6%"><path d="M50 160 C52 120 48 90 50 60" stroke="#12002B" stroke-width="6" fill="none"/><path d="M50 60 C30 40 10 45 0 55 M50 60 C70 40 90 45 100 55 M50 60 C40 30 20 20 8 22 M50 60 C60 30 80 20 92 22 M50 60 C50 30 52 15 50 5" stroke="#12002B" stroke-width="5" fill="none"/></svg>'
    return f'''<section class="w-hero"><div class="sun"></div><div class="floor"></div>{palm}{palm.replace('left:6%', 'left:auto;right:6%;transform:scaleX(-1)')}
<div class="wrap">{crumbs(c, '#FFC2E0')}<span class="w-kicker neon2">SOS AMERICA PAC · MIAMI</span>
<h1 class="w-title neon">SOS<br>AMERICA</h1>
<p class="w-lede">The Super PAC supporting Miami Mayor Francis Suarez — and the 2024 AAPC Campaign Excellence Award for Digital Campaign of the Year.</p>
<div style="margin-top:30px">{proof("https://drive.google.com/file/d/1X7S16rBiPGELuqlyJtyiXnwSvFm_2DPa/view", "VIEW THE CASE")}</div></div></section>
<section class="w-sec"><div class="wrap w-two">
<div class="trophy" data-reveal><span class="w-kicker neon2">AAPC · 2024</span><b class="neon" style="margin-top:14px">DIGITAL<br>CAMPAIGN<br>OF THE YEAR</b><div class="w-note" style="margin-top:18px">Campaign Excellence Award</div></div>
<div data-reveal><div class="frame"><img src="{UP}2025/01/img-ai-suarez.png" alt="SOS America PAC campaign for Francis Suarez" loading="lazy"></div></div>
</div></section>
<section class="w-sec" style="padding-top:0"><div class="wrap">
<span class="w-kicker" style="color:#00E5FF">FROM MIAMI TO THE NATION</span><h2 class="w-h2 neon2">AN AWARD-WINNING<br>PRESIDENTIAL PUSH</h2>
<p class="w-p" style="max-width:70ch">HMG ran digital operations for Mayor Suarez’s Super PAC, taking a Miami mayor’s message national — including campaigning in New Hampshire — with creative that won the industry’s top digital honor.</p>
</div></section>'''


def w_rand(c):
    lines = ['> boot hmg://campaign --candidate="Rand Paul" --cycle=2016', 'loading digital strategy ............ OK',
             'deploying social channels ........... OK', 'recruiting supporters ............... OK',
             '> status', 'INTERNET ARMY: ONLINE', 'new standard for digital strategy in politics: SET']
    army = ''.join(f'<i style="--d:{(i * 37) % 60}"></i>' for i in range(120))
    return f'''<section class="w-hero"><div class="wrap w-two">
<div class="crt">{crumbs(c, '#39FF14')}<span class="w-kicker" style="color:#39FF14">PRESIDENTIAL · 2016 · POLITICO</span>
<h1 class="w-title">INTERNET<br>ARMY_</h1>
<p class="w-lede">Our work on Senator Rand Paul's 2016 Presidential campaign set a new standard for digital strategy in politics, boosting his online impact and positioning him as a digitally savvy GOP candidate.</p></div>
<div class="term crt" data-term='{e(__import__("json").dumps(lines))}'><span class="out"></span></div>
</div></section>
<section class="w-sec"><div class="wrap w-two">
<div class="army" aria-hidden="true" data-reveal>{army}</div>
<div class="clip" data-reveal><div class="src">POLITICO MAGAZINE · 2015</div><q>Rand Paul’s internet army</q>
<p class="w-p">Politico profiled the digital operation HMG built for the Senator’s presidential run — a model for how a candidate can organize supporters online.</p>
{proof("https://www.politico.com/magazine/story/2015/04/rand-paul-2016-social-media-117132/", "READ ON POLITICO")}</div>
</div></section>'''


def w_cruz(c):
    return f'''<section class="w-hero"><div class="wrap">{crumbs(c, '#1A1714')}
<div class="mast"><span>VOL. HMG · TEXAS EDITION</span><b>The Digital Dispatch</b><span>U.S. SENATE</span></div>
<h1 class="headline">The <em>Underdog</em> Win</h1>
<p class="deck">How the web became part of one of the most remarkable upsets in modern Senate politics.</p>
<div class="w-two" style="align-items:start;margin-top:10px">
<div class="cols" style="columns:2 240px"><p>Vincent Harris spent over three years working with Ted Cruz, whom many have credited his successful use of the web as part of his incredible underdog win.</p>
<p>In 2012, as contenders raced to master social media, Politico took notice of the campaigns getting it right.</p>
<p>Today HMG counts Senator Cruz among the U.S. Senators whose digital operations the firm has run, alongside John Cornyn, Mitch McConnell and Rick Scott.</p></div>
<div><img class="photo-np" src="{c['logo']}" alt="Ted Cruz" loading="lazy"><div class="cap">Sen. Ted Cruz — a client of Harris Media Group.</div>
<div style="margin-top:22px"><span class="stamp">UPSET!</span></div></div>
</div></div></section>
<section class="w-sec dark"><div class="wrap w-two">
<div><span class="w-kicker" style="color:#E2725B">FROM THE ARCHIVE</span><h2 class="w-h2">“CONTENDERS’ SECRET: MASTERING SOCIAL MEDIA”</h2></div>
<div><p class="w-p">Politico, July 2012.</p>{proof("https://www.politico.com/story/2012/07/contenders-secret-mastering-social-media-079213", "READ ON POLITICO").replace('class="w-btn"', 'class="w-btn" style="color:#EFE9DD"')}</div>
</div></section>'''


def w_scott(c):
    return f'''<section class="w-hero"><div class="wrap">{crumbs(c, '#F28C28')}
<span class="w-kicker" style="color:#F28C28">FLORIDA GOVERNOR · 2010</span>
<h1 class="w-title">DARK<br><span class="h">HORSE.</span></h1>
<p class="w-lede">Rick Scott overcame all odds to narrowly win Florida’s gubernatorial race — with HMG playing an instrumental role in the win.</p>
<div class="race" data-reveal style="margin-top:46px"><div class="track">
  <div class="lane"><span class="lb">FIELD</span><span class="runner o r1">●</span></div>
  <div class="lane"><span class="lb">FIELD</span><span class="runner o r2">●</span></div>
  <div class="lane"><span class="lb">HMG</span><span class="runner us">RS</span></div>
  <div class="finish"></div></div></div>
</div></section>
<section class="w-sec"><div class="wrap">
<span class="w-kicker" style="color:#F28C28">THE WEB WON NOTICE</span><h2 class="w-h2">A CAMPAIGN OTHERS STUDIED</h2>
<div class="press">
  <div data-reveal><span class="w-note">FEATURED IN</span><b>National Review</b></div>
  <div data-reveal><span class="w-note">COVERED BY</span><b>Florida papers & blogs</b></div>
  <div data-reveal><span class="w-note">CASE STUDY BY</span><b>Facebook corporate</b></div>
</div>
<p class="w-p" style="margin-top:30px;max-width:72ch">During the 2010 cycle, Harris Media ran successful digital initiatives in 7 states. Governor Scott’s innovative use of the web was featured in the National Review and numerous Florida papers and blogs — and even led to a case study by Facebook corporate. HMG later counted Scott among the U.S. Senators whose digital operations it has run.</p>
<div class="w-facts" style="margin-top:28px"><div class="w-fact" style="border:1px solid rgba(255,255,255,.2)"><div class="n">7</div><div class="l">states with successful digital initiatives · 2010</div></div><div class="w-fact" style="border:1px solid rgba(255,255,255,.2)"><div class="n">2010</div><div class="l">Florida gubernatorial upset</div></div></div>
</div></section>'''


def w_huck(c):
    bars = ''.join(f'<i style="--h:{h}%"></i>' for h in (62, 48, 40, 34)) + '<i class="me" style="--h:92%"></i>'
    return f'''<section class="w-hero"><div class="wrap w-two">
<div>{crumbs(c, '#22303C')}<span class="w-kicker" style="color:#C8102E">PRESIDENTIAL CAMPAIGN · 2008</span>
<h1 class="w-title" style="font-size:clamp(2.6rem,8vw,6.6rem)">FROM AN<br>ASTERISK<br><span style="color:#C8102E">TO IOWA.</span></h1>
<p class="w-lede">Vincent Harris traveled with Governor Mike Huckabee from — as the Governor would say — “an asterisk in the polls” to Iowa Caucus winner.</p></div>
<span class="ast" aria-hidden="true">*</span></div></section>
<section class="w-sec"><div class="wrap w-two" style="align-items:start">
<div><span class="w-kicker" style="color:#C8102E">THE BLOG ERA</span><h2 class="w-h2">ONE OF THE FIRST CAMPAIGNS ON TWITTER</h2>
<div class="post" data-reveal><div class="ts">CAMPAIGN LOG · 01</div><h3>Two staffers. One online operation.</h3><p class="w-p">Vincent served as one of two staffers specializing in online communications on the Governor’s Presidential campaign.</p></div>
<div class="post" data-reveal><div class="ts">CAMPAIGN LOG · 02</div><h3>Blog interviews & content</h3><p class="w-p">He organized blog interviews, gathered content and helped the campaign become one of the first to ever utilize <strong>Twitter</strong>.</p></div>
<div class="post" data-reveal><div class="ts">CAMPAIGN LOG · 03 · CAUCUS EVE</div><h3>The Iowa “Blogger Bash”</h3><p class="w-p">On the eve of the Caucus, he organized the Iowa “Blogger Bash” — which received national attention.</p></div></div>
<div style="position:sticky;top:110px"><div class="poll" data-reveal aria-hidden="true">{bars}</div><div class="w-note" style="margin-top:10px">Illustration · from an asterisk to first place</div></div>
</div></section>
<section class="w-sec" style="padding-top:20px"><div class="wrap"><div class="book" data-reveal>
<q>Vincent was one of those special young men in whom I see remarkable potential. Humble and polite to the point of being over the top, he was incredibly talented in understanding the power of the Internet and the potential of using a blog to create a daily log of activities and information and to build an online community.</q>
<div class="w-note" style="opacity:.8;margin-top:22px">— Gov. Mike Huckabee, “Do the Right Thing” (2008)</div></div></div></section>'''


def w_maine(c):
    lh = '<svg class="lh" viewBox="0 0 40 120" aria-hidden="true"><rect x="14" y="10" width="12" height="10" fill="#F6D776"/><polygon points="10,20 30,20 34,120 6,120" fill="#E7EEF5"/><rect x="8" y="50" width="24" height="10" fill="#C8102E"/><rect x="7" y="85" width="26" height="10" fill="#C8102E"/><polygon points="12,10 28,10 20,0" fill="#0A1B2E"/></svg>'
    return f'''<section class="w-hero"><div class="beam"></div>{lh}<div class="fog"></div><div class="pines"></div>
<div class="wrap">{crumbs(c, '#F6D776')}<span class="w-kicker" style="color:#F6D776">NEW ENGLAND · AUGUSTA, MAINE</span>
<h1 class="w-title">PLANTING<br>A FLAG<br><span style="color:#F6D776">IN MAINE.</span></h1>
<p class="w-lede">HMG works with the Maine Republican Party — and in November 2025 opened its first dedicated New England office in Augusta.</p>
<div class="coords" style="margin-top:16px">44.3106° N · 69.7795° W — AUGUSTA, ME</div>
<div style="margin-top:28px">{proof("https://www.mainegop.com/", "VISIT MAINE GOP")}<a class="w-btn" style="margin-left:10px" href="blog-hmg-expands-to-new-england-welcomes-representative-reagan-paul-to-lead-regional-growth.html">READ THE RELEASE {ARR}</a></div></div></section>
<section class="w-sec"><div class="wrap w-two" style="align-items:start">
<div><span class="w-kicker" style="color:#F6D776">THE LOGBOOK</span><h2 class="w-h2">NEW ENGLAND, CHARTED</h2>
<div class="log">
<div class="e" data-reveal><b>THE LAST TWO YEARS</b><h3>A presence in Maine</h3><p class="w-p">HMG built its presence in the state before opening an office.</p></div>
<div class="e" data-reveal><b>2025</b><h3>Governor Paul LePage for Congress</h3><p class="w-p">Part of the team that launched Gov. LePage’s run for Congress in Maine’s Second District.</p></div>
<div class="e" data-reveal><b>NOVEMBER 2025</b><h3>First dedicated office · Augusta</h3><p class="w-p">HMG welcomed Representative Reagan Paul to lead regional growth.</p></div>
</div></div>
<div class="quote" data-reveal><q>Republicans aren’t giving up on New England.</q><div class="w-note" style="opacity:.8;margin-top:16px">— Vincent Harris, CEO, Harris Media Group</div>
<p class="w-p" style="margin-top:16px">HMG also runs governor’s and congressional races throughout Maine and New Hampshire.</p></div>
</div></section>'''


def w_mcm(c):
    words = ['STATEWIDE', 'CONNECTICUT', 'NEW ENGLAND', 'LINDA McMAHON'] * 2
    return f'''<section class="w-hero"><div class="spot s1"></div><div class="spot s2"></div><div class="stage"></div>
<div class="wrap">{crumbs(c, '#FFD666')}<div class="portrait"><img src="{c['logo']}" alt="Linda McMahon"></div>
<span class="w-kicker" style="color:#FFD666">STATEWIDE CAMPAIGNS · CONNECTICUT</span>
<h1 class="w-title" style="font-size:clamp(2.8rem,9vw,7.5rem)">LINDA<br>McMAHON</h1>
<p class="w-lede">HMG has led statewide campaigns in Connecticut for leaders like Linda McMahon — part of the firm’s growing work across New England.</p></div></section>
<div class="marquee" aria-hidden="true"><div>{''.join(f'<span>{w}</span>' for w in words * 2)}</div></div>
<section class="w-sec"><div class="wrap w-facts">
<div class="card" data-reveal><span class="w-kicker" style="color:#FFD666">THE STAGE</span><h3 class="w-h2" style="font-size:1.8rem">STATEWIDE</h3><p class="w-p">Statewide races demand reach in every media market at once — the kind of program HMG builds in-house.</p></div>
<div class="card" data-reveal><span class="w-kicker" style="color:#FFD666">THE REGION</span><h3 class="w-h2" style="font-size:1.8rem">NEW ENGLAND</h3><p class="w-p">From Connecticut to New Hampshire and Maine, HMG has proven Republicans can compete and win in the Northeast.</p></div>
<div class="card" data-reveal><span class="w-kicker" style="color:#FFD666">ALSO IN CT</span><h3 class="w-h2" style="font-size:1.8rem">BOB STEFANOWSKI</h3><p class="w-p">HMG has also led statewide campaigns for Bob Stefanowski in Connecticut.</p></div>
</div></section>'''


def w_vhha(c):
    ekg = '<svg class="ekg" viewBox="0 0 1200 200" preserveAspectRatio="none" aria-hidden="true"><path d="M0 100 H260 L280 100 L300 40 L320 160 L340 100 H560 L580 100 L600 20 L625 180 L645 100 H880 L900 100 L920 50 L940 150 L960 100 H1200"/></svg>'
    return f'''<section class="w-hero">{ekg}<div class="wrap w-two">
<div>{crumbs(c, '#0E7C86')}<span class="w-kicker" style="color:#0E7C86"><span class="pulse"></span>HEALTHCARE ADVOCACY · VIRGINIA</span>
<h1 class="w-title" style="font-size:clamp(2.8rem,8vw,6.6rem)">VITAL<br><span>SIGNS.</span></h1>
<p class="w-lede">The Virginia Hospital & Healthcare Association — a statewide organization proving HMG’s work reaches far beyond campaigns.</p>
<div style="margin-top:28px">{proof("https://vhha.com/", "VISIT VHHA")}</div></div>
<div class="monitor" data-reveal><div class="row"><span>SCOPE</span><b>STATEWIDE</b></div><div class="row"><span>SECTOR</span><b>HEALTHCARE</b></div><div class="row"><span>STATE</span><b>VIRGINIA</b></div><div class="row" style="border:0"><span>RESULT</span><b>MEASURABLE GROWTH</b></div></div>
</div></section>
<section class="w-sec"><div class="wrap w-two">
<div><span class="w-kicker" style="color:#0E7C86">ADVOCACY, NOT JUST ELECTIONS · HOW WE HELP</span><h2 class="w-h2">A STATEWIDE VOICE FOR VIRGINIA HEALTHCARE</h2>
<p class="w-p">“Whether you’re a local business or a statewide organization like the Virginia Hospital & Healthcare Association, we deliver measurable growth.” The same strategy, creative and targeting that win campaigns move public opinion for associations and causes.</p></div>
<div class="chips" data-reveal><span>Advocacy campaigns</span><span>Digital advertising</span><span>Web design</span><span>Social media</span><span>Creative</span><span>Analytics & reporting</span></div>
</div></section>'''


def w_tx(c):
    pipes = '<svg class="pipes" viewBox="0 0 1200 800" preserveAspectRatio="none" aria-hidden="true"><path class="b" d="M-20 620 H420 V420 H820 V200 H1220"/><path d="M-20 620 H420 V420 H820 V200 H1220"/><path class="b" d="M-20 720 H620 V560 H1220"/><path d="M-20 720 H620 V560 H1220"/></svg>'
    ticks = ''.join(f'<line x1="150" y1="30" x2="150" y2="44" stroke="#F2E8D5" stroke-width="2" transform="rotate({a} 150 150)"/>' for a in range(-110, 111, 22))
    gauge = f'''<svg class="gauge" viewBox="0 0 300 220" data-reveal aria-hidden="true"><path d="M30 150 A120 120 0 1 1 270 150" fill="none" stroke="#2A2A2A" stroke-width="18"/><path d="M30 150 A120 120 0 1 1 270 150" fill="none" stroke="#FFB000" stroke-width="18" stroke-dasharray="300 600"/>{ticks}<g class="needle"><line x1="150" y1="150" x2="150" y2="48" stroke="#FFB000" stroke-width="5" stroke-linecap="round"/></g><circle cx="150" cy="150" r="12" fill="#FFB000"/><text x="150" y="205" text-anchor="middle" fill="#F2E8D5" font-size="18" font-weight="900" letter-spacing="3">10+ FORTUNE 500</text></svg>'''
    return f'''<section class="w-hero">{pipes}<div class="wrap w-two">
<div>{crumbs(c, '#FFB000')}<span class="w-kicker" style="color:#FFB000">TEXAS OIL & GAS ASSOCIATION</span>
<h1 class="w-title">UNDER<br><span>PRESSURE.</span></h1>
<p class="w-lede">Energy advocacy is part of HMG’s DNA — from the Texas Oil & Gas Association to more than ten Fortune 500 energy companies.</p>
<div style="margin-top:28px">{proof("https://www.txoga.org/", "VISIT TXOGA")}</div></div>
{gauge}</div></section>
<div class="hazard" aria-hidden="true"></div>
<section class="w-sec"><div class="wrap">
<span class="w-kicker" style="color:#FFB000">THE ENERGY FILE</span><h2 class="w-h2">ADVOCACY THAT MOVES AN INDUSTRY</h2>
<div class="w-facts">
<div class="plate" data-reveal><div class="w-fact" style="padding:0"><div class="n" style="color:#FFB000"><span data-count="10" data-suffix="+">0</span></div><div class="l">Fortune 500 energy companies</div></div></div>
<div class="plate" data-reveal><div class="w-fact" style="padding:0"><div class="n" style="color:#FFB000">TX</div><div class="l">HMG office in Texas</div></div></div>
<div class="plate" data-reveal><div class="w-fact" style="padding:0"><div class="n" style="color:#FFB000">GOV</div><div class="l">alumni now government affairs executives in oil & gas</div></div></div>
</div>
<p class="w-p" style="margin-top:30px;max-width:72ch">HMG has run digital operations for Fortune 500 companies, and several of its former team members have gone on to become Government Affairs Executives in the oil and gas industry.</p>
</div></section>'''


def w_dan(c):
    dome = '''<svg class="dome" viewBox="0 0 400 300" data-reveal aria-hidden="true"><line x1="200" y1="10" x2="200" y2="40"/><circle cx="200" cy="48" r="8"/><path d="M150 120 Q200 40 250 120"/><rect x="140" y="120" width="120" height="30"/><path d="M110 150 H290 L300 175 H100 Z"/><rect x="40" y="175" width="320" height="90"/><line x1="70" y1="175" x2="70" y2="265"/><line x1="110" y1="175" x2="110" y2="265"/><line x1="150" y1="175" x2="150" y2="265"/><line x1="250" y1="175" x2="250" y2="265"/><line x1="290" y1="175" x2="290" y2="265"/><line x1="330" y1="175" x2="330" y2="265"/><rect x="180" y="215" width="40" height="50"/><line x1="10" y1="290" x2="390" y2="290"/></svg>'''
    capitol = '<svg class="dp-skyline" viewBox="0 0 600 220" aria-hidden="true"><path d="M0 220 V180 H120 V150 H200 V120 H230 Q300 20 370 120 H400 V150 H480 V180 H600 V220 Z"/><rect x="292" y="0" width="16" height="40"/><circle cx="300" cy="44" r="10"/></svg>'
    return f'''<section class="w-hero"><div class="dp-fabric" aria-hidden="true"></div><div class="flagstar">{LONESTAR}</div><div class="dp-glow" aria-hidden="true"></div>{capitol}<div class="wrap"><div class="copy">
<span class="dp-ribbon" aria-hidden="true">EST. TEXAS · HMG</span>{crumbs(c, '#0E1B3D')}<span class="w-kicker" style="color:#002868">LIEUTENANT GOVERNOR OF TEXAS</span>
<h1 class="w-title">DAN<br>PATRICK</h1>
<p class="w-lede">A Texas client for a Texas firm. HMG’s roots run through the Lone Star State — from Governor Rick Perry’s presidential run to Senators John Cornyn and Ted Cruz.</p></div></div></section>
<section class="w-sec"><div class="wrap w-two">
<div>{dome}</div>
<div><span class="w-kicker" style="color:#BF0A30">THE LONE STAR STATE</span><h2 class="w-h2">BUILT IN TEXAS</h2>
<p class="w-p">HMG keeps an office in Texas and has represented some of the state’s most prominent Republicans — including Lieutenant Governor Dan Patrick.</p>
</div>
</div></section>'''


def w_palin(c):
    return f'''<section class="w-hero"><div class="stars2" aria-hidden="true"></div><div class="aurora"></div><div class="aurora a2" aria-hidden="true"></div><div class="moon" aria-hidden="true"></div><div class="snow"></div>
<div class="mount m0" aria-hidden="true"></div><div class="mount"></div><div class="mount m2"></div><div class="lake" aria-hidden="true"></div>
<div class="wrap">{crumbs(c, '#7FD7FF')}<span class="w-kicker" style="color:#7FD7FF">THE LAST FRONTIER · ALASKA</span>
<h1 class="w-title">SARAH<br>PALIN</h1>
<p class="w-lede">Engaging supporters for one of the most recognizable names in conservative politics.</p></div></section>
<section class="w-sec"><div class="wrap w-two">
<div class="glass" data-reveal><span class="w-kicker" style="color:#2EFFAA">THE MISSION</span><h2 class="w-h2" style="font-size:clamp(1.8rem,4vw,3rem)">CUT THROUGH THE NOISE</h2>
<p class="w-p">Whether it’s engaging supporters for Sarah Palin or helping a Super PAC win the industry’s top award, HMG helps candidates cut through the noise and connect with the right voters at the right time.</p></div>
<div class="w-facts">
<div class="w-fact glass" data-reveal><div class="n" style="color:#2EFFAA">FANS</div><div class="l">Supporter engagement</div></div>
<div class="w-fact glass" data-reveal><div class="n" style="color:#7FD7FF">REACH</div><div class="l">National audience</div></div>
<div class="w-fact glass" data-reveal><div class="n" style="color:#B39CFF">VOICE</div><div class="l">Messaging & creative</div></div>
</div></div></section>'''


def w_doug(c):
    return f'''<section class="w-hero"><div class="film t"></div><div class="film b"></div><div class="wrap w-two">
<div>{crumbs(c, '#FF9E5E')}<span class="rec"><i></i>REC · GEORGIA</span>
<h1 class="w-title">ROLL<br>TAPE.</h1>
<p class="w-lede">Video-first creative for Doug Collins of Georgia, built for social feeds.</p>
<div style="margin-top:28px">{proof("https://www.facebook.com/DougCollinsGeorgia/videos/258139055355254", "WATCH THE SPOT")}</div></div>
<div class="clap" aria-hidden="true"><div class="top"></div><div class="body"><div><b>CLIENT</b> DOUG COLLINS</div><div><b>STATE</b> GEORGIA</div><div><b>FORMAT</b> SOCIAL VIDEO</div><div><b>STUDIO</b> HMG</div></div></div>
</div></section>
<section class="w-sec"><div class="wrap">
<span class="w-kicker" style="color:#FF9E5E">NOW SHOWING</span><h2 class="w-h2">THE SPOT</h2>
<a class="screen" href="https://www.facebook.com/DougCollinsGeorgia/videos/258139055355254" target="_blank" rel="noopener" aria-label="Watch the Doug Collins video on Facebook" data-reveal>
<img src="{c['logo']}" alt="" loading="lazy"><span class="play"><svg viewBox="0 0 24 24" width="36" height="36" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span></a>
<p class="w-p" style="margin-top:22px;max-width:70ch">Filming, editing and social cuts — HMG’s video editors and videographers turn a message into content people actually watch and share.</p>
</div></section>'''



# ----------------------------------------------------------------------------- extended chapters
from extra import EXTRA, SV


def chapters(c):
    x = EXTRA[c['slug']]
    st = x['style']
    out = []
    # 1 marquee
    words = ''.join(f'<span>{e(t)}</span>' for t in x['marquee'] * 2)
    out.append(f'<div class="x-marq" aria-hidden="true"><div class="x-track">{words}{words}</div></div>')
    # 2 brief with parallax word
    k, title, paras = x['brief']
    out.append(f"""<section class="x-sec x-brief"><div class="x-big" data-px="-0.25" aria-hidden="true">{e(x['big'])}</div><div class="wrap x-brief-grid">
<div data-reveal><span class="x-kicker">{k}</span><h2 class="x-h2">{e(title)}</h2></div>
<div>{''.join(f'<p class="x-p" data-reveal>{e(p)}</p>' for p in paras)}</div></div></section>""")
    # 3 facts
    if x.get('facts'):
        out.append('<section class="x-sec x-tight"><div class="wrap"><div class="x-facts">' + ''.join(
            f'<div class="x-fact" data-reveal data-tilt><div class="n">{e(n)}</div><div class="l">{e(l)}</div></div>' for n, l in x['facts']) + '</div></div></section>')
    # 4 playbook
    steps = ''.join(f'<article class="x-step" data-reveal data-tilt><span class="x-num">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, (t, d) in enumerate(x['steps']))
    out.append(f"""<section class="x-sec x-play x-style-{st}"><div class="wrap">
<div class="x-head" data-reveal><span class="x-kicker">THE PLAYBOOK</span><h2 class="x-h2">WHAT WE DID</h2></div>
<div class="x-steps" data-reveal><div class="x-line"></div>{steps}</div></div></section>""")
    # 5 timeline
    if x.get('timeline'):
        tl = ''.join(f'<div class="x-tl-item" data-reveal><b>{e(y)}</b><h3>{e(t)}</h3><p>{e(d)}</p></div>' for y, t, d in x['timeline'])
        out.append(f'<section class="x-sec x-tl"><div class="wrap"><div class="x-head" data-reveal><span class="x-kicker">TIMELINE</span><h2 class="x-h2">THE STORY SO FAR</h2></div><div class="x-tl-row">{tl}</div></div></section>')
    # 6 quote
    if x.get('quote'):
        q, src = x['quote']
        out.append(f'<section class="x-sec x-quote"><div class="wrap"><blockquote data-reveal><p class="x-words">{e(q)}</p><cite>— {e(src)}</cite></blockquote></div></section>')
    # 7 services
    chips = ''.join(f'<a class="x-chip" href="services.html#{SV[s]}">{e(s)} <span aria-hidden="true">↗</span></a>' for s in x['services'])
    out.append(f'<section class="x-sec x-tight"><div class="wrap x-svc"><div data-reveal><span class="x-kicker">DISCIPLINES DEPLOYED</span><h2 class="x-h2" style="font-size:clamp(1.6rem,3.2vw,2.6rem)">THE HMG TEAM BEHIND IT</h2></div><div class="x-chips" data-reveal>{chips}</div></div></section>')
    # 8 closing statement (word-by-word reveal)
    out.append(f'<section class="x-sec x-close"><div class="wrap"><p class="x-words x-closing">{e(x["closing"])}</p></div></section>')
    return '\n'.join(out)


BUILDERS = {'right-for-america': ('w-rfa', w_rfa), 'netanyahu-likud': ('w-likud', w_likud), 'nh-senate-republicans': ('w-nh', w_nh),
            'francis-suarez': ('w-sos', w_sos), 'rand-paul': ('w-rand', w_rand), 'ted-cruz': ('w-cruz', w_cruz),
            'rick-scott': ('w-scott', w_scott), 'mike-huckabee': ('w-huck', w_huck), 'maine-gop': ('w-maine', w_maine),
            'linda-mcmahon': ('w-mcm', w_mcm), 'vhha': ('w-vhha', w_vhha), 'txoga': ('w-tx', w_tx), 'dan-patrick': ('w-dan', w_dan),
            'sarah-palin': ('w-palin', w_palin), 'doug-collins': ('w-doug', w_doug)}


def next_portal(n, suf=''):
    from finals import FINAL
    if n['slug'] in FINAL:
        suf = ''
    return f'''<a class="w-next" href="client-{n['slug']}{suf}.html" style="--next-bg:{n['bg']}">
<img src="{n['logo']}" alt="" loading="lazy"><div class="wrap"><div class="lbl">NEXT WORLD → {e(n['world'])}</div>
<span class="nm">{e(n['name'])}</span><span class="go">ENTER {ARR}</span></div></a>'''


def build(g):
    head, header, footer, cta, out_page = g['head'], g['header'], g['footer'], g['cta'], g['page']
    css = '<link rel="stylesheet" href="assets/hmg.css">'

    def wpage(fname, title, desc, body, body_class, image=None, versions=False, fonts=''):
        extra_css = '\n<link rel="stylesheet" href="assets/worlds.css">' + ('\n<link rel="stylesheet" href="assets/versions.css">\n<link rel="stylesheet" href="assets/versions2.css">\n<link rel="stylesheet" href="assets/batch1.css">\n<link rel="stylesheet" href="assets/batch2.css">\n<link rel="stylesheet" href="assets/finals.css">\n<link rel="stylesheet" href="assets/finals3.css">' if versions else '') + (fonts or '')
        h = head(title, desc, image).replace(css, css + extra_css)
        h = h.replace('<body>', f'<body class="world world-{body_class}{" has-vbar" if versions else ""}">')
        js = '<script src="assets/worlds.js" defer></script>' + ('<script src="assets/versions.js" defer></script><script src="assets/versions2.js" defer></script><script src="assets/batch1.js" defer></script><script src="assets/batch2.js" defer></script><script src="assets/finals.js" defer></script><script src="assets/finals3.js" defer></script>' if versions else '')
        html = h + header('clients') + body + footer(js)
        open(g['os'].path.join(g['OUT'], fname), 'w', encoding='utf-8').write(html)
        g['PAGES'].append(fname)

    # ------------------------------------------------------------ hub
    n = len(CLIENTS)
    cols = [CLIENTS[i::5] for i in range(5)]
    mosaic = ''.join('<div class="hm-col"><div class="hm-track">' + ''.join(
        f'<img src="{c["logo"]}" alt="" loading="lazy" style="--c:{c["c"]}">' for c in col * 2) + '</div></div>' for col in cols)
    spectrum = ''.join(f'<a href="client-{c["slug"]}.html" style="--c:{c["c"]};--i:{i}" title="{e(c["name"])}"><span>{e(c["name"])}</span></a>' for i, c in enumerate(CLIENTS))
    rows = ''.join(f'''<li data-cat="{c['cat']}" data-reveal><a href="client-{c['slug']}.html" style="--c:{c['c']};--ink:{c['ink']}" data-img="{c['logo']}" data-world="{e(c['world'])}">
<span class="rn">{i + 1:02d}</span><span class="nm">{e(c['name'])}</span><span class="wd">WORLD · {e(c['world'])}</span><span class="ct">{e(c['tag'])}</span><span class="ar">→</span><img class="th" src="{c['logo']}" alt="" loading="lazy"></a></li>'''
                   for i, c in enumerate(CLIENTS))
    cats = [('all', 'ALL'), ('presidential', 'PRESIDENTIAL'), ('federal', 'FEDERAL'), ('state', 'STATE'), ('international', 'INTERNATIONAL'), ('advocacy', 'ADVOCACY')]
    filt = ''.join(f'<button type="button" data-f="{k}"{_Q1 if k == "all" else ""}>{t}</button>' for k, t in cats)
    also = ['John Cornyn', 'Mitch McConnell', 'Rick Perry', 'Newt Gingrich', 'Bob McDonnell', 'Paul LePage', 'Bob Stefanowski', 'Fortune 500 energy companies']
    body = f'''<section class="hub-hero2">
<div class="hm" aria-hidden="true">{mosaic}</div><div class="hm-shade" aria-hidden="true"></div>
<div class="wrap hub-copy">
  <span class="label">WHO WE’VE WORKED WITH</span>
  <h1 class="hub-title"><span class="ln"><span>15 CLIENTS.</span></span><span class="ln"><span class="o">15 WORLDS.</span></span></h1>
  <p class="lede">Presidents, prime ministers, senators, governors and the causes behind them. Every client gets its own story — pick one and step inside.</p>
  <div class="hub-actions"><a class="btn btn-primary" href="#roster"><span class="blip"></span>ENTER THE ROSTER ↓</a><a class="btn btn-ghost" href="client-{CLIENTS[0]['slug']}.html">START THE TOUR →</a></div>
  <div class="spectrum" aria-label="Jump to a client">{spectrum}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="sec-head" data-reveal><div class="title"><span class="label">THE ROSTER</span><span class="sl">//</span><h2 class="h-md">CHOOSE A WORLD</h2></div><span class="meta"><span id="cl-count">00</span> CLIENTS</span></div>
<div class="filters hub-filter" data-filters="#roster" data-counter="#cl-count" role="group" aria-label="Filter clients">{filt}</div>
<ul class="roster" id="roster">{rows}</ul>
</div></section>
<div class="hub-preview" id="hub-preview" aria-hidden="true"><img alt="" src="{CLIENTS[0]["logo"]}"><div class="cap"></div></div>
<section class="section alt"><div class="wrap">
<div class="sec-head" data-reveal><div class="title"><span class="label">THE WAR ROOM</span><span class="sl">//</span><h2 class="h-md">BY THE NUMBERS</h2></div><span class="meta">GLOBALLY RECOGNIZED</span></div>
{g['stat_tiles']()}
</div></section>
<section class="section"><div class="wrap">
<div class="sec-head" data-reveal><div class="title"><span class="label">ALSO ON THE RECORD</span><span class="sl">//</span><h2 class="h-md">MORE LEADERS WE’VE SERVED</h2></div></div>
<div class="also" data-reveal>{''.join(f'<span>{e(a)}</span>' for a in also)}</div>
</div></section>
'''
    body += cta()
    wpage('clients.html', 'Our Clients | Harris Media Group', 'Fifteen clients, fifteen worlds: the leaders and causes Harris Media Group has helped win.', body, 'hub', UP + '2025/01/img-ai-suarez.png')

    # ------------------------------------------------------------ worlds
    for i, c in enumerate(CLIENTS):
        cls, fn = BUILDERS[c['slug']]
        nxt = CLIENTS[(i + 1) % n]
        title = f"{c['name']} — {c['world'].title()} | HMG Clients"
        desc = f"{c['name']}: {c['tag'].title()}. A Harris Media Group client story."
        import versions as V
        top = lambda v: V.vbar(c, v) + V.curtain(c, v)
        import pages2 as P2
        v1 = V.upgrade_v1(fn(c))
        bg, fg, a, a2, ink, *_ = V.THEME[c['slug']]
        sig = f'<div class="v1-sig" style="--sbg:{bg};--sfg:{fg};--sa:{a}">' + P2.particle_block(c, None, colors=f'{a},{a2},{fg}', font='900 200px "Barlow Semi Condensed", sans-serif') + '</div>'
        cut = v1.index('</section>') + len('</section>')
        v1 = v1[:cut] + sig + v1[cut:]
        import finals as FN
        if c['slug'] in FN.FINAL:
            html_f, fonts = FN.build_final(c, i, n, cls, fn)
            body = V.curtain(c, 1).replace('class="v-curtain"', f'class="v-curtain cv-{FN.FINAL[c["slug"]]["cur"]}"') + html_f + next_portal(nxt) + '</div></div>' + cta()
            wpage(f"client-{c['slug']}.html", title, desc, body, cls + ' is-final', c['logo'], versions=True, fonts=fonts)
            continue
        body = top(1) + f'<div class="{cls}" style="--hot:{a}">' + v1 + chapters(c) + next_portal(nxt) + '</div>' + cta()
        wpage(f"client-{c['slug']}.html", title, desc, body, cls, c['logo'], versions=True)
        for vv in (2, 3):
            html_v, fonts = P2.build_version(c, vv, i, n)
            body = top(vv) + html_v + next_portal(nxt, f'-v{vv}') + '</div>' + cta()
            wpage(f"client-{c['slug']}-v{vv}.html", title.replace(' | ', f' · Version {vv} | '), desc, body, cls + f'-v{vv}', c['logo'], versions=True, fonts=fonts)
