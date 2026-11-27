---
epic: "01_core_engine"
spec: "01_config_and_utils"
type: "spec"
category: "core"
module_id: "config_and_utils"
requires_ui_mock: false
approved: true
implemented: true
---

# Spec: Configurações Globais (`config.py`), Utilitários (`utils/`), Exceções Semânticas e Evolução da Arquitetura / Agentes SDD

## 1. Objetivo e Escopo
- **O quê**:
  1. Implementar o módulo `config.py` na raiz com `AppSettings(BaseSettings)` (`pydantic-settings`) dotado de **validadores fail-fast** (garantindo que `PROJECT_ROOT`, `SCRIPTS_DIR`, `TARGET_HOME`, `DOTENV_PATH.parent`, `MODULE_DIR`, `MODULE_ASSETS_DIR` e `STATE_FILE_REL_PATH` existam/sejam válidos ao iniciar).
  2. Estabelecer a regra arquitetural de **Módulos de Exceções Semânticas (`exceptions.py`)**: todo pacote/domínio do sistema possui seu próprio módulo `exceptions.py` (ex: `utils/exceptions.py`, `core/exceptions.py`), sendo proibido criar ou lançar exceções genéricas fora do módulo de exceções, para permitir importação e tratamento (`try/except`) tipado entre módulos.
  3. Implementar o pacote `utils/` (`utils/__init__.py`, `utils/exceptions.py`, `utils/paths.py`, `utils/fs.py`) com validação segura de caminhos relativos e resolução de diretórios do sistema lançando exceções semânticas.
  4. Atualizar a documentação de arquitetura (`AGENTS.md`, `docs/architecture/README.md`) — incluindo a regra de `exceptions.py` por módulo — e as skills do SDD (`docs/sdd/README.md`, `.agents/skills/sdd-ideation/SKILL.md`, `.agents/skills/sdd-workflow/SKILL.md`).
- **Para quê**: Impedir que o projeto inicie com variáveis de ambiente ou diretórios base (`SCRIPTS_DIR`, `TARGET_HOME`, etc.) inexistentes ou mal configurados, fornecer erros semânticos claros e capturáveis por outros módulos, prevenir path traversal (`..` ou `/`) e formalizar no fluxo SDD a leitura de `IDEACAO.md` pré-existentes e a subdivisão proativa de escopos grandes em múltiplas specs placeholders.
- **Resultado**: Fundação compartilhada (`config.py` + `utils/` + `utils/exceptions.py`) validada e testada, com documentação de arquitetura e skills SDD atualizadas.

## 2. Grafo de Dependências e Ordem de Execução (Apenas para módulos de `scripts/`, senão `N/A`)
- `N/A` *(Entrega fundacional de código Python na raiz — `config.py` e `utils/` — não é um módulo executável de `scripts/`).*

## 3. Especificação do Registry (`YAML`) (Apenas para módulos de `scripts/`, senão `N/A`)
- `N/A` *(Não aplicável: `config.py` e `utils/` são pacotes internos da aplicação e não entram em `scripts/<categoria>/registry.yaml`).*

## 4. Modelo Pydantic (`config.py` / `AppSettings`) e Hierarquia de Exceções (`utils/exceptions.py`)

### 4.1. Módulo de Exceções (`utils/exceptions.py`)
> **Regra Arquitetural**: Nenhum módulo pode definir classes de erro espalhadas ou levantar `ValueError`/`RuntimeError` genéricos para regras de negócio/configuração. Toda exceção deve residir no módulo `exceptions.py` do respectivo pacote para ser livremente importada por consumidores.

