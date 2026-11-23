#!/usr/bin/env python3
"""Gera roteiro.txt e storyboard.html a partir dos mesmos dados de cena."""
import html, json, math, os, sys

OUT = sys.argv[1]
WPS = 2.3          # palavras por segundo (~138 palavras/min, leitura calma)
PAUSA_FALA = 0.6   # respiro entre falas
TRANSICAO = 2.0    # entrada/saída de cada cena

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cenas import N1, N2, EC, CI, CENAS

def fmt(s):
    s = int(round(s)); return f"{s//60}:{s%60:02d}"

t = 0.0; total_palavras = 0
for c in CENAS:
    palavras = sum(len(f.split()) for _, f in c["falas"])
    total_palavras += palavras
    dur = palavras / WPS + PAUSA_FALA * len(c["falas"]) + TRANSICAO + c.get("extra", 0)
    dur = math.ceil(dur)
    c.update(ini=t, fim=t + dur, dur=dur, palavras=palavras); t += dur
TOTAL = t

os.makedirs(OUT, exist_ok=True)

# ---------- roteiro.txt ----------
L = ["QUANDO A ECONOMIA DIZ O QUE DEVEMOS FAZER?",
     "Roteiro de falas — audiovisual para Ética e Ciência Econômica",
     f"Duração estimada: {fmt(TOTAL)} ({total_palavras} palavras, ~{round(WPS*60)} palavras/min)",
     "Vozes: NARRADORA 1, NARRADORA 2, ECONOMISTA, CIDADÃO (sugestão: uma voz por integrante do grupo)",
     "Observação: os valores do caso de R$ 1 bilhão são fictícios e servem só para ilustrar.", ""]
for i, c in enumerate(CENAS, 1):
    L += ["=" * 64, f"CENA {i:02d} — {c['t'].upper()}   [{fmt(c['ini'])} – {fmt(c['fim'])}]   (bloco {c['bloco']} do roteiro)", "=" * 64, ""]
    for quem, fala in c["falas"]:
        L += [f"{quem}:", fala, ""]
L += ["-" * 64, "REFERÊNCIAS CITADAS NA FALA (conferir edição/tradução usada na disciplina)",
      "- HUME, David. Tratado da Natureza Humana (1739–1740), Livro III, parte 1, seção 1 — a passagem do “é” ao “deve”.",
      "- SMITH, Adam. A Riqueza das Nações (1776), Livro I, cap. 7 — “demanda efetiva”.",
      "- MARX, Karl. Grundrisse (1857–1858), Introdução — crítica às “robinsonadas”.",
      "- MARX, Karl. O Capital, Livro I (1867), cap. 1, seção 4 — fetichismo da mercadoria.",
      "- Sistema de Contas Nacionais (ONU, SNA 2008): o PIB não inclui serviços domésticos e de cuidado não remunerados produzidos pelas famílias para consumo próprio."]
open(os.path.join(OUT, "roteiro.txt"), "w").write("\n".join(L) + "\n")

# ---------- storyboard.html ----------
e = html.escape
COR = {N1: "n1", N2: "n2", EC: "ec", CI: "ci"}
cards, barras = [], []
for i, c in enumerate(CENAS, 1):
    falas = "".join(f'<p class="fala"><span class="quem {COR[q]}">{e(q.title())}</span>{e(f)}</p>' for q, f in c["falas"])
    cards.append(f'''
<article class="cena" id="c{i}">
  <header>
    <div class="num">{i:02d}</div>
    <div class="cab"><h2>{e(c["t"])}</h2>
      <div class="meta"><span class="tempo">{fmt(c["ini"])} – {fmt(c["fim"])}</span><span>{c["dur"]} s</span><span>bloco {e(c["bloco"])}</span><span class="tag t-{e(c["tag"].replace("ç","c").replace("ã","a").replace("í","i"))}">{e(c["tag"])}</span></div></div>
  </header>
  <div class="corpo">
    <section><h3>O que aparece</h3><p class="visual">{e(c["visual"])}</p></section>
    <section><h3>Fala</h3>{falas}</section>
  </div>
</article>''')
    barras.append(f'<a href="#c{i}" class="seg t-{e(c["tag"].replace("ç","c").replace("ã","a").replace("í","i"))}" style="flex:{c["dur"]}" title="{i:02d} · {e(c["t"])} · {fmt(c["ini"])}"><span>{i}</span></a>')

