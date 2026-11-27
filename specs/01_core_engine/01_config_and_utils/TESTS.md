---
epic: "01_core_engine"
spec: "01_config_and_utils"
type: "tests"
test_file: "tests/test_config_and_utils.py"
max_recommended_tests: 5
approved: true
implemented: true
---

# Plano de Testes TDD: Configurações Globais (`config.py`), Utilitários (`utils/`) e Exceções Semânticas

## Resumo da Suíte
- **Arquivo de Teste Alvo**: `tests/test_config_and_utils.py`
- **Quantidade de Testes**: 5 (Limite recomendado: 3 a 5)

---

## Especificação dos Testes

### Teste 1: `test_app_settings_defaults_and_env_overrides`
- **Marker / Camada**: `unit`
- **O que testa**: Valida se `get_settings()` retorna os valores default corretos quando os diretórios base existem (`PROJECT_ROOT`, `TARGET_HOME`, `SCRIPTS_DIR`, `DOTENV_PATH`, `STATE_FILE_REL_PATH`, `DRY_RUN=False`) e se reflete dinamicamente sobrescritas válidas de variáveis de ambiente (`TARGET_HOME`, `SCRIPTS_DIR`, `MODULE_DIR`, `MODULE_ASSETS_DIR`, `DRY_RUN=1`).
- **Entrada (Inputs / Estado Inicial)**: Diretórios válidos criados em `tmp_path` (`home/`, `scripts/`, `mod/`, `mod/assets/`) e variáveis injetadas via `monkeypatch.setenv`.
- **Fixtures & Mocks**: `monkeypatch`, `tmp_path`
- **Resultado Esperado**: Sem overrides, `TARGET_HOME` é `Path.home()`, `SCRIPTS_DIR` é `PROJECT_ROOT / "scripts"`, `MODULE_ASSETS_DIR` é `None` e `DRY_RUN` é `False`. Com overrides apontando para os diretórios reais em `tmp_path` e `DRY_RUN="1"`, `get_settings()` instancia sem erros e retorna os caminhos correspondentes com `DRY_RUN is True`.

### Teste 2: `test_app_settings_fail_fast_semantic_exceptions`
- **Marker / Camada**: `unit`
- **O que testa**: Verifica se os validadores do `AppSettings` impedem a inicialização e lançam as exceções semânticas específicas de `utils/exceptions.py` quando variáveis de ambiente apontam para diretórios inexistentes ou inválidos.
- **Entrada (Inputs / Estado Inicial)**: Cenários isolados com `SCRIPTS_DIR` inexistente, `TARGET_HOME` inexistente, `MODULE_DIR` inexistente, `MODULE_ASSETS_DIR` inexistente, `DOTENV_PATH` com diretório pai inexistente e `STATE_FILE_REL_PATH` com path traversal (`../state.json`).
- **Fixtures & Mocks**: `monkeypatch`, `tmp_path`
- **Resultado Esperado**: `get_settings()` lança respectivamente `ScriptsDirectoryNotFoundError`, `TargetHomeNotFoundError`, `ModuleDirectoryNotFoundError`, `ModuleAssetsDirectoryNotFoundError`, `InvalidDotenvPathError` e `PathTraversalNotAllowedError` (todas subclasses de `MintLeveBaseError`).

### Teste 3: `test_validate_and_check_safe_relative_paths`
- **Marker / Camada**: `unit`
- **O que testa**: Garante que `validate_relative_path` e `is_safe_relative_path` aceitam caminhos relativos válidos (ex: `.config/gtk-3.0/gtk.css`, `.bashrc`) e lançam as exceções semânticas específicas de `utils/exceptions.py` para caminhos vazios, absolutos (`/etc/passwd`), iniciados com `~` (`~/.bashrc`) ou com path traversal (`../fora`, `a/../../b`).
- **Entrada (Inputs / Estado Inicial)**: Lista de caminhos relativos válidos e casos inválidos (vazio `""`, absoluto `"/etc/hosts"`, home `"~/.config"`, traversal `"../secret"`).
- **Fixtures & Mocks**: `Nenhuma`
- **Resultado Esperado**: Para caminhos válidos, `is_safe_relative_path` retorna `True` e `validate_relative_path` retorna o `Path` relativo. Para os inválidos, `is_safe_relative_path` retorna `False` e `validate_relative_path` lança `EmptyRelativePathError`, `AbsolutePathNotAllowedError` e `PathTraversalNotAllowedError` respectivamente.

### Teste 4: `test_resolve_target_asset_and_state_paths`
- **Marker / Camada**: `unit`
- **O que testa**: Verifica a resolução de caminhos completos dentro de `TARGET_HOME` (`resolve_target_path` e `resolve_state_file_path`) e dentro de `MODULE_ASSETS_DIR` (`resolve_asset_path`), incluindo a exceção semântica `ModuleAssetsNotConfiguredError` quando `MODULE_ASSETS_DIR` não está configurado.
- **Entrada (Inputs / Estado Inicial)**: `TARGET_HOME` apontando para diretório existente `tmp_path / "home"`; chamada a `resolve_asset_path("xsettings.xml")` primeiro com `MODULE_ASSETS_DIR=None` e depois com `MODULE_ASSETS_DIR` apontando para `tmp_path / "assets"` existente.
- **Fixtures & Mocks**: `monkeypatch`, `tmp_path`
- **Resultado Esperado**: `resolve_target_path(".gitconfig")` retorna `tmp_path / "home/.gitconfig"`; `resolve_state_file_path()` retorna `tmp_path / "home/.config/tema_mint_leve/installed_state.json"`; `resolve_asset_path` lança `ModuleAssetsNotConfiguredError` quando `MODULE_ASSETS_DIR` é `None` e retorna `tmp_path / "assets/xsettings.xml"` quando configurado.

### Teste 5: `test_file_and_dir_exists_helpers`
- **Marker / Camada**: `unit`
- **O que testa**: Confirma que `file_exists` e `dir_exists` distinguem corretamente arquivos regulares, diretórios existentes e caminhos inexistentes.
- **Entrada (Inputs / Estado Inicial)**: Um diretório real `tmp_path / "subdir"`, um arquivo real `tmp_path / "subdir/file.txt"` e um caminho inexistente `tmp_path / "missing"`.
- **Fixtures & Mocks**: `tmp_path`
- **Resultado Esperado**: `dir_exists` retorna `True` apenas para `subdir` (e `False` para `file.txt` e `missing`); `file_exists` retorna `True` apenas para `file.txt` (e `False` para `subdir` e `missing`).
