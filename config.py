"""Configurações globais e variáveis de contexto do tema_mint_leve (config.py)."""

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