doc = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Storyboard do audiovisual</title>
<style>
:root{{--bg:#f6f1e7;--card:#fffdf8;--ink:#1d2433;--muted:#5f6675;--line:#e3dccd;
--fato:#1f6fb2;--valor:#e0702b;--n1:#6b4fa3;--n2:#2f8a74;--ec:#1f6fb2;--ci:#c2541c;
--t-encenacao:#e0702b;--t-conceito:#1f6fb2;--t-caso:#2f8a74;--t-pergunta:#6b4fa3;--t-sintese:#8a6d1f;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151821;--card:#1d212c;--ink:#ece8df;--muted:#a3a8b5;--line:#2c3140;--fato:#5aa6e6;--valor:#f29a5c;--n1:#a98be0;--n2:#5cc4a8;--ec:#5aa6e6;--ci:#f0875a}}}}
:root[data-theme="dark"]{{--bg:#151821;--card:#1d212c;--ink:#ece8df;--muted:#a3a8b5;--line:#2c3140;--fato:#5aa6e6;--valor:#f29a5c;--n1:#a98be0;--n2:#5cc4a8;--ec:#5aa6e6;--ci:#f0875a}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:32px 16px 64px}}
.eyebrow{{text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:var(--muted);margin:0}}
h1{{font-size:clamp(26px,4.5vw,42px);line-height:1.1;margin:6px 0 10px;letter-spacing:-.02em}}
.lead{{color:var(--muted);max-width:760px;margin:0 0 20px}}
.resumo{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 22px}}
.resumo div{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}}
.resumo b{{display:block;font-size:20px}} .resumo span{{font-size:13px;color:var(--muted)}}
.estilo{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:22px}}
.estilo h2{{font-size:18px;margin:0 0 6px}} .estilo p{{margin:6px 0}}
.chip{{display:inline-block;padding:1px 9px;border-radius:99px;color:#fff;font-size:13px;font-weight:600}}
.linha{{display:flex;height:34px;border-radius:8px;overflow:hidden;margin:6px 0 4px;border:1px solid var(--line)}}
.seg{{display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;font-size:12px;font-weight:700;border-right:1px solid rgba(255,255,255,.5);min-width:0}}
.seg span{{overflow:hidden}}
.escala{{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-bottom:26px}}
.t-encenacao{{background:var(--t-encenacao)}}.t-conceito{{background:var(--t-conceito)}}.t-caso{{background:var(--t-caso)}}.t-pergunta{{background:var(--t-pergunta)}}.t-sintese{{background:var(--t-sintese)}}
.cena{{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:0 0 16px;overflow:hidden;scroll-margin-top:12px}}
.cena header{{display:flex;gap:14px;align-items:center;padding:14px 18px;border-bottom:1px solid var(--line)}}
.num{{font-size:26px;font-weight:800;color:var(--muted);font-variant-numeric:tabular-nums}}
.cab h2{{margin:0;font-size:19px}}
.meta{{display:flex;flex-wrap:wrap;gap:8px;font-size:13px;color:var(--muted);margin-top:2px}}
.tempo{{font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}}
.tag{{color:#fff;padding:0 8px;border-radius:99px;font-weight:600}}
.corpo{{display:grid;grid-template-columns:1fr 1.25fr}}
.corpo section{{padding:14px 18px}} .corpo section+section{{border-left:1px solid var(--line)}}
h3{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 8px}}
.visual{{margin:0}}
.fala{{margin:0 0 10px}} .quem{{display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}}
.n1{{color:var(--n1)}}.n2{{color:var(--n2)}}.ec{{color:var(--ec)}}.ci{{color:var(--ci)}}
.notas{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-top:24px}}
.notas h2{{font-size:18px;margin:0 0 8px}} .notas li{{margin:4px 0}}
@media (max-width:720px){{.corpo{{grid-template-columns:1fr}}.corpo section+section{{border-left:0;border-top:1px solid var(--line)}}.seg span{{display:none}}}}
</style></head><body><main>
<p class="eyebrow">Storyboard · Ética e Ciência Econômica · formato horizontal 16:9</p>
<h1>Quando a economia diz o que devemos fazer?</h1>
<p class="lead"><b>Ideia central:</b> indicadores e modelos mostram o que acontece e quais consequências são prováveis, mas escolher o que medir, o que priorizar e para quem envolve valores. Por isso, a pergunta “qual é a escolha economicamente correta?” já contém uma escolha ética.</p>
<div class="resumo">
 <div><b>{fmt(TOTAL)}</b><span>duração estimada</span></div>
 <div><b>{len(CENAS)}</b><span>cenas, nos 7 blocos do roteiro</span></div>
 <div><b>{total_palavras}</b><span>palavras de fala</span></div>
 <div><b>4 vozes</b><span>2 narradoras, economista, cidadão</span></div>
</div>
<section class="estilo"><h2>Estilo sugerido: “caderno de economia”</h2>
<p>Fundo de papel creme, ilustrações planas e tipografia animada. Economista e cidadão aparecem como personagens ilustrados com balões de fala, e cada integrante do grupo grava uma das quatro vozes.</p>
<p><b>Código de cores ao longo do vídeo:</b> <span class="chip" style="background:var(--fato)">azul = FATO</span> (o que é, testável) e <span class="chip" style="background:var(--valor)">laranja = VALOR</span> (o que deve ser). Toda vez que uma frase “técnica” revela uma escolha, ela muda de azul para laranja. Esse é o fio visual que conduz a ideia central.</p>
<p><b>Som:</b> trilha instrumental leve e de uso livre, em volume baixo sob as vozes, com pausa de silêncio antes da pergunta final.</p></section>
<p class="eyebrow">Linha do tempo (clique numa cena)</p>
<div class="linha">{"".join(barras)}</div>
<div class="escala"><span>0:00</span><span>{fmt(TOTAL/2)}</span><span>{fmt(TOTAL)}</span></div>
{"".join(cards)}
<section class="notas"><h2>Notas de conferência com a fonte</h2><ul>
<li>A estrutura segue os 7 blocos do roteiro do grupo. A duração fica perto dos 10 min previstos e dentro do limite de 5 a 15 min das instruções.</li>
<li>O roteiro do grupo não traz dados numéricos. O caso de R$ 1 bilhão é hipotético, e os gráficos levam o selo “valores fictícios”.</li>
<li>Os tempos são estimados a ~{round(WPS*60)} palavras/min. Depois que as vozes forem gravadas, cada cena se ajusta à duração real do áudio.</li>
<li>As referências citadas na fala (Hume, Smith, Marx e o Sistema de Contas Nacionais) estão no fim do <code>roteiro.txt</code>. Vale conferir as edições usadas na disciplina.</li>
</ul></section>
</main></body></html>'''
open(os.path.join(OUT, "storyboard.html"), "w").write(doc)
print(json.dumps({"total": fmt(TOTAL), "palavras": total_palavras, "cenas": [(c["t"], fmt(c["ini"]), c["dur"]) for c in CENAS]}, ensure_ascii=False, indent=1))

# ---------- falas por voz (para gravação separada) ----------
import unicodedata
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return s.replace(" ", "")
os.makedirs(os.path.join(OUT, "gravacao"), exist_ok=True)
for voz in (N1, N2, EC, CI):
    L = [f"FALAS DE: {voz}", "",
         "Como gravar:",
         "- Grave cada fala em um arquivo separado, com o nome indicado entre colchetes.",
         "- Pode ser no celular (gravador de voz). Formatos aceitos: m4a, mp3, wav, ogg ou opus (áudio de WhatsApp).",
         "- Lugar silencioso, celular a um palmo da boca, sem fone com microfone.",
         "- Deixe 1 segundo de silêncio antes e depois de falar; eu corto as sobras.",
         "- Errou? Repita a frase inteira no mesmo arquivo; eu uso a última versão.",
         "- Fale com calma, como se estivesse explicando para um colega.", ""]
    n = 0
    for i, c in enumerate(CENAS, 1):
        for j, (quem, fala) in enumerate(c["falas"], 1):
            if quem != voz: continue
            n += 1
            L += [f"[cena{i:02d}_fala{j:02d}_{slug(voz)}]   (cena {i:02d}: {c['t']})", fala, ""]
    L.insert(1, f"Total: {n} falas")
    open(os.path.join(OUT, "gravacao", f"falas_{slug(voz)}.txt"), "w").write("\n".join(L) + "\n")
