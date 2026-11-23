# Audiovisual: Quando a economia diz o que devemos fazer?

| Arquivo | O que é |
|---|---|
| `roteiro.txt` | falas completas, por cena |
| `storyboard.html` | tempo, fala e o que aparece em cada cena |
| `gravacao/falas_*.txt` | lista de falas de cada voz, com o nome de arquivo de cada gravação |
| `audios/` | onde entram as gravações |
| `cenas.py` | **fonte única** das falas (edite aqui para mudar texto) |
| `visuais.py` | visual e animação de cada cena |
| `montar_video.py` | monta o projeto HyperFrames em `video/` |
| `video/` | projeto HyperFrames gerado (não editar à mão) |

## Fluxo

```bash
python3 gerar_plano.py .     # atualiza roteiro.txt, storyboard.html e gravacao/
python3 montar_video.py      # monta video/ (usa os áudios de audios/ se houver)
cd video && npx hyperframes check
npx hyperframes render -o ../../exportados/audiovisual-etica.mp4
```

Trilha sonora: coloque um arquivo `video/assets/trilha.mp3` (ou .wav/.m4a/.ogg) de uso livre e rode
`montar_video.py` de novo — ela entra baixinha sob as vozes.
