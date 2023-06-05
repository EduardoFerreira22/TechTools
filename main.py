
# Bibliotecas Usadas
import PySimpleGUI as sg
import csv
import pyodbc
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import pandas as pd
from tkinter import filedialog as fd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os


def salvar_dados(headings, data):
    # Get the file path from user input
    file_path = fd.asksaveasfilename(defaultextension=".csv", filetypes=[
                                     ("CSV Files", "*.csv"), ("PDF Files", "*.pdf")])
    if not file_path:
        return  # User cancelled save dialog

    # Salva o arquivo em CSV ou PDF
    if file_path.endswith('.csv'):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(headings)
            writer.writerows(data)
    elif file_path.endswith('.pdf'):
        # Cria o documento em pdf
        pdf = canvas.Canvas(file_path, pagesize=letter)
        # seleciona a font para o documento
        pdf.setFont("Helvetica", 8)
        # Escreve os dados no documento
        y = 280
        for heading in headings:
            pdf.drawString(40, y, heading)
            y += 15
        # write data to document
        y -= 20
        for row in data:
            x = 50
            for item in row:
                pdf.drawString(x, y, str(item))
                x += 100
            y -= 20
        # save document
        pdf.save()


def obter_versao_atual():
    # Lê a versão atual do programa do arquivo "version.txt"
    versao = os.path.join(os.path.dirname(
        __file__), 'version.txt')

    with open(versao, "r") as f:
        versao_atual = f.read().strip()

    return versao_atual


