# tasks-backend

Projeto de conclusão de curso de bacharel em sistemas de informação. Gerenciador de tarefas com priorização conforme
matriz de Eisenhower adaptada.

## Run

`flask --app server --debug run` para rodar um servidor que fica observando as alterações e printando o resultado.

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
make dev/server
```

## TODO

- Calcular a % de variação em relação ao defaul para todas as ocorrências, não somente nas que se sai melhor.