## 📁 Estrutura  do Projeto

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
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── models.py
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
├── migrations/
│   ├── versions/
│   │   └── <arquivos_de_migration>.py
│   └── env.py
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

| Caminho               | Descrição                                                                     |
| --------------------- | ----------------------------------------------------------------------------- |
| **app.py**            | Arquivo principal do Streamlit. Gerencia a navegação entre páginas.           |
| **src/model/**        | Contém toda a lógica de banco de dados e CRUD.                                |
| ├── **crud.py**       | Funções de Create, Read, Update, Delete para usuários, equipamentos e locais. |
| ├── **database.py**   | Configuração do SQLAlchemy e engine do banco SQLite.                          |
| ├── **init_db.py**    | Script para criar tabelas iniciais e popular dados padrão (usuário/empresa).  |
| ├── **models.py**     | Models ORM para SQLAlchemy: Empresa, Usuario, LocalEquipamento, Equipamento.  |
| └── **shp/**          | Shapefiles usados no mapa.                                                    |
| **src/utils/**        | Funções auxiliares e componentes reutilizáveis.                               |
| ├── **components.py** | Componentes customizados (ex: cards).                                         |
| └── **sidebar.py**    | Funções da barra lateral do Streamlit.                                        |
| **src/view/**         | Elementos de visualização.                                                    |
| ├── **card.py**       | Componentes de card para dashboards.                                          |
| └── **mapa.py**       | Funções e componentes para exibição de mapas.                                 |
| **migrations/**       | Diretório do Alembic para versionamento do banco.                             |
| **pages/**            | Páginas multipage do Streamlit.                                               |
| **assets/**           | Arquivos estáticos (CSS, ícones, fontes, etc.).                               |
| **image/**            | Imagens usadas na interface ou documentação.                                  |
| **.streamlit/**       | Configurações do Streamlit.                                                   |

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

#### 3️⃣ Aplicar migrations do banco

```bash
alembic upgrade head
```

> Isso criará todas as tabelas do banco conforme definido nas migrations.

#### 4️⃣ Inicializar banco com dados padrão

```bash
python src/model/init_db.py
```

> Esse passo cria o usuário admin e a empresa padrão, garantindo que você já possa logar no sistema.

#### 5️⃣ Rodar o aplicativo

```bash
streamlit run app.py
```
