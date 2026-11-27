---
epic: "01_core_engine"
spec: "04_dependency_dag"
type: "ideation"
requires_ui_mock: false
approved: false
implemented: false
---

# Ideação (Placeholder Inicial): Controle de Dependências (DAG), Execução por Temas e Plano de Execução

> **Status**: Placeholder inicial gerado durante a subdivisão do épico `01_core_engine`. Quando esta spec for iniciada na Etapa 1 (`sdd-ideation`), o agente deve partir deste documento e detalhá-lo com o usuário antes de marcar `approved: true`.

## Objetivo e Motivação
Construir o controlador do Grafo Direcionado Acíclico (DAG) de dependências dos scripts, permitindo tanto rodar um **tema/categoria inteira** (ex: todos os scripts de instalação de apps de dev + configuração do VS Code) quanto rodar um **script independente**, identificando automaticamente suas dependências, verificando quais já estão instaladas (via duck typing da spec `03_installation_proof`) e retornando um DTO de plano de execução que avise ao usuário quais scripts adicionais (`X, Y, Z`) serão instalados.

## Pontos Já Levantados para Detalhar na Ideação desta Spec

1. **Execução por Tema / Categoria vs. Script Isolado**:
   - Seleção de todos os módulos de uma categoria ou tema (`tags`, ex: `vscode` ou `dev_workstation`) ou de um único módulo avulso (`<category_id>.<module_id>`).
2. **Resolução do Grafo (DAG) e Ordenação Topológica**:
   - Resolução recursiva de `depends_on` respeitando o campo `order`.
   - Detecção de ciclos de dependência (`CircularDependencyError`) e dependências inexistentes (`MissingDependencyError`).
3. **Integração via Duck Typing com a Prova de Instalação**:
   - Para cada dependência encontrada no grafo, o controlador chama `script.check_installation(CheckContextDTO) -> CheckResultDTO`.
   - Se a dependência já estiver instalada (`is_installed: True`), ela não precisa ser reinstalada (a menos que seja forçada).
4. **Retorno de `ExecutionPlanDTO` e Aviso ao Usuário (`Scripts X, Y, Z serão instalados também`)**:
   - O core não bloqueia com `input()` diretamente; ele retorna um `ExecutionPlanDTO` contendo:
     - `requested_modules`: Módulos que o usuário pediu explicitamente.
     - `additional_dependencies_to_install`: Dependências (`X, Y, Z`) que ainda não estão instaladas e precisarão rodar antes.
     - `already_installed_dependencies`: Dependências puladas por já possuírem prova de instalação válida.
     - `ordered_execution_queue`: Lista final em ordem topológica pronta para o runner executar após confirmação do usuário no CLI.
