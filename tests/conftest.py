"""Fixtures compartilhadas de sandbox para a suíte de testes do tema_mint_leve."""

from pathlib import Path
import pytest


@pytest.fixture
def fake_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Cria uma estrutura limpa de diretório home e a injeta como TARGET_HOME."""
    home_dir = tmp_path / "home"
    (home_dir / ".config").mkdir(parents=True, exist_ok=True)
    (home_dir / ".local" / "bin").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("TARGET_HOME", str(home_dir))
    return home_dir


@pytest.fixture
def mock_system_bins(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Cria stubs para binários de sistema no início do PATH registrando chamadas em commands.log."""
    mock_bin_dir = tmp_path / "mock_bin"
    mock_bin_dir.mkdir(parents=True, exist_ok=True)
    commands_log = tmp_path / "commands.log"
    commands_log.touch()

    stub_commands = [
        "sudo",
        "apt-get",
        "apt",
        "systemctl",
        "xfconf-query",
        "xfce4-panel",
        "gsettings",
    ]
    for cmd in stub_commands:
        script_path = mock_bin_dir / cmd
        script_path.write_text(
            f'#!/usr/bin/env bash\necho "{cmd} $*" >> "{commands_log}"\nexit 0\n',
            encoding="utf-8",
        )
        script_path.chmod(0o755)

    current_path = monkeypatch._getenv("PATH") if hasattr(monkeypatch, "_getenv") else ""
    import os

    current_path = os.environ.get("PATH", "")
    monkeypatch.setenv("PATH", f"{mock_bin_dir}:{current_path}")
    return commands_log
