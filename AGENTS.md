# AGENTS.md

## Sobre o Projeto
O **tema_mint_leve** é um repositório de automação pós-formatação e *rice* para Linux Mint (XFCE), focado em laptops antigos com prioridade em performance e duração de bateria.
Ele permite clonar o repositório em uma máquina recém-formatada e, com um único comando, instalar e configurar desde ferramentas base (`pyenv`, `uv`, `git`, `docker`, VS Code) até ajustes de sistema e preferências visuais/janelas do Mint.
Toda a automação é modular, guiada por um CLI em Python e validada por testes automatizados com `pytest`.

## Visão Geral da Arquitetura
- **Bootstrap & CLI (`install.sh` + `cli/`)**: O `install.sh` prepara a base mínima (`pyenv` e `uv`), sincroniza o ambiente Python e inicia o CLI. O `cli/` cuida apenas da interface (menus interativos por categoria, exibição dos `README.md` de cada módulo e coleta de inputs).
- **Motor Principal (`core/`)**: Contém os modelos Pydantic, o carregador de registries, o gerador de arquivos `.env`/templates e o `runner` que executa scripts `.sh` ou `.py` injetando variáveis de contexto.
- **Módulos por Domínio & Registry (`scripts/`)**: Os scripts são organizados por categorias de domínio (ex: `os_config`, `app_installers`, `dev_env`, `rice`). Cada categoria possui um `README.md` e um arquivo de `registry`. Cada módulo dentro da categoria vive em sua própria pasta autocontida com seu script (`run.sh` ou `run.py`), seu `README.md` (exibido no CLI) e sua própria pasta `assets/` local (sem `assets` global bagunçado).
- **Grafo de Dependências (`core/`)**: Os módulos podem ser executados isoladamente ou em cadeia através de um grafo de dependências (DAG) resolvido por ordenação topológica no `core/`, baseado no campo `depends_on` (ex: `app_installers.pyenv`) e na ordem de execução (`order`).
- **Testabilidade (`tests/`)**: Os módulos respeitam variáveis de contexto (como `TARGET_HOME` e `MODULE_ASSETS_DIR`), permitindo que o `pytest` use fixtures para testar a execução, a criação de arquivos `.env`/configs em sandbox e a validação pós-instalação.
- **Atomic Design System (`design_system/`)**: Catálogo vivo e navegável via Live Server (`index.html`, `tokens.html`, `atoms.html`, `molecules.html`, `organisms.html`) alimentado pelo CSS central `design_system/css/design-system.css`. Centraliza paleta de cores e tipografia (Tokens) e documenta Átomos, Moléculas e Organismos sob guardrails estritos de compatibilidade com GTK3 (`GtkCssProvider`) e XFCE (`xfwm4`).
- **Spec-Driven Development (`specs/` & `.agents/skills/`)**: Todo o desenvolvimento segue um fluxo SDD estruturado em Épicos (`specs/<epico>/<spec>/`) e dividido em etapas com limpeza de contexto entre elas: **Ideação** (`sdd-ideation`), **Mock Visual Condicional** (`sdd-ui-mock`, obrigatório sempre que `requires_ui_mock: true` para entregas de UI/temas/rice, consultando previamente o `design_system/` para reutilizar tokens/componentes e promovendo os novos átomos/moléculas/organismos aprovados para o showcase), **Planning/Spec** (`sdd-planning`), **Testes TDD** (`sdd-tdd`) e **Implementação** (`sdd-implementation`), orquestradas pela skill master (`sdd-workflow`). Cada etapa controla seu estado via YAML frontmatter (`approved: bool`, `implemented: bool`) com verificação dupla na realidade do repositório.

## Comandos
Use `uv` para executar a suíte de testes (`pytest`), filtrando por *markers* (`-m`) conforme o escopo desejado:

```bash
# Rodar a suíte padrão (unit + integration; exclui post_install por padrão)
uv run pytest

# Rodar apenas testes unitários (core, modelos Pydantic, registries e CLI)
uv run pytest -m unit

# Rodar apenas testes de integração em sandbox (execução de módulos com TARGET_HOME)
uv run pytest -m integration

# Rodar verificação pós-instalação na máquina real
uv run pytest -m post_install

# Pular testes lentos durante o desenvolvimento
uv run pytest -m "not slow"
```

## Progressive Disclosure (Documentação Detalhada)
Para não sobrecarregar o contexto, consulte os documentos específicos abaixo **apenas quando precisar trabalhar na respectiva área**:

- **[docs/sdd/README.md](docs/sdd/README.md)**: Leia **sempre** que for iniciar ou continuar o desenvolvimento de uma funcionalidade/módulo usando o fluxo de Spec-Driven Development (`specs/`, frontmatters `approved`/`implemented`, skills e templates em `docs/sdd/templates/`).
- **[design_system/README.md](design_system/README.md)**: Leia **sempre** que a spec envolver mudanças visuais/UI (`requires_ui_mock: true`) para consultar os Tokens, Átomos, Moléculas e Organismos existentes em `design_system/css/design-system.css` antes de criar mocks e para atualizar o showcase HTML (`tokens.html`, `atoms.html`, `molecules.html`, `organisms.html`).
- **[docs/architecture/README.md](docs/architecture/README.md)**: Leia ao implementar ou alterar o `install.sh`, o `core/` (modelos Pydantic, grafo de dependências, runner, geração de `.env`) ou o `cli/`.
- **[docs/modules/README.md](docs/modules/README.md)**: Leia ao criar, editar ou registrar novos módulos e categorias dentro de `scripts/`, seus `README.md` e seus `assets/` locais.
- **[docs/testing/README.md](docs/testing/README.md)**: Leia ao escrever ou rodar testes no `pytest`, criar fixtures de sandbox ou validar artefatos gerados pelos scripts.
- **[README.md](README.md)**: Consulte para referência rápida de comandos de execução do CLI, `uv` e `pytest`.
