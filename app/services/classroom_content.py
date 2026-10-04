import json


CLASSROOM_UNITS = [
    {
        "slug": "communication", "position": 1, "title_en": "Communication", "title_pt": "Comunicação",
        "source_title": "Communication - First Steps", "icon": "bi-chat-dots", "color": "violet",
        "goal_en": "Introduce yourself and learn about others.", "goal_pt": "Apresentar-se e conhecer outras pessoas.",
        "vocab": [("hello", "olá"), ("from", "de / vindo de"), ("my name is", "meu nome é"), ("nice to meet you", "prazer em conhecer você"), ("goodbye", "adeus / tchau"), ("introduce", "apresentar"), ("how are you?", "como você está?"), ("talk", "conversar"), ("live with", "morar com"), ("years old", "anos de idade")],
        "phrases": [("Hello! My name is Sara.", "Olá! Meu nome é Sara."), ("I'm from Brazil.", "Eu sou do Brasil."), ("I live with my family.", "Eu moro com minha família."), ("Nice to meet you!", "Prazer em conhecer você!"), ("We talk every day.", "Nós conversamos todos os dias.")],
        "questions": [("Who do you talk to every day?", "Com quem você conversa todos os dias?"), ("How do you introduce a friend?", "Como você apresenta um amigo?"), ("What do you say to someone new?", "O que você diz a alguém novo?")],
        "challenge": ("Complete: Hello! ___ name is Igor.", ["My", "Me", "I", "Mine"], "My", "My name is... significa Meu nome é..."),
        "dialogue": ("A: Nice to meet you!  B: ___", ["Nice to meet you, too!", "I am 20 years.", "Good night yesterday.", "My from Brazil."], "Nice to meet you, too!"),
        "writing": ("Traduza: Eu tenho 41 anos.", ["i am 41 years old", "i'm 41 years old"], "I am 41 years old."),
    },
    {
        "slug": "one-day-in-my-life", "position": 2, "title_en": "One Day in My Life", "title_pt": "Um dia na minha vida",
        "source_title": "One Day in My Life - First Steps", "icon": "bi-alarm", "color": "cyan",
        "goal_en": "Talk about your daily routine.", "goal_pt": "Falar sobre sua rotina diária.",
        "vocab": [("get up", "levantar"), ("have breakfast", "tomar café da manhã"), ("go to work", "ir trabalhar"), ("go to bed", "ir para a cama"), ("clean up", "arrumar / limpar"), ("sometimes", "às vezes"), ("o'clock", "em ponto"), ("busy", "ocupado"), ("Monday", "segunda-feira"), ("Friday", "sexta-feira")],
        "phrases": [("I get up at seven o'clock.", "Eu me levanto às sete horas."), ("I have breakfast before work.", "Eu tomo café antes do trabalho."), ("I am very busy on Friday.", "Eu fico muito ocupado na sexta-feira."), ("I sometimes eat lunch at home.", "Às vezes almoço em casa."), ("I go to bed at ten.", "Eu vou para a cama às dez.")],
        "questions": [("What time do you get up?", "A que horas você se levanta?"), ("What do you do on Monday?", "O que você faz na segunda-feira?"), ("What do you do at home?", "O que você faz em casa?")],
        "challenge": ("Complete: I ___ at 6 o'clock every day.", ["get up", "gets up", "got up", "getting"], "get up", "Com I no presente simples, usamos get up."),
        "dialogue": ("A: What time do you go to bed?  B: ___", ["At ten o'clock.", "On the bed is blue.", "I bed every day.", "Yes, Friday."], "At ten o'clock."),
        "writing": ("Traduza: Eu vou trabalhar de manhã.", ["i go to work in the morning"], "I go to work in the morning."),
    },
    {
        "slug": "food-yum-or-yuck", "position": 3, "title_en": "Food: Yum or Yuck?", "title_pt": "Comida: gostoso ou ruim?",
        "source_title": "Food + Yum or Yuck? - First Steps", "icon": "bi-egg-fried", "color": "lime",
        "goal_en": "Give basic information about foods you like and dislike.", "goal_pt": "Dar informações básicas sobre alimentos de que gosta ou não gosta.",
        "vocab": [("breakfast", "café da manhã"), ("lunch", "almoço"), ("dinner", "jantar"), ("bread", "pão"), ("fruit", "fruta"), ("egg", "ovo"), ("potato", "batata"), ("sandwich", "sanduíche"), ("plate", "prato"), ("kitchen", "cozinha")],
        "phrases": [("I eat bread for breakfast.", "Eu como pão no café da manhã."), ("I don't like fruit.", "Eu não gosto de frutas."), ("We have lunch at noon.", "Nós almoçamos ao meio-dia."), ("My family has dinner together.", "Minha família janta junta."), ("The plate is in the kitchen.", "O prato está na cozinha.")],
        "questions": [("What do you eat for breakfast?", "O que você come no café da manhã?"), ("What food don't you like?", "De qual comida você não gosta?"), ("What do you eat with your family?", "O que você come com sua família?")],
        "challenge": ("Complete: I don't ___ potatoes for breakfast.", ["eat", "eats", "eating", "ate"], "eat", "Depois de don't, usamos o verbo na forma base: eat."),
        "dialogue": ("A: Do you like fruit?  B: ___", ["Yes, I do.", "Yes, I like do.", "I am fruit.", "No, I does."], "Yes, I do."),
        "writing": ("Traduza: Eu como ovos no jantar.", ["i eat eggs for dinner", "i have eggs for dinner"], "I eat eggs for dinner."),
    },
    {
        "slug": "eating-out", "position": 4, "title_en": "Eating Out", "title_pt": "Comer fora",
        "source_title": "Eating Out - First Steps", "icon": "bi-cup-hot", "color": "amber",
        "goal_en": "Talk about what you order when you eat or drink out.", "goal_pt": "Falar sobre o que você pede ao comer ou beber fora.",
        "vocab": [("café", "cafeteria"), ("pub", "bar / pub"), ("bistro", "bistrô"), ("table", "mesa"), ("knife", "faca"), ("fish", "peixe"), ("meat", "carne"), ("sugar", "açúcar"), ("check", "conta"), ("split", "dividir")],
        "phrases": [("I want a table for two.", "Eu quero uma mesa para dois."), ("Can we have the check, please?", "Pode trazer a conta, por favor?"), ("Can we split the bill?", "Podemos dividir a conta?"), ("I order coffee at the café.", "Eu peço café na cafeteria."), ("Do you want sugar?", "Você quer açúcar?")],
        "questions": [("What do you order at a café?", "O que você pede em uma cafeteria?"), ("Do you prefer a bistro or a pub?", "Você prefere um bistrô ou um pub?"), ("Do you split the bill?", "Você divide a conta?")],
        "challenge": ("How do you ask for the bill politely?", ["Can we have the check, please?", "Give check now.", "I am the check.", "Where is pay?"], "Can we have the check, please?", "Can we have..., please? é uma forma educada de pedir."),
        "dialogue": ("Server: Are you ready to order?  You: ___", ["Yes, I'd like the fish, please.", "I ordering yesterday.", "Fish is table.", "No knife sugar."], "Yes, I'd like the fish, please."),
        "writing": ("Traduza: Nós dividimos a conta.", ["we split the bill", "we split the check"], "We split the bill."),
    },
    {
        "slug": "money", "position": 5, "title_en": "Money", "title_pt": "Dinheiro",
        "source_title": "Money - First Steps", "icon": "bi-wallet2", "color": "lime",
        "goal_en": "Talk about different types of money and how people use them.", "goal_pt": "Falar sobre tipos de dinheiro e como as pessoas os utilizam.",
        "vocab": [("bill", "cédula / conta"), ("coin", "moeda"), ("bank", "banco"), ("change", "troco"), ("save", "economizar"), ("price", "preço"), ("spend", "gastar"), ("pay", "pagar"), ("high", "alto"), ("take", "pegar / levar")],
        "phrases": [("I pay for lunch every day.", "Eu pago o almoço todos os dias."), ("I save money for a trip.", "Eu economizo dinheiro para uma viagem."), ("The price is too high.", "O preço está alto demais."), ("I get change after I pay.", "Eu recebo troco depois de pagar."), ("I have a coin in my pocket.", "Eu tenho uma moeda no bolso.")],
        "questions": [("How do you use money every day?", "Como você usa dinheiro todos os dias?"), ("Do you use coins or bills more?", "Você usa mais moedas ou cédulas?"), ("What do you save money for?", "Para que você economiza dinheiro?")],
        "challenge": ("Complete: I ___ money every month for a trip.", ["save", "spend all", "pays", "price"], "save", "Save money significa economizar dinheiro."),
        "dialogue": ("Cashier: Here is your change.  You: ___", ["Thank you.", "I am price.", "Bank yesterday.", "Coin expensive?"], "Thank you."),
        "writing": ("Traduza: Eu verifico o preço antes de comprar.", ["i check the price before i buy", "i check the price before buying"], "I check the price before I buy."),
    },
    {
        "slug": "using-technology", "position": 6, "title_en": "Using Technology", "title_pt": "Usando tecnologia",
        "source_title": "Using Technology - First Steps", "icon": "bi-laptop", "color": "cyan",
        "goal_en": "Describe how you use technology in your daily routine.", "goal_pt": "Descrever como você usa tecnologia em sua rotina diária.",
        "vocab": [("phone", "telefone"), ("computer", "computador"), ("internet", "internet"), ("camera", "câmera"), ("game", "jogo"), ("email", "e-mail"), ("cheap", "barato"), ("expensive", "caro"), ("slow", "lento"), ("fast", "rápido")],
        "phrases": [("I use my computer for work.", "Eu uso meu computador para trabalhar."), ("I send emails every morning.", "Eu envio e-mails toda manhã."), ("My new computer is fast.", "Meu computador novo é rápido."), ("I need the internet to study.", "Eu preciso da internet para estudar."), ("This laptop is expensive.", "Este notebook é caro.")],
        "questions": [("What do you use your phone for?", "Para que você usa seu telefone?"), ("What do you do on your computer?", "O que você faz no computador?"), ("Is your internet fast?", "Sua internet é rápida?")],
        "challenge": ("Complete: She ___ a computer for work.", ["uses", "use", "using", "used every"], "uses", "Com she no presente simples, use recebe s: uses."),
        "dialogue": ("A: Is your computer fast?  B: ___", ["Yes, it is.", "Yes, she are.", "Fast is computer?", "I do fast."], "Yes, it is."),
        "writing": ("Traduza: Eu uso a internet todos os dias.", ["i use the internet every day", "i use internet every day"], "I use the internet every day."),
    },
    {
        "slug": "studying-abroad", "position": 7, "title_en": "Studying Abroad", "title_pt": "Estudando no exterior",
        "source_title": "Studying Abroad - First Steps", "icon": "bi-airplane", "color": "pink",
        "goal_en": "Describe life in another country as an international student.", "goal_pt": "Descrever a vida em outro país como estudante internacional.",
        "vocab": [("country", "país"), ("language", "idioma"), ("student", "estudante"), ("program", "programa"), ("international", "internacional"), ("meet", "conhecer / encontrar"), ("easy", "fácil"), ("different", "diferente"), ("learn", "aprender"), ("every day", "todos os dias")],
        "phrases": [("I want to learn a new language.", "Eu quero aprender um novo idioma."), ("I am an international student.", "Eu sou estudante internacional."), ("I meet new people every day.", "Eu conheço pessoas novas todos os dias."), ("Life is different in a new country.", "A vida é diferente em um novo país."), ("The program has classes and activities.", "O programa tem aulas e atividades.")],
        "questions": [("Why study in another country?", "Por que estudar em outro país?"), ("What can an international student learn?", "O que um estudante internacional pode aprender?"), ("What is different abroad?", "O que é diferente no exterior?")],
        "challenge": ("Complete: I ___ new people every day.", ["meet", "meets", "meeting", "met tomorrow"], "meet", "Com I no presente simples, usamos meet."),
        "dialogue": ("A: Why do you want to study abroad?  B: ___", ["To learn a new language.", "I abroad yesterday future.", "Country is a student.", "Program meet."], "To learn a new language."),
        "writing": ("Traduza: Meu país é diferente daqui.", ["my country is different from here", "my country is different than here"], "My country is different from here."),
    },
    {
        "slug": "history", "position": 8, "title_en": "History", "title_pt": "História",
        "source_title": "History - First Steps", "icon": "bi-bank", "color": "amber",
        "goal_en": "Identify famous historical places and people.", "goal_pt": "Identificar lugares e pessoas históricas famosas.",
        "vocab": [("past", "passado"), ("queen", "rainha"), ("king", "rei"), ("bridge", "ponte"), ("built", "construiu / construído"), ("woman", "mulher"), ("leader", "líder"), ("first", "primeiro"), ("year", "ano"), ("was", "era / estava / foi")],
        "phrases": [("King Tut ruled Egypt in the past.", "O rei Tut governou o Egito no passado."), ("Workers built the Eiffel Tower in 1889.", "Trabalhadores construíram a Torre Eiffel em 1889."), ("Marie Curie won a Nobel Prize.", "Marie Curie ganhou um Prêmio Nobel."), ("Nelson Mandela was a leader.", "Nelson Mandela foi um líder."), ("People built the Colosseum long ago.", "As pessoas construíram o Coliseu há muito tempo.")],
        "questions": [("Who is an important woman from history?", "Quem é uma mulher importante da história?"), ("Can you name an important monument?", "Você sabe dizer um monumento importante?"), ("Which leader do you know?", "Qual líder você conhece?")],
        "challenge": ("Complete: People ___ the Colosseum long ago.", ["built", "builds", "building", "was build"], "built", "Built é o passado irregular de build."),
        "dialogue": ("A: Who was Neil Armstrong?  B: ___", ["He was the first man on the moon.", "He is a bridge.", "She was a queen.", "They built him."], "He was the first man on the moon."),
        "writing": ("Traduza: Cleópatra foi uma rainha do Egito.", ["cleopatra was a queen of egypt", "cleopatra was an egyptian queen"], "Cleopatra was a queen of Egypt."),
    },
    {
        "slug": "politics-and-citizenship", "position": 9, "title_en": "Politics and Citizenship", "title_pt": "Política e cidadania",
        "source_title": "Politics - First Steps", "icon": "bi-flag", "color": "violet",
        "goal_en": "Identify key figures and symbols in your country.", "goal_pt": "Identificar figuras e símbolos importantes do seu país.",
        "vocab": [("flag", "bandeira"), ("anthem", "hino"), ("national", "nacional"), ("nation", "nação"), ("capital city", "capital"), ("leader", "líder"), ("president", "presidente"), ("vote", "votar"), ("passport", "passaporte"), ("basic", "básico")],
        "phrases": [("Our flag has beautiful colors.", "Nossa bandeira tem cores bonitas."), ("The anthem is our national song.", "O hino é nossa canção nacional."), ("People vote in elections.", "As pessoas votam nas eleições."), ("A passport is an official document.", "Um passaporte é um documento oficial."), ("A good leader helps people.", "Um bom líder ajuda as pessoas.")],
        "questions": [("What do people do on national holidays?", "O que as pessoas fazem nos feriados nacionais?"), ("Who are important people in your country?", "Quem são pessoas importantes em seu país?"), ("What is a passport used for?", "Para que serve um passaporte?")],
        "challenge": ("Complete: People ___ in elections.", ["vote", "votes", "voting is", "voted tomorrow"], "vote", "People é plural; no presente simples usamos vote."),
        "dialogue": ("A: What does the flag represent?  B: ___", ["It represents our country.", "It vote a passport.", "The flag are leader.", "It is a capital person."], "It represents our country."),
        "writing": ("Traduza: Nossa nação tem muitas tradições.", ["our nation has many traditions", "our country has many traditions"], "Our nation has many traditions."),
    },
]