```python
# utils/exceptions.py
class MintLeveBaseError(Exception):
    """Exceção base semântica de todo o projeto tema_mint_leve."""


# --- Exceções Semânticas de Configuração (config.py) ---
class ConfigurationError(MintLeveBaseError):
    """Erro base para configurações ou variáveis de ambiente inválidas no AppSettings."""


class ProjectRootNotFoundError(ConfigurationError):
    """Diretório PROJECT_ROOT não existe ou não é um diretório válido."""


class ScriptsDirectoryNotFoundError(ConfigurationError):
    """Diretório SCRIPTS_DIR não existe ou não é um diretório válido."""


class TargetHomeNotFoundError(ConfigurationError):
    """Diretório TARGET_HOME não existe ou não é um diretório válido."""


class InvalidDotenvPathError(ConfigurationError):
    """DOTENV_PATH aponta para um diretório ou seu diretório pai não existe."""


class ModuleDirectoryNotFoundError(ConfigurationError):
    """Diretório MODULE_DIR informado não existe ou não é um diretório válido."""


class ModuleAssetsDirectoryNotFoundError(ConfigurationError):
    """Diretório MODULE_ASSETS_DIR informado não existe ou não é um diretório válido."""


class ModuleAssetsNotConfiguredError(ConfigurationError):
    """Tentativa de resolver um asset quando MODULE_ASSETS_DIR não está definido."""


# --- Exceções Semânticas de Caminhos e Filesystem (utils/paths.py) ---
class PathValidationError(MintLeveBaseError):
    """Erro base para validação de caminhos relativos seguros."""


class EmptyRelativePathError(PathValidationError):
    """O caminho relativo fornecido é vazio ou contém apenas espaços."""


class AbsolutePathNotAllowedError(PathValidationError):
    """O caminho fornecido é absoluto ('/') ou usa expansão de home ('~')."""


class PathTraversalNotAllowedError(PathValidationError):
    """O caminho fornecido tenta escapar do diretório base usando '..'."""
```

### 4.2. Modelo `AppSettings` com Validadores Fail-Fast (`config.py`)
```python
from pathlib import Path
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.exceptions import (
    InvalidDotenvPathError,
    ModuleAssetsDirectoryNotFoundError,
    ModuleDirectoryNotFoundError,
    ProjectRootNotFoundError,
    ScriptsDirectoryNotFoundError,
    TargetHomeNotFoundError,
)
from utils.fs import dir_exists
from utils.paths import validate_relative_path

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parent


class AppSettings(BaseSettings):
    """Configurações globais e variáveis de contexto do tema_mint_leve com validação fail-fast."""

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        populate_by_name=True,
    )

    PROJECT_ROOT: Path = Field(default=DEFAULT_PROJECT_ROOT)
    TARGET_HOME: Path = Field(default_factory=Path.home)
    SCRIPTS_DIR: Path | None = Field(default=None)
    DOTENV_PATH: Path | None = Field(default=None)
    MODULE_DIR: Path | None = Field(default=None)
    MODULE_ASSETS_DIR: Path | None = Field(default=None)
    STATE_FILE_REL_PATH: Path = Field(
        default=Path(".config/tema_mint_leve/installed_state.json")
    )
    DRY_RUN: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_and_resolve_settings(self) -> "AppSettings":
        if not dir_exists(self.PROJECT_ROOT):
            raise ProjectRootNotFoundError(
                f"PROJECT_ROOT não existe ou não é um diretório: '{self.PROJECT_ROOT}'"
            )

        if self.SCRIPTS_DIR is None:
            self.SCRIPTS_DIR = self.PROJECT_ROOT / "scripts"
        if not dir_exists(self.SCRIPTS_DIR):
            raise ScriptsDirectoryNotFoundError(
                f"SCRIPTS_DIR não existe ou não é um diretório: '{self.SCRIPTS_DIR}'"
            )

        if not dir_exists(self.TARGET_HOME):
            raise TargetHomeNotFoundError(
                f"TARGET_HOME não existe ou não é um diretório: '{self.TARGET_HOME}'"
            )

        if self.DOTENV_PATH is None:
            self.DOTENV_PATH = self.PROJECT_ROOT / ".env"
        if dir_exists(self.DOTENV_PATH) or not dir_exists(self.DOTENV_PATH.parent):
            raise InvalidDotenvPathError(
                f"DOTENV_PATH inválido (diretório pai inexistente ou caminho é uma pasta): '{self.DOTENV_PATH}'"
            )

        if self.MODULE_DIR is not None and not dir_exists(self.MODULE_DIR):
            raise ModuleDirectoryNotFoundError(
                f"MODULE_DIR não existe ou não é um diretório: '{self.MODULE_DIR}'"
            )

        if self.MODULE_ASSETS_DIR is not None and not dir_exists(self.MODULE_ASSETS_DIR):
            raise ModuleAssetsDirectoryNotFoundError(
                f"MODULE_ASSETS_DIR não existe ou não é um diretório: '{self.MODULE_ASSETS_DIR}'"
            )

        self.STATE_FILE_REL_PATH = validate_relative_path(self.STATE_FILE_REL_PATH)
        return self


def get_settings() -> AppSettings:
    """Instancia e valida AppSettings lendo o estado atual das variáveis de ambiente."""
    return AppSettings()
```

