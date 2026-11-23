"""Visual de cada cena do audiovisual (HTML, CSS e animação GSAP).

Cada função cenaN() devolve (html, css, js). No JS estão disponíveis:
  F  -> [[início, fim], ...] de cada fala da cena, em segundos locais
  D  -> duração total da cena
  T(i, f) -> instante na fala i, na fração f (0 = começo, 1 = fim)
  entra / pop / sai / escurece / fala / balao / moldura -> atalhos de animação
Estilo: "caderno de economia" — azul = FATO, laranja = VALOR.
"""

CSS_BASE = r"""
@font-face { font-family: "Fraunces"; src: url("assets/fonts/fraunces.woff2") format("woff2"); font-weight: 100 900; font-display: block; }
@font-face { font-family: "Inter"; src: url("assets/fonts/inter.woff2") format("woff2"); font-weight: 100 900; font-display: block; }
@font-face { font-family: "Caveat"; src: url("assets/fonts/caveat.woff2") format("woff2"); font-weight: 400 700; font-display: block; }
:root {
  --papel: #f4eee2; --linha: #e4d9c3; --margem: #e7a495; --tinta: #1d2433; --suave: #5f6675;
  --fato: #1f6fb2; --valor: #d66b29; --verde: #2f8a74; --roxo: #6b4fa3; --mostarda: #b8892a;
  --cartao: #fffdf8; --borda: #d9cfbb;
  --infra: #5b6b82; --saude: #2f8a74; --educ: #6b4fa3; --renda: #b8892a;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1920px; height: 1080px; overflow: hidden; background: var(--papel); }
#root { position: relative; width: 1920px; height: 1080px; font-family: "Inter", sans-serif; color: var(--tinta); }
#papel { position: absolute; inset: 0;
  background:
    linear-gradient(90deg, transparent 99px, var(--margem) 99px, var(--margem) 101px, transparent 101px),
    repeating-linear-gradient(180deg, transparent 0 53px, var(--linha) 53px 54px),
    var(--papel); }
.cena-host { position: absolute; inset: 0; }
.cena { position: absolute; inset: 0; }
.abs { position: absolute; }
.h { opacity: 0; }
.titulo { font-family: "Fraunces", serif; font-weight: 800; letter-spacing: -0.02em; line-height: 1.08; }
.mao { font-family: "Caveat", cursive; font-weight: 600; line-height: 1; }
.centro { left: 0; right: 0; text-align: center; }
.cartao { background: var(--cartao); border: 2px solid var(--borda); border-radius: 22px; box-shadow: 0 8px 0 rgba(29,36,51,.08); }
.fato { color: var(--fato); } .valor { color: var(--valor); } .suave { color: var(--suave); }
.selo { display: inline-block; padding: 8px 22px; border-radius: 99px; font-weight: 800; font-size: 28px; letter-spacing: .06em; color: #fff; background: var(--tinta); }
.selo.fato { background: var(--fato); color: #fff; } .selo.valor { background: var(--valor); color: #fff; }
.balao { position: absolute; background: #fff; border: 3px solid var(--tinta); border-radius: 28px; padding: 18px 26px;
  font-size: 34px; font-weight: 600; line-height: 1.25; box-shadow: 0 6px 0 rgba(29,36,51,.12); }
.balao::after { content: ""; position: absolute; bottom: -18px; width: 30px; height: 30px; background: #fff;
  border-right: 3px solid var(--tinta); border-bottom: 3px solid var(--tinta); transform: rotate(45deg); }
.balao.esq::after { left: 70px; } .balao.dir::after { right: 70px; }
.balao .quem { display: block; font-size: 28px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 4px; }
.pessoa { position: absolute; }
.pessoa svg { display: block; width: 100%; height: auto; }
.pessoa .nome { margin-top: 6px; text-align: center; font-size: 28px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
.ficticio { position: absolute; right: 70px; top: 36px; background: var(--tinta); color: #fff; font-weight: 800; font-size: 28px;
  letter-spacing: .1em; padding: 8px 16px; border-radius: 8px; }
.opcao { position: absolute; border-radius: 18px; background: var(--cartao); border: 2px solid var(--borda); display: flex; align-items: center;
  gap: 18px; padding: 0 24px; font-weight: 800; font-size: 28px; letter-spacing: .04em; box-shadow: 0 6px 0 rgba(29,36,51,.08); }
.opcao i { display: block; width: 18px; align-self: stretch; margin: 18px 0; border-radius: 9px; }
/* legendas */
.lg-area { position: absolute; left: 0; right: 0; bottom: 30px; height: 160px; }
.lg { position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); width: max-content; max-width: 1560px;
  background: rgba(255,253,248,.97); border: 2px solid var(--borda); border-radius: 18px; padding: 10px 30px 14px; text-align: center;
  opacity: 0; box-shadow: 0 6px 0 rgba(29,36,51,.08); }
.lg-quem { display: block; font-size: 28px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
.lg-txt { display: block; font-size: 36px; font-weight: 600; line-height: 1.25; }
"""

HELPERS = r"""
        const q = (s) => root.querySelector(s);
        const qa = (s) => Array.from(root.querySelectorAll(s));
        const el = (t) => (typeof t === "string" ? qa(t) : Array.isArray(t) ? t : [t]);
        const T = (i, f = 0) => F[i][0] + f * (F[i][1] - F[i][0]);
        const tl = gsap.timeline({ paused: true });
        function entra(t, at, de = { y: 30 }, dur = 0.6) {
          tl.fromTo(el(t), { opacity: 0, ...de }, { opacity: 1, x: 0, y: 0, duration: dur, ease: "power3.out" }, at);
        }
        function serie(t, at, gap = 0.18, de = { y: 30 }) { el(t).forEach((x, k) => entra(x, at + k * gap, de)); }
        function pop(t, at, dur = 0.5) {
          tl.fromTo(el(t), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: dur, ease: "back.out(1.7)" }, at);
        }
        function sai(t, at, dur = 0.4) { tl.to(el(t), { opacity: 0, duration: dur, ease: "power2.in" }, at); }
        function escurece(t, at, o = 0.25, dur = 0.5) { tl.to(el(t), { opacity: o, duration: dur, ease: "power1.inOut" }, at); }
        function fala(t, i) {
          const n = Math.max(1, Math.floor((F[i][1] - F[i][0]) / 0.5));
          tl.to(el(t), { y: -7, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, F[i][0]);
        }
        function balao(t, i, ate) { pop(t, T(i)); sai(t, ate === undefined ? F[i][1] + 0.3 : ate); }
        function moldura(entrada = true) {
          const c = q(".cena");
          if (entrada) tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.out" }, 0);
          tl.to(c, { opacity: 0, duration: 0.5, ease: "power1.in" }, D - 0.5);
          tl.fromTo(c, { scale: 1 }, { scale: 1.035, duration: D, ease: "none", transformOrigin: "50% 45%" }, 0);
          tl.set({}, {}, D);
        }
"""

# ---------- personagens (ilustração plana) ----------
_ECON = """<svg viewBox="0 0 200 260"><path d="M14 260 C14 186 54 160 100 160 C146 160 186 186 186 260Z" fill="#1f6fb2"/>
<path d="M78 162 L100 214 L122 162Z" fill="#fff"/><path d="M95 172 L105 172 L109 226 L100 238 L91 226Z" fill="#1d2433"/>
<rect x="86" y="128" width="28" height="36" rx="10" fill="#c98e64"/><circle cx="100" cy="94" r="52" fill="#c98e64"/>
<path d="M46 96 C44 50 74 36 102 36 C134 36 156 54 154 94 C142 70 122 60 100 62 C80 64 60 74 46 96Z" fill="#2b2b33"/>
<circle cx="80" cy="100" r="14" fill="#fff" fill-opacity=".35" stroke="#1d2433" stroke-width="4"/><circle cx="120" cy="100" r="14" fill="#fff" fill-opacity=".35" stroke="#1d2433" stroke-width="4"/>
<line x1="94" y1="100" x2="106" y2="100" stroke="#1d2433" stroke-width="4"/><circle cx="80" cy="101" r="3.5" fill="#1d2433"/><circle cx="120" cy="101" r="3.5" fill="#1d2433"/>
<path d="M88 126 Q100 134 112 126" stroke="#1d2433" stroke-width="4" fill="none" stroke-linecap="round"/></svg>"""

