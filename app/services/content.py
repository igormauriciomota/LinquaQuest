import json


LEVEL_NAMES = {1: "Básico", 2: "Intermediário", 3: "Avançado", 4: "Fluente"}


LESSONS = [
    {
        "slug": "verbo-to-be", "level": 1, "position": 1, "title": "Verbo to be",
        "subtitle": "I am, you are, he is", "icon": "bi-person-check", "color": "violet",
        "objective": "Apresentar-se e formar frases afirmativas e negativas.",
        "vocab": [("I am", "eu sou/estou"), ("you are", "você é/está"), ("he is", "ele é/está"), ("she is", "ela é/está"), ("we are", "nós somos/estamos")],
        "challenge": {"prompt": "Complete: She ___ a developer.", "options": ["am", "is", "are", "be"], "answer": "is", "explanation": "Com she, usamos is."},
        "writing": {"prompt": "Traduza: Eu sou estudante.", "accepted": ["i am a student", "i'm a student"], "model": "I am a student."},
    },
    {
        "slug": "cumprimentos", "level": 1, "position": 2, "title": "Cumprimentos",
        "subtitle": "Hello, good morning, goodbye", "icon": "bi-chat-heart", "color": "cyan",
        "objective": "Cumprimentar, apresentar-se e despedir-se com naturalidade.",
        "vocab": [("hello", "olá"), ("good morning", "bom dia"), ("good afternoon", "boa tarde"), ("good evening", "boa noite (chegada)"), ("goodbye", "adeus")],
        "challenge": {"prompt": "Qual frase usamos ao chegar à noite?", "options": ["Good evening", "Good night", "Goodbye", "See you"], "answer": "Good evening", "explanation": "Good evening é cumprimento; good night é despedida ou hora de dormir."},
        "writing": {"prompt": "Escreva em inglês: Prazer em conhecer você.", "accepted": ["nice to meet you"], "model": "Nice to meet you."},
    },
    {
        "slug": "numeros-0-50", "level": 1, "position": 3, "title": "Números 0–50",
        "subtitle": "Ouça, reconheça e fale", "icon": "bi-123", "color": "amber",
        "objective": "Reconhecer números e compreender a formação das dezenas.",
        "vocab": [("zero / oh", "zero"), ("six", "seis"), ("thirteen", "treze"), ("twenty", "vinte"), ("forty-five", "quarenta e cinco")],
        "challenge": {"prompt": "Como se escreve 40 em inglês?", "options": ["forty", "fourty", "fourteen", "four"], "answer": "forty", "explanation": "A grafia correta é forty, sem a letra u."},
        "writing": {"prompt": "Escreva 32 por extenso em inglês.", "accepted": ["thirty-two", "thirty two"], "model": "thirty-two"},
    },
    {
        "slug": "telefone", "level": 1, "position": 4, "title": "Telefone",
        "subtitle": "What's your phone number?", "icon": "bi-telephone", "color": "pink",
        "objective": "Pedir, ditar e confirmar números de telefone.",
        "vocab": [("phone number", "número de telefone"), ("What's your number?", "Qual é o seu número?"), ("six oh seven", "seis zero sete"), ("repeat, please", "repita, por favor"), ("Is that correct?", "Está correto?")],
        "challenge": {"prompt": "Você ouviu: six, oh, seven, three. Qual é o número?", "options": ["6073", "6072", "6703", "0673"], "answer": "6073", "explanation": "Em telefones, oh é uma forma comum de dizer zero."},
        "writing": {"prompt": "Escreva 3-5-0-9 em inglês, separado por espaços.", "accepted": ["three five oh nine", "three five zero nine"], "model": "three five oh nine"},
    },
    {
        "slug": "frutas-e-alimentos", "level": 2, "position": 1, "title": "Frutas e alimentos",
        "subtitle": "Food vocabulary", "icon": "bi-apple", "color": "lime",
        "objective": "Usar substantivos e preferências em situações de alimentação.",
        "vocab": [("apple", "maçã"), ("banana", "banana"), ("strawberry", "morango"), ("bread", "pão"), ("cheese", "queijo")],
        "challenge": {"prompt": "Complete: I would like ___ apple.", "options": ["an", "a", "some", "the two"], "answer": "an", "explanation": "Usamos an antes de som vocálico: an apple."},
        "writing": {"prompt": "Traduza: Eu gosto de morangos.", "accepted": ["i like strawberries"], "model": "I like strawberries."},
    },
    {
        "slug": "animais-e-lugares", "level": 2, "position": 2, "title": "Animais e lugares",
        "subtitle": "Animals around town", "icon": "bi-geo-alt", "color": "cyan",
        "objective": "Descrever animais e localizar lugares usando preposições.",
        "vocab": [("dog", "cachorro"), ("cat", "gato"), ("bird", "pássaro"), ("park", "parque"), ("countryside", "zona rural")],
        "challenge": {"prompt": "The dog is ___ the park.", "options": ["in", "at Monday", "of", "to"], "answer": "in", "explanation": "In the park indica dentro/no parque."},
        "writing": {"prompt": "Traduza: O gato está na casa.", "accepted": ["the cat is in the house"], "model": "The cat is in the house."},
    },
    {
        "slug": "presente-simples", "level": 2, "position": 3, "title": "Presente simples",
        "subtitle": "Routines and habits", "icon": "bi-calendar-check", "color": "violet",
        "objective": "Falar de rotina, frequência e hábitos no presente.",
        "vocab": [("I work", "eu trabalho"), ("I study", "eu estudo"), ("I wake up", "eu acordo"), ("I usually", "eu geralmente"), ("every day", "todos os dias")],
        "challenge": {"prompt": "Complete: He ___ Python every day.", "options": ["studies", "study", "studying", "studied"], "answer": "studies", "explanation": "Na terceira pessoa, study vira studies."},
        "writing": {"prompt": "Traduza: Eu estudo inglês todos os dias.", "accepted": ["i study english every day", "i study english everyday"], "model": "I study English every day."},
    },
    {
        "slug": "dialogos-cotidianos", "level": 2, "position": 4, "title": "Diálogos cotidianos",
        "subtitle": "Real-life conversations", "icon": "bi-people", "color": "amber",
        "objective": "Responder de forma adequada em restaurante, loja e transporte.",
        "vocab": [("How can I help?", "Como posso ajudar?"), ("I'd like...", "Eu gostaria de..."), ("How much is it?", "Quanto custa?"), ("Here you are", "Aqui está"), ("Thank you", "Obrigado")],
        "challenge": {"prompt": "Garçom: What would you like? Você responde:", "options": ["I'd like some water, please.", "I'm water.", "Where water?", "Water is blue."], "answer": "I'd like some water, please.", "explanation": "I'd like... é uma forma educada de fazer pedidos."},
        "writing": {"prompt": "Peça um café de forma educada.", "accepted": ["i'd like a coffee please", "i would like a coffee please", "can i have a coffee please"], "model": "I'd like a coffee, please."},
    },
    {
        "slug": "passado-simples", "level": 3, "position": 1, "title": "Passado simples",
        "subtitle": "Yesterday and last week", "icon": "bi-clock-history", "color": "pink",
        "objective": "Relatar acontecimentos usando verbos regulares e irregulares.",
        "vocab": [("worked", "trabalhou"), ("studied", "estudou"), ("went", "foi"), ("saw", "viu"), ("yesterday", "ontem")],
        "challenge": {"prompt": "Complete: Yesterday, I ___ to work.", "options": ["went", "go", "goed", "going"], "answer": "went", "explanation": "O passado irregular de go é went."},
        "writing": {"prompt": "Traduza: Eu estudei Python ontem.", "accepted": ["i studied python yesterday"], "model": "I studied Python yesterday."},
    },
    {
        "slug": "tempos-e-conectores", "level": 3, "position": 2, "title": "Tempos e conectores",
        "subtitle": "Build richer sentences", "icon": "bi-diagram-3", "color": "lime",
        "objective": "Conectar ideias com contraste, causa, condição e sequência.",
        "vocab": [("however", "porém"), ("therefore", "portanto"), ("although", "embora"), ("because", "porque"), ("unless", "a menos que")],
        "challenge": {"prompt": "I was tired; ___, I finished the project.", "options": ["however", "because", "unless", "therefore not"], "answer": "however", "explanation": "However introduz contraste: estava cansado, porém terminei."},
        "writing": {"prompt": "Traduza: Eu pratiquei porque queria melhorar.", "accepted": ["i practiced because i wanted to improve", "i practised because i wanted to improve"], "model": "I practiced because I wanted to improve."},
    },
    {
        "slug": "ingles-para-python", "level": 3, "position": 3, "title": "Inglês para Python",
        "subtitle": "Code, errors and documentation", "icon": "bi-code-slash", "color": "violet",
        "objective": "Entender documentação, mensagens de erro e vocabulário de código.",
        "vocab": [("variable", "variável"), ("return value", "valor de retorno"), ("loop", "laço de repetição"), ("raise an exception", "lançar uma exceção"), ("debug", "depurar")],
        "challenge": {"prompt": "O que significa 'The function returns a list'?", "options": ["A função retorna uma lista", "A lista apaga a função", "A função repete", "A lista contém um erro"], "answer": "A função retorna uma lista", "explanation": "Return é uma palavra essencial para ler documentação de APIs e funções."},
        "writing": {"prompt": "Traduza: Corrija o erro e execute os testes.", "accepted": ["fix the error and run the tests", "fix the bug and run the tests"], "model": "Fix the error and run the tests."},
    },
    {
        "slug": "git-e-equipe", "level": 3, "position": 4, "title": "Git e trabalho em equipe",
        "subtitle": "Commits, reviews and meetings", "icon": "bi-git", "color": "cyan",
        "objective": "Comunicar mudanças técnicas e colaborar em projetos.",
        "vocab": [("commit changes", "registrar alterações"), ("pull request", "solicitação de integração"), ("code review", "revisão de código"), ("branch", "ramificação"), ("merge conflict", "conflito de mesclagem")],
        "challenge": {"prompt": "Qual frase é adequada numa revisão?", "options": ["Could you clarify this function?", "Your code bad.", "Delete everything.", "No understand."], "answer": "Could you clarify this function?", "explanation": "Could you... torna o pedido claro, profissional e cortês."},
        "writing": {"prompt": "Traduza: Eu abri uma pull request.", "accepted": ["i opened a pull request", "i created a pull request"], "model": "I opened a pull request."},
    },
    {
        "slug": "arquitetura-e-apis", "level": 4, "position": 1, "title": "Arquitetura e APIs",
        "subtitle": "Explain technical decisions", "icon": "bi-braces-asterisk", "color": "amber",
        "objective": "Explicar integrações, dados, endpoints e decisões arquiteturais.",
        "vocab": [("endpoint", "ponto de acesso"), ("request payload", "corpo da requisição"), ("database query", "consulta ao banco"), ("scalable", "escalável"), ("trade-off", "compensação/escolha")],
        "challenge": {"prompt": "Choose the clearest technical sentence:", "options": ["The endpoint validates the payload before saving it.", "Endpoint make save maybe.", "The payload is endpointing.", "Database request good."], "answer": "The endpoint validates the payload before saving it.", "explanation": "A frase usa sujeito, verbo, objeto e sequência de forma precisa."},
        "writing": {"prompt": "Traduza: A API retorna uma resposta em JSON.", "accepted": ["the api returns a json response", "the api returns a response in json"], "model": "The API returns a JSON response."},
    },
    {
        "slug": "entrevista-tecnica", "level": 4, "position": 2, "title": "Entrevista técnica",
        "subtitle": "Present your experience", "icon": "bi-mic", "color": "pink",
        "objective": "Apresentar experiência, projetos e raciocínio em entrevistas.",
        "vocab": [("strength", "ponto forte"), ("challenge", "desafio"), ("achievement", "conquista"), ("maintainable code", "código de fácil manutenção"), ("problem-solving", "resolução de problemas")],
        "challenge": {"prompt": "Interviewer: Tell me about a challenge. Melhor início:", "options": ["In my last project, I had to...", "I no challenge.", "Challenge is bad.", "Next question."], "answer": "In my last project, I had to...", "explanation": "A resposta cria contexto e prepara ação e resultado (método STAR)."},
        "writing": {"prompt": "Traduza: Meu ponto forte é resolver problemas.", "accepted": ["my strength is solving problems", "my strength is problem-solving", "my strength is problem solving"], "model": "My strength is problem-solving."},
    },
    {
        "slug": "reunioes-e-negociacao", "level": 4, "position": 3, "title": "Reuniões e negociação",
        "subtitle": "Agree, disagree and clarify", "icon": "bi-briefcase", "color": "lime",
        "objective": "Participar de reuniões, esclarecer requisitos e negociar prazos.",
        "vocab": [("deadline", "prazo final"), ("requirement", "requisito"), ("Could you clarify?", "Você poderia esclarecer?"), ("I see your point", "Entendo seu ponto"), ("Let's follow up", "Vamos retomar depois")],
        "challenge": {"prompt": "Como discordar de modo profissional?", "options": ["I see your point, but I have a concern.", "You are wrong.", "That is nonsense.", "No."], "answer": "I see your point, but I have a concern.", "explanation": "Reconhecer o ponto antes de expor uma preocupação reduz confronto."},
        "writing": {"prompt": "Traduza: Podemos revisar o prazo amanhã?", "accepted": ["can we review the deadline tomorrow", "could we review the deadline tomorrow"], "model": "Can we review the deadline tomorrow?"},
    },
    {
        "slug": "projeto-final", "level": 4, "position": 4, "title": "Projeto final",
        "subtitle": "English for a software demo", "icon": "bi-trophy", "color": "violet",
        "objective": "Apresentar uma aplicação, seu valor, arquitetura e próximos passos.",
        "vocab": [("live demo", "demonstração ao vivo"), ("user feedback", "retorno do usuário"), ("key feature", "funcionalidade principal"), ("deployment", "implantação"), ("next steps", "próximos passos")],
        "challenge": {"prompt": "Complete: This feature ___ users to import data.", "options": ["allows", "allow", "letting", "make"], "answer": "allows", "explanation": "Feature é terceira pessoa do singular, portanto usamos allows."},
        "writing": {"prompt": "Traduza: Agora vou demonstrar a principal funcionalidade.", "accepted": ["now i will demonstrate the main feature", "now i'll demonstrate the key feature", "now i am going to demonstrate the main feature"], "model": "Now I'll demonstrate the key feature."},
    },
]