- **Validações Semânticas Garantidas no Startup (`AppSettings`)**:
  - `PROJECT_ROOT`: Deve existir fisicamente como diretório (`ProjectRootNotFoundError`).
  - `SCRIPTS_DIR`: Se não informado, assume `PROJECT_ROOT / "scripts"`; deve existir fisicamente como diretório (`ScriptsDirectoryNotFoundError`).
  - `TARGET_HOME`: Deve existir fisicamente como diretório (`TargetHomeNotFoundError`).
  - `DOTENV_PATH`: Se não informado, assume `PROJECT_ROOT / ".env"`; seu diretório pai (`DOTENV_PATH.parent`) deve existir e o caminho em si não pode ser um diretório (`InvalidDotenvPathError`).
  - `MODULE_DIR`: Quando definido, deve existir fisicamente como diretório (`ModuleDirectoryNotFoundError`).
  - `MODULE_ASSETS_DIR`: Quando definido, deve existir fisicamente como diretório (`ModuleAssetsDirectoryNotFoundError`).
  - `STATE_FILE_REL_PATH`: Deve ser um caminho estritamente relativo válido (`PathValidationError` e subclasses).

## 5. Contrato de Execução, Idempotência e Assets
- **Entrypoint & Runner**: Módulos Python importáveis (`config.py`, `utils/__init__.py`, `utils/exceptions.py`, `utils/paths.py`, `utils/fs.py`).
- **Variáveis de Contexto consumidas**: `PROJECT_ROOT`, `TARGET_HOME`, `SCRIPTS_DIR`, `DOTENV_PATH`, `MODULE_DIR`, `MODULE_ASSETS_DIR`, `STATE_FILE_REL_PATH`, `DRY_RUN`.
- **Assets locais (`assets/`)**: `N/A` (não aplicável).
- **Arquivos gerados/modificados**:
  - Código: `config.py`, `utils/__init__.py`, `utils/exceptions.py`, `utils/paths.py`, `utils/fs.py` (e garantia de existência do diretório `scripts/` na raiz do projeto).
  - Documentação e Skills SDD: `AGENTS.md`, `docs/architecture/README.md`, `docs/sdd/README.md`, `.agents/skills/sdd-ideation/SKILL.md`, `.agents/skills/sdd-workflow/SKILL.md`.
- **Regras de Idempotência**:
  - Todas as funções de `utils/` e `get_settings()` são determinísticas em relação às variáveis de ambiente e ao estado do filesystem, sem efeitos colaterais em disco.
- **Portabilidade de UI do Mock & Atomic Design para o OS (Obrigatório se `requires_ui_mock: true`, senão `N/A`)**:
  - `N/A` (`requires_ui_mock: false`).

## 6. Snippets Principais de Implementação