_CID = """<svg viewBox="0 0 200 260"><path d="M14 260 C14 186 54 160 100 160 C146 160 186 186 186 260Z" fill="#d66b29"/>
<path d="M76 162 Q100 186 124 162" stroke="#b9551b" stroke-width="6" fill="none"/>
<rect x="86" y="128" width="28" height="36" rx="10" fill="#8d5a3b"/><circle cx="100" cy="94" r="52" fill="#8d5a3b"/>
<circle cx="62" cy="62" r="20" fill="#1d1a1a"/><circle cx="86" cy="46" r="22" fill="#1d1a1a"/><circle cx="114" cy="46" r="22" fill="#1d1a1a"/>
<circle cx="138" cy="62" r="20" fill="#1d1a1a"/><circle cx="100" cy="40" r="18" fill="#1d1a1a"/>
<circle cx="80" cy="101" r="5" fill="#1d1a1a"/><circle cx="120" cy="101" r="5" fill="#1d1a1a"/>
<path d="M72 86 L88 84" stroke="#1d1a1a" stroke-width="4" stroke-linecap="round"/><path d="M112 82 L128 86" stroke="#1d1a1a" stroke-width="4" stroke-linecap="round"/>
<path d="M90 126 Q100 130 110 126" stroke="#1d1a1a" stroke-width="4" fill="none" stroke-linecap="round"/></svg>"""

_GENTE = """<svg viewBox="0 0 100 130"><circle cx="50" cy="32" r="24" fill="{c}"/><path d="M8 130 C8 84 26 64 50 64 C74 64 92 84 92 130Z" fill="{c}"/></svg>"""


def pessoa(tipo, pid, left, top, w, nome=True, h=True):
    svg = _ECON if tipo == "ec" else _CID
    rot = ('<div class="nome" style="color:%s">%s</div>' % (("var(--fato)", "Economista") if tipo == "ec" else ("#c2541c", "Cidadão"))) if nome else ""
    return f'<div class="pessoa{" h" if h else ""}" id="{pid}" style="left:{left}px;top:{top}px;width:{w}px">{svg}{rot}</div>'


def gente(cor, extra=""):
    return _GENTE.format(c=cor) if not extra else _GENTE.format(c=cor).replace("<svg", f"<svg {extra}")


def balao(bid, quem, texto, left, top, w, lado="esq"):
    cor = "var(--fato)" if quem == "Economista" else "#c2541c" if quem == "Cidadão" else "var(--suave)"
    return (f'<div class="balao {lado} h" id="{bid}" style="left:{left}px;top:{top}px;width:{w}px">'
            f'<span class="quem" style="color:{cor}">{quem}</span>{texto}</div>')


def opcao(oid, nome, cor, left, top, w, h=110, extra_cls="h"):
    return f'<div class="opcao {extra_cls}" id="{oid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px"><i style="background:{cor}"></i>{nome}</div>'


# =====================================================================
def cena1():
    chips = [("crescimento", 210, 120, 46), ("PIB", 820, 90, 64), ("custo", 1500, 140, 52), ("eficiência", 300, 560, 58),
             ("R$", 1640, 470, 70), ("meta fiscal", 1180, 650, 44), ("%", 1560, 690, 80), ("produtividade", 1150, 220, 46),
             ("juros", 820, 720, 50), ("orçamento", 170, 760, 42)]
    h = "".join(f'<div class="abs titulo s1-chip{" h" if k >= 3 else ""}" style="left:{x}px;top:{y}px;font-size:{fs}px;color:{"var(--fato)" if k % 3 == 0 else "var(--tinta)"}">{t}</div>'
                for k, (t, x, y, fs) in enumerate(chips))
    h += """
<div id="s1-quote" class="abs titulo centro h" style="top:330px;font-size:88px"><span class="valor">“</span>a escolha economicamente correta<span class="valor">”</span></div>
<div id="s1-q2" class="abs centro h" style="top:500px;font-size:40px;font-weight:700"><span class="selo fato" style="font-size:36px">DESCREVE O MUNDO?</span>
  <span style="margin:0 24px" class="suave">ou</span><span class="selo valor" style="font-size:36px">DECIDE POR NÓS?</span></div>
<div id="s1-int" class="abs titulo centro valor h" style="top:-60px;font-size:900px;line-height:1">?</div>
<div id="s1-tit" class="abs titulo centro h" style="left:200px;right:200px;top:300px;font-size:116px">Quando a economia diz o que <span class="valor">devemos</span> fazer?</div>
<div id="s1-sub" class="abs centro h" style="top:640px;font-size:30px;letter-spacing:.24em;font-weight:800;color:var(--suave)">ÉTICA E CIÊNCIA ECONÔMICA</div>
"""
    js = r"""
        moldura(false);
        const chips = qa(".s1-chip");
        const rot = [-6, 4, -3, 7, -5, 3, -8, 5, -2, 6];
        chips.forEach((c, k) => {
          tl.set(c, { rotation: rot[k] }, 0);
          if (k < 3) tl.set(c, { opacity: 1 }, 0);
          else entra(c, 0.3 + (k - 3) * 0.55, { y: -50 });
        });
        tl.to(chips, { opacity: 0.16, duration: 0.8 }, T(0, 0.4));
        pop("#s1-quote", T(0, 0.42));
        entra("#s1-q2", T(0, 0.74));
        sai(["#s1-quote", "#s1-q2"], F[1][0] - 0.2);
        sai(chips, F[1][0]);
        tl.fromTo(q("#s1-int"), { opacity: 0, scale: 0.4 }, { opacity: 0.1, scale: 1, duration: 0.9, ease: "power3.out" }, T(1, 0.05));
        entra("#s1-tit", T(1, 0.2), { y: 40 }, 0.9);
        entra("#s1-sub", T(1, 0.6));
"""
    return h, "", js


