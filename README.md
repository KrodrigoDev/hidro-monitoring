## 📁 Estrutura do Projeto

```
📦 nome-do-projeto
├── app.py
├── LICENSE
├── README.md
├── requirements.txt
├── .env
│
├── src/
│   ├── model/
│   │   ├── bomba_model.py
│   │   ├── login_model.py
│   │   └── shp/
│   │       ├── *.shp
│   │       ├── *.shx
│   │       ├── *.dbf
│   │       └── *.prj
│   │
│   ├── utils/
│   │   ├── components.py
│   │   └── sidebar.py
│   │
│   └── view/
│       ├── card.py
│       └── mapa.py
│
├── pages/
│   ├── 1_dashboard.py
│   ├── 2_registrar_equipamento.py
│   ├── 3_historico.py
│   └── login.py
│
├── assets/
│   └── style.css
├── image/
└── .streamlit/
    └── config.toml
```

---

## 🧩 Descrição das Pastas e Arquivos

| Caminho                            | Descrição                                                                                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **app.py**                         | Arquivo principal do Streamlit. Gerencia a navegação entre páginas e importa os módulos necessários.                                                    |
| **.env**                           | Contém variáveis de ambiente, incluindo a URL com os dados consumidos pelo `bomba_model.py`. Deve ser carregado pelo projeto (ex: via `python-dotenv`). |
| **src/model/**                     | Lógica de negócio e dados.                                                                                                                              |
| ├── **bomba_model.py**             | Modelo de dados das bombas, consome dados da URL definida em `.env`.                                                                                    |
| ├── **login_model.py**             | Autenticação e gerenciamento de usuários.                                                                                                               |
| └── **shp/**                       | Contém shapefiles usados na aplicação (`.shp`, `.shx`, `.dbf`, `.prj`).                                                                                 |
| **src/utils/**                     | Funções auxiliares e componentes reutilizáveis.                                                                                                         |
| ├── **components.py**              | Carrega componentes visuais customizados.                                                                                                               |
| └── **sidebar.py**                 | Funções e lógica da sidebar do Streamlit.                                                                                                               |
| **src/view/**                      | Elementos de visualização da aplicação.                                                                                                                 |
| ├── **card.py**                    | Componentes de card para dashboards.                                                                                                                    |
| └── **mapa.py**                    | Funções e componentes para exibição de mapas.                                                                                                           |
| **pages/**                         | Páginas multipage do Streamlit.                                                                                                                         |
| ├── **1_dashboard.py**             | Dashboard principal.                                                                                                                                    |
| ├── **2_registrar_equipamento.py** | Registro de equipamentos.                                                                                                                               |
| ├── **3_historico.py**             | Histórico de registros/ações.                                                                                                                           |
| └── **login.py**                   | Tela de login de usuários.                                                                                                                              |
| **assets/**                        | Arquivos estáticos (CSS, ícones, fontes, etc.).                                                                                                         |
| └── **style.css**                  | Estilos customizados para a interface.                                                                                                                  |
| **image/**                         | Imagens usadas na interface ou documentação.                                                                                                            |
| **.streamlit/**                    | Configurações do Streamlit.                                                                                                                             |
| └── **config.toml**                | Configurações de tema, layout e autenticação.                                                                                                           |

---

## ⚙️ Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto:

```
URL_DATAFRAME=https://exemplo.com/dados/bombas.csv
```

---

## ⚡ Execução do Projeto

#### 1️⃣ Criar e ativar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
```

#### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

#### 3️⃣ Rodar o aplicativo
```bash
streamlit run app.py
```
