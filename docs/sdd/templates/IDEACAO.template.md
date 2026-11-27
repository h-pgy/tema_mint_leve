# Modelo de Documento: `referencias/IDEACAO.md` (Etapa 1 — Ideação)

> **Regras deste Modelo**:
> - **Onde salvar**: `specs/<epico>/<NN_nome_da_spec>/referencias/IDEACAO.md`
> - **Frontmatter Obrigatório**: O bloco YAML no topo com `epic`, `spec`, `type: "ideation"`, `requires_ui_mock`, `approved` e `implemented` é estrito e obrigatório.
> - **Corpo Livre**: O conteúdo abaixo do frontmatter tem formato livre e direto. Serve para registrar o objetivo técnico da entrega ("O que fazer e para conseguir o quê"), as respostas rápidas do usuário (`Sim/Não`, `1/2/3`), se requer mock visual (`requires_ui_mock`), como o script se encaixa no grafo de dependências e o rascunho do YAML do registry.

```markdown
---
epic: "<nome_do_epico>"
spec: "<NN_nome_da_spec>"
type: "ideation"
requires_ui_mock: false
approved: false
implemented: false
---

# Ideação: <Título da Entrega>

## Objetivo e Motivação
<Registro direto do que será feito/instalado, qual problema evita e qual resultado habilita.>

## Decisões Rápidas e Escopo
- **Categoria / Localização**: <ex: `scripts/app_installers/pyenv` ou `core/...`>
- **Requer Mock Visual (`requires_ui_mock`)**: <`true` se envolver UI, cores de tema GTK3, bordas `xfwm4`, `xfce4-panel` ou rice; `false` caso contrário>
- **Grafo de Dependências**: <Quando roda, `order`, `depends_on` e se pode rodar isolado>
- **Idempotência e Sandbox**: <Comportamento ao rodar 2x e comandos externos que precisam de mock>

## Rascunho do Registry (`YAML`)
```yaml
id: <module_id>
name: "<Nome Amigável>"
entrypoint: run.sh
runner: bash
requires_sudo: false
order: 10
depends_on: []
env_prompts: []
expected_files: []
```
```
