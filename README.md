# LinguaQuest

**Learning through memorization** — plataforma web em Flask para aprender inglês do nível básico ao fluente com áudio, jogos de associação, repetição espaçada e uma trilha especial de inglês para profissionais de tecnologia.

## Visão do produto

O LinguaQuest transforma vocabulário e gramática em uma jornada visual, curta e progressiva. O projeto foi inspirado em cartões ilustrados, atividades de combinar pares e aplicativos de aprendizagem gamificada, mas possui identidade e lógica próprias.

O estudante encontra:

- quatro níveis: **Básico, Intermediário, Avançado e Fluente**;
- painel em quatro **mundos**, com 16 fases numeradas, missão recomendada e desbloqueio progressivo;
- 16 lições da trilha principal e 80 exercícios iniciais;
- 9 unidades bilíngues extraídas das aulas presenciais, com 54 novos jogos;
- 15 textos avançados para leitura, escuta, *shadowing* e prática oral;
- exercícios de múltipla escolha, escuta, escrita e associação;
- números de 0 a 50 e treino de telefone com `oh` para zero;
- cumprimentos, frutas, alimentos, animais, lugares, diálogos e tempos verbais;
- inglês para Python, Git, APIs, entrevistas, reuniões e apresentações técnicas;
- temas presenciais: comunicação, rotina, alimentação, restaurante, dinheiro, tecnologia, intercâmbio, história e cidadania;
- XP, sequência diária, percentual de domínio e desbloqueio progressivo;
- revisão inteligente pelo método Leitner;
- cartões pessoais com imagem, tradução e pronúncia;
- interface responsiva construída com Bootstrap, Bootstrap Icons e CSS próprio.
- **Arena de Pares** com 8 temas, 92 associações inglês–português e XP próprio;
- **Laboratório de Áudio — Família, cidade e cumprimentos**, com 64 trechos bilíngues e 128 áudios em velocidade normal e lenta;
- temas escuro e claro persistentes, painel de alto contraste e ajuste de texto;
- navegação completa por mouse, toque e teclado, com foco visível e avisos para leitor de tela;
- glassmorphism, microanimações e profundidade 3D responsiva feita somente com CSS.

## Tecnologias

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| Back-end | Python 3.11+ e Flask 3 | rotas, sessões, regras e APIs JSON |
| Banco | SQLite | usuários, lições, exercícios, progresso e revisões |
| Imagens | Pillow (PIL) | validação, orientação EXIF, recorte, miniatura e WEBP |
| Segurança de nomes | `secure_filename` + UUID | remove caracteres perigosos e evita colisões |
| Interface | HTML5, Jinja2, CSS Grid, Bootstrap 5 local | páginas acessíveis, responsivas e independentes de CDN |
| Ícones | Flaticon + Bootstrap Icons | ilustração dos mundos e controles funcionais |
| Áudio | MP3 das aulas + Web Speech API | escuta normal/lenta e pronúncia dinâmica |
| Acessibilidade | HTML semântico, ARIA e preferências locais | teclado, leitor de tela, contraste e redução de movimento |
| Testes | `unittest` + cliente de testes Flask | autenticação, lições, CSRF e upload |

## Arquitetura