# =====================================================================
def cena2():
    seg_a = [8, 12, 16, 22, 42]
    seg_d = [5, 8, 12, 19, 56]
    cores = ["#c9d6e6", "#a7bfdc", "#7fa3cf", "#4f81bd", "#1f6fb2"]
    barra = lambda segs, bid: (f'<div id="{bid}" style="display:flex;height:64px;border-radius:12px;overflow:hidden;width:640px">'
                               + "".join(f'<div style="width:{s}%;background:{c}"></div>' for s, c in zip(segs, cores)) + "</div>")
    h = pessoa("ec", "s2-ec", 150, 420, 300) + pessoa("cid", "s2-ci", 1470, 420, 300)
    h += f"""
<div id="s2-quadro" class="abs cartao h" style="left:560px;top:110px;width:800px;height:620px;padding:34px 40px">
  <div class="mao suave" style="font-size:44px">proposta: política X</div>
  <div id="s2-fase1" class="abs" style="left:40px;right:40px;top:110px;height:470px">
    <div class="abs" style="left:150px;bottom:60px;width:160px;height:250px;background:#a7bfdc;border-radius:12px 12px 0 0;transform-origin:bottom" id="s2-b1"></div>
    <div class="abs" style="left:410px;bottom:60px;width:160px;height:310px;background:var(--fato);border-radius:12px 12px 0 0;transform-origin:bottom" id="s2-b2"></div>
    <div class="abs" style="left:150px;bottom:14px;width:160px;text-align:center;font-weight:700;font-size:26px">antes</div>
    <div class="abs" style="left:410px;bottom:14px;width:160px;text-align:center;font-weight:700;font-size:26px">depois</div>
    <div class="abs titulo fato h" id="s2-mais" style="left:400px;top:0;font-size:46px">+ riqueza</div>
    <div class="abs suave" style="left:0;top:6px;font-size:30px;font-weight:700">renda total do país</div>
  </div>
  <div id="s2-fase2" class="abs h" style="left:40px;right:40px;top:120px">
    <div style="font-size:28px;font-weight:700" class="suave">como a renda se divide (cada faixa = 20% das pessoas)</div>
    <div style="margin-top:34px;font-weight:700;font-size:26px">antes</div>{barra(seg_a, "s2-ba")}
    <div style="margin-top:30px;font-weight:700;font-size:26px">depois</div>{barra(seg_d, "s2-bd")}
    <div style="display:flex;justify-content:space-between;width:640px;margin-top:14px;font-size:28px;font-weight:700" class="suave"><span>20% mais pobres</span><span>20% mais ricos →</span></div>
    <div class="titulo valor" style="font-size:42px;margin-top:26px">+ desigualdade</div>
  </div>
  <div class="abs mao suave" style="right:30px;bottom:18px;font-size:30px">números ilustrativos</div>
</div>
{balao("s2-bal0", "Economista", "A economia cresce, a riqueza aumenta!", 80, 140, 440)}
{balao("s2-bal1", "Cidadão", "E quem fica com essa riqueza?", 1400, 150, 440, "dir")}
{balao("s2-bal2", "Economista", "A desigualdade aumenta… mas, no agregado, todos <i>poderiam</i> estar melhor.", 80, 90, 460)}
{balao("s2-bal3", "Cidadão", '<span class="titulo valor" style="font-size:52px">Eficiente para quem?</span>', 1380, 140, 480, "dir")}
<div id="s2-n" class="abs cartao h" style="left:420px;right:420px;top:200px;padding:56px 40px;text-align:center">
  <div class="titulo s2-n" style="font-size:66px">Riqueza maior,<br>desigualdade maior.</div>
  <div class="titulo valor s2-n" style="font-size:76px;margin-top:24px">É uma boa política?</div>
  <div class="s2-n suave" style="font-size:34px;margin-top:26px;font-weight:600">Os números não respondem sozinhos.</div>
</div>
"""
    js = r"""
        moldura();
        entra("#s2-ec", 0.2, { x: -120 }); entra("#s2-ci", 0.5, { x: 120 });
        pop("#s2-quadro", 0.8);
        tl.fromTo(el("#s2-b1"), { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "power2.out" }, T(0, 0.1));
        tl.fromTo(el("#s2-b2"), { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power2.out" }, T(0, 0.45));
        pop("#s2-mais", T(0, 0.7));
        balao("#s2-bal0", 0, F[1][0]); fala("#s2-ec", 0);
        balao("#s2-bal1", 1, F[2][0]); fala("#s2-ci", 1);
        sai("#s2-fase1", T(2, 0.05)); entra("#s2-fase2", T(2, 0.15));
        tl.fromTo(el(["#s2-ba", "#s2-bd"]), { scaleX: 0, transformOrigin: "left center" }, { scaleX: 1, duration: 0.8, stagger: 0.6, ease: "power2.out" }, T(2, 0.2));
        balao("#s2-bal2", 2, F[3][0]); fala("#s2-ec", 2);
        balao("#s2-bal3", 3, F[4][0] + 0.2); fala("#s2-ci", 3);
        tl.to(el("#s2-bal3"), { scale: 1.08, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }, T(3, 0.8));
        escurece(["#s2-ec", "#s2-ci", "#s2-quadro"], F[4][0], 0.15);
        entra("#s2-n", T(4, 0.0));
        tl.set(el(".s2-n"), { opacity: 0 }, 0);
        serie(".s2-n", T(4, 0.05), (F[4][1] - F[4][0]) * 0.33);
"""
    return h, "", js


# =====================================================================
def cena3():
    h = f"""
<div id="s3-fato" class="abs cartao h" style="left:170px;top:80px;width:760px;height:300px;border:4px solid var(--fato);padding:34px 40px">
  <span class="selo fato">FATO · o que é</span>
  <div class="titulo" style="font-size:54px;margin-top:26px">“A política aumenta<br>o PIB em X%.”</div>
  <div id="s3-test" class="abs h mao fato" style="right:36px;bottom:24px;font-size:46px">testável com dados ✔</div>
</div>
<div id="s3-valor" class="abs cartao h" style="left:990px;top:80px;width:760px;height:300px;border:4px solid var(--valor);padding:34px 40px">
  <span class="selo valor">VALOR · o que deve ser</span>
  <div class="titulo" style="font-size:54px;margin-top:26px">“Devemos<br>escolhê-la?”</div>
  <div id="s3-dep" class="abs h mao valor" style="right:36px;bottom:24px;font-size:46px">depende do que valorizamos</div>
</div>
<div id="s3-vals" class="abs centro" style="top:450px">
  {"".join(f'<span class="selo valor s3-v h" style="margin:0 12px;font-size:32px">{v}</span>' for v in ["crescimento", "igualdade", "liberdade", "segurança"])}
</div>
<div id="s3-pos" class="abs h titulo fato" style="left:170px;width:760px;top:400px;text-align:center;font-size:40px">economia POSITIVA <span class="suave" style="font-family:Inter;font-weight:600;font-size:32px">· descreve</span></div>
<div id="s3-nor" class="abs h titulo valor" style="left:990px;width:760px;top:400px;text-align:center;font-size:40px">economia NORMATIVA <span class="suave" style="font-family:Inter;font-weight:600;font-size:32px">· prescreve</span></div>
<div id="s3-hume" class="abs h" style="left:0;right:0;top:500px;height:240px">
  <div class="abs cartao titulo fato" style="left:520px;top:20px;width:250px;height:150px;font-size:92px;display:flex;align-items:center;justify-content:center;border:4px solid var(--fato)">É</div>
  <svg class="abs" style="left:800px;top:50px" width="320" height="90" viewBox="0 0 320 90"><line x1="10" y1="45" x2="290" y2="45" stroke="#1d2433" stroke-width="8" stroke-dasharray="20 14"/><path d="M280 20 L312 45 L280 70" fill="none" stroke="#1d2433" stroke-width="8"/>
    <g id="s3-x"><line x1="125" y1="10" x2="195" y2="80" stroke="#d66b29" stroke-width="14" stroke-linecap="round"/><line x1="195" y1="10" x2="125" y2="80" stroke="#d66b29" stroke-width="14" stroke-linecap="round"/></g></svg>
  <div class="abs cartao titulo valor" style="left:1150px;top:20px;width:290px;height:150px;font-size:80px;display:flex;align-items:center;justify-content:center;border:4px solid var(--valor)">DEVE</div>
  <div class="abs centro suave" style="top:196px;font-size:28px;font-weight:700">David Hume · <i>Tratado da Natureza Humana</i> (1739–1740)</div>
</div>
{pessoa("ec", "s3-ec", 260, 500, 230)}
{balao("s3-b3", "Economista", "Eu mostro as consequências; quem decide são os outros.", 540, 470, 520)}
{pessoa("cid", "s3-ci", 1430, 500, 230)}
{balao("s3-b4", "Cidadão", "Será? Vamos ver se é tão simples assim.", 1000, 530, 400, "dir")}
"""
    js = r"""
        moldura();
        entra("#s3-fato", T(0, 0), { x: -60 });
        pop("#s3-test", T(0, 0.62));
        entra("#s3-valor", T(1, 0), { x: 60 });
        pop("#s3-dep", T(1, 0.45));
        serie(".s3-v", T(1, 0.6), 0.35);
        sai(".s3-v", F[2][0]);
        entra("#s3-hume", T(2, 0.05));
        tl.fromTo(el("#s3-x"), { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T(2, 0.3));
        entra(["#s3-pos"], T(2, 0.66)); entra(["#s3-nor"], T(2, 0.78));
        sai("#s3-hume", F[3][0] - 0.1);
        entra("#s3-ec", F[3][0], { x: -80 }); balao("#s3-b3", 3, D); fala("#s3-ec", 3);
        entra("#s3-ci", F[4][0] - 0.1, { x: 80 }); balao("#s3-b4", 4, D); fala("#s3-ci", 4);
"""
    return h, "", js


