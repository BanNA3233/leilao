# 🔄 Sistema de Leilão Inverso - Cotações

![GitHub repo size](https://img.shields.io/github/repo-size/BanNA3233/leilao?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/BanNA3233/leilao?color=brightgreen)
![GitHub issues](https://img.shields.io/github/issues/BanNA3233/leilao)
![GitHub stars](https://img.shields.io/github/stars/BanNA3233/leilao?style=social)

---

## 📖 Visão Geral

O **Sistema de Leilão Inverso** é uma aplicação web onde **compradores solicitam cotações de produtos** e **vendedores competem oferecendo o menor preço**.  
Diferente de um leilão tradicional (onde vence o maior lance), aqui vence o **menor preço ofertado**.  

A plataforma é ideal para empresas ou indivíduos que desejam **reduzir custos em compras** por meio da competitividade entre fornecedores.

---

## ✨ Funcionalidades

- ✅ Cadastro/Login de compradores e vendedores  
- ✅ Comprador cria solicitações de cotações  
- ✅ Vendedores enviam lances com seus preços  
- ✅ Histórico de lances por cotação  
- ✅ Escolha automática do vencedor (menor lance)  
- ✅ Interface responsiva com **Bootstrap**  
- 🔜 Relatórios e comparativos de fornecedores  

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Flask](https://flask.palletsprojects.com/)  
- **Templates:** [Jinja2](https://jinja.palletsprojects.com/)  
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)  
- **Banco de Dados:** MySQL  
- **Frontend:** HTML5, CSS3, [Bootstrap](https://getbootstrap.com/)  

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.9+  
- MySQL rodando localmente ou remoto  
- Virtualenv (recomendado)  

### Passo a passo

```bash
# 1. Clonar o repositório
git clone git@github.com:BanNA3233/leilao.git

# 2. Acessar o diretório
cd leilao

# 3. Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Criar banco no MySQL
CREATE DATABASE leilao;

# 6. Configurar variáveis de ambiente
cp .env.example .env
# editar com usuário, senha e nome do banco

# 7. Rodar migrações (se houver)
flask db upgrade

# 8. Rodar servidor
flask run
```

---

## 📂 Estrutura do Projeto

```bash
leilao/
├── app/
│   ├── __init__.py      # Inicialização do Flask
│   ├── models.py        # Modelos com SQLAlchemy
│   ├── routes.py        # Rotas do sistema
│   ├── templates/       # Páginas HTML (Jinja2 + Bootstrap)
│   │   ├── base.html
│   │   ├── index.html
│   │   └── cotacao.html
│   ├── static/          # CSS, JS, imagens
│   │   ├── css/
│   │   └── js/
│   └── utils/           # Funções auxiliares
├── migrations/          # Controle de versões do banco
├── tests/               # Testes
├── requirements.txt     # Dependências
├── config.py            # Configurações do Flask/MySQL
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md            # Documentação
```

---

## 🎮 Exemplos de Uso

- **Criar cotação (comprador):**  
  Acesse `/nova-cotacao`, informe o produto, quantidade e prazo.  

- **Dar lance (vendedor):**  
  Acesse a página da cotação e insira seu preço.  

- **Encerramento automático:**  
  Quando o prazo expira, o sistema identifica o menor lance e registra o vencedor.  

---

## 🤝 Como Contribuir

1. Faça um *fork* do repositório  
2. Crie uma branch:  
   ```bash
   git checkout -b minha-feature
   ```
3. Faça suas alterações  
4. Commit:  
   ```bash
   git commit -m "Minha nova feature"
   ```
5. Push:  
   ```bash
   git push origin minha-feature
   ```
6. Abra um *pull request* 🚀  

---

## 📌 Roadmap Futuro

- [ ] Implementar lances em tempo real (WebSockets)  
- [ ] Envio de notificações (email/push)  
- [ ] Dashboard administrativo para compradores  
- [ ] API REST para integração com ERP  

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para mais detalhes.  

---

## 📧 Contato

- 👨‍💻 Autor: [BanNA3233](https://github.com/BanNA3233)  
- 📩 Email: rfr3233@gmail.com  
