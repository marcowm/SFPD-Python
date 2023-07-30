# [SFPD-Python]()
Sistema de filas para processamento de dados
Serviço em Python para executar a leitura da base inicial e popular a primeira fila de mensagens, atuando como um "producer", que terá as suas mensagens enviadas
lidas pelo backend em Java "subscriber / consumer".

## Inicialização rápida

## Comandos no Terminal

1. Instale o Python 3 à partir de [Python.org Official Page](https://www.python.org/downloads/).
2. Abra o Terminal ou editor visual como o vs code [Tutorial Configuração Python no VsCode](https://code.visualstudio.com/docs/python/python-tutorial)
3. Navegue para seu diretório do projeto
4. Execute no terminal: `Digite o comando python seguida do caminho para o arquivo de script assim: "python app.py" Então aperte ENTER do teclado, e é isso, caso use o editor vscode basta clicar em Run com as devidas variaveis de ambiente já setadas.`
6. E Finalmente teremos um servidor web em python rodando, somente aguardando as requisições do frontend para iniciar a leitura dos dados e alocar as mensagens na fila inicial.
