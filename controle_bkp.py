
from dotenv import load_dotenv
# Importa a função 'load_dotenv' do módulo 'dotenv', que é usada para carregar variáveis de ambiente de um arquivo .env.

import os
# Importa o módulo 'os', que fornece uma maneira de usar funcionalidades dependentes do sistema operacional, como ler variáveis de ambiente.

from PyQt5 import uic, QtWidgets
# Importa os módulos 'uic' e 'QtWidgets' do PyQt5, usados para carregar a interface do usuário e criar widgets.

import pymysql
# Importa o módulo 'pymysql' para conectar-se a um banco de dados MySQL.

load_dotenv()
# Carrega as variáveis de ambiente a partir de um arquivo .env localizado na raiz do projeto. no arquivo .env

conexao = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)
# Cria uma conexão com o banco de dados MySQL utilizando as variáveis de ambiente carregadas do arquivo .env para obter o host, usuário, senha e nome do banco de dados.

numero_id = 0

def editar():
    """
    Abre a janela de edição com os dados do registro selecionado na lista.

    Obtém o id do registro selecionado na lista, busca os dados desse registro no banco de dados e preenche a janela de edição com esses dados.
    """

    global numero_id

    # Obtém o índice da linha selecionada na tabela da janela de lista
    dados = lista.tableWidget.currentRow()

    # Cria um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Executa uma consulta SQL para obter todos os ids do banco de dados
    cursor.execute("SELECT id FROM produtos_bkp")

    # Fetcha todos os ids do banco de dados
    leitura_banco = cursor.fetchall()

    # Obtém o valor do id do registro selecionado na lista
    valor_id = leitura_banco[dados][0]

    # Executa uma consulta SQL para obter todos os dados do registro com o id correspondente
    cursor.execute("SELECT * FROM produtos_bkp WHERE id =" + str(valor_id))

    # Fetcha todos os dados do registro com o id correspondente
    leitura_banco = cursor.fetchall()

    # Mostra a janela de edição
    editar.show()

    numero_id = valor_id

    # Preenche os campos de texto da janela de edição com os dados do registro
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarProduto.setText(str(leitura_banco[0][1]))
    editar.txtAlterarLocalArmazenamento.setText(str(leitura_banco[0][2]))
    editar.txtAlterarEstoque.setText(str(leitura_banco[0][3]))
    editar.txtAlterarNf.setText(str(leitura_banco[0][4]))
    editar.txtAlterarDescricao.setText(str(leitura_banco[0][5]))

def salvar_dados():
    
    global numero_id

    id = editar.txtAlterarId.text()
    produto = editar.txtAlterarProduto.text()
    localarmazenamento = editar.txtAlterarLocalArmazenamento.text()
    estoque = editar.txtAlterarEstoque.text()
    nf = editar.txtAlterarNf.text()
    descricao = editar.txtAlterarDescricao.text()


def lista():
    """
    Mostra a lista de todos os registros do banco de dados.

    Abre a janela com a lista de todos os registros do banco de dados. O 
    conteúdo da lista é lido do banco de dados com uma consulta SQL e 
    preenchido na tabela.
    """

    # Mostra a janela com a lista
    lista.show()

    # Cria um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Comando SQL para selecionar todos os registros da tabela
    comando_SQL = "SELECT * FROM produtos_bkp"

    # Executa o comando SQL
    cursor.execute(comando_SQL)

    # Fetcha todos os registros da tabela
    leitura_banco = cursor.fetchall()

    # Define o número de linhas na tabela
    lista.tableWidget.setRowCount(len(leitura_banco))

    # Define o número de colunas na tabela
    lista.tableWidget.setColumnCount(6)

    # Preenche a tabela com os registros
    for i in range(0, len(leitura_banco)):
        for j in range(0, 6):
            # Cria um item da tabela com o conteúdo do registro
            item_tabela = QtWidgets.QTableWidgetItem(str(leitura_banco[i][j]))

            # Adiciona o item à tabela
            lista.tableWidget.setItem(i, j, item_tabela)

def inserir():
    """
    Função para inserir um novo registro no banco de dados com as informações do formulário. - Funçao concluida

    """
    
    # Obtém os valores digitados no formulário
    produto = formulario.txtProduto.text()
    localarmazenamento = formulario.txtLocalArmazenamento.text()
    estoque = formulario.txtEstoque.text()
    nf = formulario.txtNf.text()
    descricao = formulario.txtDescricao.text()
    
    # Cria um cursor para executar um comando SQL
    cursor = conexao.cursor()
    
    # Comando SQL para inserir um novo registro
    comando_SQL = "INSERT INTO produtos_bkp (produto, armazenamento, estoque, nf, descricao) VALUES (%s, %s, %s, %s, %s)" 
    
    # Dados a serem inseridos
    dados = (str(produto), str(localarmazenamento), str(estoque), str(nf), str(descricao))
    
    # Executa o comando SQL
    cursor.execute(comando_SQL, dados)
    
    # Confirma a alteração no banco de dados
    conexao.commit()
    
    # Limpa os campos do formulário

    formulario.txtProduto.setText('')
    formulario.txtLocalArmazenamento.setText('')
    formulario.txtEstoque.setText('')
    formulario.txtNf.setText('')
    formulario.txtDescricao.setText('')
    formulario.lblConfirmacao.setText('Dados Inseridos com sucesso!')




app = QtWidgets.QApplication([])
# Cria uma instancia da aplica o Qt. O argumento '[]' pode ser usado para passar argumentos de linha de comando.

formulario = uic.loadUi('formulario_bkp.ui')
# Carrega a interface do usu rio a partir do arquivo 'formulario.ui' criado no Qt Designer.

formulario.btnCadastrar.clicked.connect(inserir)

formulario.btnRelatorio.clicked.connect(lista)
# Associa o evento de clique do botão 'btnCadastrar' ao evento 'inserir' e ao evento 'close' da janela do formulario.

lista = uic.loadUi('lista_bkp.ui')
# Carrega a interface do usuario a partir do arquivo 'lista.ui' criado no Qt Designer.

lista.btnAlterar.clicked.connect(editar)

editar = uic.loadUi('editar_bkp.ui')
# Carrega a interface do usuario a partir do arquivo 'editar.ui' criado no Qt Designer.

formulario.show()
# Mostra a janela do formulario.

app.exec()
# Executa a aplica o, fazendo com que o loop de eventos seja executado.
