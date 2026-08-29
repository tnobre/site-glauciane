# Site — Glauciane Nobre Advocacia Empresarial

Site estático gerado com [Eleventy](https://www.11ty.dev/), publicado na Netlify,
com painel de edição para a Glauciane alterar os textos sem mexer em código.

## Rodar na sua máquina

```
npm install
npm start        # http://localhost:8080, recarrega ao salvar
npm run build    # gera a pasta _site/
```

Requer Node 18+. O build da Netlify usa a versão fixada em `.nvmrc` (22).

## Estrutura

```
src/
├── _data/                 CONTEÚDO — é o que o painel edita
│   ├── site.json          telefone, e-mail, OAB, menus (vale para todas as páginas)
│   ├── home.json          textos da página inicial
│   ├── sobre.json         textos da página "Sobre"
│   ├── areas.json         textos de "Áreas de atuação"
│   ├── reforma.json       textos de "Reforma tributária"
│   ├── blog.json          textos fixos da página de blog
│   ├── contato.json       textos da página de contato
│   ├── privacidade.json   textos da política de privacidade
│   └── eleventyComputed.js liga cada página ao seu arquivo de conteúdo
├── _includes/
│   ├── base.njk           <head>, cabeçalho, menu e rodapé de todas as páginas
│   └── icones.njk         SVGs dos cards, escolhidos por nome no painel
├── posts/*.md             artigos do blog (um arquivo por artigo)
├── admin/                 painel de edição (Sveltia CMS)
├── *.njk                  as 7 páginas — só a estrutura, sem texto fixo
├── css/  js/  assets/     copiados sem alteração para o site final

design/                    arte-fonte da logo; NÃO vai para o site publicado
comparar-conteudo.py       verifica que nenhum texto se perdeu
comparar-estrutura.py      verifica que o HTML entregue não mudou de forma
```

A regra: **texto fica em `_data/` ou em `posts/`; estrutura fica nos `.njk`.**
Se um texto está escrito dentro de um `.njk`, a Glauciane não consegue editá-lo.

## Como ela edita

Acessa `https://<site>/admin`, faz login com a conta do GitHub e edita em
formulários com rótulos em português. Ao salvar, o Sveltia CMS grava um commit
no repositório, a Netlify reconstrói e a alteração entra no ar em cerca de um
minuto. Como cada edição é um commit, dá para desfazer qualquer mudança.

Fica fora do painel, por decisão de projeto: layout, CSS, ícones e a estrutura
das páginas.

## Formulário de contato

Usa **Netlify Forms**: o atributo `data-netlify` em `src/contato.njk` faz a
Netlify reconhecer o formulário no build e passar a receber os envios; o
`js/main.js` valida os campos e faz o POST. Não há backend nem chave de API.
Os envios aparecem no painel da Netlify e são enviados por e-mail. O campo-isca
`bot-field` barra robôs sem precisar de captcha. O plano gratuito cobre 100
envios por mês.

## Verificação

Os dois scripts comparam o site gerado com o commit `acbd9ba` — o site estático
original, antes da migração:

```
npm run build
python comparar-conteudo.py     # nenhum texto perdido ou alterado
python comparar-estrutura.py    # HTML com a mesma estrutura e classes
```

As diferenças intencionais (posts que passaram a ser gerados no build, campos do
Netlify Forms) estão listadas com justificativa no topo de cada script. Qualquer
diferença fora dessa lista faz o script falhar — use-os depois de mexer nos
templates.

## Publicação

Configurada em `netlify.toml`: build `npm run build`, pasta publicada `_site`.
Todo commit na branch `main` republica o site.

## Pendências conhecidas

- **`src/admin/config.yml`** está com `repo: USUARIO/REPOSITORIO` — precisa
  apontar para o repositório real antes do painel funcionar.
- **Analytics** já está ligado no template, mas inativo: preencher
  `analytics_token` em `site.json` com o código do Cloudflare Web Analytics.
- **Política de privacidade** tem dois trechos-modelo entre colchetes que
  precisam de revisão jurídica — mais relevante agora que o formulário
  realmente coleta dados.
- **Artigos do blog** não têm página individual. Os cards mostram título e
  resumo, e o link "Ler artigo" ainda não leva a lugar nenhum. Os arquivos em
  `src/posts/` já têm um campo de texto para o artigo completo; para publicar
  as páginas, basta remover `permalink: false` de `src/posts/posts.json` e
  criar o template do artigo.
- **Publicidade advocatícia**: revisar a linguagem do site à luz do Provimento
  205/2021 da OAB antes de divulgar.
