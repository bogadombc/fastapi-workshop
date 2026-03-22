Workshop FastAPI Moderno - Felipe Azambuja

13/03/26

ferramentas de ambiente:

### usará o pipx para instalar o poetry (ferramenta que gerencia versões do python, ambientes virtuais e bibliotecas)

$ sudo apt install pipx

$ pipx ensurepath

$ pipx install poetry

$ pipx inject poetry poetry-plugin-shell

se o poetry for instalado com o python 3.10.12

installed package poetry 2.3.2, installed using Python 3.10.12
  These apps are now globally available
    - poetry
done! ✨ 🌟 ✨

como instalo o poetry com o python 3.13 ?

$ pipx install poetry --python python3.13


## Vídeo 01 - 21/03/26

Início do curso do Workshop FastApi
extensão recomendada no vsc / antigravity
apenas a extensão python

$ poetry --version
$ poetry new --flat products_api

$ cd products_api

### caso queira instalar uma versão do python com o poetry:
$ poetry python install 3.13.1

### criando e ativando um ambiente virtual com poetry
$ poetry env use 3.13.1
obs: ao acessar a pasta do projeto, ele já usa o ambiente virtual criado

- saída do terminal
poetry env use 3.13.1
Creating virtualenv products-api-_Ft0C94f-py3.13 in /home/marcelobc/.cache/pypoetry/virtualenvs
Using virtualenv: /home/marcelobc/.cache/pypoetry/virtualenvs/products-api-_Ft0C94f-py3.13

$ poetry env info

escolher no vsc o ambiente virtual

- ajusta o pyproject.toml com o limite de versão: 4.0
requires-python = ">=3.13,<4.0"

$ poetry install  (cria o poetry.lock)

### instalando o FastApi
$ poetry add 'fastapi[standard]'

### executando o app
poetry run fastapi dev products_api/app.py (sobe a aplicação na porta 8000 por padrão)

### acessando a documentação
http://localhost:8000/docs  (abre o swagger, é como se fosse o manual de uso da api, conforme a api vai sendo construída, a documentação também é atualizada)
http://localhost:8000/redoc (abre o redoc, outra forma de documentação da api)

22/03/2026
- instalando o ruff e taskipy apenas em ambiente de desenvolvimento
$ poetry add ruff taskipy --group dev

1h 40'
coloca essa configuração no pyproject.toml

[tool.ruff]
line-length = 79
exclude = [
  ".bzr",
  ".direnv",
  ".eggs",
  ".git",
  ".gitignore",
  ".git-rewrite",
  ".hg",
  ".ipynb_checkpoints",
  ".mypy_cache",
  ".nox",
  ".pants.d",
  ".pyenv",
  ".pytest_cache",
  ".pytype",
  ".ruff_cache",
  ".svn",
  ".tox",
  ".venv",
  ".vscode",
  "__pypackages__",
  "__pycache__",
  "_build",
  "buck-out",
  "build",
  "dist",
  "node_modules",
  "site-packages",
  "venv",
  "alembic",
  "migrations",
]

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
ignore = ['PLR2004', 'PLR0917', 'PLR0913']

[tool.ruff.format]
preview = true
quote-style = 'single'

[tool.taskipy.tasks]
lint = 'ruff check'
pre_format = 'ruff check --fix'
format = 'ruff format'
run = 'fastapi dev products_api/app.py' (agora inicia o projeto com 'poetry run task run')