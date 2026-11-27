"""Módulo de exceções semânticas de configuração e validação de caminhos (utils/exceptions.py)."""


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
