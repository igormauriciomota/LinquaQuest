# LinguaQuest 3.0 — Arena Inclusiva

## O que mudou

- visual maior, vibrante e responsivo, com área útil de até 1500 px;
- modo escuro e claro com preferência salva no navegador;
- painel de acessibilidade para tamanho de texto, alto contraste e redução de movimento;
- foco visível, link “pular para conteúdo”, HTML semântico e mensagens `aria-live`;
- nova Arena de Pares inglês–português com oito temas e 92 pares;
- suporte a mouse, toque, `Tab`, `Shift+Tab`, `Enter` e `Espaço`;
- pronúncia automática da palavra inglesa selecionada;
- progresso da Arena salvo em SQLite e 20 XP na primeira conclusão de cada tema;
- glassmorphism, microanimações e objetos 3D em CSS, sem dependências gráficas pesadas;
- cartões e telas de exercício ampliados para uso confortável em monitores grandes;
- testes automatizados ampliados para cobrir a Arena e sua regra de XP.

## Decisões de produto

A página pública continua curta e organizada em seções, com chamadas para ação visíveis. O curso após o login permanece dividido em páginas porque isso melhora a navegação, o histórico, o foco do aluno e o salvamento de progresso.

SSL, CDN, Smart CRM e Agent Hub não foram simulados. Eles pertencem à camada de hospedagem e integrações comerciais e podem ser adicionados com serviços reais quando o sistema for publicado.
