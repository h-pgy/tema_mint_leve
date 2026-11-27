"""Testes TDD (Spec 01 - 01_config_and_utils): config.py, utils/ e utils/exceptions.py."""

from pathlib import Path
import pytest


@pytest.mark.unit
def test_app_settings_defaults_and_env_overrides(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Valida defaults de get_settings() e sobrescritas dinâmicas via variáveis de ambiente."""
    from config import DEFAULT_PROJECT_ROOT, get_settings

    for var in (
        "PROJECT_ROOT",
        "TARGET_HOME",
        "SCRIPTS_DIR",
        "DOTENV_PATH",
        "MODULE_DIR",
        "MODULE_ASSETS_DIR",
        "STATE_FILE_REL_PATH",
        "DRY_RUN",
    ):
        monkeypatch.delenv(var, raising=False)

    default_settings = get_settings()
    assert default_settings.PROJECT_ROOT == DEFAULT_PROJECT_ROOT
    assert default_settings.TARGET_HOME == Path.home()
    assert default_settings.SCRIPTS_DIR == DEFAULT_PROJECT_ROOT / "scripts"
    assert default_settings.DOTENV_PATH == DEFAULT_PROJECT_ROOT / ".env"
    assert default_settings.MODULE_DIR is None
    assert default_settings.MODULE_ASSETS_DIR is None
    assert default_settings.STATE_FILE_REL_PATH == Path(
        ".config/tema_mint_leve/installed_state.json"
    )
    assert default_settings.DRY_RUN is False

    custom_home = tmp_path / "home"
    custom_scripts = tmp_path / "scripts"
    custom_mod = tmp_path / "mod"
    custom_assets = custom_mod / "assets"
    for directory in (custom_home, custom_scripts, custom_mod, custom_assets):
        directory.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("TARGET_HOME", str(custom_home))
    monkeypatch.setenv("SCRIPTS_DIR", str(custom_scripts))
    monkeypatch.setenv("MODULE_DIR", str(custom_mod))
    monkeypatch.setenv("MODULE_ASSETS_DIR", str(custom_assets))
    monkeypatch.setenv("DRY_RUN", "1")

    overridden = get_settings()
    assert overridden.TARGET_HOME == custom_home
    assert overridden.SCRIPTS_DIR == custom_scripts
    assert overridden.MODULE_DIR == custom_mod
    assert overridden.MODULE_ASSETS_DIR == custom_assets
    assert overridden.DRY_RUN is True


@pytest.mark.unit
def test_app_settings_fail_fast_semantic_exceptions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Verifica se AppSettings falha imediatamente com exceções semânticas para caminhos inválidos."""
    from config import get_settings
    from utils.exceptions import (
        InvalidDotenvPathError,
        MintLeveBaseError,
        ModuleAssetsDirectoryNotFoundError,
        ModuleDirectoryNotFoundError,
        PathTraversalNotAllowedError,
        ProjectRootNotFoundError,
        ScriptsDirectoryNotFoundError,
        TargetHomeNotFoundError,
    )

    valid_root = tmp_path / "project"
    valid_scripts = valid_root / "scripts"
    valid_home = tmp_path / "home"
    valid_scripts.mkdir(parents=True, exist_ok=True)
    valid_home.mkdir(parents=True, exist_ok=True)

    def reset_valid_env() -> None:
        monkeypatch.setenv("PROJECT_ROOT", str(valid_root))
        monkeypatch.setenv("SCRIPTS_DIR", str(valid_scripts))
        monkeypatch.setenv("TARGET_HOME", str(valid_home))
        monkeypatch.setenv("DOTENV_PATH", str(valid_root / ".env"))
        monkeypatch.delenv("MODULE_DIR", raising=False)
        monkeypatch.delenv("MODULE_ASSETS_DIR", raising=False)
        monkeypatch.delenv("STATE_FILE_REL_PATH", raising=False)

    for exc_cls in (
        ProjectRootNotFoundError,
        ScriptsDirectoryNotFoundError,
        TargetHomeNotFoundError,
        ModuleDirectoryNotFoundError,
        ModuleAssetsDirectoryNotFoundError,
        InvalidDotenvPathError,
        PathTraversalNotAllowedError,
    ):
        assert issubclass(exc_cls, MintLeveBaseError)

    # 1. PROJECT_ROOT inexistente
    reset_valid_env()
    monkeypatch.setenv("PROJECT_ROOT", str(tmp_path / "nonexistent_root"))
    with pytest.raises(ProjectRootNotFoundError):
        get_settings()

    # 2. SCRIPTS_DIR inexistente
    reset_valid_env()
    monkeypatch.setenv("SCRIPTS_DIR", str(tmp_path / "nonexistent_scripts"))
    with pytest.raises(ScriptsDirectoryNotFoundError):
        get_settings()

    # 3. TARGET_HOME inexistente
    reset_valid_env()
    monkeypatch.setenv("TARGET_HOME", str(tmp_path / "nonexistent_home"))
    with pytest.raises(TargetHomeNotFoundError):
        get_settings()

    # 4. MODULE_DIR inexistente
    reset_valid_env()
    monkeypatch.setenv("MODULE_DIR", str(tmp_path / "nonexistent_mod"))
    with pytest.raises(ModuleDirectoryNotFoundError):
        get_settings()

    # 5. MODULE_ASSETS_DIR inexistente
    reset_valid_env()
    monkeypatch.setenv("MODULE_ASSETS_DIR", str(tmp_path / "nonexistent_assets"))
    with pytest.raises(ModuleAssetsDirectoryNotFoundError):
        get_settings()

    # 6. DOTENV_PATH com diretório pai inexistente
    reset_valid_env()
    monkeypatch.setenv("DOTENV_PATH", str(tmp_path / "missing_parent" / ".env"))
    with pytest.raises(InvalidDotenvPathError):
        get_settings()

    # 7. STATE_FILE_REL_PATH com path traversal
    reset_valid_env()
    monkeypatch.setenv("STATE_FILE_REL_PATH", "../state.json")
    with pytest.raises(PathTraversalNotAllowedError):
        get_settings()


@pytest.mark.unit
def test_validate_and_check_safe_relative_paths() -> None:
    """Garante validação de caminhos relativos seguros e exceções semânticas específicas."""
    from utils.exceptions import (
        AbsolutePathNotAllowedError,
        EmptyRelativePathError,
        PathTraversalNotAllowedError,
    )
    from utils.paths import is_safe_relative_path, validate_relative_path

    valid_paths = [".config/gtk-3.0/gtk.css", ".bashrc", "subdir/file.txt"]
    for rel in valid_paths:
        assert is_safe_relative_path(rel) is True
        assert validate_relative_path(rel) == Path(rel)

    for empty_case in ("", "   ", "."):
        assert is_safe_relative_path(empty_case) is False
        with pytest.raises(EmptyRelativePathError):
            validate_relative_path(empty_case)

    for abs_case in ("/etc/hosts", "/etc/passwd", "~/.config", "~/.bashrc"):
        assert is_safe_relative_path(abs_case) is False
        with pytest.raises(AbsolutePathNotAllowedError):
            validate_relative_path(abs_case)

    for traversal_case in ("../secret", "../fora", "a/../../b"):
        assert is_safe_relative_path(traversal_case) is False
        with pytest.raises(PathTraversalNotAllowedError):
            validate_relative_path(traversal_case)


@pytest.mark.unit
def test_resolve_target_asset_and_state_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Verifica resolução de caminhos dentro de TARGET_HOME e MODULE_ASSETS_DIR."""
    from utils.exceptions import ModuleAssetsNotConfiguredError
    from utils.paths import (
        resolve_asset_path,
        resolve_state_file_path,
        resolve_target_path,
    )

    home_dir = tmp_path / "home"
    scripts_dir = tmp_path / "scripts"
    assets_dir = tmp_path / "assets"
    for directory in (home_dir, scripts_dir, assets_dir):
        directory.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("TARGET_HOME", str(home_dir))
    monkeypatch.setenv("SCRIPTS_DIR", str(scripts_dir))
    monkeypatch.delenv("MODULE_ASSETS_DIR", raising=False)
    monkeypatch.delenv("STATE_FILE_REL_PATH", raising=False)

    assert resolve_target_path(".gitconfig") == home_dir / ".gitconfig"
    assert (
        resolve_state_file_path()
        == home_dir / ".config/tema_mint_leve/installed_state.json"
    )

    with pytest.raises(ModuleAssetsNotConfiguredError):
        resolve_asset_path("xsettings.xml")

    monkeypatch.setenv("MODULE_ASSETS_DIR", str(assets_dir))
    assert resolve_asset_path("xsettings.xml") == assets_dir / "xsettings.xml"


@pytest.mark.unit
def test_file_and_dir_exists_helpers(tmp_path: Path) -> None:
    """Confirma que file_exists e dir_exists distinguem arquivos, diretórios e inexistentes."""
    from utils.fs import dir_exists, file_exists

    subdir = tmp_path / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)
    file_txt = subdir / "file.txt"
    file_txt.write_text("ok", encoding="utf-8")
    missing = tmp_path / "missing"

    assert dir_exists(subdir) is True
    assert dir_exists(file_txt) is False
    assert dir_exists(missing) is False

    assert file_exists(file_txt) is True
    assert file_exists(subdir) is False
    assert file_exists(missing) is False
