"""Pacote de utilitários compartilhados e exceções semânticas (utils/)."""

from utils.exceptions import (
    AbsolutePathNotAllowedError,
    ConfigurationError,
    EmptyRelativePathError,
    InvalidDotenvPathError,
    MintLeveBaseError,
    ModuleAssetsDirectoryNotFoundError,
    ModuleAssetsNotConfiguredError,
    ModuleDirectoryNotFoundError,
    PathTraversalNotAllowedError,
    PathValidationError,
    ProjectRootNotFoundError,
    ScriptsDirectoryNotFoundError,
    TargetHomeNotFoundError,
)
from utils.fs import dir_exists, file_exists
from utils.paths import (
    is_safe_relative_path,
    resolve_asset_path,
    resolve_state_file_path,
    resolve_target_path,
    validate_relative_path,
)

__all__ = [
    "MintLeveBaseError",
    "ConfigurationError",
    "ProjectRootNotFoundError",
    "ScriptsDirectoryNotFoundError",
    "TargetHomeNotFoundError",
    "InvalidDotenvPathError",
    "ModuleDirectoryNotFoundError",
    "ModuleAssetsDirectoryNotFoundError",
    "ModuleAssetsNotConfiguredError",
    "PathValidationError",
    "EmptyRelativePathError",
    "AbsolutePathNotAllowedError",
    "PathTraversalNotAllowedError",
    "file_exists",
    "dir_exists",
    "validate_relative_path",
    "is_safe_relative_path",
    "resolve_target_path",
    "resolve_asset_path",
    "resolve_state_file_path",
]
