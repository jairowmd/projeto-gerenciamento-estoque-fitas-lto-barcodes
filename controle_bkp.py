
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

def excluir():
    """
    Exclui o registro selecionado na lista do banco de dados.

    Obtém o id do registro selecionado na lista, busca os dados desse registro no banco de dados e exclui o registro com o id correspondente.
    
    """

    remover = lista.tableWidget.currentRow()
    # Obtém o índice da linha selecionada na tabela da janela de lista

    lista.tableWidget.removeRow(remover)
    # Remove a linha selecionada da tabela

    cursor = conexao.cursor()
    # Cria um cursor para interagir com o banco de dados

    cursor.execute("SELECT id FROM produtos_bkp")
    # Executa uma consulta SQL para obter todos os ids do banco de dados

    leitura_banco = cursor.fetchall()
    # Fetcha todos os ids do banco de dados

    valor_id = leitura_banco[remover][0]
    # Obtém o valor do id do registro selecionado na lista

    cursor.execute("DELETE FROM produtos_bkp WHERE id = " + str(valor_id))
    # Executa uma consulta SQL para excluir o registro com o id correspondente

    conexao.commit()
    # Confirma a alteração no banco de dados

def editar():
    """
    Abre a janela de edição com os dados do registro selecionado na lista.

    Obtém o id do registro selecionado na lista, busca os dados desse registro no banco de dados e preenche a janela de edição com esses dados.

    """

    global numero_id

    dados = lista.tableWidget.currentRow()
    # Obtém o índice da linha selecionada na tabela da janela de lista

    cursor = conexao.cursor()
    # Cria um cursor para interagir com o banco de dados

    cursor.execute("SELECT id FROM produtos_bkp")
    # Executa uma consulta SQL para obter todos os ids do banco de dados

    leitura_banco = cursor.fetchall()
    # Fetcha todos os ids do banco de dados

    valor_id = leitura_banco[dados][0]
    # Obtém o valor do id do registro selecionado na lista

    cursor.execute("SELECT * FROM produtos_bkp WHERE id =" + str(valor_id))
    # Executa uma consulta SQL para obter todos os dados do registro com o id correspondente

    leitura_banco = cursor.fetchall()
    # Fetcha todos os dados do registro com o id correspondente

    editar.show()
    # Mostra a janela de edição

    numero_id = valor_id
    # Define o número do id do registro selecionado na lista

    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarProduto.setText(str(leitura_banco[0][1]))
    editar.txtAlterarLocalArmazenamento.setText(str(leitura_banco[0][2]))
    editar.txtAlterarEstoque.setText(str(leitura_banco[0][3]))
    editar.txtAlterarNf.setText(str(leitura_banco[0][4]))
    editar.txtAlterarDescricao.setText(str(leitura_banco[0][5]))
    # Preenche os campos de texto da janela de edição com os dados do registro


def salvar_dados():
    """
    Salva as alterações feitas na janela de edição e fecha as janelas de edição e lista.

    Obtém os valores digitados nos campos de texto da janela de edição, executa uma consulta SQL para atualizar o registro com o id correspondente no banco de dados, fecha as janelas de edição e lista e abre a janela do formulário.

    """

    global numero_id
    # Define o número do id do registro

    id = editar.txtAlterarId.text()
    produto = editar.txtAlterarProduto.text()
    localarmazenamento = editar.txtAlterarLocalArmazenamento.text()
    estoque = editar.txtAlterarEstoque.text()
    nf = editar.txtAlterarNf.text()
    descricao = editar.txtAlterarDescricao.text()
    # Obtém os valores digitados nos campos de texto da janela de edição

    cursor = conexao.cursor()
    # Cria um cursor para interagir com o banco de dados

    cursor.execute("UPDATE produtos_bkp SET id = '{}', produto = '{}', armazenamento = '{}', estoque = '{}', nf = '{}', descricao = '{}' WHERE id={}".format(id, produto, localarmazenamento, estoque, nf, descricao, numero_id))
   # Executa uma consulta SQL para atualizar o registro com o id correspondente no banco de dados

    editar.close()
    # Fecha a janela de edição

    lista.close()
    # Fecha a janela de lista

    formulario.show()
    # Mostra a janela do formulário

    conexao.commit()
    # Confirma a alteração no banco de dados

