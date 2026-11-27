# Atomic Design System (`design_system/`) — Tema Mint Leve

Esta pasta contém o **Design System vivo e navegável** do projeto `tema_mint_leve`, estruturado segundo os princípios do **Atomic Design** e restrito aos **Guardrails de compatibilidade com GTK3 (`GtkCssProvider`) e XFCE (`xfwm4` / `xfce4-panel`)**.

## Como Visualizar (Live Server)

Abra qualquer um dos arquivos HTML abaixo usando a extensão **Live Server** (ou diretamente no navegador). Todas as páginas possuem uma barra de navegação superior que permite transitar entre as camadas do Atomic Design:

- **[index.html](index.html)**: Visão geral da arquitetura visual e regras do fluxo SDD + Atomic Design.
- **[tokens.html](tokens.html)**: **Nível 0 (Tokens)** — Paleta de cores centralizada (`:root`), tipografia compatível com Pango e medidas de bordas com mapeamento 1:1 para `@define-color` no `gtk.css` e `themerc` no `xfwm4`.
- **[atoms.html](atoms.html)**: **Nível 1 (Átomos)** — Elementos indivisíveis (botões GTK3, inputs `entry`, controles de janela `xfwm4`, badges, switches e separadores), com snippet, quando usar e seletor de destino no OS.
- **[molecules.html](molecules.html)**: **Nível 2 (Moléculas)** — Combinações funcionais de átomos (barra de título `xfwm4` ativa/inativa, grupo Whisker Menu + Workspaces, itens de Tasklist, Systray + Relógio e notificações `xfce4-notifyd`).
- **[organisms.html](organisms.html)**: **Nível 3 (Organismos)** — Showcase completo das interfaces geradas no sistema (Painel XFCE integrado, Janela ativa de terminal, Janela inativa `:backdrop` com widgets GTK3).
- **[css/design-system.css](css/design-system.css)**: Folha de estilo centralizada que alimenta tanto este portfólio quanto os mocks de cada spec (`specs/<epico>/<spec>/referencias/mock.html`).

---

## Regra de Ouro no Fluxo SDD

1. **Consulta Prévia Obrigatória (Antes do Mock)**:
   - Sempre que uma spec tiver `requires_ui_mock: true`, o agente `sdd-ui-mock` **DEVE** inspecionar `design_system/css/design-system.css` e os HTMLs desta pasta **antes** de criar `referencias/mock.html`.
   - O `mock.html` da spec deve importar `../../../../design_system/css/design-system.css` para reutilizar a fonte, a paleta de cores (`--ds-*`), os átomos (`.ds-atom-*`) e as moléculas (`.ds-mol-*`) existentes, criando CSS novo apenas para o que for inédito na spec.
2. **Promoção Obrigatória ao Design System (Após Aprovação e Implementação)**:
   - Sempre que um mock visual for aprovado e portado para os arquivos reais do sistema (`gtk.css`, `themerc`, `.xpm`, etc.), os novos tokens, átomos, moléculas e o **organismo final** devem ser promovidos para `design_system/css/design-system.css` e adicionados em `tokens.html`, `atoms.html`, `molecules.html` e `organisms.html`.