# =====================================================================
def cena4():
    ex = [("costumes", "fazer fila"), ("regras", "respeitar o sinal"), ("convicções", "cuidar da família")]
    cards = "".join(f'''<div class="abs cartao s4-c h" style="left:{170 + k * 280}px;top:360px;width:250px;height:220px;padding:26px 22px">
  <div style="font-size:28px;font-weight:800;letter-spacing:.08em;text-transform:uppercase" class="suave">{a}</div>
  <div class="mao" style="font-size:50px;margin-top:22px">{b}</div></div>''' for k, (a, b) in enumerate(ex))
    h = f"""
<div id="s4-moral" class="abs h" style="left:170px;top:110px">
  <div class="titulo" style="font-size:130px">Moral</div>
  <div class="mao suave" style="font-size:52px;margin-top:6px">valores vividos no dia a dia</div>
</div>
{cards}
<div id="s4-div" class="abs h" style="left:1040px;top:110px;width:4px;height:640px;background:var(--borda)"></div>
<div id="s4-etica" class="abs h" style="left:1120px;top:110px">
  <div class="titulo valor" style="font-size:130px">Ética</div>
  <div class="mao suave" style="font-size:52px;margin-top:6px">reflexão sobre esses valores</div>
</div>
{"".join(f'<div class="abs titulo s4-q h" style="left:1130px;top:{360 + k * 86}px;font-size:52px">{t}</div>' for k, t in enumerate(["por que seguimos?", "faz sentido?", "a quem serve?"]))}
<svg id="s4-lupa" class="abs h" style="left:1500px;top:330px" width="220" height="240" viewBox="0 0 220 240">
  <circle cx="90" cy="90" r="72" fill="#fff" fill-opacity=".35" stroke="#d66b29" stroke-width="14"/><line x1="142" y1="142" x2="205" y2="225" stroke="#d66b29" stroke-width="22" stroke-linecap="round"/></svg>
<div id="s4-ef" class="abs h" style="left:1120px;top:650px;display:flex;align-items:center;gap:22px">
  <div class="balao" style="position:relative;font-size:40px"><span class="titulo valor">Eficiente para quem?</span></div>
  <span class="selo valor" style="font-size:30px">É ÉTICA</span></div>
"""
    js = r"""
        moldura();
        entra("#s4-moral", 0.3);
        serie(".s4-c", T(0, 0.3), 0.45);
        entra("#s4-div", F[1][0] - 0.3, { y: 0 });
        entra("#s4-etica", T(1, 0), { x: 40 });
        entra("#s4-lupa", T(1, 0.08), { x: 60 });
        tl.to(el("#s4-lupa"), { x: -1270, y: 20, duration: 1.2, ease: "power2.inOut" }, T(1, 0.14));
        tl.to(el("#s4-lupa"), { x: -990, duration: 0.8, ease: "power2.inOut" }, T(1, 0.28));
        tl.to(el("#s4-lupa"), { x: -710, duration: 0.8, ease: "power2.inOut" }, T(1, 0.40));
        tl.to(el("#s4-lupa"), { x: 0, y: 0, opacity: 0, duration: 0.8, ease: "power2.in" }, T(1, 0.52));
        serie(".s4-q", T(1, 0.16), (F[1][1] - F[1][0]) * 0.12);
        pop("#s4-ef", T(1, 0.6));
"""
    return h, "", js


# =====================================================================
def cena5():
    nomes = ["ALIMENTAÇÃO", "MORADIA", "SAÚDE", "CELULAR", "VIAGEM"]
    cards = "".join(f'<div class="abs cartao s5-c h" id="s5-c{k}" style="left:{370 + k * 240}px;top:90px;width:226px;height:100px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px;letter-spacing:0">{n}</div>'
                    for k, n in enumerate(nomes))
    h = pessoa("ec", "s5-ec", 70, 470, 230) + pessoa("cid", "s5-ci", 1620, 470, 230) + cards + f"""
<div id="s5-cols" class="abs h" style="left:400px;top:250px;width:1120px;height:580px">
  <div class="abs titulo verde" style="left:0;width:540px;top:0;text-align:center;font-size:46px;color:var(--verde)">necessidade</div>
  <div class="abs titulo" style="left:580px;width:540px;top:0;text-align:center;font-size:46px;color:var(--roxo)">desejo</div>
  <div id="s5-linha" class="abs" style="left:558px;top:0;width:0;height:480px;border-left:6px dashed var(--borda)"></div>
</div>
{"".join(f'<div class="abs mao s5-u h" style="left:{x}px;top:{y}px;font-size:44px;color:#c2541c">{t}</div>' for t, x, y in [("emprego", 980, 196), ("escola", 1140, 196), ("banco", 1280, 196)])}
<div id="s5-quem" class="abs titulo valor h" style="left:760px;width:400px;top:760px;text-align:center;font-size:60px">quem decide?</div>
{balao("s5-b0", "Cidadão", "Mas o que é uma necessidade?", 1420, 230, 440, "dir")}
{balao("s5-b1", "Economista", "Alimentação, moradia, saúde.", 40, 250, 400)}
{balao("s5-b2", "Cidadão", "E o celular? Sem ele não procuro emprego…", 1420, 200, 440, "dir")}
{balao("s5-b3", "Economista", "Hum… talvez seja uma necessidade.", 40, 250, 400)}
{balao("s5-b4", "Cidadão", "E uma viagem de férias?", 1420, 250, 440, "dir")}
{balao("s5-b5", "Economista", "Aí já é um desejo.", 40, 280, 380)}
{balao("s5-b6", "Cidadão", "Para quem? Quem decide?", 1420, 250, 440, "dir")}
"""
    js = r"""
        moldura();
        entra("#s5-ec", 0.2, { x: -80 }); entra("#s5-ci", 0.4, { x: 80 });
        serie(".s5-c", T(0, 0.1), 0.25, { y: -40 });
        entra("#s5-cols", T(0, 0.7));
        const voz = ["#s5-ci", "#s5-ec", "#s5-ci", "#s5-ec", "#s5-ci", "#s5-ec", "#s5-ci"];
        for (let i = 0; i < 7; i++) { balao("#s5-b" + i, i, i < 6 ? F[i + 1][0] - 0.05 : D); fala(voz[i], i); }
        const vai = (k, left, top, at) => tl.to(el("#s5-c" + k), { x: left - (370 + k * 240), y: top - 90, duration: 0.8, ease: "power3.inOut" }, at);
        vai(0, 460, 360, T(1, 0.05)); vai(1, 460, 490, T(1, 0.35)); vai(2, 460, 620, T(1, 0.65));
        tl.to(el("#s5-c3"), { borderColor: "#d66b29", scale: 1.08, duration: 0.3 }, T(2, 0));
        serie(".s5-u", T(2, 0.4), 0.35, { y: 10 });
        sai(".s5-u", F[3][0]);
        tl.to(el("#s5-c3"), { x: 847 - 1090, y: 480 - 90, scale: 1, duration: 0.9, ease: "power3.inOut" }, T(3, 0));
        for (let k = 0; k < 4; k++) tl.to(el("#s5-c3"), { rotation: k % 2 ? 5 : -5, duration: 0.35, ease: "sine.inOut" }, T(3, 0.4) + k * 0.35);
        tl.to(el("#s5-c3"), { rotation: 0, duration: 0.3 }, T(3, 0.4) + 1.4);
        tl.to(el("#s5-c4"), { borderColor: "#d66b29", scale: 1.08, duration: 0.3 }, T(4, 0));
        tl.to(el("#s5-c4"), { x: 1100 - 1330, y: 360 - 90, scale: 1, duration: 0.8, ease: "power3.inOut" }, T(5, 0));
        tl.to(el("#s5-linha"), { borderColor: "#d66b29", duration: 0.4 }, T(6, 0.2));
        pop("#s5-quem", T(6, 0.35));
"""
    return h, "", js


