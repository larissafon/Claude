#!/usr/bin/env python3
"""Gera roteiro.txt e storyboard.html a partir dos mesmos dados de cena."""
import html, json, math, os, sys

OUT = sys.argv[1]
WPS = 2.3          # palavras por segundo (~138 palavras/min, leitura calma)
PAUSA_FALA = 0.6   # respiro entre falas
TRANSICAO = 2.0    # entrada/saída de cada cena

N1, N2, EC, CI = "NARRADORA 1", "NARRADORA 2", "ECONOMISTA", "CIDADÃO"

CENAS = [
 dict(t="Abertura", bloco="—", tag="pergunta",
  visual="Fundo de papel creme. Manchetes e números (PIB, %, R$) caem e se empilham na tela. A frase “a escolha economicamente correta” aparece entre aspas, depois as aspas se transformam num grande ponto de interrogação. Título: QUANDO A ECONOMIA DIZ O QUE DEVEMOS FAZER?",
  falas=[(N1,"Toda semana, alguma decisão pública chega até nós embalada em números: crescimento, custo, eficiência. E quase sempre vem acompanhada de uma frase: essa é a escolha economicamente correta. Mas o que exatamente essa frase está dizendo? Ela descreve o mundo, ou já está decidindo por nós como ele deve ser?"),
         (N2,"Este audiovisual parte de uma pergunta simples: quando a economia diz o que devemos fazer?")],
  extra=3),
 dict(t="A pergunta", bloco="1", tag="encenação",
  visual="Apresentação dos dois personagens (ilustração plana): ECONOMISTA ao lado de um quadro com gráfico; CIDADÃO de frente. Gráfico 1: barra “Renda total” sobe. Gráfico 2: a mesma renda dividida em fatias por grupo (mais pobres → mais ricos); a fatia de cima cresce muito mais. Balão do cidadão: “Eficiente para quem?” fica marcado em laranja.",
  falas=[(EC,"Tenho aqui uma proposta. Segundo o nosso modelo, esta política aumenta a renda total do país. A economia cresce, a riqueza aumenta."),
         (CI,"E quem fica com essa riqueza?"),
         (EC,"Bom... o modelo também indica que a desigualdade aumenta. Os mais ricos ganham bem mais que os mais pobres. Mas, no agregado, todos poderiam estar melhor."),
         (CI,"Poderiam. Mas vão estar? Você diz que é eficiente. Eficiente para quem?"),
         (N1,"Riqueza maior, desigualdade maior. É uma boa política? Repare que os números não respondem a isso sozinhos. Para responder, precisamos dizer o que consideramos bom.")]),
 dict(t="Fato e valor", bloco="2", tag="conceito",
  visual="Tela dividida. À esquerda, em AZUL (código de FATO): “A política aumenta o PIB em X%” com selo ✓ “testável com dados”. À direita, em LARANJA (código de VALOR): “Devemos escolhê-la?” com selo ⚖ “depende do que valorizamos”. Entre os dois, uma ponte que se quebra: ‘É’ ↛ ‘DEVE’ (Hume, séc. XVIII). Rótulos finais: economia POSITIVA / NORMATIVA.",
  falas=[(N2,"Existem dois tipos de frase nessa conversa. A primeira: a política aumenta o PIB em X por cento. Ela pode ser testada: os dados confirmam ou não. É uma afirmação sobre o que é."),
         (N1,"A segunda: devemos escolher essa política. Nenhum dado, sozinho, confirma essa frase. Ela depende do que valorizamos: crescimento, igualdade, liberdade, segurança. É uma afirmação sobre o que deve ser."),
         (N2,"No século dezoito, o filósofo David Hume já apontava que não se chega a um deve partindo apenas de um é. Na economia, essa separação aparece como a distinção entre economia positiva, que descreve, e economia normativa, que prescreve."),
         (EC,"Então meu trabalho é só a parte positiva. Eu mostro as consequências; quem decide são os outros."),
         (CI,"Será? Vamos ver se é tão simples assim.")]),
 dict(t="Moral e ética", bloco="2", tag="conceito",
  visual="Duas palavras grandes lado a lado. MORAL: ícones de costumes, regras e convicções do dia a dia (fila, aperto de mão, placa). ÉTICA: uma lupa passa por cima desses ícones com a pergunta “por quê? a quem serve?”. Retorno rápido ao balão “Eficiente para quem?”, agora com a etiqueta ÉTICA.",
  falas=[(N1,"Para avançar, vale distinguir duas palavras que costumamos usar como sinônimos. Moral são os valores vividos: os costumes, as regras e as convicções que orientam o que uma sociedade considera certo ou errado no dia a dia."),
         (N2,"Ética é a reflexão sobre esses valores: perguntar por que os seguimos, se fazem sentido e a quem servem. Quando o cidadão pergunta eficiente para quem, ele está fazendo exatamente isso: trazendo a reflexão ética para dentro de uma conversa que parecia apenas técnica.")]),
 dict(t="O que é uma necessidade?", bloco="3", tag="encenação",
  visual="Cinco cartas entram uma a uma: ALIMENTAÇÃO, MORADIA, SAÚDE, CELULAR, VIAGEM. O economista arrasta as cartas para duas colunas, “necessidade” e “desejo”; o CELULAR oscila entre as duas e VIAGEM vai para “desejo”. A linha que separa as colunas fica tracejada com a pergunta “quem decide?”.",
  falas=[(CI,"Me responde uma coisa. A economia diz que estuda como satisfazer as necessidades das pessoas. Mas o que é uma necessidade?"),
         (EC,"Alimentação, moradia, saúde. Isso é básico."),
         (CI,"E um celular? Hoje, sem celular, eu não consigo procurar emprego, falar com a escola do meu filho, acessar o banco."),
         (EC,"Hum... talvez seja uma necessidade, então."),
         (CI,"E uma viagem de férias?"),
         (EC,"Aí já é um desejo."),
         (CI,"Para quem? Quem decide onde termina a necessidade e começa o desejo?")]),
 dict(t="Necessidade, desejo e demanda", bloco="3", tag="conceito",
  visual="Três círculos concêntricos/sobrepostos: NECESSIDADES (dignidade, época, sociedade), DESEJOS (cultura, publicidade), DEMANDA (desejo + poder de compra, ícone de carteira). Citação: Adam Smith, “demanda efetiva” (A Riqueza das Nações, Livro I, cap. 7). Final: uma curva de demanda; uma silhueta com fome e carteira vazia fica do lado de fora do gráfico e vai sumindo.",
  falas=[(N2,"Podemos separar três ideias. Necessidades são condições para viver com dignidade em uma determinada sociedade e época. Desejos são moldados pela cultura, pela publicidade, pelo que é visto como normal ou desejável."),
         (N1,"E demanda é outra coisa: é o desejo sustentado por poder de compra. Adam Smith já distinguia a simples vontade de ter algo da demanda efetiva, aquela de quem pode pagar."),
         (N2,"Aqui está o ponto: o mercado responde à demanda, não à necessidade. Uma pessoa com fome e sem dinheiro não aparece na curva de demanda. Se a economia olha apenas para o que é demandado, quem não pode pagar simplesmente some da análise.")]),
 dict(t="A economia começa a escolher", bloco="4", tag="conceito",
  visual="Painel de indicadores (PIB, emprego, inflação) com uma mão escolhendo qual acender. Exemplo: um “PIB” montado como quebra-cabeça em que falta a peça TRABALHO DOMÉSTICO E DE CUIDADO NÃO REMUNERADO (peça em tracejado). As palavras O QUE MEDIR · O QUE PRIORIZAR · PARA QUEM mudam de azul (fato) para laranja (valor).",
  falas=[(N1,"Voltemos ao economista que dizia apenas descrever. Antes de qualquer cálculo, ele precisa decidir: o que vou medir? Qual indicador vai representar estar melhor?"),
         (N2,"Um exemplo: o PIB não contabiliza o trabalho doméstico e de cuidado não remunerado, realizado majoritariamente por mulheres. Uma política que aumente esse trabalho invisível pode aparecer, nos números, como neutra ou até positiva."),
         (CI,"Então escolher o indicador já é escolher o que conta."),
         (EC,"E quem conta."),
         (N1,"Escolher o que medir, o que priorizar e para quem: essas são decisões de valor, tomadas antes mesmo de o modelo começar a rodar.")]),
 dict(t="Reducionismo mainstream", bloco="4", tag="conceito",
  visual="Uma multidão de silhuetas diversas é “achatada” numa única figura padronizada: HOMO ECONOMICUS (racional · isolado · maximizador), dentro de uma caixa. Rótulo: INDIVIDUALISMO METODOLÓGICO. Ao redor da caixa, palavras ficam do lado de fora, esmaecidas: justiça, poder, finalidade — carimbo “não econômico?”.",
  falas=[(N2,"Boa parte da economia dominante, chamada de mainstream, parte de uma figura simplificada: o homo economicus, um indivíduo racional, isolado, que maximiza sua própria satisfação diante de recursos escassos."),
         (N1,"Esse é o individualismo metodológico: explicar os fenômenos sociais a partir das escolhas de indivíduos. Simplificações são úteis; todo modelo simplifica. O problema começa quando a simplificação passa a ser tratada como a própria realidade, e perguntas sobre justiça, poder e finalidade são deixadas de fora como não econômicas. É isso que chamamos de reducionismo.")]),
 dict(t="A crítica marxiana", bloco="4", tag="conceito",
  visual="Ilha com um Robinson Crusoé sozinho (a “robinsonada”). A câmera se afasta e revela fios ligando a ilha a fábricas, trabalhadores e proprietários: relações sociais e de classe. Uma mercadoria (etiqueta de preço) fica transparente e mostra as pessoas por trás dela: FETICHISMO DA MERCADORIA (Marx, O Capital, Livro I, cap. 1).",
  falas=[(N2,"A crítica marxiana vai na raiz desse ponto de partida. Para Marx, o indivíduo isolado não é o começo da história, é um produto dela. Ele ironizava as robinsonadas dos economistas, que imaginavam a economia a partir de um Robinson Crusoé sozinho em uma ilha."),
         (N1,"As pessoas produzem e consomem dentro de relações sociais: entre trabalhadores e proprietários, entre classes, com conflitos de interesse. Ao tratar preços e mercados como fenômenos naturais, a teoria esconde que por trás das mercadorias há relações entre pessoas. Marx chamou isso de fetichismo da mercadoria."),
         (CI,"Então quando o modelo diz todos poderiam estar melhor, ele está apagando quem ganha e quem perde.")]),
 dict(t="Caso hipotético: R$ 1 bilhão", bloco="5", tag="caso",
  visual="Moeda/saco “R$ 1 bilhão” no centro, quatro caminhos: INFRAESTRUTURA, SAÚDE, EDUCAÇÃO, TRANSFERÊNCIA DE RENDA. Quatro gráficos aparecem lado a lado, cada um com um vencedor diferente: crescimento no curto prazo (infraestrutura), vidas/saúde (saúde), ganho no longo prazo, 15–20 anos (educação), redução imediata da pobreza (transferência). Selo fixo no canto: VALORES FICTÍCIOS — ILUSTRATIVO.",
  falas=[(N1,"Vamos testar tudo isso em um caso hipotético. O governo tem um bilhão de reais para investir, e quatro opções: infraestrutura, saúde, educação ou transferência de renda."),
         (EC,"Rodei as simulações. Infraestrutura gera o maior crescimento no curto prazo. Transferência de renda reduz mais a pobreza agora. Saúde salva mais vidas e reduz doenças. Educação tem os maiores ganhos, mas só daqui a quinze ou vinte anos."),
         (CI,"E qual é a melhor?"),
         (EC,"Depende de qual gráfico você olha."),
         (N2,"Os números são fictícios, mas o dilema é real. Cada gráfico mostra um resultado dentro do modelo, e nenhum deles diz, sozinho, qual escolher.")],
  extra=4),
 dict(t="Quem escolhe os pesos?", bloco="5", tag="encenação",
  visual="O cidadão gira um seletor de prioridades (crescimento / fome hoje / netos) e o destaque pula entre os quatro gráficos. O economista monta uma balança com pesinhos para formar um “índice único”; um pesinho é ampliado e ganha a etiqueta laranja VALOR. Frase final em destaque: “correta segundo qual objetivo — e para quem?”.",
  falas=[(CI,"Se eu priorizo crescimento, escolho infraestrutura. Se priorizo quem está passando fome hoje, escolho transferência. Se penso nos meus netos, educação."),
         (EC,"E se eu juntar tudo num único índice, com pesos para cada objetivo?"),
         (CI,"Quem escolhe os pesos?"),
         (EC,"Eu escolho. Ou alguém escolhe. Tá, entendi: os pesos são valores."),
         (N1,"A pergunta qual é a escolha economicamente correta já contém uma escolha ética: correta segundo qual objetivo, e para quem?")]),
 dict(t="Fechamento", bloco="6", tag="síntese",
  visual="Os gráficos do caso se reorganizam e, sobre cada barra, surgem rostos/silhuetas de pessoas: números viram pessoas. Uma etiqueta “resultado técnico” é arrancada e revela “decisão com autor”. Economista e cidadão aparecem lado a lado, do mesmo lado da mesa.",
  falas=[(N2,"Nada disso significa abandonar a economia. Sem ela, não saberíamos quanto custa cada opção, nem quais consequências são prováveis. Os modelos e indicadores são indispensáveis para enxergar a realidade."),
         (N1,"O problema não é usar a economia para decidir. É esquecer que as decisões afetam pessoas, e tratá-las como se fossem resultados técnicos, neutros, sem autor."),
         (EC,"Talvez meu trabalho não seja só mostrar os meios. Também é deixar claro quais fins estou assumindo."),
         (CI,"E abrir espaço para que as pessoas afetadas participem dessa escolha.")]),
 dict(t="Pergunta final e créditos", bloco="7", tag="pergunta",
  visual="Mensagem em tipografia: MEIOS (azul) e FINS (laranja). Silêncio de 3 s com a pergunta final sozinha na tela. Créditos: integrantes do grupo, disciplina Ética e Ciência Econômica, professor, referências citadas e créditos da trilha sonora.",
  falas=[(N2,"A economia é indispensável para compreender o mundo. Mas seus limites éticos exigem que o economista reflita sobre as finalidades, e não apenas sobre os meios."),
         (N1,"Então fica a pergunta: a economia pode, sozinha, dizer o que devemos fazer?")],
  extra=14),
]

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