def _exercise_set(unit):
    vocab = unit["vocab"]
    translations = [item[1] for item in vocab[:5]]
    matching = {left: right for left, right in vocab[:5]}
    challenge_prompt, challenge_options, challenge_answer, challenge_explanation = unit["challenge"]
    dialogue_prompt, dialogue_options, dialogue_answer = unit["dialogue"]
    writing_prompt, accepted, writing_model = unit["writing"]
    return [
        {"kind": "choice", "prompt": f'Qual é a tradução de “{vocab[0][0]}”?', "instruction": "Escolha a tradução em português.", "payload": {"options": translations, "speak": vocab[0][0]}, "answer": vocab[0][1], "explanation": f'{vocab[0][0]} = {vocab[0][1]}.', "xp": 10},
        {"kind": "match", "prompt": "Combine o vocabulário da aula", "instruction": "Ligue cada expressão em inglês à tradução.", "payload": {"pairs": [{"left": a, "right": b} for a, b in vocab[:5]]}, "answer": matching, "explanation": "Esses pares vieram do vocabulário central da aula presencial.", "xp": 20},
        {"kind": "listen", "prompt": "O que a frase significa?", "instruction": "Ouça e selecione a tradução correta.", "payload": {"options": [p[1] for p in unit["phrases"]], "speak": unit["phrases"][0][0]}, "answer": unit["phrases"][0][1], "explanation": f'{unit["phrases"][0][0]} = {unit["phrases"][0][1]}', "xp": 15},
        {"kind": "choice", "prompt": challenge_prompt, "instruction": "Aplique o conteúdo da aula.", "payload": {"options": challenge_options}, "answer": challenge_answer, "explanation": challenge_explanation, "xp": 15},
        {"kind": "choice", "prompt": dialogue_prompt, "instruction": "Escolha a resposta mais natural para o diálogo.", "payload": {"options": dialogue_options, "speak": dialogue_prompt.replace("___", "")}, "answer": dialogue_answer, "explanation": f'Resposta natural: {dialogue_answer}', "xp": 15},
        {"kind": "write", "prompt": writing_prompt, "instruction": "Digite em inglês. Pontuação e maiúsculas são opcionais.", "payload": {"placeholder": "Write in English...", "accepted": accepted}, "answer": accepted, "explanation": f'Modelo: {writing_model}', "xp": 20},
    ]


