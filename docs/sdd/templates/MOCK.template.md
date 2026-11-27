# Modelo de Documento: `referencias/MOCK.md` (Etapa 1.5 Opcional — Mock Visual / UI)

> **Regras deste Modelo**:
> - **Quando usar**: Obrigatório sempre que `referencias/IDEACAO.md` tiver `requires_ui_mock: true` (qualquer entrega que altere UI, temas GTK3, painel XFCE, bordas de janelas `xfwm4`, cores, fontes ou elementos visuais).
> - **Onde salvar**: `specs/<epico>/<NN_nome_da_spec>/referencias/MOCK.md` (acompanhado do arquivo visual `specs/<epico>/<NN_nome_da_spec>/referencias/mock.html`).
> - **Integração com o Atomic Design System (`design_system/`)**:
>   1. **Consulta Prévia**: Antes de criar o `mock.html`, consulte `design_system/css/design-system.css` e reutilize os Tokens (`--ds-*`), Átomos (`.ds-atom-*`), Moléculas (`.ds-mol-*`) e Organismos (`.ds-org-*`) existentes.
>   2. **Importação no `mock.html`**: O `mock.html` deve importar `<link rel="stylesheet" href="../../../../design_system/css/design-system.css" />` para funcionar no Live Server.
>   3. **Promoção ao Portfólio**: Após a aprovação (`approved: true`), todo novo token, átomo, molécula e organismo aprovado sobe para `design_system/css/design-system.css` e para os showcases `design_system/{tokens,atoms,molecules,organisms}.html`.
> - **Frontmatter Obrigatório**: O bloco YAML no topo com `epic`, `spec`, `type: "ui_mock"`, `mock_html`, `target_subsystems`, `approved` e `implemented` é estrito e obrigatório.

```markdown
---
epic: "<nome_do_epico>"
spec: "<NN_nome_da_spec>"
type: "ui_mock"
mock_html: "referencias/mock.html"
target_subsystems: ["gtk3-css", "xfce4-panel", "xfwm4"]
approved: false
implemented: false
---

# Mock Visual, Atomic Design & Guia de Portabilidade: <Título da Entrega>

## 1. Arquivo de Preview Visual & Inventário Atomic Design
- **Mock HTML (Live Server)**: `specs/<epico>/<NN_nome_da_spec>/referencias/mock.html` (importa `design_system/css/design-system.css`)
- **Tokens, Átomos e Moléculas Reutilizados de `design_system/`**:
  - **Tokens**: `<Ex: --ds-bg-surface, --ds-fg-primary, --ds-accent-primary, --ds-font-sans>`
  - **Átomos / Moléculas**: `<Ex: .ds-atom-btn, .ds-atom-win-ctrl, .ds-mol-xfwm-titlebar>`
- **Novos Componentes a Promover para o `design_system/`**:
  - **Novos Tokens (`tokens.html`)**: `<Nenhum ou lista de novos --ds-*>`
  - **Novos Átomos (`atoms.html`)**: `<Nenhum ou lista de novos .ds-atom-*>`
  - **Novas Moléculas (`molecules.html`)**: `<Nenhum ou lista de novas .ds-mol-*>`
  - **Organismo Final (`organisms.html`)**: `<Ex: .ds-org-xfce-panel / .ds-org-window exibindo o resultado real completo>`

## 2. Paleta e Tokens Visuais (1:1 com OS)
| Token (`design-system.css`) | Valor (`#hex` / `rgba`) | Destino no `gtk.css` (`@define-color`) | Destino no `xfwm4` (`themerc` / `.xpm`) |
| :--- | :--- | :--- | :--- |
| `--ds-bg-surface` | `#1e1e2e` | `@define-color bg_surface #1e1e2e;` | Cor base nos `.xpm` (`title-1..5-active.xpm`) |
| `--ds-fg-primary` | `#cdd6f4` | `@define-color fg_primary #cdd6f4;` | `active_text_color=#cdd6f4` no `themerc` |
| `--ds-accent-primary` | `#89b4fa` | `@define-color accent_primary #89b4fa;` | Borda lateral/inferior nos `.xpm` ativos |

## 3. Checklist de Guardrails (Validação de Realismo GTK3 / XFCE)
- [x] **Sem `backdrop-filter` / `filter: blur()` / `mix-blend-mode`**: Usado apenas `#hex` sólido ou `rgba()` puro compatível com `GtkCssProvider`.
- [x] **Sem `transform` (`scale`, `rotate`, `translate`)**: Efeitos de interação usam apenas troca de `background-color`, `border-color`, `color` ou `box-shadow: inset`.
- [x] **Geometria estática em `:hover` / `:focus`**: `padding` e `border-width` não mudam em hover, evitando *layout jitter* nos containers nativos do GTK3.
- [x] **Separação Estrita `xfwm4` vs. `gtk.css`**: Bordas e barras de título do `xfwm4` usam geometria retangular e cores sólidas portáveis para `themerc` + slices `.xpm`.
- [x] **Foco em Performance/Bateria**: Sem `@keyframes` contínuos ou sombras multicamadas pesadas.

## 4. Mapa de Portabilidade (Mock CSS -> Sistema Operacional)
| Seletor no `mock.html` | Arquivo Alvo no OS (`TARGET_HOME`) | Seletor / Propriedade Nativa Equivalente | Ajustes na Conversão |
| :--- | :--- | :--- | :--- |
| `.mock-panel` | `.config/gtk-3.0/gtk.css` | `.xfce4-panel, .xfce4-panel.background` | Trocar `height` por `min-height`; converter `var(--x)` para `@x` |
| `.mock-panel-btn:hover` | `.config/gtk-3.0/gtk.css` | `.xfce4-panel button:hover` | Manter `border-radius`, `background-color` e `color` |
| `.mock-xfwm4-frame.active` | `.themes/<Tema>/xfwm4/themerc` + `*.xpm` | `active_text_color`, `button_offset`, `title-*-active.xpm` | Gerar slices `.xpm` com a largura de borda e cor definidas |
| `.mock-window.is-backdrop` | `.config/gtk-3.0/gtk.css` / `xfwm4` | `:backdrop` / `*-inactive.xpm` | Aplicar paleta inativa |
```
