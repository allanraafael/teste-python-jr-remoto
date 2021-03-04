# Teste Técnico Desenvolvedor(a) Python Júnior [REMOTO]

Minha solução auxilia a Vough na conferência de seus clientes do meio open source.



Para executar o projeto:

1- instale as dependências

```shell script
> pipenv install
```

2- Crie um banco de dados no postgres com nome db_vough

3- Crie um arquivo .env no diretório raiz do projeto copie e cole e atribua as variáveis com suas credenciais:

> ##### SECRET_KEY=123
> ##### DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/db_vough

4- Execute as migrações

```shell script
> python manage.py migrate
```

5- Execute o projeto
```shell script
> python manage.py runserver
```

6- Para executar os testes execute

```shell script
> k6 run -e API_BASE='http://localhost:8000/' tests-open.js
```

```shell script
> python manage.py test
```
