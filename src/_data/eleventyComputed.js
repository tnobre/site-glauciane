// Cada página declara no topo do arquivo qual bloco de conteúdo usa
// (ex.: `pagina: sobre` → src/_data/sobre.json). Isto copia o título e a
// descrição de lá para o <head>, evitando que esses textos precisem ser
// repetidos no template — a Glauciane edita só no painel.
export default {
  titulo_pagina: (data) =>
    data.pagina && data[data.pagina] ? data[data.pagina].titulo_pagina : data.titulo_pagina,
  descricao: (data) =>
    data.pagina && data[data.pagina] ? data[data.pagina].descricao : data.descricao,
};
