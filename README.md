# HSEQ Report System

Sistema web desenvolvido em **Django** para gerenciamento de relatórios de incidentes, tipos de acidentes, tipos de lesões e ações corretivas/preventivas.

O sistema foi desenvolvido com foco em **HSEQ (Health, Safety, Environment and Quality)**, permitindo registrar, acompanhar e gerenciar ocorrências de segurança e suas respectivas ações.

---

## 📋 Sobre o Projeto

O **HSEQ Report System** centraliza o registro e acompanhamento de incidentes e ações relacionadas à segurança.

O sistema permite que usuários:

* Criem novos relatórios de incidentes;
* Consultem relatórios registrados;
* Visualizem detalhes de cada ocorrência;
* Atualizem relatórios;
* Acompanhem ações atribuídas;
* Identifiquem ações atrasadas;
* Gerenciem responsáveis;
* Classifiquem acidentes e lesões;
* Acompanhem o status dos registros;
* Gerenciem usuários, quando possuem privilégios administrativos.

---

## 🚀 Principais Funcionalidades

### 👤 Autenticação

O sistema possui autenticação baseada no sistema de usuários do Django.

Funcionalidades:

* Login;
* Logout;
* Controle de usuário autenticado;
* Proteção das páginas através de autenticação;
* Controle de acesso para administradores;
* Gerenciamento de usuários.

---

### 📊 Dashboard / Start

A página inicial apresenta informações relevantes para o usuário conectado.

São exibidos:

* Relatórios em que o usuário é o responsável;
* Relatórios criados pelo usuário;
* Ações atribuídas ao usuário;
* Status das ações;
* Prazos;
* Identificação de ações atrasadas;
* Acesso rápido para criação e consulta de relatórios.

---

## 🚨 Gerenciamento de Incidentes

O sistema possui um módulo para gerenciamento de incidentes através do modelo:

```text
Injury
```

Cada relatório pode conter informações como:

* Unidade;
* Data do relatório;
* Usuário que realizou o registro;
* Tipo do incidente;
* Status;
* Título;
* Descrição;
* Data do incidente;
* Responsável;
* Causas subjacentes;
* Local do incidente;
* Dias de trabalho perdidos;
* Parte do corpo lesionada;
* Empresa;
* Nome da pessoa envolvida;
* Condição da pessoa lesionada;
* Potencial de risco.

---

## 🏷️ Classificação dos Incidentes

O sistema permite associar diferentes classificações ao incidente.

### Type Accident

Representa os tipos de acidentes associados ao relatório.

Um incidente pode possuir **mais de um tipo de acidente**.

### Type Injury

Representa os tipos de lesões associados ao relatório.

Um incidente também pode possuir **mais de um tipo de lesão**.

---

## 📝 Ações

Cada incidente pode possuir ações relacionadas através do modelo:

```text
ActionInjury
```

As ações possuem informações como:

* Tarefa;
* Descrição;
* Responsável;
* Prazo;
* Data de conclusão;
* Status.

O sistema também identifica ações que estão atrasadas.

Exemplo de fluxo:

```text
Incident
   │
   ├── Type Accident
   │
   ├── Type Injury
   │
   └── Actions
          ├── Action 1
          ├── Action 2
          └── Action 3
```

---

## 🔐 Controle de Permissões

O sistema diferencia usuários comuns de administradores.

Usuários com privilégios administrativos possuem acesso a funcionalidades adicionais, como:

* Gerenciamento de usuários;
* Controle de contas;
* Administração do sistema.

Exemplo utilizado no template:

```django
{% if request.user.is_superuser %}
    ...
{% endif %}
```

Além disso, o sistema utiliza o usuário autenticado para determinar quem pode visualizar ou gerenciar determinadas informações.

---
Uma estrutura simplificada do projeto é:

```text
project/
│
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── incident/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── report_system/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── master.html
│   ├── start/
│   │   └── index.html
│   └── ...
│
├── static/
│   ├── css/
│   └── js/
│
└── db.sqlite3
```

A estrutura pode variar conforme a organização final do projeto.

---

# Tecnologias

O projeto utiliza principalmente:

* **Python**
* **Django**
* **HTML5**
* **Tailwind CSS**
* **JavaScript**
* **SQLite**
* **Git**
* **GitHub**

---

# Requisitos

Antes de executar o projeto, certifique-se de possuir:

* Python 3.x
* pip
* Git
* Ambiente virtual Python

Verifique a instalação:

```bash
python --version
```

```bash
pip --version
```

---

# Instalação

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entrar no diretório:

```bash
cd <NOME_DO_PROJETO>
```

---

## 2. Criar ambiente virtual

### Windows

```bash
python -m venv venv
```

Ativar:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Ativar:

```bash
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` ainda não exista:

```bash
pip freeze > requirements.txt
```

---

# Banco de Dados

Após instalar as dependências, execute as migrations:

```bash
python manage.py makemigrations
```

Depois:

```bash
python manage.py migrate
```

---

# Executar o Projeto

Inicie o servidor:

```bash
python manage.py runserver
```

O sistema ficará disponível, normalmente, em:

```text
http://127.0.0.1:8000/
```

# Fluxo do Sistema

O fluxo principal do sistema pode ser representado da seguinte forma:

```text
                    ┌───────────────┐
                    │     Login     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Start      │
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       New Report      View Reports    My Actions
             │              │              │
             ▼              ▼              ▼
          Injury          Injury        ActionInjury
             │
       ┌─────┴─────┐
       ▼           ▼
Type Accident  Type Injury
       │           │
       └─────┬─────┘
             │
             ▼
          Actions
             │
             ▼
       Responsible
             │
             ▼
      Action Completed
```

