"""Validação e resolução segura de caminhos relativos do sistema (utils/paths.py)."""

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