def lista():
    """
    Mostra a lista de todos os registros do banco de dados.

    Abre a janela com a lista de todos os registros do banco de dados. O 
    conteúdo da lista é lido do banco de dados com uma consulta SQL e 
    preenchido na tabela.
    """

    lista.show()
    # Mostra a janela com a lista

    cursor = conexao.cursor()
    # Cria um cursor para interagir com o banco de dados

    comando_SQL = "SELECT * FROM produtos_bkp"
    # Comando SQL para selecionar todos os registros da tabela

    cursor.execute(comando_SQL)
    # Executa o comando SQL

    leitura_banco = cursor.fetchall()
    # Fetcha todos os registros da tabela

    lista.tableWidget.setRowCount(len(leitura_banco))
    # Define o número de linhas na tabela

    lista.tableWidget.setColumnCount(6)
    # Define o número de colunas na tabela

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
    
    produto = formulario.txtProduto.text()
    localarmazenamento = formulario.txtLocalArmazenamento.text()
    estoque = formulario.txtEstoque.text()
    nf = formulario.txtNf.text()
    descricao = formulario.txtDescricao.text()
    # Obtém os valores digitados no formulário
    
    
    cursor = conexao.cursor()
    # Cria um cursor para executar um comando SQL

    comando_SQL = "INSERT INTO produtos_bkp (produto, armazenamento, estoque, nf, descricao) VALUES (%s, %s, %s, %s, %s)" 
    # Comando SQL para inserir um novo registro

    
    dados = (str(produto), str(localarmazenamento), str(estoque), str(nf), str(descricao))
    # Dados a serem inseridos

    
    cursor.execute(comando_SQL, dados)
    # Executa o comando SQL

    
    conexao.commit()
    # Confirma a alteração no banco de dados


    formulario.txtProduto.setText('')
    formulario.txtLocalArmazenamento.setText('')
    formulario.txtEstoque.setText('')
    formulario.txtNf.setText('')
    formulario.txtDescricao.setText('')
    formulario.lblConfirmacao.setText('Dados Inseridos com sucesso!')
    # Limpa os campos do formulário




app = QtWidgets.QApplication([])
# Cria uma instancia da aplica o Qt. O argumento '[]' pode ser usado para passar argumentos de linha de comando.

formulario = uic.loadUi('formulario_bkp.ui')
# Carrega a interface do usu rio a partir do arquivo 'formulario.ui' criado no Qt Designer.

formulario.btnCadastrar.clicked.connect(inserir)
# Associa o evento de clique do botão 'btnCadastrar' ao evento 'inserir'

formulario.btnRelatorio.clicked.connect(lista)
# Associa o evento de clique do botão 'btnCadastrar' ao evento 'inserir' e ao evento 'close' da janela do formulario.

lista = uic.loadUi('lista_bkp.ui')
# Carrega a interface do usuario a partir do arquivo 'lista.ui' criado no Qt Designer.

lista.btnAlterar.clicked.connect(editar)    
# Associa o evento de clique do botão 'btnAlterar' ao evento 'editar'

lista.btnDeletar.clicked.connect(excluir)    
# Associa o evento de clique do botão 'btnDeletar' ao evento 'excluir'

editar = uic.loadUi('editar_bkp.ui')
# Carrega a interface do usuario a partir do arquivo 'editar.ui' criado no Qt Designer.

editar.btnConfirmar.clicked.connect(salvar_dados)    
# Associa o evento de clique do botão 'btnConfirmar' ao evento 'salvar_dados'

formulario.show()
# Mostra a janela do formulario.

app.exec()
# Executa a aplica o, fazendo com que o loop de eventos seja executado.