```python
# utils/paths.py — Validação e resolução segura de caminhos com exceções semânticas
from pathlib import Path
from typing import TYPE_CHECKING

from utils.exceptions import (
    AbsolutePathNotAllowedError,
    EmptyRelativePathError,
    ModuleAssetsNotConfiguredError,
    PathTraversalNotAllowedError,
    PathValidationError,
)

if TYPE_CHECKING:
    from config import AppSettings


def validate_relative_path(path: str | Path) -> Path:
    """Garante que o caminho é relativo, não vazio e sem traversal ('..')."""
    raw = str(path).strip()
    if not raw or raw == ".":
        raise EmptyRelativePathError("O caminho relativo não pode ser vazio.")
    candidate = Path(raw)
    if candidate.is_absolute() or raw.startswith("/") or raw.startswith("~"):
        raise AbsolutePathNotAllowedError(
            f"Caminho absoluto ou '~' não permitido: '{path}'"
        )
    if ".." in candidate.parts:
        raise PathTraversalNotAllowedError(
            f"Path traversal ('..') não permitido: '{path}'"
        )
    return candidate


def is_safe_relative_path(path: str | Path) -> bool:
    """Retorna True se o caminho for estritamente relativo e seguro."""
    try:
        validate_relative_path(path)
        return True
    except PathValidationError:
        return False


def resolve_target_path(
    rel_path: str | Path, settings: "AppSettings | None" = None
) -> Path:
    """Resolve um caminho relativo validado dentro de TARGET_HOME."""
    if settings is None:
        from config import get_settings
        settings = get_settings()
    safe_rel = validate_relative_path(rel_path)
    return settings.TARGET_HOME / safe_rel


def resolve_asset_path(
    rel_path: str | Path, settings: "AppSettings | None" = None
) -> Path:
    """Resolve um caminho relativo validado dentro de MODULE_ASSETS_DIR."""
    if settings is None:
        from config import get_settings
        settings = get_settings()
    if settings.MODULE_ASSETS_DIR is None:
        raise ModuleAssetsNotConfiguredError(
            "MODULE_ASSETS_DIR não está definido nas configurações atuais."
        )
    safe_rel = validate_relative_path(rel_path)
    return settings.MODULE_ASSETS_DIR / safe_rel


def resolve_state_file_path(settings: "AppSettings | None" = None) -> Path:
    """Retorna o caminho completo do arquivo installed_state.json em TARGET_HOME."""
    if settings is None:
        from config import get_settings
        settings = get_settings()
    return resolve_target_path(settings.STATE_FILE_REL_PATH, settings=settings)
```

## 7. Critérios de Aceite
- [x] `utils/exceptions.py` centraliza todas as exceções semânticas de configuração (`ConfigurationError` e subclasses: `ProjectRootNotFoundError`, `ScriptsDirectoryNotFoundError`, `TargetHomeNotFoundError`, `InvalidDotenvPathError`, `ModuleDirectoryNotFoundError`, `ModuleAssetsDirectoryNotFoundError`, `ModuleAssetsNotConfiguredError`) e de validação de caminhos (`PathValidationError` e subclasses: `EmptyRelativePathError`, `AbsolutePathNotAllowedError`, `PathTraversalNotAllowedError`), sem nenhuma classe de erro criada fora de módulos de exceções.
- [x] `config.py` existe na raiz do projeto exportando `AppSettings` e `get_settings()`, validando fail-fast a existência de `PROJECT_ROOT`, `SCRIPTS_DIR`, `TARGET_HOME`, `DOTENV_PATH.parent`, `MODULE_DIR` (se definido), `MODULE_ASSETS_DIR` (se definido) e a segurança de `STATE_FILE_REL_PATH`, lançando as respectivas exceções semânticas de `utils/exceptions.py`.
- [x] `utils/` exporta em `utils/__init__.py` as funções (`is_safe_relative_path`, `validate_relative_path`, `resolve_target_path`, `resolve_asset_path`, `resolve_state_file_path`, `file_exists`, `dir_exists`) e as exceções de `utils/exceptions.py`.
- [x] `AGENTS.md` e `docs/architecture/README.md` estão atualizados refletindo `config.py`, `utils/` e a regra arquitetural obrigatória de **Módulos de Exceções Semânticas (`exceptions.py`) por pacote/domínio**.
- [x] `.agents/skills/sdd-ideation/SKILL.md`, `.agents/skills/sdd-workflow/SKILL.md` e `docs/sdd/README.md` estão atualizados com as regras de: (1) verificar e continuar a partir de `referencias/IDEACAO.md` pré-existente e (2) subdividir escopos grandes em múltiplas specs com placeholders `IDEACAO.md` (`approved: false`).
