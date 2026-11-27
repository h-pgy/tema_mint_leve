# Modelo de Documento: `SPEC.md` (Etapa 2 — Planning e Especificação)

> **Regras deste Modelo**:
> - **Onde salvar**: `specs/<epico>/<NN_nome_da_spec>/SPEC.md`
> - **Formato Travado**: Todas as 7 seções abaixo e o YAML Frontmatter são obrigatórios para manter todas as especificações do repositório no mesmo padrão.
> - **Snippets Principais**: A seção 6 deve trazer apenas os trechos-chave da lógica (o "coração" do script ou função) para revisão rápida, nunca o código inteiro despejado.

```markdown
---
epic: "<nome_do_epico>"
spec: "<NN_nome_da_spec>"
type: "spec"
category: "<categoria_ou_core>"
module_id: "<id_do_modulo_ou_componente>"
requires_ui_mock: false
approved: false
implemented: false
---

# Spec: <Título da Entrega>

## 1. Objetivo e Escopo
- **O quê**: <Ação técnica principal>
- **Para quê**: <Problema que resolve/evita>
- **Resultado**: <Capacidade habilitada no sistema/projeto>

## 2. Grafo de Dependências e Ordem de Execução
- **`order`**: `<int>`
- **`depends_on`**: `["<cat>.<mod>"]`
- **Impacto no Grafo (DAG)**: <Explicação de como este módulo se conecta a scripts anteriores ou posteriores e como se comporta quando invocado isoladamente via `--module`>

## 3. Especificação do Registry (`YAML`)
```yaml
# Trecho exato para scripts/<category>/registry.yaml
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

## 4. Modelo Pydantic (`core/models.py`)
```python
# Representação/validação Pydantic do ScriptModule (ou novos modelos/campos do core)
...
```

## 5. Contrato de Execução, Idempotência e Assets
- **Entrypoint & Runner**: `run.sh` (`bash`) ou `run.py` (`python`)
- **Variáveis de Contexto consumidas**: `TARGET_HOME`, `MODULE_ASSETS_DIR`, `DOTENV_PATH`, `DRY_RUN` + variáveis do `.env`
- **Assets locais (`assets/`)**: <Lista de arquivos em `scripts/<cat>/<mod>/assets/`>
- **Arquivos gerados/modificados (`expected_files`)**: <Caminhos relativos a `TARGET_HOME`>
- **Regras de Idempotência**: <Como o script garante execução segura repetida>
- **Portabilidade de UI do Mock & Atomic Design para o OS (Obrigatório se `requires_ui_mock: true`, senão `N/A`)**:
  - **Mock de Origem**: `referencias/MOCK.md` e `referencias/mock.html`
  - **Sincronização com `design_system/`**: <Quais Tokens (`--ds-*`), Átomos (`.ds-atom-*`), Moléculas (`.ds-mol-*`) e Organismos (`.ds-org-*`) são reutilizados ou promovidos para `design_system/css/design-system.css` e `design_system/{tokens,atoms,molecules,organisms}.html`>
  - **Tokens de Cor e Tipografia**: <Mapeamento `--ds-*` para `@define-color` no `gtk.css` e propriedades do `themerc`/`.xpm` no `xfwm4`>
  - **Mapeamento de Seletores e Propriedades**: <Tradução das classes `.ds-*` para seletores nativos `GtkCssProvider` (`.xfce4-panel`, `headerbar`, `:backdrop`, `min-width`/`min-height`) e assets `.xpm`/`themerc` do `xfwm4`>

## 6. Snippets Principais de Implementação
> Apenas os trechos-chave da lógica (comandos principais, checagem de idempotência ou assinaturas/algoritmo central), sem despejar o arquivo inteiro.

```bash
# Snippet principal (ex: trecho central do run.sh, run.py ou função do core)
...
```

## 7. Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2
```