def _exercise_set(lesson):
    vocab = lesson["vocab"]
    first, second = vocab[0], vocab[1]
    translations = [pair[1] for pair in vocab]
    challenge = lesson["challenge"]
    writing = lesson["writing"]
    matching_answer = {left: right for left, right in vocab}
    return [
        {
            "kind": "choice", "prompt": f'Qual é a tradução de “{first[0]}”?',
            "instruction": "Escolha a melhor opção.",
            "payload": {"options": translations, "speak": first[0]}, "answer": first[1],
            "explanation": f'{first[0]} = {first[1]}.', "xp": 10,
        },
        {
            "kind": "match", "prompt": "Combine os pares",
            "instruction": "Selecione uma palavra em inglês e depois a tradução correspondente.",
            "payload": {"pairs": [{"left": left, "right": right} for left, right in vocab]},
            "answer": matching_answer, "explanation": "Ótimo! As associações fortalecem a memória de reconhecimento.", "xp": 20,
        },
        {
            "kind": "listen", "prompt": "O que você ouviu?",
            "instruction": "Use o botão de áudio e escolha a tradução.",
            "payload": {"options": translations, "speak": second[0]}, "answer": second[1],
            "explanation": f'A expressão foi “{second[0]}”, que significa “{second[1]}”.', "xp": 15,
        },
        {
            "kind": "choice", "prompt": challenge["prompt"],
            "instruction": "Aplique a regra no contexto.",
            "payload": {"options": challenge["options"]}, "answer": challenge["answer"],
            "explanation": challenge["explanation"], "xp": 15,
        },
        {
            "kind": "write", "prompt": writing["prompt"],
            "instruction": "Digite a resposta. Maiúsculas e pontuação são opcionais.",
            "payload": {"placeholder": "Escreva em inglês...", "accepted": writing["accepted"]},
            "answer": writing["accepted"], "explanation": f'Modelo: {writing["model"]}', "xp": 20,
        },
    ]


