# tema_mint_leve

Automação pós-formatação, configuração de ambiente de desenvolvimento e *rice* para **Linux Mint (XFCE)**, pensado para laptops antigos com foco em **performance e duração de bateria**.

Com um único repositório, você formata o laptop, clona o projeto e executa o instalador interativo para configurar desde `pyenv`, `uv`, `git` e `docker` até otimizações do sistema operacional e preferências de janelas/temas leves do Mint.

---

## Quickstart (Pós-Formatação)

Logo após clonar o repositório em uma máquina recém-instalada, rode o script de bootstrap (que instala `pyenv` e `uv`, prepara o ambiente Python isolado e abre o CLI interativo):

```bash
chmod +x install.sh
./install.sh
```

---

## Comandos do CLI

Depois que o `uv` estiver disponível, você pode executar o CLI tanto pelo `./install.sh` quanto diretamente via `uv run`:

```bash
# Abrir o menu interativo completo (navegação por categorias e READMEs dos módulos)
uv run python -m cli

# Listar todas as categorias e módulos registrados
uv run python -m cli --list

# Rodar apenas uma categoria específica (ex: rice ou dev_env)
uv run python -m cli --category rice

# Rodar módulos específicos diretamente
uv run python -m cli --module app_installers.docker --module dev_env.vscode

# Modo simulação (Dry-Run): mostra o que seria executado e gera preview sem alterar o sistema
uv run python -m cli --dry-run
```

---

## Comandos de Teste (`pytest`)

O projeto utiliza `pytest` com fixtures de sandbox para testar a integridade do registry e garantir que os scripts criem todos os arquivos `.env` e configurações esperadas:

```bash
# Rodar a suíte padrão (unit + integration; exclui post_install por padrão)
uv run pytest

# Rodar apenas testes unitários (registries, modelos Pydantic, core e CLI)
uv run pytest -m unit

# Rodar apenas testes de integração em sandbox (execução dos módulos com TARGET_HOME temporário)
uv run pytest -m integration

# Rodar verificação pós-instalação na máquina real (checa se tudo foi instalado de verdade)
uv run pytest -m post_install

# Rodar pulando testes lentos
uv run pytest -m "not slow"
```

---

## Comandos de Desenvolvimento (`uv`)

```bash
# Sincronizar dependências do projeto (ambiente virtual gerenciado pelo uv)
uv sync

# Adicionar uma nova dependência Python ao core/cli
uv add <pacote>

# Adicionar uma dependência apenas de desenvolvimento/teste
uv add --dev <pacote>
```

---

## Documentação e Arquitetura

A documentação do projeto segue o princípio de *progressive disclosure*:

- **[AGENTS.md](AGENTS.md)**: Visão geral concisa do projeto e guia de navegação para agentes e contribuidores.
- **[docs/sdd/README.md](docs/sdd/README.md)**: Fluxo de Spec-Driven Development (SDD), organização de Épicos em `specs/`, templates em `docs/sdd/templates/` e agentes/skills de Ideação, Planning, TDD e Implementação.
- **[docs/architecture/README.md](docs/architecture/README.md)**: Detalhes da arquitetura (`install.sh` $\rightarrow$ `cli/` $\rightarrow$ `core/` $\rightarrow$ `scripts/`), modelos Pydantic, grafo de dependências e contrato de execução.
- **[docs/modules/README.md](docs/modules/README.md)**: Como funcionam as categorias de domínio, o `registry`, os `README.md` de cada script e os `assets/` co-localizados.
- **[docs/testing/README.md](docs/testing/README.md)**: Estratégia de testes com `pytest`, fixtures de sandbox (`TARGET_HOME`) e verificação pós-instalação.
