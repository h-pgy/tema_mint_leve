# Estratégia de Testes (`tests/` com Pytest)

A testabilidade é um pilar central do projeto: queremos garantir que o registry esteja sempre íntegro e que todos os scripts (`.sh` e `.py`) criem os arquivos `.env` e configurações esperadas sem precisar formatar o computador para testar.

---

## 1. Camadas de Teste

### Camada 1: Testes Unitários — Registry, Core e Estrutura (`@pytest.mark.unit`)
- Focados em validação rápida e isolada, sem execução de scripts externos nem I/O real no sistema.
- Em `tests/test_registry.py`, carrega todas as categorias dentro de `scripts/*/` através dos modelos Pydantic (`CategoryRegistry` e `ScriptModule`) e verifica automaticamente:
  - Se todos os arquivos de `registry` têm sintaxe e campos válidos.
  - Se o `entrypoint` (`run.sh` ou `run.py`) existe e tem permissão adequada.
  - Se o `README.md` da categoria e de cada módulo existem e não estão vazios.
  - Se todas as referências em `depends_on` apontam para IDs de módulos válidos.
- Cobre também testes unitários da lógica do `core/` (geração de `.env`, templates, resolução de dependências) e do `cli/`.

### Camada 2: Testes de Integração em Sandbox (`@pytest.mark.integration`)
- Em `tests/test_modules.py`, testa a execução real dos scripts (`run.sh` e `run.py`) via `core/runner.py` em um ambiente controlado usando fixtures do `pytest`.
- Verifica se o código de saída (`returncode`) é `0`.
- Valida se todos os arquivos declarados em `expected_files` no Pydantic Model (assim como arquivos `.env` gerados) foram efetivamente criados dentro do `TARGET_HOME` de teste e possuem o conteúdo esperado.

### Camada 3: Verificação Pós-Instalação Real (`@pytest.mark.post_install`)
- Testes marcados com `@pytest.mark.post_install` que rodam contra a máquina real após uma instalação completa.
- Checam se os binários (`pyenv`, `uv`, `git`, `docker`, etc.) estão no `PATH` e se os arquivos reais em `$HOME` foram aplicados corretamente.
- **Não rodam por padrão** no `uv run pytest`, pois dependem do estado real da máquina hospedeira.

---

## 2. Flags (*Markers*) do Pytest

Todos os testes do projeto devem ser categorizados com *markers* do `pytest` para permitir execuções seletivas com `-m`:

| Flag (`-m`) | Escopo | Quando usar |
| --- | --- | --- |
| `unit` | Testes unitários rápidos (modelos Pydantic, registries, gerador de `.env`, `core/` e `cli/`) | Feedback imediato durante o desenvolvimento |
| `integration` | Execução de scripts e fluxos integrados em sandbox (`TARGET_HOME` + `mock_bin`) | Validar que módulos e `runner` funcionam juntos sem tocar no sistema real |
| `post_install` | Verificações na máquina real após rodar o instalador | Auditar o ambiente real após formatação/instalação |
| `slow` | Testes mais demorados (ex: cadeias completas de módulos ou simulações pesadas) | Pode ser combinado com `not slow` para ciclos rápidos |

### Exemplos de Execução com `uv`

```bash
# Suíte padrão de desenvolvimento (unit + integration; exclui post_install)
uv run pytest

# Apenas testes unitários
uv run pytest -m unit

# Apenas testes de integração em sandbox
uv run pytest -m integration

# Verificação pós-instalação na máquina real
uv run pytest -m post_install

# Combinando flags (ex: testes rápidos de integração ou tudo exceto lentos)
uv run pytest -m "integration and not slow"
uv run pytest -m "not slow"
```

### Registro no `pyproject.toml`

Os *markers* devem ser declarados explicitamente no `pyproject.toml` com `--strict-markers` para evitar erros de digitação, excluindo `post_install` da execução padrão:

```toml
[tool.pytest.ini_options]
addopts = "--strict-markers -m 'not post_install'"
markers = [
    "unit: testes unitários rápidos e isolados (core, cli, registries)",
    "integration: testes de integração em sandbox (TARGET_HOME e mock_bin)",
    "post_install: verificação pós-instalação na máquina real",
    "slow: testes demorados (podem ser pulados com -m 'not slow')",
]
```

---

## 3. Fixtures Principais (`tests/conftest.py`)

Para que scripts Bash e Python possam ser testados sem alterar o sistema hospedeiro durante o desenvolvimento:

1. **`fake_home(tmp_path)`**:
   - Cria uma estrutura limpa de diretório home (`tmp_path / "home"`, incluindo `.config/`, `.local/bin/`, etc.) e a injeta como `TARGET_HOME`.
2. **`mock_system_bins(tmp_path, monkeypatch)`**:
   - Cria um diretório `tmp_path / "mock_bin"` adicionado ao início do `PATH`.
   - Fornece *stubs* para comandos de sistema que exigiriam root ou alterariam o OS durante testes unitários (ex: `sudo`, `apt-get`, `systemctl`, `xfconf-query`), registrando todas as chamadas em um arquivo `commands.log` para que o teste possa fazer *assertions* sobre quais comandos o script executou.
3. **`sandbox_context(fake_home, mock_system_bins)`**:
   - Instancia um `ExecutionContext` do Pydantic apontando para o `fake_home` e para o `.env` de teste, pronto para ser passado ao `core/runner.py`.