# =====================================================================
def cena6():
    h = f"""
<div id="s6-k0" class="abs cartao h" style="left:150px;top:90px;width:500px;height:330px;padding:34px;border-top:16px solid var(--verde)">
  <div class="titulo" style="font-size:50px;color:var(--verde)">Necessidades</div>
  <div style="font-size:31px;margin-top:20px;font-weight:600;line-height:1.35">condições para viver com <b>dignidade</b> numa sociedade e numa época</div></div>
<div id="s6-k1" class="abs cartao h" style="left:710px;top:90px;width:500px;height:330px;padding:34px;border-top:16px solid var(--roxo)">
  <div class="titulo" style="font-size:50px;color:var(--roxo)">Desejos</div>
  <div style="font-size:31px;margin-top:20px;font-weight:600;line-height:1.35">moldados pela <b>cultura</b>, pela <b>publicidade</b>, pelo que parece normal</div></div>
<div id="s6-k2" class="abs cartao h" style="left:1270px;top:90px;width:500px;height:330px;padding:34px;border-top:16px solid var(--fato)">
  <div class="titulo fato" style="font-size:50px">Demanda</div>
  <div style="font-size:31px;margin-top:20px;font-weight:600;line-height:1.35">desejo <b>+ poder de compra</b></div>
  <svg class="abs" style="right:34px;bottom:30px" width="120" height="90" viewBox="0 0 120 90"><rect x="4" y="14" width="112" height="72" rx="12" fill="#1f6fb2"/><rect x="70" y="36" width="46" height="28" rx="8" fill="#a7bfdc"/><circle cx="86" cy="50" r="6" fill="#1f6fb2"/></svg></div>
<div id="s6-smith" class="abs cartao h" style="left:330px;right:330px;top:480px;padding:30px 40px;text-align:center">
  <div class="titulo" style="font-size:48px">Adam Smith: <span class="fato">“demanda efetiva”</span></div>
  <div style="font-size:30px;margin-top:12px;font-weight:600" class="suave">a demanda de quem pode pagar · <i>A Riqueza das Nações</i> (1776), Livro I, cap. 7</div></div>
<svg id="s6-graf" class="abs h" style="left:220px;top:90px" width="820" height="620" viewBox="0 0 820 620">
  <line x1="80" y1="20" x2="80" y2="560" stroke="#1d2433" stroke-width="6"/><line x1="80" y1="560" x2="800" y2="560" stroke="#1d2433" stroke-width="6"/>
  <text x="30" y="50" font-family="Inter" font-weight="800" font-size="34" fill="#1d2433">P</text>
  <text x="770" y="605" font-family="Inter" font-weight="800" font-size="34" fill="#1d2433">Q</text>
  <path id="s6-curva" d="M120 70 C 260 330, 420 450, 760 520" pathLength="1" fill="none" stroke="#1f6fb2" stroke-width="10" stroke-linecap="butt" style="stroke-dasharray:1;stroke-dashoffset:1"/>
  <text x="470" y="400" font-family="Caveat" font-weight="600" font-size="48" fill="#1f6fb2">curva de demanda</text></svg>
<div id="s6-pess" class="abs h" style="left:1260px;top:170px;width:300px;text-align:center">
  {gente("#5f6675", 'width="170"')}
  <div class="mao" style="font-size:46px;margin-top:10px">com fome,<br>sem dinheiro</div></div>
<div id="s6-fora" class="abs selo valor h" style="left:1210px;top:560px;font-size:32px">não aparece na curva</div>
<div id="s6-frase" class="abs titulo centro h" style="top:760px;font-size:50px">O mercado responde à <span class="fato">demanda</span>, não à <span style="color:var(--verde)">necessidade</span>.</div>
"""
    js = r"""
        moldura();
        entra("#s6-k0", T(0, 0.05)); entra("#s6-k1", T(0, 0.5));
        entra("#s6-k2", T(1, 0.0));
        entra("#s6-smith", T(1, 0.45));
        sai(["#s6-k0", "#s6-k1", "#s6-k2", "#s6-smith"], F[2][0] - 0.1);
        entra("#s6-graf", T(2, 0.0));
        tl.to(el("#s6-curva"), { strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }, T(2, 0.03));
        entra("#s6-frase", T(2, 0.12));
        entra("#s6-pess", T(2, 0.32), { x: 40 });
        pop("#s6-fora", T(2, 0.52));
        escurece("#s6-pess", T(2, 0.78), 0.12, 1.2);
"""
    return h, "", js


# =====================================================================
def cena7():
    tiles = ["PIB", "EMPREGO", "INFLAÇÃO", "BEM-ESTAR?"]
    h = "".join(f'<div class="abs cartao s7-t h" id="s7-t{k}" style="left:{200 + k * 390}px;top:130px;width:340px;height:190px;display:flex;align-items:center;justify-content:center;font-family:Fraunces;font-weight:800;font-size:{56 if k < 3 else 46}px;border-width:4px">{t}</div>'
                for k, t in enumerate(tiles))
    pecas = [("indústria", 0, 0), ("serviços", 1, 0), ("agropecuária", 0, 1)]
    h += f"""
<div id="s7-perg" class="abs mao centro h" style="top:390px;font-size:64px">o que vou medir? qual indicador representa “estar melhor”?</div>
<div id="s7-pib" class="abs h" style="left:360px;top:90px;width:1200px;height:560px">
  <div class="abs titulo" style="left:0;top:0;font-size:60px">PIB</div>
  {"".join(f'<div class="abs s7-p h" style="left:{x * 600}px;top:{90 + y * 200}px;width:580px;height:180px;background:#a7bfdc;border-radius:18px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:38px;color:#173c62">{n}</div>' for n, x, y in pecas)}
  <div id="s7-falta" class="abs h" style="left:600px;top:290px;width:580px;height:180px;border:6px dashed var(--valor);border-radius:18px;display:flex;align-items:center;justify-content:center;text-align:center;padding:0 30px;font-weight:800;font-size:32px;color:var(--valor)">trabalho doméstico e de cuidado não remunerado</div>
  <div id="s7-nao" class="abs selo valor h" style="left:740px;top:486px;font-size:30px">não entra no PIB</div>
</div>
<div id="s7-mulher" class="abs mao h" style="left:420px;top:680px;font-size:50px;color:var(--valor)">feito majoritariamente por mulheres</div>
<div id="s7-neutro" class="abs mao h" style="left:1080px;top:680px;font-size:50px">→ nos números, parece neutro</div>
{balao("s7-b2", "Cidadão", "Escolher o indicador já é escolher o que conta.", 200, 660, 640)}
{balao("s7-b3", "Economista", "…e quem conta.", 1300, 670, 380, "dir")}
<div id="s7-tres" class="abs titulo centro h" style="top:290px;font-size:76px"><span class="s7-w">o que medir</span> · <span class="s7-w">o que priorizar</span> · <span class="s7-w">para quem</span></div>
<div id="s7-dv" class="abs centro h" style="top:470px"><span class="selo valor" style="font-size:40px">DECISÕES DE VALOR</span></div>
<div id="s7-antes" class="abs mao centro h" style="top:590px;font-size:56px">tomadas antes mesmo de o modelo rodar</div>
"""
    js = r"""
        moldura();
        serie(".s7-t", T(0, 0.0), 0.2);
        entra("#s7-perg", T(0, 0.3));
        [3, 2, 1].forEach((k, n) => {
          tl.to(el("#s7-t" + k), { borderColor: "#1f6fb2", duration: 0.2 }, T(0, 0.45) + n * 0.6);
          tl.to(el("#s7-t" + k), { borderColor: "#d9cfbb", duration: 0.2 }, T(0, 0.45) + n * 0.6 + 0.45);
        });
        tl.to(el("#s7-t0"), { borderColor: "#1f6fb2", color: "#1f6fb2", scale: 1.08, duration: 0.3 }, T(0, 0.85));
        escurece(["#s7-t1", "#s7-t2", "#s7-t3"], T(0, 0.85), 0.3);
        sai([".s7-t", "#s7-perg"], F[1][0] - 0.2);
        entra("#s7-pib", T(1, 0)); serie(".s7-p", T(1, 0.02), 0.25, { y: -40 });
        pop("#s7-falta", T(1, 0.12)); pop("#s7-nao", T(1, 0.3));
        entra("#s7-mulher", T(1, 0.45)); entra("#s7-neutro", T(1, 0.75));
        sai(["#s7-mulher", "#s7-neutro"], F[2][0] - 0.1);
        balao("#s7-b2", 2, F[4][0]); balao("#s7-b3", 3, F[4][0]);
        sai("#s7-pib", F[4][0] - 0.1);
        entra("#s7-tres", T(4, 0.05));
        tl.fromTo(el(".s7-w"), { color: "#1f6fb2" }, { color: "#d66b29", duration: 0.5, stagger: 0.3 }, T(4, 0.45));
        pop("#s7-dv", T(4, 0.55)); entra("#s7-antes", T(4, 0.75));
"""
    return h, "", js


