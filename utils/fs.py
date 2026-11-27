"""Utilitários de verificação de arquivos e diretórios no sistema de arquivos (utils/fs.py)."""

from pathlib import Path


def file_exists(path: str | Path) -> bool:
    """Retorna True se o caminho existir e for um arquivo regular."""
    candidate = Path(path)
    return candidate.exists() and candidate.is_file()


def dir_exists(path: str | Path) -> bool:
    """Retorna True se o caminho existir e for um diretório."""
    candidate = Path(path)
    return candidate.exists() and candidate.is_dir()
