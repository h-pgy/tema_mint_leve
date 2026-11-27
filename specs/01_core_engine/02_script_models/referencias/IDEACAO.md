---
epic: "01_core_engine"
spec: "02_script_models"
type: "ideation"
requires_ui_mock: false
approved: false
implemented: false
---

# Ideação (Rascunho Inicial): Modelos Pydantic de Scripts, Tipos (`ScriptType`) e Validações (`core/models.py`)

> **Status**: Rascunho inicial gerado durante a subdivisão do épico `01_core_engine`. Quando esta spec for iniciada na Etapa 1 (`sdd-ideation`), o agente deve partir deste documento e refiná-lo com o usuário antes de marcar `approved: true`.

## Objetivo e Motivação
Definir os contratos de dados e validações estruturais de scripts e categorias em `core/models.py` (usando Pydantic v2 e consumindo `config.py` e `utils/` criados na spec `01_config_and_utils`).

## Pontos Já Levantados para Detalhar na Ideação desta Spec

1. **Diferenciação de Scripts por Tipo (`script_type: ScriptType`)**:
   - Enum obrigatório no modelo do script para classificar a natureza de cada módulo:
     - `app_install`: Instalação de aplicativos, pacotes ou runtimes (ex: Docker, VS Code, Pyenv, pacotes `apt`/Flatpak).
     - `app_config`: Configuração de aplicativos ou ambiente de desenvolvimento pós-instalação (ex: `settings.json` e extensões do VS Code, `.gitconfig`, plugins do shell).
     - `sys_util`: Utilitários de sistema, ferramentas CLI ou scripts auxiliares de manutenção/limpeza.
     - `os_theme`: Tema visual do sistema operacional / *rice* (ex: temas GTK3, bordas `xfwm4`, ícones, fontes, aparência do `xfce4-panel` e terminal).
     - `os_config`: Configurações funcionais e de performance/bateria do OS (ex: ZRAM, `swappiness`, TLP/auto-cpufreq, atalhos do XFCE, serviços `systemd`).
2. **Organização por Categorias e Temas (`tags` / `themes`)**:
   - Manter a pasta física por Categoria (`scripts/<categoria>/registry.yaml`) + suportar `tags` / `themes` no `ScriptModule` para permitir que o usuário rode todos os scripts de um tema transversal (ex: todos os scripts de instalação de apps de dev + configuração do VS Code).
3. **Modelos Pydantic Previstos**:
   - `EnvPrompt`: `key` (`UPPER_SNAKE_CASE`), `prompt`, `default`, `secret`.
   - `ScriptModule`: `id` (`snake_case`), `name`, `description`, `script_type` (`ScriptType`), `entrypoint` (`run.sh` ou `run.py`), `runner` (`bash` ou `python`), `requires_sudo`, `order`, `tags` (`list[str]`), `depends_on` (`list[str]`), `env_prompts` (`list[EnvPrompt]`), `expected_files` (`list[str]`), `check_command` (`str | None`).
   - `CategoryRegistry`: `category_id`, `title`, `description`, `order`, `modules` (`list[ScriptModule]`, validando unicidade de `id`).
4. **Classe / Regras de Validação (usando `utils/` e `config.py`)**:
   - Compatibilidade entre `runner` (`bash` vs `python`) e extensão do `entrypoint` (`.sh` vs `.py`).
   - Validação de `expected_files` usando `utils.validate_relative_path` (sem paths absolutos `/` ou `..`).
   - Validação no sistema de arquivos (usando `utils.file_exists` / `utils.dir_exists`) garantindo que a pasta do módulo, o `entrypoint` e o `README.md` existem.

## Rascunho do Registry (`YAML`)
```yaml
category_id: dev_env
title: "Ambiente de Desenvolvimento"
order: 20
modules:
  - id: vscode_base
    name: "VS Code (Configuração & Extensões)"
    script_type: app_config
    entrypoint: run.sh
    runner: bash
    requires_sudo: false
    order: 10
    tags:
      - vscode
      - dev_workstation
    depends_on:
      - app_installers.vscode
      - dev_env.git_config
    env_prompts:
      - key: VSCODE_PROFILE_NAME
        prompt: "Nome do perfil padrão do VS Code"
        default: "Default"
        secret: false
    expected_files:
      - ".config/Code/User/settings.json"
    check_command: "code --version"
```