---

# Status

### Incident

Os incidentes possuem diferentes estados definidos no modelo.

Exemplo:

```text
Open
Closed
```

### Action

As ações podem possuir estados como:

```text
Active
Completed
```

Além do status, uma ação pode ser identificada como:

```text
Overdue
```

quando o prazo foi ultrapassado.

---

# Página Inicial

A página inicial apresenta três áreas principais:

### Quick Actions

Atalhos para:

* Criar relatório;
* Visualizar relatórios;
* Gerenciar usuários.

### My Reports

Exibe relatórios relacionados ao usuário:

```text
Responsible
```

e

```text
Reported By
```

### My Actions

Exibe ações cujo responsável é o usuário autenticado.

São apresentadas informações como:

```text
Report
Task
Due Date
Completed
Status
Action
```

---

# Interface

A interface utiliza uma abordagem moderna e responsiva.

Características:

* Layout responsivo;
* Cards;
* Tabelas;
* Badges de status;
* Estados vazios;
* Hover effects;
* Navegação entre registros;
* Identificação visual de ações atrasadas.

A interface utiliza uma paleta baseada em:

```text
Slate
Blue
Indigo
Emerald
Amber
Red
```

As cores são utilizadas principalmente para diferenciar estados e prioridades.

---

# Exemplo de Consulta

A view inicial utiliza o usuário autenticado para recuperar os registros relacionados:

```python
Injury.objects.filter(
    responsible=request.user
)
```

e:

```python
Injury.objects.filter(
    reported_by=request.user
)
```

As ações atribuídas ao usuário são recuperadas através de:

```python
ActionInjury.objects.filter(
    responsible=request.user
)
```

---

# Relacionamento entre os Modelos

A arquitetura pode ser representada conceitualmente como:

```text
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Injury       ActionInjury
 │               │
 │               │
 ├── reported_by │
 ├── responsible │
 │               └── responsible
 │
 ├── accident_types
 │
 └── injury_types
```

---

# Desenvolvimento

Durante o desenvolvimento, recomenda-se executar:

```bash
python manage.py check
```

para verificar problemas na configuração do Django.

Para verificar migrations:

```bash
python manage.py makemigrations --check
```

E para executar os testes:

```bash
python manage.py test
```

---

# Segurança

Em ambiente de produção, recomenda-se:

* Não utilizar `DEBUG=True`;
* Configurar corretamente `ALLOWED_HOSTS`;
* Utilizar variáveis de ambiente;
* Manter `SECRET_KEY` fora do código;
* Utilizar HTTPS;
* Configurar banco de dados de produção;
* Configurar arquivos estáticos;
* Configurar CSRF corretamente;
* Aplicar princípio do menor privilégio aos usuários.

---

# Produção

Para implantação em produção, a configuração deve incluir:

```text
Django
    │
    ├── Web Server
    │      └── Gunicorn / Uvicorn
    │
    ├── Reverse Proxy
    │      └── Nginx
    │
    ├── Database
    │      └── PostgreSQL
    │
    └── Static / Media
```

O ambiente de produção deve possuir configurações separadas do ambiente de desenvolvimento.

---

# Arquivos Importantes

| Arquivo            | Função                                 |
| ------------------ | -------------------------------------- |
| `manage.py`        | Gerenciamento do projeto Django        |
| `settings.py`      | Configurações do Django                |
| `urls.py`          | Rotas principais                       |
| `models.py`        | Modelos do banco                       |
| `forms.py`         | Formulários                            |
| `views.py`         | Regras de apresentação e processamento |
| `templates/`       | Interface HTML                         |
| `static/`          | CSS, JavaScript e arquivos estáticos   |
| `requirements.txt` | Dependências Python                    |

---

# Comandos Úteis

Criar aplicação:

```bash
python manage.py startapp nome_app
```

Criar migrations:

```bash
python manage.py makemigrations
```

Aplicar migrations:

```bash
python manage.py migrate
```

Criar superusuário:

```bash
python manage.py createsuperuser
```

Executar servidor:

```bash
python manage.py runserver
```

Abrir shell do Django:

```bash
python manage.py shell
```

Verificar projeto:

```bash
python manage.py check
```

Executar testes:

```bash
python manage.py test
```

---

# Roadmap

Possíveis evoluções do sistema:

* [ ] Dashboard com indicadores HSEQ;
* [ ] Filtros avançados de incidentes;
* [ ] Exportação para Excel/PDF;
* [ ] Sistema de notificações;
* [ ] E-mail automático para responsáveis;
* [ ] Alertas de ações próximas do vencimento;
* [ ] Histórico de alterações;
* [ ] Auditoria de registros;
* [ ] Upload de evidências;
* [ ] Controle de permissões por grupo;
* [ ] API REST;
* [ ] Dashboard gerencial;
* [ ] Integração com Power BI;
* [ ] PostgreSQL em produção.

---

# Licença

Este projeto possui finalidade de desenvolvimento e gerenciamento interno.

A definição da licença deve ser ajustada de acordo com as regras da organização responsável pelo projeto.

---

# Autor

**Calebe Moura**

Projeto desenvolvido para gerenciamento de informações relacionadas a **HSEQ, incidentes e ações de segurança**.

---

## Objetivo

O objetivo do sistema é fornecer uma plataforma centralizada para:

**Registrar → Classificar → Atribuir → Acompanhar → Concluir**

incidentes e respectivas ações, proporcionando maior controle sobre os processos de segurança e HSEQ.
