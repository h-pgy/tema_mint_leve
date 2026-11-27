---
epic: "01_core_engine"
spec: "01_config_and_utils"
type: "ideation"
requires_ui_mock: false
approved: true
implemented: true
---

# Ideação: Configurações Globais (`config.py`), Utilitários (`utils/`) e Evolução da Arquitetura / Agentes SDD

## Objetivo e Motivação
Estabelecer a base compartilhada do projeto (`config.py` e `utils/`) e atualizar a documentação de arquitetura e as skills/agentes do fluxo SDD antes de implementar os modelos de domínio e o motor de dependências.

Esta spec entrega:
1. **`config.py` (na raiz do repositório)**: Uma classe `AppSettings` baseada em `pydantic-settings` (`BaseSettings`) que centraliza, valida e retorna todas as variáveis de ambiente e diretórios base do projeto (`TARGET_HOME`, `PROJECT_ROOT`, `SCRIPTS_DIR`, `DOTENV_PATH`, `MODULE_DIR`, `MODULE_ASSETS_DIR`, `STATE_FILE_REL_PATH`, `DRY_RUN`).
2. **`utils/` (pacote de utilitários comuns)**: Funções reutilizáveis tanto pelo `core/` quanto por `N` scripts em Python (`run.py`), como checar se arquivo/diretório existe, resolver caminhos do sistema a partir das variáveis de ambiente do `config.py` e validar caminhos relativos seguros (impedindo paths absolutos `/` ou traversal `..`).
3. **Atualização da Documentação de Arquitetura (`docs/architecture/README.md` e `AGENTS.md`)**:
   - Incluir oficialmente o módulo `config.py` (na raiz) e o pacote `utils/` na arquitetura do sistema.
   - Documentar a visão geral dos contratos do `core/` (modelos tipados por `script_type`, verificação de instalação via ABC/Duck Typing + DTOs e grafo DAG).
4. **Atualização dos Agentes/Skills do SDD (`.agents/skills/sdd-ideation/SKILL.md`, `.agents/skills/sdd-workflow/SKILL.md` e `docs/sdd/README.md`)**:
   - **Leitura de Ideação Pré-existente**: O agente de ideação (`sdd-ideation`) deve **sempre verificar primeiro** se já existe uma versão inicial/placeholder de `referencias/IDEACAO.md` na pasta da spec e partir dela (refinando e detalhando o que já foi anotado, em vez de começar do zero).
   - **Subdivisão Proativa de Specs**: O agente de ideação passa a ter a responsabilidade explícita de avaliar se o escopo discutido está grande demais e **subdividir em múltiplas specs menores e autocontidas**, criando imediatamente os diretórios `specs/<epico>/<NN_spec>/referencias/IDEACAO.md` (com `approved: false`) como *placeholders* ricos para as próximas entregas.

---

## Escopo Detalhado desta Spec (`01_config_and_utils`)

- **Requer Mock Visual (`requires_ui_mock`)**: `false` (infraestrutura Python, utilitários e atualização de documentação/skills).
- **1. Módulo `config.py` (na raiz)**:
  - Classe `AppSettings(BaseSettings)` (usando `pydantic-settings`):
    - `PROJECT_ROOT: Path` (calculado automaticamente a partir da raiz onde `config.py` está).
    - `TARGET_HOME: Path` (lê da env `TARGET_HOME`; se não definida, assume `Path.home()`).
    - `SCRIPTS_DIR: Path` (lê da env `SCRIPTS_DIR`; default: `PROJECT_ROOT / "scripts"`).
    - `DOTENV_PATH: Path` (lê da env `DOTENV_PATH`; default: `PROJECT_ROOT / ".env"`).
    - `MODULE_DIR: Path | None = None` (lê da env `MODULE_DIR` quando dentro da execução de um módulo).
    - `MODULE_ASSETS_DIR: Path | None = None` (lê da env `MODULE_ASSETS_DIR` quando dentro da execução de um módulo).
    - `STATE_FILE_REL_PATH: Path = Path(".config/tema_mint_leve/installed_state.json")`.
    - `DRY_RUN: bool = False` (lê da env `DRY_RUN`, aceitando `0/1`, `true/false`).
  - Helper `get_settings() -> AppSettings` para instanciar/recarregar configurações dinamicamente (facilitando testes no `pytest` com `monkeypatch.setenv("TARGET_HOME", ...)`).
- **2. Pacote `utils/` (`utils/__init__.py`, `utils/fs.py` / `utils/paths.py`)**:
  - `is_safe_relative_path(path: str | Path) -> bool` e `validate_relative_path(path: str | Path) -> Path`: Garante que um caminho seja estritamente relativo (proibindo caminhos absolutos iniciados com `/` e escapes com `..`).
  - `resolve_target_path(rel_path: str | Path, settings: AppSettings | None = None) -> Path`: Gera o caminho completo dentro de `TARGET_HOME` a partir de um caminho relativo validado.
  - `resolve_asset_path(rel_path: str | Path, settings: AppSettings | None = None) -> Path`: Gera o caminho completo dentro de `MODULE_ASSETS_DIR` (ou lança erro claro se `MODULE_ASSETS_DIR` não estiver configurado).
  - `resolve_state_file_path(settings: AppSettings | None = None) -> Path`: Retorna o caminho completo do manifesto de instalação (`TARGET_HOME / STATE_FILE_REL_PATH`).
  - `file_exists(path: str | Path) -> bool` e `dir_exists(path: str | Path) -> bool`: Checagem padronizada de existência de arquivo ou diretório no sistema de arquivos.
- **3. Atualização de `docs/architecture/README.md`, `AGENTS.md`, `docs/sdd/README.md` e `.agents/skills/`**:
  - Refletir `config.py` e `utils/` na árvore de diretórios e fluxo de execução.
  - Atualizar `.agents/skills/sdd-ideation/SKILL.md` e `.agents/skills/sdd-workflow/SKILL.md` com a regra de **Subdivisão de Specs em Placeholders** e **Continuação a partir de `IDEACAO.md` inicial já existente**.

---

## Subdivisão do Épico `01_core_engine` (Ideações Separadas Criadas)

As demais entregas levantadas nesta sessão já foram desmembradas em suas próprias pastas de spec com seus respectivos arquivos iniciais de ideação (`approved: false`):
- `specs/01_core_engine/01_config_and_utils/referencias/IDEACAO.md` *(Esta Spec)*
- `specs/01_core_engine/02_script_models/referencias/IDEACAO.md` *(Modelos Pydantic dos scripts/categorias, `ScriptType`, `tags`/temas, validações estruturais e loader)*
- `specs/01_core_engine/03_installation_proof/referencias/IDEACAO.md` *(Arquitetura ABC/Duck Typing de Prova de Instalação + DTOs de entrada/saída)*
- `specs/01_core_engine/04_dependency_dag/referencias/IDEACAO.md` *(Placeholder do Grafo de Dependências DAG, filtro por temas e retorno do `ExecutionPlanDTO` avisando sobre scripts X, Y, Z)*
