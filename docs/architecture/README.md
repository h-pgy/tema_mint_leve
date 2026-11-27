# Arquitetura do Sistema (`tema_mint_leve`)

Este documento detalha o funcionamento interno do bootstrap, do motor em Python (`core/`), da interface (`cli/`) e do contrato de execução dos scripts.

---

## 1. Fluxo de Execução Ponta a Ponta

```mermaid
%%{init: {'themeVariables': {'fontSize': '16px'}, 'flowchart': {'nodeSpacing': 30, 'rankSpacing': 35}}}%%
flowchart TD
    A["./install.sh"] -->|"1. Instala pyenv e uv / 2. uv sync"| B["cli/ (Python CLI)"]
    B -->|"3. Lê categorias"| C["core/registry.py (Pydantic Models)"]
    C -->|"4. Coleta inputs"| D["core/env_manager.py (Gera .env / configs)"]
    D -->|"5. Dispara selecionados"| E["core/runner.py"]
    E -->|"Injeta TARGET_HOME, MODULE_ASSETS_DIR, .env"| F["scripts/categoria/modulo/run.sh ou run.py"]
```

1. **Bootstrap (`install.sh`)**:
   - Garante dependências mínimas do sistema (`curl`, `git`, dependências de build se necessário).
   - Instala/valida o `pyenv` e o `uv`.
   - Cria/sincroniza o ambiente virtual do projeto com `uv sync`.
   - Repassa a execução para o CLI em Python (`uv run python -m cli`).
2. **Descoberta (`core/registry.py`)**:
   - Varre `scripts/*/` procurando categorias válidas e seus arquivos de `registry`.
   - Valida a estrutura e os caminhos no disco usando **Pydantic**.
3. **Interação (`cli/`)**:
   - Apresenta as categorias e seus módulos no terminal.
   - Renderiza o `README.md` de cada categoria/módulo para que o usuário saiba exatamente o que será feito.
   - Coleta variáveis dinâmicas declaradas nos módulos (`env_prompts`) antes de iniciar a instalação.
4. **Execução e Resolução do Grafo de Dependências (`core/runner.py`)**:
   - Constrói um **Grafo Direcionado Acíclico (DAG)** de dependências a partir do campo `depends_on` (formato `<category_id>.<module_id>` ou `<module_id>` na mesma categoria) e do campo `order`.
   - Permite tanto rodar um script isoladamente (resolvendo e executando automaticamente seus pré-requisitos declarados no grafo) quanto rodar múltiplos módulos/categorias respeitando a ordenação topológica e detectando ciclos.
   - Gera o `.env` necessário e executa cada módulo (`.sh` via Bash ou `.py` via Python) passando o contexto por variáveis de ambiente.

---

## 2. Organização de Diretórios

```text
tema_mint_leve/
├── AGENTS.md                  # Contexto rápido e índice (Progressive Disclosure)
├── README.md                  # Comandos de uso do CLI, uv e pytest
├── install.sh                 # Bootstrap inicial (pyenv + uv + chamada do CLI)
├── pyproject.toml             # Dependências gerenciadas pelo uv
├── config.py                  # AppSettings (pydantic-settings) com validação fail-fast e get_settings()
├── utils/                     # Utilitários compartilhados (exceptions.py, paths.py, fs.py)
├── docs/                      # Documentação organizada por domínio (architecture, modules, testing, sdd)
├── specs/                     # Épicos e especificações do Spec-Driven Development
├── cli/                       # Camada de interface (menus, flags, renderização de READMEs)
├── core/                      # Lógica central (exceptions.py, models Pydantic, loader, prova de instalação, DAG, runner)
├── scripts/                   # Módulos separados por domínio (rice, os_config, dev_env, etc.)
└── tests/                     # Suíte pytest e fixtures de sandbox
```

---

## 2.1. Configurações Globais (`config.py`), Utilitários (`utils/`) e Exceções Semânticas (`exceptions.py`)

### Regra Arquitetural: Módulos de Exceções Semânticas (`exceptions.py`)
Nenhum módulo do sistema pode definir classes de erro espalhadas ou levantar `ValueError`/`RuntimeError` genéricos para regras de negócio, validação de caminhos ou configuração.
- Todo pacote/domínio possui seu próprio módulo `exceptions.py` (ex: `utils/exceptions.py`, `core/exceptions.py`), permitindo importação limpa e tratamento tipado (`try/except`) entre módulos.
- Todas as exceções do projeto herdam de `MintLeveBaseError` (definida em `utils/exceptions.py`).

