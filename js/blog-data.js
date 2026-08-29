// ============================================================
// blog-data.js — conteúdo dos artigos do blog.
//
// Por que um array JS e não um fetch em data/posts.json?
// Navegadores bloqueiam fetch() de arquivos abertos direto do
// disco (protocolo file://). Assim que o site for publicado em
// um servidor real (Vercel, Netlify, hospedagem própria), esse
// array pode ser substituído por:
//   fetch('/data/posts.json').then(r => r.json())
// mantendo exatamente o mesmo formato. Veja data/posts.json,
// que já existe pronto para essa migração.
// ============================================================

const BLOG_POSTS = [
  {
    slug: "ibs-cbs-o-que-muda-para-empresas",
    date: "2026-06-10",
    title: "IBS e CBS: o que muda na prática para sua empresa",
    excerpt:
      "Um resumo direto de como o novo sistema de tributação sobre o consumo altera apuração, créditos e obrigações acessórias.",
  },
  {
    slug: "cronograma-transicao-reforma-tributaria",
    date: "2026-05-22",
    title: "Cronograma da transição: o que entra em vigor e quando",
    excerpt:
      "Da fase de testes até a extinção dos tributos antigos: entenda os prazos que já estão definidos até 2033.",
  },
  {
    slug: "planejamento-tributario-antes-da-reforma",
    date: "2026-04-30",
    title: "Por que revisar seu planejamento tributário agora",
    excerpt:
      "Decisões tomadas hoje sobre regime, contratos e precificação têm efeito direto na transição para o novo modelo.",
  },
];