```text
linguaquest/
├── app/
│   ├── __init__.py                 # fábrica create_app e registro dos módulos
│   ├── database.py                 # conexão SQLite e inicialização
│   ├── schema.sql                  # estrutura relacional e índices
│   ├── security.py                 # CSRF, login obrigatório e normalização
│   ├── blueprints/
│   │   ├── auth/                   # cadastro, login e logout
│   │   ├── main/                   # landing page e painel/trilha
│   │   ├── learning/               # lições, respostas, revisão e resultado
│   │   └── profile/                # perfil, uploads e cartões pessoais
│   ├── services/
│   │   ├── content.py              # currículo e criação de 80 exercícios
│   │   ├── classroom_content.py    # 9 aulas presenciais e 54 jogos bilíngues
│   │   ├── reading_content.py      # 15 textos dos níveis avançado e fluente
│   │   ├── match_content.py        # 8 temas e 92 pares bilíngues
│   │   ├── images.py               # pipeline seguro com Pillow
│   │   └── learning.py             # correção e algoritmo de revisão
│   ├── static/
│   │   ├── audio/family/            # 128 áudios importados da aula fornecida
│   │   ├── images/brand/            # ilustrações WEBP originais e otimizadas
│   │   ├── images/flaticon/         # ícones dos quatro mundos
│   │   ├── css/app.css              # sistema visual responsivo
│   │   └── js/                      # áudio, jogos, números e laboratórios
│   └── templates/                  # páginas Jinja2
├── tools/import_family_lesson.py   # importador reproduzível do HTML da aula
├── instance/                       # banco e uploads locais (não versionados)
├── tests/test_app.py               # testes automatizados
├── config.py                       # configurações e limites
├── run.py                          # desenvolvimento
├── wsgi.py                         # produção/Gunicorn
└── requirements.txt
```

## Como executar no Windows

Abra o terminal do VS Code na pasta do projeto:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
py run.py
```

Se o PowerShell bloquear a ativação, execute uma vez no terminal atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Acesse `http://127.0.0.1:5000`.

Como atalho, também é possível clicar duas vezes em `INICIAR_WINDOWS.bat`; ele cria o ambiente virtual, instala as dependências e inicia o servidor.

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Fluxo de aprendizado

1. O aluno cria a conta; a senha é armazenada como hash, nunca em texto puro.
2. A primeira lição é liberada e as demais dependem da conclusão anterior.
3. Cada exercício é validado no servidor — a resposta correta não é enviada antecipadamente ao navegador.
4. Ao acertar pela primeira vez, o aluno recebe todo o XP; repetições corretas rendem apenas 2 XP para evitar pontuação artificial.
5. Com pelo menos 60% de acertos, a lição é concluída e a próxima é liberada.
6. Cada resposta entra no sistema Leitner. Acertos aumentam o intervalo para 1, 3, 7, 14 e 30 dias; erros voltam à primeira caixa.

## Arena de Pares

A rota `/aprender/arena-pares` apresenta as palavras em duas colunas explícitas: **English** à esquerda e **Português** à direita. Há oito conjuntos: cumprimentos, números, cores, partes do corpo, comidas e bebidas, animais e frutas, lugares e direções, e Python e tecnologia.

O jogador pode usar:

- mouse ou toque: clicar na palavra inglesa e depois na tradução;
- teclado: `Tab` e `Shift+Tab` para navegar, `Enter` ou `Espaço` para selecionar;
- leitor de tela: cada seleção, erro, acerto e progresso é anunciado em uma região `aria-live`.

Cada tema concluído pela primeira vez rende 20 XP. O SQLite guarda melhor pontuação, número de tentativas e conclusão sem permitir XP repetido ilimitadamente.

## Mundos, fases e páginas de aula

O painel autenticado apresenta uma jornada fácil de compreender:

1. **Mundo 1 — Primeiros passos:** base, verbo *to be*, números e vocabulário essencial;
2. **Mundo 2 — Vida em movimento:** rotina, lugares, comidas e situações reais;
3. **Mundo 3 — Inglês em ação:** textos, argumentação e tecnologia;
4. **Mundo 4 — Comunicação sem fronteiras:** fluência e comunicação profissional.

Cada card de fase possui um botão explícito e abre sua própria URL de aula. Cards de laboratórios levam à Arena de Pares, ao Laboratório de Áudio ou à biblioteca de leitura. Os cards das aulas presenciais também abrem páginas próprias com o conteúdo e os exercícios daquele tema.

Na versão 5, o painel principal segue uma composição editorial semelhante à referência aprovada: hero fotográfico amplo, progresso em glassmorphism, quatro mundos em uma grade única e três laboratórios visuais. Cada mundo abre uma página própria em `/mundo/1` até `/mundo/4`, onde suas quatro fases são exibidas.

