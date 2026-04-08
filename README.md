# MVP Loja Backend - PUC-Rio

## Descrição do Projeto
Esta é uma API REST desenvolvida em Python com FastAPI para o Produto Mínimo Viável (MVP) da disciplina de Desenvolvimento Back-end Avançado da PUC-Rio. O sistema atua no **Cenário 1.1**, servindo como o Back-End de uma aplicação de loja online. Ele é responsável por gerenciar a autenticação dos usuários (via JWT), persistir os dados em um banco SQLite e consumir dados de produtos através de uma API externa de terceiros.

## API Externa Utilizada
Este projeto consome a **FakeStore API** para a listagem de produtos.
* **Serviço:** FakeStore API
* **Documentação:** https://fakestoreapi.com/docs
* **Licença/Uso:** API pública e gratuita, sem necessidade de cadastro ou tokens de autenticação.
* **Rotas utilizadas:** `GET https://fakestoreapi.com/products`

## Tecnologias Utilizadas
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI
* **Banco de Dados:** SQLite + SQLAlchemy
* **Autenticação:** JWT (JSON Web Tokens) e Bcrypt
* **Conteinerização:** Docker

## Instruções de Instalação e Execução

### Opção 1: Execução local (Ambiente Virtual)

1. Clone o repositório:
```bash
git clone https://github.com/kleysongomes/mvp-loja-backend-puc-rio.git
cd mvp-loja-backend-puc-rio
```

2. Crie e ative o ambiente virtual:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python run.py
```

---

### Opção 2: Execução via Docker

Certifique-se de ter o Docker instalado e em execução na sua máquina.

1. Construa a imagem Docker:
```bash
docker build -t mvp-backend-loja .
```

2. Execute o contêiner:
```bash
docker run -d -p 8000:8000 --name meu-backend mvp-backend-loja
```

---

## Acesso à Documentação da API (Swagger)

Com a aplicação em execução (local ou via Docker), acesse o link abaixo no seu navegador para interagir com a documentação do Swagger e testar as rotas disponíveis:

**URL:** http://127.0.0.1:8000/docs

