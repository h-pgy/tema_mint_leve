# Modelo de Documento: `TESTS.md` (Etapas 2 e 3 — Planning & TDD)

> **Regras Estritas deste Modelo**:
> - **Onde salvar**: `specs/<epico>/<NN_nome_da_spec>/TESTS.md`
> - **Política Anti-Bloat**: Planeje entre **3 e 5 testes** de alto valor por spec.
> - **Zero Código Python**: Este documento **NÃO** deve conter código de implementação dos testes. Ele serve para o usuário revisar quais testes existirão, qual a entrada, quais fixtures serão usadas e qual o resultado esperado.
> - **Formato Travado de 4 Campos por Teste**: Todo teste deve conter obrigatoriamente:
>   1. **Marker / Camada** + **O que testa**
>   2. **Entrada (Inputs / Estado Inicial)**
>   3. **Fixtures & Mocks**
>   4. **Resultado Esperado**

```markdown
---
epic: "<nome_do_epico>"
spec: "<NN_nome_da_spec>"
type: "tests"
test_file: "tests/<arquivo_de_teste>.py"
max_recommended_tests: 5
approved: false
implemented: false
---

# Plano de Testes TDD: <Título da Entrega>

## Resumo da Suíte
- **Arquivo de Teste Alvo**: `tests/<arquivo_de_teste>.py`
- **Quantidade de Testes**: <N> (Limite recomendado: 3 a 5)

---

## Especificação dos Testes

### Teste 1: `test_<nome_descritivo_1>`
- **Marker / Camada**: `unit` | `integration` | `post_install`
- **O que testa**: <Descrição curta de 1 linha do objetivo do teste>
- **Entrada (Inputs / Estado Inicial)**: <Parâmetros passados, variáveis do `.env`, arquivos pré-existentes ou flags como `DRY_RUN=0`>
- **Fixtures & Mocks**: <Ex: `fake_home`, `mock_system_bins` (`git`, `curl`), `sandbox_context` ou `Nenhuma`>
- **Resultado Esperado**: <O que deve acontecer exatamente: código de retorno, arquivos criados no `TARGET_HOME`, conteúdo esperado, comandos registrados no `commands.log` ou exceção levantada>

### Teste 2: `test_<nome_descritivo_2>`
- **Marker / Camada**: `integration`
- **O que testa**: ...
- **Entrada (Inputs / Estado Inicial)**: ...
- **Fixtures & Mocks**: ...
- **Resultado Esperado**: ...

### Teste 3: `test_<nome_descritivo_3>`
- **Marker / Camada**: `integration`
- **O que testa**: ...
- **Entrada (Inputs / Estado Inicial)**: ...
- **Fixtures & Mocks**: ...
- **Resultado Esperado**: ...
```