def seed_content(db):
    for lesson in LESSONS:
        db.execute(
            """
            INSERT INTO lessons (slug, level, position, title, subtitle, icon, color, objective)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                title=excluded.title, subtitle=excluded.subtitle, icon=excluded.icon,
                color=excluded.color, objective=excluded.objective
            """,
            (lesson["slug"], lesson["level"], lesson["position"], lesson["title"],
             lesson["subtitle"], lesson["icon"], lesson["color"], lesson["objective"]),
        )
        lesson_id = db.execute("SELECT id FROM lessons WHERE slug = ?", (lesson["slug"],)).fetchone()["id"]
        for position, exercise in enumerate(_exercise_set(lesson), start=1):
            db.execute(
                """
                INSERT INTO exercises
                    (lesson_id, position, kind, prompt, instruction, payload, answer, explanation, xp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(lesson_id, position) DO UPDATE SET
                    kind=excluded.kind, prompt=excluded.prompt, instruction=excluded.instruction,
                    payload=excluded.payload, answer=excluded.answer,
                    explanation=excluded.explanation, xp=excluded.xp
                """,
                (lesson_id, position, exercise["kind"], exercise["prompt"], exercise["instruction"],
                 json.dumps(exercise["payload"], ensure_ascii=False),
                 json.dumps(exercise["answer"], ensure_ascii=False),
                 exercise["explanation"], exercise["xp"]),
            )
