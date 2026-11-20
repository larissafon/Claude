# Como retomar

Pasta preparada para criar vídeos com o HyperFrames (HeyGen) — https://github.com/heygen-com/hyperframes

- Projeto do vídeo: `meu-primeiro-video/index.html` (animação de 5 s, título "Meu primeiro vídeo")
- Vídeo exportado: `exportados/meu-primeiro-video.mp4`

Requisitos: Node.js 22+, FFmpeg e Chrome/Chromium.

Numa sessão nova do Claude Code (neste repositório, branch `claude/hyperframes-setup-video-mnqfwf`):

```bash
npm install        # reinstala o hyperframes (0.9.71)
npm run doctor     # confere Node, FFmpeg e Chrome
npm run check      # valida a composição
npm run render     # gera exportados/meu-primeiro-video.mp4
```
