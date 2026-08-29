// ============================================================
// Configuração do Eleventy.
//
// O site continua sendo HTML/CSS/JS estático — o Eleventy só
// evita a duplicação do cabeçalho/rodapé e lê os textos dos
// arquivos em src/_data, que são o que a Glauciane edita pelo
// painel em /admin.
// ============================================================

export default function (eleventyConfig) {
  // Arquivos que vão direto para o site, sem processamento.
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/admin");

  // Coleção de posts do blog, do mais recente para o mais antigo.
  eleventyConfig.addCollection("posts", (collection) =>
    collection.getFilteredByGlob("src/posts/*.md").sort((a, b) => b.data.date - a.data.date)
  );

  // Data no formato "10 de junho de 2026".
  //
  // A string vem como "2026-06-10" e é montada em UTC para evitar
  // o deslocamento de um dia que acontecia na versão anterior do
  // site, onde a data era interpretada em UTC e exibida no fuso
  // local (America/Sao_Paulo, UTC-3) — 10/06 virava 09/06.
  eleventyConfig.addFilter("dataPtBr", (valor) => {
    const d = valor instanceof Date ? valor : new Date(`${valor}T00:00:00Z`);
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
      timeZone: "UTC",
    }).format(d);
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