O hero e a seção das aulas presenciais usam imagem de fundo com `background-size: cover`, `background-position: center`, camada de contraste em `rgba()` e `background-attachment: fixed`. Em celulares, o fundo passa automaticamente para `scroll`, evitando problemas de desempenho e compatibilidade.

Bootstrap 5.3.8, Bootstrap Icons 1.13.1, o CSS principal e o JavaScript são servidos pela própria aplicação. A URL versionada dos arquivos (`?v=5.0`) evita que uma versão antiga do CSS permaneça no cache e quebre a nova estrutura.

## Laboratório de áudio das aulas presenciais

O arquivo HTML “Família, cidade e cumprimentos” foi convertido em uma aula interativa com 64 trechos e 128 arquivos MP3. Cada item apresenta inglês, tradução em português, reprodução normal e lenta. O aluno pode pesquisar, filtrar por parte da aula e acompanhar os trechos já ouvidos. Aos 48 itens, recebe 30 XP apenas uma vez.

Para refazer a importação a partir do material original:

```bash
python tools/import_family_lesson.py /caminho/para/aula_familia_cidade_cumprimentos.html
```

## Design inclusivo nativo

O menu de acessibilidade está disponível em todas as páginas. Ele oferece texto entre 90% e 130%, alto contraste, redução de movimentos e restauração das preferências. O tema claro/escuro acompanha inicialmente a configuração do dispositivo e pode ser alternado manualmente; as escolhas ficam salvas no navegador.

Os cartões de vidro usam bordas visíveis e fundos sólidos de reserva. Efeitos 3D e microanimações são decorativos, não carregam informação essencial e são desligados automaticamente por `prefers-reduced-motion` ou pelo controle interno. Foco por teclado, texto e ícones comunicam os estados sem depender somente de cor.

## Processamento profissional de imagens

O serviço `app/services/images.py` executa o seguinte pipeline:

1. limita o corpo da requisição a 5 MB;
2. aceita somente extensões JPG, JPEG, PNG e WEBP;
3. passa o nome por `secure_filename`;
4. acrescenta UUID para impedir colisões e adivinhação de nomes;
5. abre e verifica os bytes com Pillow, evitando aceitar arquivo falso;
6. corrige a orientação registrada nos metadados EXIF;
7. converte para RGB;
8. recorta avatares e limita imagens comuns a 1200 × 900;
9. cria miniatura 320 × 240;
10. salva em WEBP otimizado, com qualidade adequada à web.

Os arquivos ficam em `instance/uploads`. Em produção, recomenda-se armazená-los em serviço próprio para objetos, como S3, e servi-los por CDN.

## Áudio e pronúncia

O botão de áudio usa `speechSynthesis` com preferência por uma voz `en-US`. A estratégia deixa o projeto leve e permite ouvir qualquer cartão criado pelo estudante. Chrome, Edge e Safari normalmente oferecem vozes nativas. Para um produto comercial, pode-se substituir essa camada por áudios humanos ou TTS em nuvem sem alterar a lógica dos exercícios.

## Conteúdo das aulas presenciais

As dez apostilas fornecidas foram analisadas e transformadas em nove unidades. Os materiais “Food” e “Yum or Yuck?” apresentavam o mesmo conteúdo e foram consolidados em uma única unidade, preservando vocabulário, frases e objetivos.

Cada unidade possui:

- objetivo pedagógico em inglês e português;
- dez palavras ou expressões bilíngues;
- frases para ouvir e repetir;
- perguntas para conversação;
- associação de pares;
- compreensão auditiva;
- múltipla escolha contextual;
- diálogo com resposta natural;
- tradução escrita;
- pontuação, tentativa e registro de conclusão.

## Reading & Speaking Lab

