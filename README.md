# Site — Glauciane Advocacia Tributária (MVP)

## Como abrir

Duas formas:

1. **Rápido, só para visualizar**: dê duplo clique em `index.html`. Funciona, mas
   alguns navegadores (Chrome) bloqueiam pequenos recursos ao abrir arquivos
   direto do disco.
2. **Recomendado**: rode um servidor local simples. Com Python já instalado:
   ```
   cd site
   python3 -m http.server 8080
   ```
   Depois acesse `http://localhost:8080` no navegador. Isso evita qualquer
   limitação de segurança do navegador para arquivos locais e já simula como o
   site vai se comportar hospedado.

## Estrutura

```
site/
├── index.html              Home
├── sobre.html
├── areas-de-atuacao.html
├── reforma-tributaria.html  Hub de conteúdo sobre a reforma
├── blog.html
├── contato.html             Formulário + WhatsApp
├── privacidade.html         Texto-modelo de política de privacidade (LGPD)
├── css/style.css            Todos os estilos, com tokens no topo do arquivo
├── js/main.js               Menu mobile, validação do formulário, ano do rodapé
├── js/blog-data.js          Conteúdo dos posts do blog (ver nota abaixo)
└── data/posts.json          Mesmo conteúdo em JSON, pronto para virar backend
```

## Por que essas escolhas técnicas

**HTML/CSS/JS puro, sem build tool.** Para o tamanho atual do site (6 páginas),
qualquer framework (React, Next.js, Vue) adicionaria complexidade sem benefício
real — e exigiria que quem for editar o conteúdo soubesse rodar `npm install`,
lidar com dependências, etc. HTML puro roda em qualquer lugar, para sempre, sem
manutenção de dependências.

**CSS com variáveis (design tokens) no topo do `style.css`.** Cores, fontes,
espaçamentos e raios de borda estão centralizados em `:root`. Isso significa
que trocar a cor principal do site, por exemplo, é uma linha só — não uma
busca por todo o CSS.

**Header e rodapé duplicados em cada página.** É a única concessão consciente
nesta versão: sem um servidor de templates, replicar o HTML do menu em cada
arquivo é mais simples do que usar `fetch()` para montar a página (que, aliás,
não funciona ao abrir arquivos direto do disco). Se o número de páginas
crescer muito, vale migrar para uma ferramenta de templates (próxima seção).

**Blog com dados em JS, espelhados em JSON.** Hoje os posts vivem em
`js/blog-data.js` como um array. O arquivo `data/posts.json` tem exatamente o
mesmo conteúdo e formato — é o "molde" para quando o site for publicado num
servidor de verdade, onde então dá para trocar `blog-data.js` por um simples
`fetch('/data/posts.json')`.

## O que provavelmente vai ser pedido no futuro (e como este projeto já se
prepara para isso)

| Pedido futuro | Caminho recomendado |
|---|---|
| "Quero adicionar posts sem mexer no código" | Migrar para um site estático com CMS: **Astro** ou **Eleventy (11ty)** + um CMS headless simples como **Decap CMS** ou **Sanity**. A estrutura de conteúdo em JSON já criada aqui migra quase direto. |
| "Quero que o formulário realmente envie e-mail" | Plugar um serviço como **Formspree**, **Resend** ou **EmailJS** — só trocar o comentário indicado em `js/main.js` (`initContactForm`) por uma chamada `fetch` real. Não precisa reescrever o formulário. |
| "Quero agendamento automático de consulta" | Embutir um widget do **Calendly** ou **Cal.com** na página de contato. |
| "O site cresceu, ficou difícil de manter o menu em toda página" | Migrar para **Astro** (componentes reaproveitáveis, sem virar uma SPA pesada) ou, se quiser algo com mais tooling de front-end, **Next.js**. A estrutura de CSS com tokens e o conteúdo já escrito aqui aproveitam quase 100%. |
| "Quero múltiplos idiomas" | Astro e Next.js têm suporte nativo a i18n; nesse ponto compensa migrar. |
| "Quero medir de onde vêm os clientes" | Adicionar Google Analytics ou Plausible via tag no `<head>` — não exige mudança de arquitetura. |

Resumindo: para o volume de conteúdo de um MVP, HTML/CSS/JS puro é a escolha
certa — rápido de carregar, fácil de hospedar em qualquer lugar (Netlify,
Vercel, GitHub Pages, hospedagem compartilhada) e sem dependências para
quebrar. O ponto de virada para um framework é quando o **conteúdo** (número de
posts, páginas, idiomas) crescer o suficiente para que copiar/colar HTML vire
dor de cabeça — e aí a estrutura de tokens e conteúdo já escrita aqui migra sem
retrabalho.

## Antes de publicar

- Substituir todos os campos entre colchetes `[ ]` (nome completo, OAB, e-mail,
  telefone, formação, textos de "Sobre") pelos dados reais.
- Trocar as fotos placeholder (blocos cinza) por fotos reais em `assets/img/`.
- Revisar o texto de `privacidade.html` com apoio jurídico especializado em
  LGPD antes de publicar.
- Confirmar que toda a linguagem do site está alinhada ao Provimento 205/2021
  da OAB sobre publicidade advocatícia (evitar termos como "desconto",
  "promoção", garantias de resultado).
