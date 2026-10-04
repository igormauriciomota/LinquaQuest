# LinguaQuest 5.0 — Painel editorial fiel à referência

## Correção principal

A tela sem formatação era causada pela combinação de dependências externas e cache de uma versão anterior do CSS. A versão 5 inclui Bootstrap, Bootstrap Icons, CSS e JavaScript localmente e usa URLs versionadas para forçar o carregamento dos estilos atuais.

## Novo painel

- hero fotográfico amplo com camada de contraste;
- imagem de fundo responsiva com `cover`, posição central e efeito parallax;
- painel de progresso com glassmorphism;
- CSS Grid com quatro mundos em uma única linha no desktop;
- CSS Grid com três laboratórios visuais;
- reorganização automática para duas ou uma coluna em tablets e celulares;
- tema claro inicial e dark mode disponível no botão do cabeçalho;
- cards inteiros clicáveis por mouse, com links acessíveis por teclado;
- seção parallax para as nove aulas presenciais;
- barra de atalhos do estudante.

## Navegação por páginas

- `/mundo/1` — Básico / Primeiros passos;
- `/mundo/2` — Intermediário / Vida em movimento;
- `/mundo/3` — Avançado / Inglês em ação;
- `/mundo/4` — Fluente / Comunicação sem fronteiras.

Cada página mostra quatro fases com status disponível, concluída ou bloqueada. Os botões abrem a aula específica daquela fase.

## Arquivos visuais

- `docs/design-reference-v5.png` — referência visual personalizada;
- `app/static/images/brand/` — imagens WEBP usadas no site;
- `app/static/images/flaticon/` — ícones com créditos no rodapé.

## Validação

Oito testes automatizados aprovados, incluindo as quatro novas páginas de mundos, os laboratórios, o jogo, o banco SQLite e uploads com Pillow.