# =====================================================================
def cena8():
    cores = ["#1f6fb2", "#d66b29", "#2f8a74", "#6b4fa3", "#b8892a", "#c2541c", "#5b6b82", "#8d5a3b"]
    escalas = [1.0, .85, 1.1, .9, 1.05, .8, 1.0, .95, 1.1, .85, .9, 1.05, .8, 1.0, .92]
    pessoas = "".join(f'<div class="abs s8-p h" style="left:{360 + (k % 5) * 250}px;top:{110 + (k // 5) * 230}px;width:{int(130 * escalas[k])}px">{gente(cores[k % 8])}</div>'
                      for k in range(15))
    h = pessoas + f"""
<div id="s8-caixa" class="abs cartao h" style="left:700px;top:150px;width:520px;height:460px;border:4px solid var(--tinta);text-align:center;padding-top:30px">
  <div style="width:150px;margin:0 auto">{gente("#9aa0ab")}</div>
  <div class="titulo" style="font-size:52px;margin-top:14px">homo economicus</div>
  <div class="s8-tr h" style="font-size:32px;font-weight:700;margin-top:14px">racional</div>
  <div class="s8-tr h" style="font-size:32px;font-weight:700">isolado</div>
  <div class="s8-tr h" style="font-size:32px;font-weight:700">maximizador</div></div>
<div id="s8-im" class="abs centro h" style="top:56px"><span class="selo fato" style="font-size:32px">INDIVIDUALISMO METODOLÓGICO</span></div>
<div id="s8-simp" class="abs mao fato h" style="left:200px;top:300px;font-size:56px;width:420px">todo modelo<br>simplifica ✔</div>
{"".join(f'<div class="abs titulo s8-f h" style="left:1330px;top:{220 + k * 120}px;font-size:60px">{t}</div>' for k, t in enumerate(["justiça", "poder", "finalidade"]))}
<div id="s8-ne" class="abs selo valor h" style="left:1300px;top:570px;font-size:38px">“não econômico”?</div>
<div id="s8-red" class="abs titulo centro valor h" style="top:650px;font-size:96px">reducionismo</div>
"""
    js = r"""
        moldura();
        const ps = qa(".s8-p");
        ps.forEach((p, k) => entra(p, 0.3 + k * 0.08, { y: 20 }, 0.4));
        ps.forEach((p, k) => {
          const cx = 360 + (k % 5) * 250, cy = 110 + Math.floor(k / 5) * 230;
          tl.to(p, { x: 890 - cx, y: 230 - cy, scale: 0.5, opacity: 0, duration: 1.2, ease: "power3.in" }, T(0, 0.3) + k * 0.03);
        });
        pop("#s8-caixa", T(0, 0.45));
        serie(".s8-tr", T(0, 0.6), (F[0][1] - F[0][0]) * 0.1);
        pop("#s8-im", T(1, 0.02));
        entra("#s8-simp", T(1, 0.32), { x: -30 });
        serie(".s8-f", T(1, 0.6), 0.3, { x: 30 });
        escurece(".s8-f", T(1, 0.74), 0.3);
        tl.fromTo(el("#s8-ne"), { opacity: 0, scale: 1.6, rotation: -10 }, { opacity: 1, scale: 1, rotation: -10, duration: 0.4, ease: "power3.in" }, T(1, 0.76));
        pop("#s8-red", T(1, 0.9));
"""
    return h, "", js


# =====================================================================
def cena9():
    nos = [("trabalhadores", 200, 170), ("proprietários", 1420, 170), ("fábricas", 200, 560), ("mercados", 1420, 560)]
    h = f"""
<div id="s9-ilha" class="abs h" style="left:560px;top:90px;width:800px;height:520px">
  <svg width="800" height="520" viewBox="0 0 800 520">
    <ellipse cx="400" cy="380" rx="390" ry="120" fill="#bcd8e8"/>
    <ellipse cx="400" cy="360" rx="230" ry="62" fill="#e9d5a1"/>
    <path d="M440 350 C 440 270, 452 200, 476 150" stroke="#7a5a3a" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M476 150 C 420 120, 380 140, 360 170 M476 150 C 530 110, 580 130, 600 170 M476 150 C 470 95, 500 70, 540 70 M476 150 C 440 100, 400 90, 380 100" stroke="#2f8a74" stroke-width="22" fill="none" stroke-linecap="round"/>
    <g transform="translate(330 268) scale(.75)">{gente("#1d2433")[gente("#1d2433").index(">") + 1:-6]}</g>
  </svg></div>
<div id="s9-rob" class="abs mao h" style="left:1300px;top:120px;font-size:64px;color:var(--valor)">a “robinsonada”</div>
<div id="s9-cit" class="abs cartao h" style="left:300px;right:300px;top:640px;padding:26px 40px;text-align:center">
  <div class="titulo" style="font-size:44px">Para Marx, o indivíduo isolado não é o começo da história: é um <span class="valor">produto</span> dela.</div>
  <div class="suave" style="font-size:28px;font-weight:700;margin-top:10px">síntese da Introdução aos <i>Grundrisse</i> (1857)</div></div>
<svg id="s9-rede" class="abs h" style="left:0;top:0" width="1920" height="860" viewBox="0 0 1920 860">
  {"".join(f'<line class="s9-l" x1="960" y1="400" x2="{x + 150}" y2="{y + 50}" pathLength="1" stroke="#1d2433" stroke-width="5" stroke-dasharray="1" stroke-dashoffset="1"/>' for _, x, y in nos)}
</svg>
{"".join(f'<div class="abs cartao s9-n h" style="left:{x}px;top:{y}px;width:300px;height:100px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:32px">{n}</div>' for n, x, y in nos)}
<div id="s9-rel" class="abs titulo centro h" style="top:740px;font-size:46px">relações sociais · classes · <span class="valor">conflitos de interesse</span></div>
<div id="s9-tag" class="abs h" style="left:640px;top:130px;width:640px;height:340px">
  <div id="s9-tagbg" class="abs cartao" style="inset:0;border:4px solid var(--tinta);border-radius:30px 30px 30px 120px"></div>
  <div id="s9-preco" class="abs titulo centro" style="top:110px;font-size:110px">R$ 49,90</div>
  <div id="s9-gente" class="abs h" style="left:110px;top:60px;display:flex;gap:40px">{"".join(f'<div style="width:120px">{gente(c)}</div>' for c in ["#1f6fb2", "#c2541c", "#2f8a74"])}</div></div>
<div id="s9-fet" class="abs centro h" style="top:510px"><span class="selo valor" style="font-size:38px">FETICHISMO DA MERCADORIA</span>
  <div class="suave" style="font-size:28px;font-weight:700;margin-top:14px">Marx, <i>O Capital</i>, Livro I (1867), cap. 1</div></div>
{pessoa("cid", "s9-ci", 1600, 460, 230)}
{balao("s9-b2", "Cidadão", "“Todos poderiam estar melhor” apaga quem ganha e quem perde.", 1300, 170, 460, "dir")}
<div id="s9-gp" class="abs h" style="left:240px;top:620px;display:flex;gap:30px"><span class="selo" style="background:var(--verde);font-size:34px">quem ganha?</span><span class="selo valor" style="font-size:34px">quem perde?</span></div>
"""
    js = r"""
        moldura();
        entra("#s9-ilha", 0.3);
        entra("#s9-rob", T(0, 0.35), { x: 30 });
        entra("#s9-cit", T(0, 0.5));
        sai(["#s9-cit", "#s9-rob"], F[1][0] - 0.1);
        tl.to(el("#s9-ilha"), { scale: 0.55, y: 30, duration: 1, ease: "power3.inOut" }, T(1, 0));
        entra("#s9-rede", T(1, 0.05), { y: 0 });
        tl.to(el(".s9-l"), { strokeDashoffset: 0, duration: 0.8, stagger: 0.2, ease: "power2.out" }, T(1, 0.08));
        serie(".s9-n", T(1, 0.12), 0.25);
        entra("#s9-rel", T(1, 0.25));
        escurece(["#s9-ilha", "#s9-rede", ".s9-n", "#s9-rel"], T(1, 0.55), 0.0);
        pop("#s9-tag", T(1, 0.58));
        tl.to(el("#s9-tagbg"), { backgroundColor: "rgba(255,253,248,0.25)", duration: 0.6 }, T(1, 0.75));
        tl.to(el("#s9-preco"), { opacity: 0.12, duration: 0.6 }, T(1, 0.75));
        entra("#s9-gente", T(1, 0.78), { y: 10 });
        pop("#s9-fet", T(1, 0.82));
        sai("#s9-fet", F[2][0] - 0.1);
        entra("#s9-ci", F[2][0] - 0.2, { x: 80 }); balao("#s9-b2", 2, D); fala("#s9-ci", 2);
        pop("#s9-gp", T(2, 0.5));
"""
    return h, "", js


