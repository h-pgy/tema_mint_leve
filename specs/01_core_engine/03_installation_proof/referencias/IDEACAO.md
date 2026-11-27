---
epic: "01_core_engine"
spec: "03_installation_proof"
type: "ideation"
requires_ui_mock: false
approved: false
implemented: false
---

# Ideação (Rascunho Inicial): Arquitetura de "Prova de Instalação" (ABC / Duck Typing + DTOs)

> **Status**: Rascunho inicial gerado durante a subdivisão do épico `01_core_engine`. Quando esta spec for iniciada na Etapa 1 (`sdd-ideation`), o agente deve partir deste documento e refiná-lo com o usuário antes de marcar `approved: true`.

## Objetivo e Motivação
Construir uma arquitetura extensível e polimórfica para verificar se um script já foi instalado ("Prova de Instalação"), permitindo que o controlador de dependências consulte qualquer script através de uma **mesma assinatura padronizada (ABC / Duck Typing)** com entradas e saídas fortemente tipadas por **classes DTO**.

## Pontos Já Levantados para Detalhar na Ideação desta Spec

1. **Contrato Abstrato (`ABC` + Duck Typing)**:
   - Ter uma classe base abstrata (`abc.ABC` com `@abstractmethod`, ex: `InstallableScriptABC` ou `InstallationCheckerABC`) que o modelo do script é obrigado a implementar.
   - Todo script (ou verificador de script) segue exatamente a mesma assinatura para ser chamado pelo controlador sem acoplamento:
     `check_installation(context: CheckContextDTO) -> CheckResultDTO`
   - Cada script pode ter sua própria lógica de checagem (declarativa ou customizada), mas todos respondem ao mesmo contrato.
2. **Entradas e Saídas Tipadas com Classes DTO (Pydantic)**:
   - **DTO de Entrada (`CheckContextDTO`)**:
     - Dados de contexto tipados, incluindo `settings: AppSettings` (de `config.py`), `target_home: Path`, `module_full_id: str`, `module_dir: Path | None`, caminho do manifesto de estado, etc.
   - **DTO de Saída (`CheckResultDTO`)**:
     - `module_id: str`
     - `is_installed: bool`
     - `strategy_used: str`
     - `missing_files: list[Path]`
     - `command_exit_code: int | None`
     - `in_state_manifest: bool`
     - `reason: str` (mensagem clara explicando o resultado da verificação).
3. **As 3 Fontes de Prova de Instalação (usando `utils/` e `config.py`)**:
   - **Arquivos/diretórios esperados (`expected_files`)**: Caminhos relativos ao `TARGET_HOME` (ex: `.pyenv/version`, `.config/Code/User/settings.json`) verificados via `utils/`.
   - **Comando / Binário no PATH (`check_command`)**: Comando que retorna exit code `0` quando a ferramenta já está instalada (ex: `docker --version`).
   - **Manifesto de Estado do Core (`installed_state.json`)**: Arquivo gerenciado pelo próprio core em `TARGET_HOME/.config/tema_mint_leve/installed_state.json` registrando módulos executados com sucesso.
   - **Checagem Customizada por Script**: Possibilidade de um módulo fornecer um verificador específico herdando da ABC e mantendo a assinatura `check_installation(context: CheckContextDTO) -> CheckResultDTO`.