Os níveis 3 e 4 incluem quinze textos progressivos. Os primeiros trabalham rotina, estudo, viagens e projetos Python. Os últimos tratam de apresentações profissionais, entrevistas, análise de dados, APIs, segurança, revisão de código e inteligência artificial.

O método de cada texto segue quatro etapas:

1. ler o conteúdo em inglês antes de consultar a tradução;
2. ouvir em velocidade normal ou lenta;
3. repetir cada frase pelo método de *shadowing*;
4. responder perguntas de compreensão e revisar o vocabulário.

Quando o navegador oferece `SpeechRecognition`, o aluno pode falar a frase e receber uma estimativa de palavras reconhecidas. O LinguaQuest não grava nem armazena o áudio; o processamento depende do mecanismo de voz do navegador. A permissão do microfone só é solicitada quando o aluno escolhe iniciar essa prática.

## Segurança implementada

- hash de senha do Werkzeug;
- consultas SQLite parametrizadas;
- token CSRF em formulários e requisições JSON;
- cookies `HttpOnly` e `SameSite=Lax`;
- limite de upload e validação real da imagem;
- nomes saneados e aleatórios;
- controle de propriedade ao excluir cartões;
- respostas dos exercícios corrigidas no back-end;
- cabeçalhos contra MIME sniffing e carregamento em iframe.

Antes de publicar, copie `.env.example` para `.env`, use uma `SECRET_KEY` longa e ative `SESSION_COOKIE_SECURE=1` quando o site estiver em HTTPS.

## Testes

Com o ambiente virtual ativo:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam:

- criação de conta e carga das 16 lições/80 exercícios;
- conclusão integral de uma lição;
- bloqueio de requisição com CSRF inválido;
- upload, saneamento do nome e geração de miniatura WEBP.
- carga das 9 aulas presenciais, 54 desafios e 15 textos;
- abertura de unidade presencial, laboratório de leitura e registro de conclusão.
- abertura da Arena de Pares, salvamento de pontuação, XP único e repetição sem duplicar recompensa.
- abertura do Laboratório de Áudio, renderização dos 64 cards e recompensa única de 30 XP.
- abertura das quatro páginas de mundos e presença de quatro fases específicas em cada uma.

Os créditos dos ícones, ilustrações e materiais importados estão documentados em [`CREDITS.md`](CREDITS.md). A atribuição dos ícones Flaticon também permanece visível no rodapé da aplicação.

## Escopo de produção e hospedagem

O projeto inclui analytics educacional local — XP, sequência, progresso por lição, leitura e tema de associação. SSL, CDN global, CRM e agentes de IA são serviços de infraestrutura e negócio: devem ser conectados no momento da publicação, em vez de simulados no código local. A landing page usa navegação curta em seções, enquanto o ambiente autenticado permanece multipágina para manter URLs, progresso e exercícios bem definidos.

## Como criar uma nova lição

Abra `app/services/content.py` e acrescente um dicionário a `LESSONS` com:

- `slug`, nível, posição, título, subtítulo, ícone e cor;
- objetivo pedagógico;
- cinco pares de vocabulário;
- desafio contextual com quatro opções;
- atividade escrita com variações aceitas.

Ao iniciar o sistema, `seed_content` registra ou atualiza a lição. A função `_exercise_set` transforma cada definição em cinco atividades diferentes.

## Próximas evoluções comerciais

- painel administrativo para professores e importação de cursos;
- gravação e avaliação de pronúncia pelo microfone;
- áudios humanos em velocidade lenta e natural;
- metas semanais, ligas, conquistas e desafios entre amigos;
- trilhas A1–C2 alinhadas ao CEFR;
- PWA para instalação e estudo offline;
- PostgreSQL, fila de tarefas e armazenamento em nuvem;
- relatórios de domínio por habilidade e exportação para PDF;
- assinatura, planos de turma e gestão escolar.

## Licença

Código entregue para estudo e evolução do projeto. Antes de comercializar, defina uma licença própria, política de privacidade, termos de uso e direitos sobre todo conteúdo visual e sonoro publicado.