# =====================================================================
OPC = [("INFRAESTRUTURA", "var(--infra)", "Infra"), ("SAÚDE", "var(--saude)", "Saúde"),
       ("EDUCAÇÃO", "var(--educ)", "Educ."), ("TRANSFERÊNCIA DE RENDA", "var(--renda)", "Renda")]


def cena10():
    # valores fictícios (0–10) por critério, na ordem Infra, Saúde, Educ., Renda
    graf = [("Crescimento no curto prazo", [8, 3, 2, 5]), ("Redução da pobreza agora", [2, 3, 1, 9]),
            ("Vidas salvas e menos doenças", [3, 9, 4, 5]), ("Ganho em 15–20 anos", [5, 6, 9, 4])]

    def chart(k, titulo, vals):
        vence = vals.index(max(vals))
        barras = "".join(f'<div class="abs s10-bar{k}{" s10-win" if j == vence else " s10-lose"}" style="left:{30 + j * 85}px;bottom:70px;width:62px;height:{v * 30}px;background:{OPC[j][1]};border-radius:8px 8px 0 0;transform-origin:bottom"></div>'
                         f'<div class="abs" style="left:{14 + j * 85}px;bottom:26px;width:94px;text-align:center;font-size:28px;font-weight:700">{OPC[j][2]}</div>'
                         for j, v in enumerate(vals))
        return f'''<div class="abs cartao s10-g h" id="s10-g{k}" style="left:{140 + k * 420}px;top:110px;width:390px;height:500px">
  <div class="abs" style="left:26px;right:20px;top:24px;font-weight:800;font-size:28px;line-height:1.2">{titulo}</div>
  <div class="abs" style="left:24px;right:24px;bottom:70px;height:3px;background:var(--tinta)"></div>{barras}</div>'''

    h = f"""
<div id="s10-moeda" class="abs h" style="left:780px;top:170px;width:360px;height:360px;border-radius:50%;background:#e9c46a;border:14px solid #b8892a;display:flex;align-items:center;justify-content:center;text-align:center">
  <div class="titulo" style="font-size:70px;color:#5b4410">R$ 1<br>bilhão</div></div>
{opcao("s10-o0", OPC[0][0], OPC[0][1], 200, 190, 470)}
{opcao("s10-o1", OPC[1][0], OPC[1][1], 1250, 190, 470)}
{opcao("s10-o2", OPC[2][0], OPC[2][1], 200, 440, 470)}
{opcao("s10-o3", OPC[3][0], OPC[3][1], 1250, 440, 470)}
<div id="s10-pq" class="abs mao centro h" style="top:600px;font-size:60px">em quê investir?</div>
{"".join(chart(k, t, v) for k, (t, v) in enumerate(graf))}
<div id="s10-fic" class="ficticio h">VALORES FICTÍCIOS · ILUSTRATIVO</div>
<div id="s10-melhor" class="abs cartao titulo centro h" style="left:560px;right:560px;top:250px;padding:40px;font-size:76px">E qual é <span class="valor">a melhor</span>?</div>
<div id="s10-dep" class="abs cartao titulo centro h" style="left:440px;right:440px;top:650px;padding:22px;font-size:50px">“Depende de qual gráfico você olha.”</div>
<div id="s10-fim" class="abs titulo centro h" style="top:650px;font-size:52px">Números fictícios, dilema real: <span class="valor">nenhum gráfico escolhe sozinho.</span></div>
"""
    js = r"""
        moldura();
        pop("#s10-moeda", 0.4);
        entra("#s10-pq", T(0, 0.2));
        [0, 1, 2, 3].forEach((k) => entra("#s10-o" + k, T(0, 0.45) + k * 0.4, { y: 20 }));
        sai(["#s10-moeda", "#s10-o0", "#s10-o1", "#s10-o2", "#s10-o3", "#s10-pq"], F[1][0] - 0.1);
        pop("#s10-fic", T(1, 0.02));
        const ordem = [0, 1, 2, 3], quando = [0.05, 0.3, 0.52, 0.72];
        ordem.forEach((k, n) => {
          entra("#s10-g" + k, T(1, quando[n]), { y: 30 });
          tl.fromTo(el(".s10-bar" + k), { scaleY: 0 }, { scaleY: 1, duration: 0.6, stagger: 0.08, ease: "power2.out" }, T(1, quando[n]) + 0.2);
          tl.to(el(".s10-bar" + k + ".s10-lose"), { opacity: 0.3, duration: 0.4 }, T(1, quando[n]) + 1.0);
        });
        escurece(".s10-g", F[2][0], 0.25);
        pop("#s10-melhor", T(2, 0));
        sai("#s10-melhor", F[3][0]);
        tl.to(el(".s10-g"), { opacity: 1, duration: 0.4 }, F[3][0]);
        pop("#s10-dep", T(3, 0.05));
        [0, 1, 2, 3].forEach((k) => tl.to(el(".s10-bar" + k + ".s10-win"), { scaleY: 1.12, duration: 0.25, yoyo: true, repeat: 1 }, T(3, 0.15) + k * 0.35));
        sai("#s10-dep", F[4][0]);
        entra("#s10-fim", T(4, 0.35));
"""
    return h, "", js


# =====================================================================
def cena11():
    h = "".join(opcao(f"s11-o{k}", OPC[k][0] if k < 3 else "RENDA", OPC[k][1], 250 + k * 370, 90, 330, 100) for k in range(4))
    h += "".join(f'<div class="abs titulo centro s11-p h" style="top:240px;font-size:56px">prioridade: <span class="valor">{t}</span></div>'
                 for t in ["crescimento", "quem passa fome hoje", "os netos"])
    h += f"""
<svg id="s11-bal" class="abs h" style="left:560px;top:250px" width="800" height="460" viewBox="0 0 800 460">
  <path d="M400 120 L400 420 M300 430 L500 430" stroke="#1d2433" stroke-width="14" stroke-linecap="round"/>
  <g id="s11-braco">
    <line x1="100" y1="120" x2="700" y2="120" stroke="#1d2433" stroke-width="14" stroke-linecap="round"/>
    <path d="M100 120 L40 260 M100 120 L160 260 M700 120 L640 260 M700 120 L760 260" stroke="#1d2433" stroke-width="4"/>
    <path d="M20 260 L180 260 Q100 320 20 260Z" fill="#1d2433"/><path d="M620 260 L780 260 Q700 320 620 260Z" fill="#1d2433"/>
    <rect x="34" y="200" width="56" height="60" rx="8" fill="#5b6b82"/><rect id="s11-peso" x="100" y="170" width="64" height="90" rx="8" fill="#b8892a"/>
    <rect x="640" y="190" width="56" height="70" rx="8" fill="#2f8a74"/><rect x="704" y="180" width="60" height="80" rx="8" fill="#6b4fa3"/>
  </g>
  <circle cx="400" cy="120" r="18" fill="#d66b29"/>
</svg>
<div id="s11-ind" class="abs centro h" style="top:740px;font-size:40px;font-weight:700">índice único = soma de <span class="valor">peso</span> × resultado</div>
{balao("s11-b2", "Cidadão", '<span class="titulo valor" style="font-size:48px">Quem escolhe os pesos?</span>', 1380, 420, 460, "dir")}
<div id="s11-val" class="abs selo valor h" style="left:610px;top:240px;font-size:34px">VALOR</div>
{balao("s11-b3", "Economista", "…Eu escolho. Ou alguém escolhe. Os pesos são valores.", 100, 300, 480)}
<div id="s11-frase" class="abs titulo centro h" style="left:160px;right:160px;top:260px;font-size:86px">correta segundo <span class="valor">qual objetivo</span> — e <span class="valor">para quem</span>?</div>
<div id="s11-sub" class="abs centro h suave" style="top:560px;font-size:40px;font-weight:700">a pergunta “técnica” já contém uma escolha ética</div>
"""
    js = r"""
        moldura();
        serie(["#s11-o0", "#s11-o1", "#s11-o2", "#s11-o3"], 0.3, 0.15);
        const ps = qa(".s11-p"), alvo = [0, 3, 2], fr = [0.02, 0.36, 0.72];
        ps.forEach((p, n) => {
          entra(p, T(0, fr[n]));
          tl.to(el("#s11-o" + alvo[n]), { scale: 1.12, borderColor: "#d66b29", duration: 0.3 }, T(0, fr[n]) + 0.2);
          if (n < 2) { sai(p, T(0, fr[n + 1]) - 0.1); tl.to(el("#s11-o" + alvo[n]), { scale: 1, borderColor: "#d9cfbb", duration: 0.3 }, T(0, fr[n + 1]) - 0.1); }
        });
        sai(ps[2], F[1][0] - 0.1);
        tl.to(el("#s11-o2"), { scale: 1, borderColor: "#d9cfbb", duration: 0.3 }, F[1][0] - 0.1);
        entra("#s11-bal", T(1, 0.05));
        tl.fromTo(el("#s11-braco"), { rotation: -6, svgOrigin: "400 120" }, { rotation: 4, svgOrigin: "400 120", duration: 1.2, ease: "sine.inOut" }, T(1, 0.2));
        tl.to(el("#s11-braco"), { rotation: 0, svgOrigin: "400 120", duration: 1.0, ease: "sine.inOut" }, T(1, 0.2) + 1.2);
        entra("#s11-ind", T(1, 0.45));
        balao("#s11-b2", 2, F[3][0]);
        tl.to(el("#s11-peso"), { scale: 1.35, svgOrigin: "132 260", duration: 0.5, ease: "back.out(2)" }, T(2, 0.2));
        pop("#s11-val", T(3, 0.05));
        balao("#s11-b3", 3, F[4][0] - 0.1);
        sai(["#s11-bal", "#s11-ind", "#s11-val", "#s11-o0", "#s11-o1", "#s11-o2", "#s11-o3"], F[4][0] - 0.2);
        entra("#s11-frase", T(4, 0.35));
        entra("#s11-sub", T(4, 0.8));
"""
    return h, "", js