def tela_principal():
    import execut
    import utili
    import os
    import subprocess
    import psutil
    import re
    versao_atual = obter_versao_atual()

    sg.theme('Reddit')
    hostname = socket.gethostname()
    # Lista de servidores de banco de dados e seus apelidos
    servidores = {'mysqld.exe': 'MySQL', 'sqlservr.exe': 'SQL Server',
                  'fbserver.exe': 'Firebird Server', 'mongodb': 'MongoDB'}

    # Lista de processos encontrados
    processos = []

    # Percorre todos os processos em execução
    for proc in psutil.process_iter():
        try:
            # Obtém informações do processo
            pinfo = proc.as_dict(attrs=['pid', 'name'])

            # Verifica se o nome do processo corresponde a algum dos servidores de banco de dados
            for servidor in servidores:
                if re.search(servidor, pinfo['name'], re.IGNORECASE):
                    processos.append(servidores.get(servidor))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Remove duplicatas da lista de processos encontrados
    processos = list(set(processos))

    # Transforma a lista de processos encontrados em uma string
    processos_str = " - ".join(processos)

    # Layout da Tela Principal
    layout = [

        [sg.Button('IB Expert', font=('M Hei PRC', 10, 'bold'), size=10, button_color="#e69138", key='ib', pad=(15, 0)),
         sg.Button('Utilitarios', font=('M Hei PRC', 10, 'bold'),
                   size=10, button_color="#e69138", key='util', pad=(10, 0)),
         sg.Button('Portal Hiperador', font=('M Hei PRC', 10, 'bold'),
                   key='portal', button_color="#e69138", pad=(10, 0)),
         sg.Button('Hiper Gestão', key='hiper', font=(
             'M Hei PRC', 10, 'bold'), button_color="#e69138", pad=(10, 0)),
         sg.Button('CANCELAR', font=('Helvetica', 10, 'bold'), key='cancelar', button_color="#e32636", pad=(20, 0))],
        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],


        [sg.Text('Servidor:', font=("Helvetica", 12, "bold"), text_color='#ffffff',
                 background_color="#104e8b"), sg.Text('Ex: "Nome_computador\Instância"', font=('Helvetica 8'),
                                                      text_color="#f0ffff", background_color="#104e8b")],
        [sg.Text(f"Servers Ativos: ( {processos_str} )", background_color="#104e8b", font=(
            'New', 8, 'bold'), text_color="#ffbf00")],


        [sg.Input(default_text=(f"{hostname}\\"),
                  key='servidor', font=('Arial '), size=40),

         sg.Button('CONECTAR', font=('Helvetica', 10, 'bold'), button_color="#44ab4c", size=15)],


        [sg.Text('DATA_BASE', font=('Helvetica', 10, 'bold'), pad=(2),
                 text_color="#f0ffff", background_color="#104e8b"),
         sg.Text('LOGON', pad=(45, 0), font=('Helvetica', 10, 'bold'),
                 text_color="#f0ffff", background_color="#104e8b"),
         sg.Text('SENHA', pad=(5, 0), font=('Helvetica', 10, 'bold'),
                 text_color="#f0ffff", background_color="#104e8b"),
         sg.Text('SERVIDOR BD', pad=(45, 0), font=('Helvetica', 10, 'bold'), text_color="#f0ffff", background_color="#104e8b")],


        [sg.Input(size=15, key='BD', pad=(2)), sg.Input(size=10, key='user', pad=(20, 0)), sg.Input(size=10, key='senha'),
         sg.Combo(['MySQL', 'SQL Server', 'SQLite'], key='combo',
                  text_color='#e32636', size=12, pad=(15, 0)),
         sg.Checkbox('Autenticação \ndo Windows*', background_color="#104e8b",
                     font=('New', 9), key='autenti', text_color='#ffbf00', checkbox_color='#fcfcfc')],  # Combo de Seleção para que tipo de banco de dados
        [sg.Text('Para Bancos de Dados SQLite selecione o arquivo .db .', font=('New', 8, 'bold'),
                 text_color='#ffbf00', pad=(0, 0), background_color="#104e8b")],
        [sg.Input(key='arquivo', pad=(0, 0)), sg.FileBrowse(
            button_text='Selecionar', button_color="#e69138", font=('Helvetica', 10, 'bold'))],


        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],

        [sg.Text('Selecione o tipo de dados que deseja baixar:', font=("Helvetica", 10, "bold"), text_color='#ffffff',
                 background_color="#104e8b")],
        # [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],

        [sg.Checkbox('CLIENTES*', background_color="#104e8b",
                     font=('Arial', 10, 'bold'), key='clientes', checkbox_color='#fcfcfc', pad=(15, 10)),
         sg.Checkbox('FORNECEDORES*', background_color="#104e8b",
                     font=('Arial', 10, 'bold'), key='fornecedor', checkbox_color='#fcfcfc', pad=(40, 10)),
         sg.Checkbox('PRODUTOS*', background_color="#104e8b",
                     font=('Arial', 10, 'bold'), key='pd', checkbox_color='#fcfcfc')],


        [sg.Button('BAIXAR ARQUIVO CSV', key='csv', font=(
            'Helvetica', 10, 'bold'), button_color="#44ab4c", pad=(0, 0))],

        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],

        [sg.Text('Insira sua query abaixo:', font=('Helvetica', 14),
                 text_color='white', background_color="#104e8b")],

        [sg.Multiline(key='query', size=(100, 3),
                      background_color="#fcfcfc", text_color="#000000")],

        [sg.Button('EXECUTAR QUERY', size=15,  font=(
            'Helvetica', 10, 'bold'), button_color="#44ab4c"),
         sg.Button('MOSTRAR TABELAS', size=20,  font=(
             'Helvetica', 10, 'bold'), button_color="#44ab4c", key='tabelas')],
        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],


    ]
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'IMG.ico')
    # Cria a janela com o layout do programa
    janela = sg.Window((f"Tech_Tools Pro v{versao_atual}                                                          by: @eduardo_ferreira_22"), layout=layout, size=(600, 560), background_color="#104e8b", finalize=True,
                       icon=(icon_path))

    # Query's que serão responsáveis pelas consultas no banco de dados
    query_clientes = ("""SELECT
    DISTINCT
    CASE
    WHEN tipo_entidade = 1 THEN 'Pessoa física'
    WHEN tipo_entidade = 2 THEN 'Pessoa jurídica'
    WHEN tipo_entidade = 3 THEN 'Pessoa simplificada'
    END AS 'Tipo cliente',
    E.NOME,E.LOGRADOURO,E.NUMERO_ENDERECO,
	   E.BAIRRO,E.COMPLEMENTO,E.CEP,
	   E.FONE_PRIMARIO_DDD,E.FONE_PRIMARIO_NUMERO,
	   F.CPF,F.RG,J.CNPJ,J.IE,J.NOME_FANTASIA,
	   C.NOME AS CIDADE,C.UF	   
    FROM ENTIDADE E
    LEFT JOIN PESSOA_FISICA F
    ON E.ID_ENTIDADE = F.ID_ENTIDADE
    LEFT JOIN PESSOA_JURIDICA J
    ON E.ID_ENTIDADE = J.ID_ENTIDADE
    LEFT JOIN CIDADE C
    ON E.ID_CIDADE = C.ID_CIDADE
    ORDER BY  [Tipo cliente] DESC
    """)

    query_fornecedor = (""" SELECT
    t1.nome AS 'Nome fornecedor',
    CASE
    WHEN t3.ie <> '' THEN t3.ie
    WHEN t4.ie <> '' THEN t4.ie
    WHEN t3.ie = ' ' AND t1.tipo_entidade = 1 THEN 'Sem I.E'
    WHEN t4.ie = ' ' AND t1.tipo_entidade = 2 THEN 'Sem I.E'
    WHEN t1.tipo_entidade = 3 THEN 'Sem I.E'
    END AS 'Inscrição estadual',
    codigo AS 'Código',
    CASE
    WHEN fone_primario_ddd IS NOT NULL THEN '(' + fone_primario_ddd + ')' +' '+
    fone_primario_numero
    WHEN fone_secundario_ddd IS NOT NULL THEN '(' + fone_secundario_ddd + ')' +' '+
    fone_secundario_numero
    WHEN fone_secundario_ddd IS NULL AND fone_primario_ddd IS NULL THEN 'Sem telefone
    cadastrado'
    END AS 'Telefone',
    ISNULL(t2.nome + ' - ' + t2.uf, 'Sem cidade/UF cadastrada') AS 'Localidade',
    CASE
    WHEN t1.logradouro = '' THEN 'Sem logradouro cadastrado'
    WHEN t1.logradouro <> '' THEN t1.logradouro
    END AS 'Logradouro',
    CASE
    WHEN ISNUMERIC(t1.numero_endereco) = 0 THEN 'Sem número cadastrado'
    WHEN ISNUMERIC(t1.numero_endereco) = 1 THEN t1.numero_endereco
    END AS 'Número endereço',
    CASE
    WHEN t1.bairro = ' ' THEN 'Sem bairro cadastrado'
    WHEN t1.bairro <> '' THEN t1.bairro
    END AS 'Bairro',
    CASE
    WHEN tipo_entidade = 1 THEN t3.cpf + ' - ' +'CPF'
    WHEN tipo_entidade = 2 THEN t4.cnpj + ' - ' + 'CNPJ'
    WHEN tipo_entidade NOT IN (1,2) THEN 'Sem CPF ou CNPJ'
    END AS 'CPF/CNPJ',
    CASE
    WHEN flag_fornecedor = 1 THEN 'É fornecedor'
    END AS 'Tipo'
    FROM entidade t1
    LEFT JOIN cidade t2 ON t1.id_cidade = t2.id_cidade
    LEFT JOIN pessoa_fisica t3 ON t1.id_entidade = t3.id_entidade
    LEFT JOIN pessoa_juridica t4 ON t1.id_entidade = t4.id_entidade
    WHERE t1.flag_fornecedor = 1 AND t1.excluido = 0""")

    query_produtos = ("""SELECT
       t1.codigo,
    COALESCE(t2.codigo_barras, '') AS codigo_barras,
    t1.referencia_interna_produto,
       t1.nome AS nome_produto,
    t9.codigo AS codigo_fornecedor,
       t4.sigla as sigla_unidade_medida,
       t6.quantidade as Estoque,
       t1.preco_aquisicao AS precoFornecedor,
       t1.preco_custo AS preço_de_custo,
       t1.preco_minimo_venda,
       t1.preco_venda,
       t3.id_ncm AS NCM,
       isnull(cast(t5.id_situacao_tributaria_icms AS VARCHAR), '') AS Codigo_situacao_tributaria_ICMS,
       isnull(cast(t5.id_situacao_tributaria_simples_nacional AS VARCHAR), '') AS CSOSN,
       isnull(cast(t5.aliquota_icms AS VARCHAR), '') AS AliquotaICMS,
       isnull(cast(t5.percentual_reducao_base_icms AS VARCHAR), '') AS ReducaoICMS,
       isnull(cast(t5.mva AS VARCHAR), '') AS MVA
    FROM produto t1
       LEFT JOIN produto_sinonimo t2 ON t1.id_produto = t2.id_produto
       LEFT JOIN ncm t3 ON t1.id_ncm = t3.id_ncm
       LEFT JOIN unidade_medida t4 ON t1.id_unidade_medida = t4.id_unidade_medida
       LEFT JOIN regra_tributacao_icms_personalizada t5 ON t1.id_produto = t5.id_produto
       LEFT JOIN saldo_estoque t6 ON t1.id_produto = t6.id_produto
       LEFT JOIN entidade t9 ON t1.id_entidade_fornecedor = t9.id_entidade
    WHERE t1.codigo <> 1
       --GROUP BY t6.id_produto, t1.codigo, t2.codigo_barras, t1.referencia_interna_produto, t1.nome, t9.codigo, t4.sigla, t6.quantidade --t1.codigo, t2.codigo_barras, t1.referencia_interna_produto, t1.nome, t9.codigo, t4.sigla, t6.quantidade,
       ORDER BY t1.codigo""")

    # Cria o loop responsável por ler os eventos da tela
    while True:
        evento, valores = janela.read()  # WIN_CLOSE É O EVENTO DE CLICAR NO BOTÃO FECHAR
        if evento == sg.WIN_CLOSED or evento == 'cancelar':
            break

        # Dados

        if valores['combo'] == 'SQL Server' and evento == 'CONECTAR':
            servidor = valores['servidor'].strip()
            server = servidor
            database = valores['BD']
            username = valores['user']
            password = valores['senha']
            try:
                conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                                      ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

                # abre a conexão com o banco de dados
                cursor = conn.cursor()
                if cursor:
                    sg.popup('Conectado com sucesso!')
            except Exception as e:
                sg.popup_error(
                    f"Não foi possível conectar ao banco de dados! \n MOTIVO DO ERRO:" + str(e))

        if valores['combo'] == 'SQL Server' and evento == 'CONECTAR':
            if valores == 'autenti':
                servidor = valores['servidor'].strip()
                server = servidor
                database = valores['BD']
                try:
                    conn_str = f"Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;"
                    conn = pyodbc.connect(conn_str)
                    # abre a conexão com o banco de dados
                    cursor = conn.cursor()
                    if cursor:
                        sg.popup('Conectado com sucesso!')
                except Exception as e:
                    sg.popup_error(
                        f"Não foi possível conectar ao banco de dados! \n MOTIVO DO ERRO:" + str(e))

        if valores['combo'] == 'MySQL' and evento == 'CONECTAR':
            import mysql.connector

            try:
                # estabelece a conexão
                conn = mysql.connector.connect(
                    user=valores['user'],
                    password=valores['senha'],
                    host='localhost',
                    database=valores['BD']
                )

                # abre a conexão com o banco de dados
                cursor = conn.cursor()
                if cursor:
                    sg.popup('Conectado com sucesso!')
                else:
                    sg.popup_error(
                        'Não foi possível estabelecer uma conexão com o servidor.')

            except mysql.connector.Error as error:
                sg.popup_error(
                    f"Não foi possível conectar ao banco de dados! \n MOTIVO DO ERRO: {error}"
                )

        if valores['combo'] == 'MySQL' and evento == 'CONECTAR':
            # Define as configurações da conexão
            if valores == 'autenti':

                import mysql.connector
                from mysql.connector.constants import ClientFlag

                # Define o nome do banco de dados
                nome_banco = valores['DB']

                # Define as configurações de conexão
                config = {
                    'user': 'root',
                    'password': '',
                    'host': 'localhost',
                    'database': nome_banco,
                    'client_flags': [ClientFlag.LOCAL_FILES],
                    'auth_plugin': 'mysql_native_password',
                    'allow_local_infile': True,
                    'use_pure': False,
                    'buffered': True,
                    'get_warnings': True,
                    'raise_on_warnings': True
                }

                # Define a autenticação do Windows
                conn = pyodbc.connect(
                    'DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=localhost;DATABASE={nome_banco};Trusted_Connection=yes;')

                # Conecta ao MySQL
                cnx = mysql.connector.connect(**config)

                # Realiza uma consulta
                cursor = cnx.cursor()

                if cursor:
                    sg.popup('Conectado com sucesso!')
                else:
                    sg.popup_error(
                        'Não foi possível estabelecer uma conexão com o servidor.')

                cursor.close()
                cnx.close()
                conn.close()

        if valores['combo'] == 'SQLite' and evento == 'CONECTAR':
            import sqlite3
            sqlite = valores['arquivo']
            try:  # Conecta ao banco de dados SQLite
                conn = sqlite3.connect(sqlite)

                # Cria um cursor para executar consultas
                cursor = conn.cursor()
                if cursor:
                    sg.popup('Conectado com sucesso!')
                else:
                    sg.popup_error(
                        'Não foi possível estabelecer uma conexão com o servidor.')

            except mysql.connector.Error as error:
                sg.popup_error(
                    f"Não foi possível conectar ao banco de dados! \n MOTIVO DO ERRO: {error}"
                )

        # Executa as querys inseridas manualmente no Multline
        if evento == 'EXECUTAR QUERY':
            try:     # Função para executar a query e exibir os resultados em uma nova janela
                query = valores['query']
                cursor = conn.cursor()
                cursor.execute(query)
                data = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                df = pd.DataFrame.from_records(data, columns=columns)

                layout = [
                    [sg.Table(values=df.values.tolist(
                    ), headings=df.columns.tolist(), num_rows=min(30, len(df)), col_widths=min(5, len(df)), auto_size_columns=False)],
                    [sg.Button('Salvar', key='salvar', size=(15)), sg.Button(
                        'Fechar', button_color="#e32636", size=(15))]
                ]

                icon_path = os.path.join(os.path.dirname(
                    __file__), 'resources', 'IMG.ico')
                window = sg.Window('Resultado da Query', layout, size=(1000, 560), finalize=True,
                                   icon=(icon_path))

                while True:
                    event, _ = window.read()
                    if event in (sg.WIN_CLOSED, 'Fechar'):
                        break
                    elif event == 'salvar':
                        salvar_dados(df.columns.tolist(), df.values.tolist())

                conn.close()
                window.close()

            except Exception as e:
                sg.popup_error(f"Erro ao executar a query: {e}")

            # Obtém os Dados de clientes
        if valores['clientes'] and evento == 'csv':

            # Execulta a consulta e recupera os dados

            cursor.execute(query_clientes)
            linhas = cursor.fetchall()

            # Abre a caixa de diálogo para salvar o arquivo CSV
            # Tk().withdraw()  # Esconde a janela principal do tkinter
            filename = filedialog.asksaveasfile(defaultextension='.csv')

            # verifica se o usuário selecionou um arquivo
            if filename is not None:

                # obtém o arquivo escolhido
                nome_do_arquivo = filename.name

                # cria o objeto csv.writer
                with (open(nome_do_arquivo, 'w', newline='')) as f:

                    writer = csv.writer(f, delimiter=';')
                    # Escreve os cabeçalhos
                    writer.writerow(['TIPO', 'NOME', 'LOGRADOURO', 'NUMERO_ENDERECO', 'BAIRRO', 'COMPLEMENTO', 'CEP',
                                    'FONE_PRIMARIO_DDD', 'FONE_PRIMARIO_NUMERO', 'CPF', 'RG', 'CNPJ', 'IE', 'NOME_FANTASIA', 'CIDADE', 'UF'])
                    # Escreve os dados no arquivo CSV usando o método writerows
                    writer.writerows(linhas)
                    # Fecha o aquivo csv
                    filename.close()
                # Fecha a conexão
                conn.close()

        # Obtém os Dados de clientes

        if valores['fornecedor'] and evento == 'csv':

            # Execulta a consulta e recupera os dados
            # Execulta a consulta e recupera os dados

            # Execulta a consulta e recupera os dados

            cursor.execute(query_fornecedor)
            linhas = cursor.fetchall()

            # Abre a caixa de diálogo para salvar o arquivo CSV
            # Tk().withdraw()  # Esconde a janela principal do tkinter
            filename = filedialog.asksaveasfile(defaultextension='.csv')

            # verifica se o usuário selecionou um arquivo
            if filename is not None:

                # obtém o arquivo escolhido
                nome_do_arquivo = filename.name

                # cria o objeto csv.writer
                with (open(nome_do_arquivo, 'w', newline='')) as f:

                    writer = csv.writer(f, delimiter=';')
                    # Escreve os cabeçalhos
                    writer.writerow(['NOME_FORNECEDOR', 'INCRICAO_ESTADUAL', 'CODIGO', 'TELEFONE',
                                     'CIDADE', 'ENDERECO', 'NUMERO', 'BAIRRO', 'CPF/CNPJ', 'TIPO'])
                    # Escreve os dados no arquivo CSV usando o método writerows
                    writer.writerows(linhas)
                    # Fecha o aquivo csv
                    filename.close()
                    # Fecha a conexão
                conn.close()

        if valores['pd'] and evento == 'csv':

            # Execulta a consulta e recupera os dados

            cursor.execute(query_produtos)
            linhas = cursor.fetchall()

            # Abre a caixa de diálogo para salvar o arquivo CSV
            # Tk().withdraw()  # Esconde a janela principal do tkinter
            filename = filedialog.asksaveasfile(defaultextension='.csv')

            # verifica se o usuário selecionou um arquivo
            if filename is not None:

                # obtém o arquivo escolhido
                nome_do_arquivo = filename.name

                # cria o objeto csv.writer
                with (open(nome_do_arquivo, 'w', newline='')) as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(['CODIGO', 'CODIGO_BARRAS', 'REFERENCIA_INTERNA', 'NOME_PRODUTO', 'COD_FORNECEDOR', 'UN_MEDIDA', 'ESTOQUE', 'PRECO_FORNECEDOR',
                                    'PRECO_CUSTO', 'PRECO_MINIMO_VENDA', 'PRECO_VENDA', 'NCM', 'COD_SITUACAO T._ICM', 'CSOSN', 'ALICOTA_ICMS', 'REDUCAO_ICMS', 'MVA'])
                    # Escreve os dados no arquivo CSV usando o método writerows
                    writer.writerows(linhas)
                    # Fecha o aquivo csv
                    filename.close()
                # Fecha a conexão
                conn.close()

        # Todos os links e processos da tela principal do programa

        if evento == 'portal':
            sg.webbrowser.open('https://portal.hiper.com.br')
        if evento == 'hiper':
            sg.webbrowser.open('https://mundo-2021.hiper.com.br/#/login')

        if evento == 'ib':
            execut.ibexpress()

        if evento == 'util':
            utili.utilitarios()

        if evento == 'tabelas':
            if valores['combo'] == 'SQL Server':
                def conexao_sqlserver():
                    servidor = valores['servidor'].strip()
                    server = servidor
                    database = valores['BD']
                    username = valores['user']
                    password = valores['senha']
                    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                                          ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
                    cursor = conn.cursor()
                    cursor.execute(
                        f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_CATALOG='{database}'")
                    resultados = cursor.fetchall()
                    lista_tabelas = [tabela[0] for tabela in resultados]
                    conn.close()

                    # Concatenar os elementos da lista em uma string com formatação de tabela
                    tabela_formatada = '\n'.join(
                        [f'| {tabela} |' for tabela in lista_tabelas])

                    return tabela_formatada

                # Criar layout da janela
                layout = [
                    [sg.Button('Buscar tabelas', font=(
                        'Helvetica', 10, 'bold'), button_color="#e69138")],
                    [sg.Multiline('', size=(50, 15), font=(
                        'New', 9, 'bold'), key='-OUTPUT-')],
                    [sg.Button('Limpar', font=('Helvetica', 10, 'bold'), button_color="#e69138"),
                     sg.Button('Voltar', font=('Helvetica', 10, 'bold'), button_color="#e32636")]]

                icon_path = os.path.join(os.path.dirname(
                    __file__), 'resources', 'IMG.ico')
                # Criar janela
                window = sg.Window('Tabelas Disponíveis', layout,
                                   background_color="#104e8b", icon=(icon_path))

                # Loop de eventos
                while True:
                    event, values = window.read()
                    if event == sg.WINDOW_CLOSED or event == 'Voltar':
                        break
                    if event == 'Buscar tabelas':
                        tabelas = conexao_sqlserver()
                        window['-OUTPUT-'].update(tabelas)
                    if event == 'Limpar':
                        window['-OUTPUT-'].update('')

                        # Fechar janela
                window.close()

        if evento == 'tabelas':
            if valores['combo'] == 'MySQL':
                def conexao_mysql():
                    import mysql.connector
                    # estabelece a conexão
                    conn = mysql.connector.connect(
                        user=valores['user'],
                        password=valores['senha'],
                        host='localhost',
                        database=valores['BD']
                    )

                    cursor = conn.cursor()
                    cursor.execute('SHOW TABLES;')
                    resultados = cursor.fetchall()
                    lista_tabelas = [tabela[0] for tabela in resultados]
                    conn.close()

                    # Concatenar os elementos da lista em uma string com formatação de tabela
                    tabela_formatada = '\n'.join(
                        [f'| {tabela} |' for tabela in lista_tabelas])

                    return tabela_formatada

                # Criar layout da janela
                layout = [
                    [sg.Button('Buscar tabelas', font=(
                        'Helvetica', 10, 'bold'), button_color="#e69138")],
                    [sg.Multiline('', size=(50, 15), font=(
                        'New', 9, 'bold'), key='-OUTPUT-')],
                    [sg.Button('Limpar', font=('Helvetica', 10, 'bold'), button_color="#e69138"),
                     sg.Button('Voltar', font=('Helvetica', 10, 'bold'), button_color="#e32636")]]

                icon_path = os.path.join(os.path.dirname(
                    __file__), 'resources', 'IMG.ico')
                # Criar janela
                window = sg.Window('Tabelas Disponíveis', layout,
                                   background_color="#104e8b", icon=(icon_path))

                # Loop de eventos
                while True:
                    event, values = window.read()
                    if event == sg.WINDOW_CLOSED or event == 'Voltar':
                        break
                    if event == 'Buscar tabelas':
                        tabelas = conexao_mysql()
                        window['-OUTPUT-'].update(tabelas)
                    if event == 'Limpar':
                        window['-OUTPUT-'].update('')

                        # Fechar janela
                window.close()

        if evento == 'tabelas':
            if valores['combo'] == 'SQLite':
                def conexao_sqlite():
                    conn = sqlite3.connect(sqlite)

                    # Cria um cursor para executar consultas
                    cursor = conn.cursor()
                    cursor.execute(
                        f"SELECT name FROM sqlite_master WHERE type='table';")
                    resultados = cursor.fetchall()
                    lista_tabelas = [tabela[0] for tabela in resultados]
                    conn.close()

                    # Concatenar os elementos da lista em uma string com formatação de tabela
                    tabela_formatada = '\n'.join(
                        [f'| {tabela} |' for tabela in lista_tabelas])

                    return tabela_formatada

                # Criar layout da janela
                layout = [
                    [sg.Button('Buscar tabelas', font=(
                        'Helvetica', 10, 'bold'), button_color="#e69138")],
                    [sg.Multiline('', size=(50, 15), font=(
                        'New', 9, 'bold'), key='-OUTPUT-')],
                    [sg.Button('Limpar', font=('Helvetica', 10, 'bold'), button_color="#e69138"),
                     sg.Button('Voltar', font=('Helvetica', 10, 'bold'), button_color="#e32636")]]

                icon_path = os.path.join(os.path.dirname(
                    __file__), 'resources', 'IMG.ico')
                # Criar janela
                window = sg.Window('Tabelas Disponíveis', layout,
                                   background_color="#104e8b", icon=(icon_path))

                # Loop de eventos
                while True:
                    event, values = window.read()
                    if event == sg.WINDOW_CLOSED or event == 'Voltar':
                        break
                    if event == 'Buscar tabelas':
                        tabelas = conexao_sqlite()
                        window['-OUTPUT-'].update(tabelas)
                    if event == 'Limpar':
                        window['-OUTPUT-'].update('')

                        # Fechar janela
                window.close()

                janela.close()


tela_principal()
