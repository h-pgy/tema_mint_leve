# Guia de Categorias, Módulos e Registry (`scripts/`)

Toda a lógica de instalação de pacotes, configuração do sistema operacional, ambiente de desenvolvimento e *rice* fica dentro de `scripts/`, dividida por **domínio**.

---

## 1. Divisão por Domínios (Categorias)

As categorias organizam os scripts por finalidade e formam o menu principal do CLI. Exemplos de categorias principais (novas categorias podem ser adicionadas livremente criando uma nova pasta com seu `registry` e `README.md`):

- **`os_config/`**: Ajustes do sistema operacional, kernel, otimização de bateria e performance para laptop antigo (ex: TLP/auto-cpufreq, ZRAM, `swappiness`, serviços do systemd).
- **`app_installers/`**: Instalação de dependências, ferramentas e aplicativos (ex: Docker, Pyenv, pacotes base via `apt`, utilitários de terminal, Flatpaks).
- **`dev_env/`**: Configurações de ferramentas de desenvolvimento separadas por tecnologia/editor (ex: `python/`, `vscode/`, `git/`).
- **`rice/`**: Customizações visuais e de usabilidade do Linux Mint XFCE (ex: temas leves, preferências de janelas do `xfwm4`, atalhos de teclado, painel, terminal).

---

## 2. Anatomia de uma Categoria e de um Módulo

Não existe uma pasta `assets/` global. Cada módulo é **autocontido** e guarda seus próprios arquivos de configuração, templates e scripts na sua própria subpasta:

```text
scripts/
└── rice/                                # Pasta da Categoria (Domínio)
    ├── README.md                        # Descrição da categoria (exibida no CLI)
    ├── registry.yaml                    # Registro dos módulos pertencentes a 'rice'
    │
    ├── xfce_light_theme/                # Módulo 1
    │   ├── README.md                    # Explica o que o módulo faz (exibido no CLI)
    │   ├── run.sh                       # Script principal do módulo
    │   └── assets/                      # Assets exclusivos deste módulo
    │       └── xsettings.xml
    │
    └── xfce_window_prefs/               # Módulo 2
        ├── README.md
        ├── run.py                       # Módulos também podem ser escritos em Python
        └── assets/
            └── xfwm4.xml
```

---

## 3. Regras para Escrever um Módulo (`run.sh` ou `run.py`)

1. **Sempre tenha um `README.md` curto e claro**:
   - O CLI lê esse arquivo para mostrar ao usuário o que aquele script instala ou altera antes de rodar.
2. **Use `TARGET_HOME` e `MODULE_ASSETS_DIR`**:
   - Nunca escreva `cp assets/arquivo ~/.config/...` com caminho fixo para `~`.
   - Use sempre `"$TARGET_HOME/.config/..."` e `"$MODULE_ASSETS_DIR/arquivo"`. Isso garante que o `pytest` consiga testar seu script em um diretório temporário sem sobrescrever a máquina real.
3. **Idempotência**:
   - Um script deve poder rodar duas vezes seguidas sem quebrar (use `mkdir -p`, verifique se um repositório/binário já existe antes de baixar novamente, faça backup ou substituição limpa).
4. **Declare `expected_files` no Registry**:
   - Sempre que o script criar ou atualizar arquivos de configuração (como `.env`, `.gitconfig`, configs do XFCE ou do VS Code), liste esses caminhos relativos ao `TARGET_HOME` em `expected_files` no `registry` da categoria.