# =====================================================================
def cena12():
    alt = [300, 240, 270, 330]
    barras = "".join(f'<div class="abs s12-b h" style="left:{470 + k * 260}px;top:{620 - a}px;width:180px;height:{a}px;background:{OPC[k][1]};border-radius:12px 12px 0 0"></div>'
                     f'<div class="abs s12-lb h" style="left:{440 + k * 260}px;top:632px;width:240px;text-align:center;font-weight:800;font-size:30px">{OPC[k][2]}</div>'
                     for k, a in enumerate(alt))
    gentes = "".join(f'<div class="abs s12-g h" style="left:{478 + k * 260 + j * 56}px;top:{620 - a - 74}px;width:52px">{gente(["#1d2433", "#8d5a3b", "#c98e64"][j])}</div>'
                     for k, a in enumerate(alt) for j in range(3))
    h = f"""
<div id="s12-tit" class="abs titulo centro h" style="top:70px;font-size:60px">A economia é <span class="fato">indispensável</span></div>
{barras}{gentes}
<div id="s12-tags" class="abs centro h" style="top:700px"><span class="selo fato" style="font-size:30px;margin:0 10px">quanto custa</span><span class="selo fato" style="font-size:30px;margin:0 10px">consequências prováveis</span></div>
<div id="s12-autor" data-layout-allow-overlap class="abs selo valor h" style="left:760px;top:700px;width:400px;text-align:center;font-size:38px">decisão com autor</div>
<div id="s12-tec" data-layout-allow-overlap class="abs cartao h" style="left:740px;top:688px;width:440px;height:80px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:36px;background:#e8e2d4">resultado técnico</div>
<div id="s12-pes" class="abs mao h" style="left:1500px;top:200px;font-size:56px;color:var(--valor)">números<br>são pessoas</div>
{pessoa("ec", "s12-ec", 620, 380, 260)}
{pessoa("cid", "s12-ci", 1040, 380, 260)}
<div id="s12-mesa" class="abs h" style="left:560px;top:760px;width:800px;height:18px;border-radius:9px;background:var(--tinta)"></div>
{balao("s12-b2", "Economista", "Deixar claro quais fins estou assumindo.", 130, 220, 460)}
{balao("s12-b3", "Cidadão", "E abrir espaço para as pessoas afetadas participarem.", 1330, 200, 480, "dir")}
"""
    js = r"""
        moldura();
        entra("#s12-tit", 0.3);
        tl.set(el(".s12-b"), { transformOrigin: "bottom" }, 0);
        tl.fromTo(el(".s12-b"), { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.7, stagger: 0.15, ease: "power2.out" }, T(0, 0.15));
        serie(".s12-lb", T(0, 0.2), 0.15, { y: 10 });
        entra("#s12-tags", T(0, 0.45));
        sai("#s12-tags", F[1][0] - 0.1);
        tl.set(el("#s12-autor"), { opacity: 1 }, F[1][0]);
        entra("#s12-tec", T(1, 0.02), { y: 0 });
        serie(".s12-g", T(1, 0.18), 0.08, { y: -20 });
        entra("#s12-pes", T(1, 0.3), { x: 30 });
        tl.to(el("#s12-tec"), { y: 320, rotation: 22, opacity: 0, duration: 0.9, ease: "power2.in" }, T(1, 0.62));
        escurece([".s12-b", ".s12-g", ".s12-lb", "#s12-tit", "#s12-pes", "#s12-autor"], F[2][0] - 0.2, 0.0);
        entra("#s12-ec", F[2][0], { x: -60 }); entra("#s12-ci", F[2][0] + 0.2, { x: 60 }); entra("#s12-mesa", F[2][0] + 0.3, { y: 0 });
        balao("#s12-b2", 2, D); fala("#s12-ec", 2);
        balao("#s12-b3", 3, D); fala("#s12-ci", 3);
"""
    return h, "", js


# =====================================================================
def cena13():
    h = """
<div id="s13-a" class="abs titulo centro h" style="top:120px;font-size:56px">A economia é indispensável para compreender o mundo.</div>
<div id="s13-fins" class="abs titulo valor h" style="left:360px;top:330px;font-size:190px">FINS</div>
<div id="s13-meios" class="abs h" style="left:1000px;top:380px">
  <div class="mao suave" style="font-size:56px">e não apenas os</div>
  <div class="titulo fato" style="font-size:130px">MEIOS</div></div>
<div id="s13-q" class="abs titulo centro h" style="left:180px;right:180px;top:290px;font-size:104px">A economia pode, <span class="valor">sozinha</span>, dizer o que devemos fazer?</div>
<div id="s13-cred" class="abs h" style="left:140px;right:140px;top:70px;text-align:center">
  <div class="titulo" style="font-size:60px">Quando a economia diz o que <span class="valor">devemos</span> fazer?</div>
  <div style="font-size:32px;font-weight:700;margin-top:40px;line-height:1.5">Ana Luísa Mathias Costa · Fernada Cruz de Souza<br>Isis Mirelle de Santana Silva · Larissa Carneiro Fonseca</div>
  <div class="suave" style="font-size:30px;font-weight:600;margin-top:30px;line-height:1.5">Ética e Ciência Econômica · Prof. Múcio Tosta Gonçalves<br>Ciências Econômicas (COECO) · 2º semestre de 2026</div>
  <div class="suave" style="font-size:28px;font-weight:600;margin-top:34px;line-height:1.5">Referências: Hume, <i>Tratado da Natureza Humana</i> (1739–40) · Smith, <i>A Riqueza das Nações</i> (1776) ·
  Marx, <i>Grundrisse</i> (1857–58) e <i>O Capital</i>, Livro I (1867) · ONU, <i>Sistema de Contas Nacionais</i> (2008)<br>
  Os valores do caso de R$ 1 bilhão são fictícios, para ilustração. · Trilha sonora: a definir · Feito com HyperFrames</div></div>
"""
    js = r"""
        moldura();
        entra("#s13-a", T(0, 0.02));
        pop("#s13-fins", T(0, 0.62));
        entra("#s13-meios", T(0, 0.8), { x: 40 });
        sai(["#s13-a", "#s13-fins", "#s13-meios"], F[1][0] - 0.1);
        entra("#s13-q", T(1, 0.15), { y: 30 }, 1.0);
        const fimQ = F[1][1] + 5;
        sai("#s13-q", fimQ, 0.8);
        entra("#s13-cred", fimQ + 1.0, { y: 20 }, 1.0);
"""
    return h, "", js


CENAS = {1: cena1, 2: cena2, 3: cena3, 4: cena4, 5: cena5, 6: cena6, 7: cena7, 8: cena8, 9: cena9,
         10: cena10, 11: cena11, 12: cena12, 13: cena13}