def seed_classroom_content(db):
    for unit in CLASSROOM_UNITS:
        db.execute(
            """
            INSERT INTO classroom_units
                (slug, position, title_en, title_pt, source_title, icon, color,
                 learning_goal_en, learning_goal_pt, vocabulary, phrases, questions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                position=excluded.position, title_en=excluded.title_en, title_pt=excluded.title_pt,
                source_title=excluded.source_title, icon=excluded.icon, color=excluded.color,
                learning_goal_en=excluded.learning_goal_en, learning_goal_pt=excluded.learning_goal_pt,
                vocabulary=excluded.vocabulary, phrases=excluded.phrases, questions=excluded.questions
            """,
            (unit["slug"], unit["position"], unit["title_en"], unit["title_pt"], unit["source_title"],
             unit["icon"], unit["color"], unit["goal_en"], unit["goal_pt"],
             json.dumps(unit["vocab"], ensure_ascii=False), json.dumps(unit["phrases"], ensure_ascii=False),
             json.dumps(unit["questions"], ensure_ascii=False)),
        )
        unit_id = db.execute("SELECT id FROM classroom_units WHERE slug = ?", (unit["slug"],)).fetchone()["id"]
        for position, exercise in enumerate(_exercise_set(unit), 1):
            db.execute(
                """
                INSERT INTO classroom_exercises
                    (unit_id, position, kind, prompt, instruction, payload, answer, explanation, xp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(unit_id, position) DO UPDATE SET
                    kind=excluded.kind, prompt=excluded.prompt, instruction=excluded.instruction,
                    payload=excluded.payload, answer=excluded.answer,
                    explanation=excluded.explanation, xp=excluded.xp
                """,
                (unit_id, position, exercise["kind"], exercise["prompt"], exercise["instruction"],
                 json.dumps(exercise["payload"], ensure_ascii=False), json.dumps(exercise["answer"], ensure_ascii=False),
                 exercise["explanation"], exercise["xp"]),
            )
