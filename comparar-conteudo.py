"""
Compara o texto visível de cada página gerada pelo Eleventy (_site/)
com o do site estático original (commit inicial, antes da migração).

Objetivo: provar que a conversão não perdeu nem alterou nenhum texto.
Ignora espaços em branco e a ordem de atributos — compara só o que a
pessoa lê na tela.

Uso:  python comparar-conteudo.py
"""
import re
import subprocess
import sys
from html.parser import HTMLParser

PAGINAS = [
    "index.html",
    "sobre.html",
    "areas-de-atuacao.html",
    "reforma-tributaria.html",
    "blog.html",
    "contato.html",
    "privacidade.html",
]

COMMIT_ORIGINAL = "acbd9ba"

# Textos que passam a existir depois da migração, com a justificativa.
# Qualquer diferença fora desta lista é tratada como regressão.
#
# Os posts do blog aparecem aqui porque no site antigo eles eram montados
# por JavaScript no navegador — o HTML entregue vinha com a lista vazia.
# Agora são gerados no build. O texto em si não mudou: é conferido contra
# o js/blog-data.js original pela função `conferir_posts()`.
POSTS_RENDERIZADOS_NO_BUILD = {
    "IBS e CBS: o que muda na prática para sua empresa",
    "Um resumo direto de como o novo sistema de tributação sobre o consumo "
    "altera apuração, créditos e obrigações acessórias.",
    "Cronograma da transição: o que entra em vigor e quando",
    "Da fase de testes até a extinção dos tributos antigos: entenda os prazos "
    "que já estão definidos até 2033.",
    "Por que revisar seu planejamento tributário agora",
    "Decisões tomadas hoje sobre regime, contratos e precificação têm efeito "
    "direto na transição para o novo modelo.",
    "10 de junho de 2026",
    "22 de maio de 2026",
    "30 de abril de 2026",
    "Ler artigo →",
}

DIFERENCAS_ESPERADAS = {
    "index.html": POSTS_RENDERIZADOS_NO_BUILD,
    "blog.html": POSTS_RENDERIZADOS_NO_BUILD,
    "contato.html": {
        # Campo-isca anti-robô do Netlify Forms; fica com `hidden`,
        # invisível para quem visita e para leitores de tela.
        "Não preencha este campo:",
        # Aviso novo, exibido só se o envio falhar.
        "Não consegui enviar sua mensagem. Tente novamente ou fale comigo pelo WhatsApp.",
    },
}


class ExtratorDeTexto(HTMLParser):
    """Coleta o texto visível, ignorando script, style e comentários."""

    IGNORAR = {"script", "style", "head", "title", "meta", "link"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha = []
        self.partes = []

    def handle_starttag(self, tag, attrs):
        self.pilha.append(tag)

    def handle_endtag(self, tag):
        if tag in self.pilha:
            while self.pilha and self.pilha.pop() != tag:
                pass

    def handle_data(self, dados):
        if any(t in self.IGNORAR for t in self.pilha):
            return
        texto = dados.strip()
        if texto:
            self.partes.append(texto)


def texto_visivel(html):
    p = ExtratorDeTexto()
    p.feed(html)
    # normaliza espaços internos de cada trecho
    return [re.sub(r"\s+", " ", t) for t in p.partes]


def versao_original(caminho):
    return subprocess.run(
        ["git", "show", f"{COMMIT_ORIGINAL}:{caminho}"],
        capture_output=True, check=True,
    ).stdout.decode("utf-8")


def conferir_posts():
    """Garante que título, resumo e data dos posts continuam idênticos ao
    js/blog-data.js do site antigo, agora vindos de src/posts/*.md."""
    original = versao_original("js/blog-data.js")
    campos_antigos = set(
        re.findall(r'(?:title|excerpt):\s*\n?\s*"([^"]+)"', original)
        + re.findall(r'date:\s*"([^"]+)"', original)
    )

    import glob
    campos_novos = set()
    for caminho in glob.glob("src/posts/*.md"):
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        campos_novos |= set(re.findall(r'(?:title|excerpt):\s*"([^"]+)"', texto))
        campos_novos |= set(re.findall(r"date:\s*(\S+)", texto))

    faltando = campos_antigos - campos_novos
    if faltando:
        print("DIFF  posts do blog: conteudo perdido na migracao para Markdown:")
        for t in sorted(faltando):
            print(f"        - {t[:110]}")
        return False
    print(f"OK    posts do blog: {len(campos_antigos)} campos preservados de blog-data.js")
    return True


def main():
    houve_regressao = not conferir_posts()

    for pagina in PAGINAS:
        antes = texto_visivel(versao_original(pagina))
        with open(f"_site/{pagina}", encoding="utf-8") as f:
            depois = texto_visivel(f.read())

        esperados = DIFERENCAS_ESPERADAS.get(pagina, set())
        set_antes, set_depois = set(antes), set(depois)
        sumiu = [t for t in set_antes - set_depois]
        surgiu = [t for t in set_depois - set_antes if t not in esperados]

        if not sumiu and not surgiu:
            print(f"OK    {pagina}: {len(depois)} trechos de texto, identicos")
            continue

        houve_regressao = True
        print(f"DIFF  {pagina}:")
        for t in sorted(sumiu):
            print(f"        - SUMIU:  {t[:110]}")
        for t in sorted(surgiu):
            print(f"        + SURGIU: {t[:110]}")

    print()
    if houve_regressao:
        print("RESULTADO: ha diferencas de texto para revisar.")
        sys.exit(1)
    print("RESULTADO: nenhum texto perdido ou alterado nas 7 paginas.")


if __name__ == "__main__":
    main()