### Configurações Globais Fail-Fast (`config.py`)
O módulo `config.py` na raiz centraliza a leitura de variáveis de ambiente via `AppSettings(BaseSettings)` (`pydantic-settings`) e expõe `get_settings() -> AppSettings`. Ao ser instanciado, valida imediatamente (*fail-fast*) o estado do sistema de arquivos, lançando exceções semânticas de `utils/exceptions.py`:
- `PROJECT_ROOT`: Diretório raiz do projeto (`ProjectRootNotFoundError`).
- `SCRIPTS_DIR`: Diretório de categorias e módulos, default `PROJECT_ROOT / "scripts"` (`ScriptsDirectoryNotFoundError`).
- `TARGET_HOME`: Diretório home alvo, default `Path.home()` (`TargetHomeNotFoundError`).
- `DOTENV_PATH`: Arquivo `.env` alvo, default `PROJECT_ROOT / ".env"` (`InvalidDotenvPathError` se apontar para diretório ou se `DOTENV_PATH.parent` não existir).
- `MODULE_DIR` e `MODULE_ASSETS_DIR`: Diretórios opcionais do módulo em execução (`ModuleDirectoryNotFoundError`, `ModuleAssetsDirectoryNotFoundError`).
- `STATE_FILE_REL_PATH`: Caminho relativo seguro do manifesto de estado instalado, default `.config/tema_mint_leve/installed_state.json` (`PathValidationError` e subclasses).
- `DRY_RUN`: Booleano indicando simulação sem efeitos colaterais (`False` por padrão).

### Pacote `utils/`
Fornece funções puras e reutilizáveis pelo `core/` e pelos scripts Python (`run.py`):
- `utils/paths.py`: `validate_relative_path`, `is_safe_relative_path` (bloqueando caminhos vazios, absolutos `/`, expansão `~` ou path traversal `..` com `EmptyRelativePathError`, `AbsolutePathNotAllowedError` e `PathTraversalNotAllowedError`), além de `resolve_target_path`, `resolve_asset_path` (que lança `ModuleAssetsNotConfiguredError` se `MODULE_ASSETS_DIR` for `None`) e `resolve_state_file_path`.
- `utils/fs.py`: `file_exists` e `dir_exists`.

---

## 3. Modelagem com Pydantic (`core/models.py`)

O `core` utiliza modelos Pydantic para representar e validar categorias, módulos e o contexto de execução. As estruturas principais são:

- **`EnvPrompt`**: Define uma variável que o CLI deve perguntar ao usuário (ou assumir um valor default) para compor o `.env` (ex: `GIT_USER_EMAIL`, `PYTHON_DEFAULT_VERSION`).
- **`ScriptModule`**: Representa um módulo instalável dentro de uma categoria:
  - `id`: Identificador único dentro da categoria (ex: `xfce_light_theme`).
  - `name`: Nome amigável exibido no CLI.
  - `entrypoint`: Arquivo executável (`run.sh` ou `run.py`).
  - `runner`: Tipo de executor (`bash` ou `python`).
  - `requires_sudo`: Indica se o script precisa de privilégios administrativos.
  - `depends_on`: Lista opcional de módulos que devem rodar antes.
  - `env_prompts`: Lista opcional de variáveis solicitadas pelo módulo.
  - `expected_files`: Lista de caminhos (relativos ao `TARGET_HOME`) que o módulo deve criar/configurar — usada para validação pós-execução e testes no `pytest`.
  - *Validação de sistema de arquivos*: O validator do Pydantic garante que o `entrypoint` e o `README.md` do módulo existam na pasta do módulo.
- **`CategoryRegistry`**: Agrupa os metadados da categoria (`category_id`, `title`, `order`) e a lista de `ScriptModule`.
- **`ExecutionContext`**: Define o ambiente injetado em cada execução (`target_home`, `module_dir`, `assets_dir`, `dotenv_path`, `dry_run`).

---

## 4. Contrato de Variáveis de Ambiente do Runner

Para evitar caminhos fixos (*hardcoded*) e permitir que qualquer script funcione tanto na máquina real quanto dentro do `pytest`, o `core/runner.py` sempre injeta no processo filho:

| Variável | Descrição | Valor em Produção | Valor no Pytest (Sandbox) |
| :--- | :--- | :--- | :--- |
| `TARGET_HOME` | Diretório home alvo das configurações | `$HOME` (`/home/usuario`) | `tmp_path / "home"` |
| `MODULE_DIR` | Pasta raiz do módulo sendo executado | `.../scripts/<cat>/<mod>` | `.../scripts/<cat>/<mod>` |
| `MODULE_ASSETS_DIR` | Pasta `assets/` local daquele módulo | `.../scripts/<cat>/<mod>/assets` | `.../scripts/<cat>/<mod>/assets` |
| `DOTENV_PATH` | Caminho para o arquivo `.env` gerado | `.../.env` | `tmp_path / ".env"` |
| `DRY_RUN` | Flag indicando simulação sem efeitos colaterais | `0` (ou `1` via flag `--dry-run`) | Configurável pela fixture |
