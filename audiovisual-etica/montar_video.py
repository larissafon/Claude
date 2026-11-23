#!/usr/bin/env python3
"""Monta o projeto HyperFrames em video/ a partir de cenas.py + visuais.py.

Uso:  python3 montar_video.py

- Se houver gravações em audios/ (nome começando com o id da fala, ex.:
  cena02_fala04_cidadao.m4a), elas são limpas (silêncio das pontas),
  niveladas em volume e colocadas no tempo certo; a duração real de cada
  fala passa a definir o tempo das cenas.
- Sem gravação, a fala usa a duração estimada (2,3 palavras/s) e o vídeo
  fica só com legendas.
- Se existir video/assets/trilha.(mp3|wav|m4a|ogg), ela entra baixinha ao fundo.
"""
import glob, html, json, os, re, subprocess, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from cenas import CENAS, N1, N2, EC, CI  # noqa: E402
import visuais  # noqa: E402

VIDEO = os.path.join(AQUI, "video")
AUD_IN = os.path.join(AQUI, "audios")
AUD_OUT = os.path.join(VIDEO, "assets", "vozes")

WPS = 2.3            # estimativa sem áudio
GAP = 0.7            # respiro entre falas
PAD_INI, PAD_FIM = 1.0, 1.5
# folgas específicas por cena (início, fim) para entradas e momentos sem fala
FOLGA = {1: (1.5, 3.5), 2: (1.6, 1.5), 10: (1.2, 3.0), 13: (1.0, 22.0)}
LEGENDAS = True
VOL_VOZ, VOL_TRILHA = 1.0, 0.12

COR_VOZ = {N1: "#6b4fa3", N2: "#2f8a74", EC: "#1f6fb2", CI: "#c2541c"}


def slug(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace(" ", "")


def duracao(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def preparar_audio(fid):
    """Procura a gravação da fala, limpa e normaliza. Retorna (arquivo_relativo, duração) ou None."""
    achados = sorted(glob.glob(os.path.join(AUD_IN, f"{fid}.*")) + glob.glob(os.path.join(AUD_IN, f"{fid}_*")))
    if not achados:
        return None
    src = achados[0]
    os.makedirs(AUD_OUT, exist_ok=True)
    dst = os.path.join(AUD_OUT, f"{fid}.wav")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        filtro = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,"
                  "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.25,areverse,"
                  "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", filtro,
                        "-ar", "48000", "-ac", "1", dst], check=True)
    return f"assets/vozes/{fid}.wav", duracao(dst)


def calcular_tempos():
    t = 0.0
    plano = []
    for i, c in enumerate(CENAS, 1):
        pre, pos = FOLGA.get(i, (PAD_INI, PAD_FIM))
        cur = pre
        falas = []
        for j, (quem, txt) in enumerate(c["falas"], 1):
            fid = f"cena{i:02d}_fala{j:02d}_{slug(quem)}"
            aud = preparar_audio(fid)
            dur = aud[1] if aud else round(len(txt.split()) / WPS, 2)
            falas.append(dict(id=fid, quem=quem, txt=txt, s=round(cur, 2), e=round(cur + dur, 2),
                              audio=aud[0] if aud else None))
            cur += dur + GAP
        D = round(cur - GAP + pos, 2)
        plano.append(dict(n=i, titulo=c["t"], ini=round(t, 2), dur=D, falas=falas))
        t += D
    return plano, round(t, 2)


