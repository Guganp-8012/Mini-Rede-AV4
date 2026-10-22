# Rede Social Simples

Piauí Instituto de Tecnologia – PIT
→ Trabalho final da disciplina de Algoritmos, Estruturas de Dados e Programação.
Professor: Joselito Mendes Sousa Júnior

## Descrição

O sistema simula uma rede social simples utilizando Python e SQLite, permitindo o gerenciamento de usuários e amizades com persistência de dados entre execuções.

## Funcionalidades

* Cadastro de usuários
* Remoção de usuários
* Criação de amizades
* Remoção de amizades
* Listagem de perfis
* Listagem de amigos

## Pré-requisitos

Antes de executar o projeto, é necessário possuir:

* Python 3.10 ou superior
* SQLite (já incluído na instalação padrão do Python)

Para verificar a versão do Python instalada:

```bash
python --version
```

## Como Executar

### Método 1 - Pelo Terminal

1. Abra um terminal na pasta do projeto.

No Windows, você pode:

* Abrir a pasta do projeto no Explorador de Arquivos.
* Clicar na barra de endereço.
* Digitar `cmd` e pressionar Enter.

2. Criar o banco de dados:

```bash
py init_db.py
```

3. Popular o banco com dados de exemplo (opcional):

```bash
py popular_banco.py
```

4. Executar o sistema:

```bash
py main.py
```

5. Executar os testes:

```bash
py teste_sistema.py
```

### Método 2 - Execução Direta

Após criar o banco de dados, localize o arquivo `main.py` e execute-o diretamente com um duplo clique (caso o Python esteja corretamente associado aos arquivos `.py`).

## Como Executar no VS Code

### Instalação do VS Code

Baixe e instale o Visual Studio Code.

### Extensões Recomendadas

* Python (Microsoft)
* SQLite Viewer (opcional, para visualizar o banco de dados)

### Executando o Projeto

1. Abra a pasta do projeto no VS Code.
2. Abra o arquivo `main.py`.
3. Clique em **Run Python File** ou pressione `Ctrl + F5`.

## Estrutura do Projeto

```text
usuario.py          -> Representa a entidade Usuário
database.py         -> Operações de acesso ao banco SQLite
rede.py             -> Camada intermediária entre interface e banco
init_db.py          -> Criação do banco de dados e tabelas
popular_banco.py    -> Inserção de dados de exemplo
teste_sistema.py    -> Testes básicos do sistema
main.py             -> Menu principal da aplicação
README.md           -> Documentação do projeto
```

## Exemplo de Uso

### Cadastro de usuário

```text
Username: joao123
Nome: João Silva
Idade: 20
```

### Criação de amizade

```text
Username 1: joao123
Username 2: maria456
```

### Listagem de perfis

```text
ID: 1 | Username: joao123 | Nome: João Silva | Idade: 20 | Amigos: 2
```

## Observações

* Os dados são armazenados em um banco SQLite para garantir persistência entre execuções.
* Ao remover um usuário, todas as amizades associadas também são removidas.
* O sistema foi desenvolvido utilizando Programação Orientada a Objetos e banco de dados relacional SQLite.

# Divisão do projeto

| Integrante | Participação |
|------------|------------------|
| Gustavo | 'main.py', 'rede.py', relatório e revisão geral do projeto |
| Pedro | 'database.py', 'init_db.py' |
| Vinícius | 'usuario.py', 'popular_banco.py', 'teste_sistema.py' e 'README' |

# Autores
 - Vinícius Fernandes Vieira
 - Pedro Malcon Cabral Silva
 - Gustavo Soares Lima Rios
