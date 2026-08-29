"""
Compara a ESTRUTURA HTML das páginas geradas com a do site original:
sequência de tags, atributos e classes. Se isto bate, o navegador
desenha a mesma coisa — é uma prova mais forte que uma captura de tela,
porque cobre as 7 páginas inteiras, e não só a parte visível.

Ignora apenas espaços em branco entre tags.

Uso:  python comparar-estrutura.py
"""
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

# Mudanças estruturais intencionais, com o motivo.
IGNORAR_TAG_COM_ATRIBUTO = [
    # Os posts eram montados por JavaScript; o <script> que fazia isso e o
    # arquivo de dados saíram, porque agora a lista é gerada no build.
    ("script", "src", "js/blog-data.js"),
]

# Elementos que passam a existir no HTML entregue, com a justificativa.
# São comparados por prefixo do evento gerado pelo parser.
NOVOS_ESPERADOS = {
    # Antes o navegador criava estes cards por JavaScript, a partir do
    # blog-data.js — o HTML saía do servidor com a lista vazia. Agora
    # saem prontos do build. As classes são as mesmas que o JS gerava.
    '<article class="card post-card"',
    '<span class="date"',
    '<a class="read-more" href="blog.html"',
    '<a class="read-more" href="#"',
    "<h3 ",
    "<p ",
    "</h3",
    "</p",
    "</a",
    "</span",
    "</article",
    # Netlify Forms: identificação do formulário e campo-isca anti-robô.
    '<form data-netlify="true"',
    '<input name="form-name" type="hidden" value="contato"',
    '<p aria-hidden="true" hidden=""',
    '<input autocomplete="off" name="bot-field" tabindex="-1"',
    "<label ",
    "</label",
    # Aviso exibido quando o envio do formulário falha.
    '<div class="form-falha" role="alert"',
    "</div",
}

# Elementos que deixam de existir, com a justificativa.
REMOVIDOS_ESPERADOS = {
    # Substituído pela versão com os atributos do Netlify Forms.
    '<form id="contact-form" novalidate=""',
    # O <script> inline que montava os cards do blog no navegador —
    # essa montagem passou para o build.
    "<script ",
    "</script",
}


class Estrutura(HTMLParser):
    """Reduz o HTML a uma lista de eventos de tag, com atributos ordenados."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.eventos = []

    def handle_starttag(self, tag, attrs):
        pares = sorted((k, (v or "").strip()) for k, v in attrs)
        self.eventos.append(f"<{tag} " + " ".join(f'{k}="{v}"' for k, v in pares))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.eventos.append(f"</{tag}")


def estrutura(html):
    p = Estrutura()
    p.feed(html)
    return p.eventos


def versao_original(caminho):
    return subprocess.run(
        ["git", "show", f"{COMMIT_ORIGINAL}:{caminho}"],
        capture_output=True, check=True,
    ).stdout.decode("utf-8")


def filtrar(eventos):
    saida = []
    for e in eventos:
        if any(f"<{t} " in e and f'{a}="{v}"' in e for t, a, v in IGNORAR_TAG_COM_ATRIBUTO):
            continue
        saida.append(e)
    return saida


def main():
    import difflib

    houve_diferenca = False
    for pagina in PAGINAS:
        antes = filtrar(estrutura(versao_original(pagina)))
        with open(f"_site/{pagina}", encoding="utf-8") as f:
            depois = filtrar(estrutura(f.read()))

        if antes == depois:
            print(f"OK    {pagina}: {len(depois)} elementos, estrutura identica")
            continue

        linhas = []
        for l in difflib.unified_diff(antes, depois, "antes", "depois", n=0, lineterm=""):
            if not l.startswith(("+", "-")) or l.startswith(("+++", "---")):
                continue
            conteudo = l[1:]
            esperados = NOVOS_ESPERADOS if l[0] == "+" else REMOVIDOS_ESPERADOS
            if any(conteudo.startswith(e) for e in esperados):
                continue
            linhas.append(l)
        if not linhas:
            print(f"OK    {pagina}: estrutura identica")
            continue

        houve_diferenca = True
        print(f"DIFF  {pagina}: {len(linhas)} diferencas")
        for l in linhas[:25]:
            print(f"        {l[:120]}")
        if len(linhas) > 25:
            print(f"        ... e mais {len(linhas) - 25}")

    print()
    if houve_diferenca:
        print("RESULTADO: revisar as diferencas acima.")
        sys.exit(1)
    print("RESULTADO: estrutura HTML identica nas 7 paginas.")


if __name__ == "__main__":
    main()