def legendas(plano, total):
    """Divide cada fala em trechos curtos (por frase, até ~15 palavras) com tempo proporcional."""
    blocos = []
    for c in plano:
        for f in c["falas"]:
            frases = re.split(r"(?<=[.?!:;])\s+", f["txt"])
            trechos = []
            for fr in frases:
                w = fr.split()
                while len(w) > 15:
                    corte = 12 if len(w) > 20 else len(w) // 2
                    trechos.append(" ".join(w[:corte])); w = w[corte:]
                if w:
                    trechos.append(" ".join(w))
            total_c = sum(len(x) for x in trechos)
            s0, dur = c["ini"] + f["s"], f["e"] - f["s"]
            acc = 0
            for x in trechos:
                a = s0 + dur * acc / total_c
                acc += len(x)
                b = s0 + dur * acc / total_c
                blocos.append(dict(s=round(a, 2), e=round(b, 2), quem=f["quem"], txt=x))
    itens = "\n".join(
        f'      <div class="lg" id="lg{k}"><span class="lg-quem" style="color:{COR_VOZ[b["quem"]]}">{html.escape(b["quem"].title())}</span>'
        f'<span class="lg-txt">{html.escape(b["txt"])}</span></div>' for k, b in enumerate(blocos))
    tempos = json.dumps([[b["s"], b["e"]] for b in blocos])
    return f'''<template id="legendas-template">
  <div data-composition-id="legendas" data-width="1920" data-height="1080" data-duration="{total}">
    <div class="lg-area">
{itens}
    </div>
    <script>
      (function () {{
        const root = document.querySelector('[data-composition-id="legendas"]');
        const tempos = {tempos};
        const tl = gsap.timeline({{ paused: true }});
        tempos.forEach(([s, e], k) => {{
          const el = root.querySelector("#lg" + k);
          tl.set(el, {{ opacity: 1 }}, s);
          tl.set(el, {{ opacity: 0 }}, e);
        }});
        tl.set({{}}, {{}}, {total});
        window.__timelines = window.__timelines || {{}};
        window.__timelines["legendas"] = tl;
      }})();
    </script>
  </div>
</template>
'''


def main():
    plano, total = calcular_tempos()
    os.makedirs(os.path.join(VIDEO, "compositions"), exist_ok=True)

    for c in plano:
        cid = f"cena{c['n']:02d}"
        F = [[f["s"], f["e"]] for f in c["falas"]]
        corpo, css, js = visuais.CENAS[c["n"]]()
        doc = f'''<template id="{cid}-template">
  <div data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{c['dur']}">
    <div class="cena">
{corpo}
    </div>
    <style>
{css}
    </style>
    <script>
      (function () {{
        const root = document.querySelector('[data-composition-id="{cid}"]');
        const F = {json.dumps(F)};
        const D = {c['dur']};
{visuais.HELPERS}
{js}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["{cid}"] = tl;
      }})();
    </script>
  </div>
</template>
'''
        open(os.path.join(VIDEO, "compositions", f"{cid}.html"), "w").write(doc)

    if LEGENDAS:
        open(os.path.join(VIDEO, "compositions", "legendas.html"), "w").write(legendas(plano, total))

    hosts = []
    for c in plano:
        cid = f"cena{c['n']:02d}"
        hosts.append(f'''      <div id="{cid}-host" class="clip cena-host" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{c['ini']}" data-duration="{c['dur']}" data-track-index="1"></div>''')
    if LEGENDAS:
        hosts.append(f'''      <div id="legendas-host" class="clip cena-host" data-track-kind="captions" data-composition-id="legendas" data-composition-src="compositions/legendas.html"
        data-start="0" data-duration="{total}" data-track-index="2"></div>''')
    audios, n_aud = [], 0
    for c in plano:
        for f in c["falas"]:
            if f["audio"]:
                n_aud += 1
                audios.append(f'''      <audio id="voz-{f['id']}" src="{f['audio']}" data-start="{round(c['ini'] + f['s'], 2)}" data-duration="{round(f['e'] - f['s'], 2)}" data-track-index="3" data-volume="{VOL_VOZ}"></audio>''')
    trilha = sorted(glob.glob(os.path.join(VIDEO, "assets", "trilha.*")))
    if trilha:
        audios.append(f'''      <audio id="trilha" src="assets/{os.path.basename(trilha[0])}" data-start="0" data-duration="{total}" data-track-index="4" data-volume="{VOL_TRILHA}" data-fade-in="2" data-fade-out="4"></audio>''')

    index = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Quando a economia diz o que devemos fazer?</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{visuais.CSS_BASE}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
      <div id="papel" class="clip" data-start="0" data-duration="{total}" data-track-index="0"></div>
{chr(10).join(hosts)}
{chr(10).join(audios)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {total});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    open(os.path.join(VIDEO, "index.html"), "w").write(index)
    json.dump(dict(total=total, cenas=plano), open(os.path.join(VIDEO, "tempos.json"), "w"), ensure_ascii=False, indent=1)
    m, s = divmod(round(total), 60)
    n_falas = sum(len(c["falas"]) for c in plano)
    print(f"Vídeo montado: {m}:{s:02d} · {len(plano)} cenas · {n_aud}/{n_falas} falas com áudio gravado")


if __name__ == "__main__":
    main()
