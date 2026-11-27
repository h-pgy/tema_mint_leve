---
name: sdd-workflow
description: >-
  Skill Master do fluxo de Spec-Driven Development (SDD) do tema_mint_leve.
  Ative sempre que o usuário quiser iniciar, continuar ou verificar o status de
  um épico ou spec em specs/<epico>/<spec>/, ou quando mencionar ideação,
  planning, spec, testes TDD ou implementação de uma entrega.
---

# Skill Master: Spec-Driven Development (`sdd-workflow`)

Você é o **Orquestrador do Fluxo SDD** do projeto `tema_mint_leve`.
Todo o desenvolvimento deste projeto segue um ciclo de **4 etapas principais + 1 etapa opcional de Mock Visual (1.5)** isoladas por contexto, organizado dentro de `specs/<epico>/<NN_nome_da_spec>/`.

Para detalhes estruturais e referências aos modelos de documentos, consulte [docs/sdd/README.md](../../../docs/sdd/README.md) e a pasta [docs/sdd/templates/](../../../docs/sdd/templates/).

---

## 1. Estrutura Obrigatória do Diretório da Spec

Cada spec vive dentro de um diretório de Épico temático (`specs/<epico>/<NN_nome_da_spec>/`).
Na raiz da pasta da spec só podem existir **três itens**:
1. `SPEC.md` (A especificação técnica formal com YAML do registry, modelo Pydantic, grafo de dependências e, quando aplicável, o guia de portabilidade do mock visual para o OS).
2. `TESTS.md` (O plano e especificação enxuta dos testes TDD).
3. `referencias/` (Subpasta contendo `IDEACAO.md`, `MOCK.md` + `mock.html` quando `requires_ui_mock: true`, e quaisquer outros arquivos de referência).

---

## 2. Regra de Ouro: Frontmatter (`approved` + `implemented`) & Double-Check

**NUNCA** assuma que uma etapa está pronta apenas porque o arquivo `.md` existe no disco (a conversa anterior pode ter sido interrompida antes da aprovação ou conclusão).

Todo arquivo de controle (`referencias/IDEACAO.md`, `referencias/MOCK.md`, `SPEC.md`, `TESTS.md`) possui um bloco YAML Frontmatter no topo com duas flags booleanas:
- `approved: true | false`
- `implemented: true | false`

Além disso, `referencias/IDEACAO.md` e `SPEC.md` possuem a flag booleana:
- `requires_ui_mock: true | false` (obrigatória como `true` sempre que a spec envolver mudanças de interface de usuário, tema GTK3, painel XFCE, bordas de janelas `xfwm4`, cores, fontes ou *rice*).

### Como determinar a etapa atual (Máquina de Estados com Double-Check):

Inspecione a pasta `specs/<epico>/<spec>/`:

1. **Etapa 1 — Ideação (`sdd-ideation`)**:
   - **Quando acionar**: A pasta da spec não existe, ou `referencias/IDEACAO.md` existe mas está com `approved: false` (e `SPEC.md` ainda não existe).
   - **Ação**: Leia e siga `.agents/skills/sdd-ideation/SKILL.md`.

2. **Etapa 1.5 (Opcional / Condicional) — Mock Visual e Guardrails de UI (`sdd-ui-mock`)**:
   - **Quando acionar**: `referencias/IDEACAO.md` existe com `approved: true` e **`requires_ui_mock: true`**, mas `referencias/MOCK.md` ainda não existe ou está com `approved: false` (ou o arquivo `referencias/mock.html` não existe no disco).
   - **Double-Check**: Verifique se a ideação definiu quais elementos visuais (tema GTK3, painel XFCE, bordas `xfwm4`, terminal, etc.) serão customizados.
   - **Ação**: Leia e siga `.agents/skills/sdd-ui-mock/SKILL.md`. Só avance para a Etapa 2 depois que o usuário visualizar `referencias/mock.html` e aprovar o mock (`approved: true` em `referencias/MOCK.md`).

3. **Etapa 2 — Planning / Spec (`sdd-planning`)**:
   - **Quando acionar**:
     - Para specs sem UI (`requires_ui_mock: false`): `referencias/IDEACAO.md` existe com `approved: true` e `implemented: false` (ou `SPEC.md` foi iniciado mas está com `approved: false`).
     - Para specs com UI (`requires_ui_mock: true`): `referencias/IDEACAO.md` está com `approved: true` **E** `referencias/MOCK.md` está com `approved: true` (com `referencias/mock.html` presente no disco), enquanto `SPEC.md` ainda não existe ou está com `approved: false`.
   - **Double-Check**: Verifique se `referencias/IDEACAO.md` contém objetivo, dependências e rascunho do registry, e (se `requires_ui_mock: true`) se `referencias/MOCK.md` contém a tabela de tokens de cor, checklist de guardrails GTK3/XFCE e mapa de portabilidade.
   - **Ação**: Leia e siga `.agents/skills/sdd-planning/SKILL.md`. Ao concluir o `SPEC.md` e o `TESTS.md`, o agente atualiza `referencias/IDEACAO.md` (e `referencias/MOCK.md`, se houver) para `implemented: true`.

4. **Etapa 3 — Testes TDD (`sdd-tdd`)**:
   - **Quando acionar**: `SPEC.md` existe com `approved: true` (e `referencias/IDEACAO.md` está com `implemented: true`), mas `TESTS.md` ainda está com `approved: false` ou `implemented: false`.
   - **Double-Check**:
     1. Verifique se `SPEC.md` está com `approved: true` (e se `requires_ui_mock: true`, confirme que `referencias/MOCK.md` também está com `approved: true` e `implemented: true`).
     2. Rode `uv run pytest` para garantir que a suíte existente passa sem erros antes de criar novos testes.
   - **Ação**: Leia e siga `.agents/skills/sdd-tdd/SKILL.md`.

5. **Etapa 4 — Implementação (`sdd-implementation`)**:
   - **Quando acionar**: `SPEC.md` está com `approved: true` e `implemented: false`, E `TESTS.md` está com `approved: true` e `implemented: true`.
   - **Double-Check**:
     1. Verifique se o arquivo de teste apontado em `test_file` no frontmatter de `TESTS.md` realmente existe em `tests/`.
     2. Rode `uv run pytest` antes de tocar no código: a suíte existente deve estar íntegra e apenas os testes TDD da spec atual devem estar falhando (fase *Red*). Se outros testes quebrarem ou houver erro de sintaxe nos testes, **PARE e avise o usuário**.
   - **Ação**: Leia e siga `.agents/skills/sdd-implementation/SKILL.md`.

6. **Concluído**:
   - `SPEC.md` possui `approved: true` e `implemented: true`, `TESTS.md` possui `approved: true` e `implemented: true`, e `uv run pytest` passa 100% (*Green*).

---

## 3. Isolamento de Contexto vs. Subagentes

- O fluxo padrão é rodar **uma etapa por conversa**: ao terminar uma etapa e obter a aprovação do usuário, atualize o frontmatter do arquivo correspondente e oriente o usuário a limpar o contexto (`/clear` ou `/compact`) antes de iniciar a próxima etapa.
- Caso o usuário peça explicitamente para rodar uma etapa em um subagente isolado sem sair da conversa atual, use a ferramenta `invoke_subagent` (`TypeName: "self"`), instruindo o subagente a carregar a skill específica da etapa (`sdd-ideation`, `sdd-ui-mock`, `sdd-planning`, `sdd-tdd` ou `sdd-implementation`).
