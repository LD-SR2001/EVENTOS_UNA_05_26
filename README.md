# Sistema de Cadastro e Notificação de Eventos

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos — UNA 2026.

Sistema de console em Python que permite cadastrar, consultar e gerenciar eventos da cidade, com confirmação de presença por usuário.

---

## Como executar

```bash
python3 main.py
```

> Requisito: Python 3.9 ou superior. Nenhuma dependência externa necessária.

---

## Funcionalidades

- Cadastro e login de usuários por CPF
- Cadastro de eventos com categoria, endereço, data/hora e duração
- Listagem de eventos ordenados pelo mais próximo
- Identificação de eventos em andamento no momento
- Seção de eventos já encerrados
- Confirmação e cancelamento de presença
- Persistência automática em `events.data` (carregado ao abrir o programa)

---

## Fluxo de uso

```
Abertura do programa
│
├── Criar conta  →  informa nome, e-mail, CPF, telefone e cidade
└── Login        →  informa CPF cadastrado
    │
    └── Menu principal
        ├── 1. Próximos eventos       (ordenados por data, mais perto primeiro)
        ├── 2. Eventos em andamento   (ocorrendo agora)
        ├── 3. Eventos passados       (já encerrados)
        ├── 4. Cadastrar novo evento
        ├── 5. Meus eventos confirmados
        └── 6. Trocar de conta
```

Ao selecionar um evento em qualquer listagem, o sistema exibe seus detalhes completos e oferece a opção de **confirmar** ou **cancelar** a participação.

---

## Categorias de eventos disponíveis

| # | Categoria           |
|---|---------------------|
| 1 | Festa               |
| 2 | Show Musical        |
| 3 | Evento Esportivo    |
| 4 | Teatro              |
| 5 | Cinema              |
| 6 | Exposição           |
| 7 | Feira Cultural      |
| 8 | Gastronomia         |
| 9 | Evento Religioso    |
|10 | Evento Corporativo  |
|11 | Evento Educacional  |
|12 | Outro               |

---

## Atributos dos dados

**Usuário**

| Campo    | Descrição                    |
|----------|------------------------------|
| Nome     | Nome completo                |
| E-mail   | Endereço de e-mail           |
| CPF      | Usado como identificador único e para login |
| Telefone | Número de contato            |
| Cidade   | Cidade de residência         |

**Evento**

| Campo     | Descrição                                      |
|-----------|------------------------------------------------|
| Nome      | Nome do evento                                 |
| Endereço  | Local onde ocorre                              |
| Categoria | Uma das 12 categorias disponíveis              |
| Data/Hora | Data e hora de início (`DD/MM/AAAA HH:MM`)     |
| Duração   | Duração em horas (usado para calcular término) |
| Descrição | Texto livre descrevendo o evento               |

---

## Estrutura do projeto

```
EVENTOS/
├── main.py                        # Entrada da aplicação
├── models/
│   ├── category.py                # Enum com as categorias
│   ├── event.py                   # Modelo de Evento
│   └── user.py                    # Modelo de Usuário
├── controllers/
│   ├── event_controller.py        # Regras de negócio dos eventos
│   └── user_controller.py        # Autenticação e gestão de usuários
├── repositories/
│   ├── event_repository.py        # Leitura e escrita de events.data
│   └── user_repository.py        # Leitura e escrita de users.data
├── views/
│   └── console_view.py            # Interface de console (menus e formulários)
├── events.data                    # Gerado automaticamente na primeira execução
└── .gitignore
```

O projeto segue o padrão arquitetural **MVC**:

- **Model** — classes `Event`, `User` e `Category` em `models/`
- **View** — classe `ConsoleView` em `views/`, responsável por toda entrada e saída no terminal
- **Controller** — classes `EventController` e `UserController` em `controllers/`, contendo toda a lógica de negócio

Os **Repositories** formam uma camada adicional responsável exclusivamente pela persistência em arquivo, mantendo os controllers desacoplados do sistema de arquivos.

---

## Persistência de dados

Os eventos são salvos em `events.data` no formato JSON. O arquivo é carregado automaticamente ao iniciar o programa e atualizado a cada alteração (novo evento, confirmação ou cancelamento de presença).

Os dados dos usuários ficam em `users.data`, excluído do controle de versão por conter informações pessoais.

---

## Diagrama de classes

```
+------------------+          +-------------------+
|      User        |          |       Event       |
+------------------+          +-------------------+
| id: str          |          | id: str           |
| name: str        |          | name: str         |
| email: str       |          | address: str      |
| cpf: str         |          | category: Category|
| phone: str       |          | datetime: datetime|
| city: str        |          | description: str  |
| confirmed_events |          | duration_hours    |
+------------------+          | participants: list|
| to_dict()        |          +-------------------+
| from_dict()      |          | is_happening_now()|
+------------------+          | is_past()         |
                              | is_upcoming()     |
                              | to_dict()         |
                              | from_dict()       |
                              +-------------------+

+--------------------+
|     Category       |   (Enum)
+--------------------+
| FESTA              |
| SHOW               |
| ESPORTE            |
| TEATRO             |
| CINEMA             |
| EXPOSICAO          |
| FEIRA_CULTURAL     |
| GASTRONOMIA        |
| RELIGIOSO          |
| CORPORATIVO        |
| EDUCACIONAL        |
| OUTRO              |
+--------------------+

+--------------------------+       +-------------------------+
|   EventController        |       |   UserController        |
+--------------------------+       +-------------------------+
| get_upcoming_events()    |       | register()              |
| get_past_events()        |       | login()                 |
| get_happening_now()      |       | logout()                |
| get_event_by_id()        |       | find_by_cpf()           |
| add_event()              |       | save_current_user()     |
| confirm_participation()  |       +-------------------------+
| cancel_participation()   |
| get_user_events()        |
+--------------------------+

+-------------------------+       +-------------------------+
|   EventRepository       |       |   UserRepository        |
+-------------------------+       +-------------------------+
| load_all() -> [Event]   |       | load_all() -> [User]    |
| save_all([Event])       |       | save_all([User])        |
+-------------------------+       +-------------------------+
         |                                   |
    events.data                         users.data
```
