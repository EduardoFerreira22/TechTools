import PySimpleGUI as sg
import webbrowser
import os
import psutil
import subprocess
from atualiza import verificar_atualizacoes


def utilitarios():

    sg.theme('Reddit')
    # dicionários de link
    links1 = {
        'Hiper.Setup': 'https://downloads.hiper.com.br/Hiper.Setup.exe',
        'E-Trade instalador': 'https://vrsystem.info/files/Install_ETrade.exe',
        'E-Trade versão stable': 'https://vrsystem.info/files/Stable_ETrade.exe',
        'Bancos de Dados dos Estados': 'https://drive.google.com/drive/folders/1hvI1N9nA7PSZx-5HV53qjzI7ekTcJcTf',

        'SQL Server 2014 + SSMS x86': 'https://download.microsoft.com/download/0/1/5/015567C0-E851-4AC6-964F-9BBA9B31D6BC/ExpressAndTools%2032BIT/SQLEXPRWT_x86_PTB.exe',
        'SQL Server 2014 + SSMS x64': 'https://download.microsoft.com/download/0/1/5/015567C0-E851-4AC6-964F-9BBA9B31D6BC/ExpressAndTools%2064BIT/SQLEXPRWT_x64_PTB.exe',
        'SQL Server® 2019 Express': 'https://www.microsoft.com/pt-br/download/confirmation.aspx?id=101064',



    }

    links = {

        # BEMATECH
        'Bematech MP-100S TH 32bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_100_SpoolerDrivers_x86_v4.4.0.3.rar',
        'Bematech MP-100S TH 64bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_100_SpoolerDrivers_x64_v4.4.0.3.rar',
        'Bematech MP-2800 TH 32 bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_2800_SpoolerDrivers_x86_v1.3.rar',
        'Bematech MP-2800 TH 64 bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_2800_SpoolerDrivers_x64_v1.3.rar',
        'Bematech MP-4200 TH 32 bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_4200_SpoolerDrivers_x86_v4.3.1.0.rar',
        'Bematech MP-4200 TH 64 bits': 'https://gbinfosistemas.com.br/atualiza/nv/Impressoras/Bematech_MP_4200_SpoolerDrivers_x64_v4.3.1.0.rar',
        # DARUMA
        'Diebold Todos os Drivers': 'https://dieboldnixdorf.com.br/wp-content/uploads/2021/04/4900c52a69e4dd711601380202f91e8b-1.zip',
        'Daruma DR-800': 'https://drive.google.com/drive/folders/17nZFyaAZsFN-Ub3-kaj2Qg6TSqaIDROf',
        # EPSON
        'Epson TM-T20': 'https://download.epson-biz.com/modules/pos/index.php?page=single_soft&cid=6888&scat=31&pcat=3',
        'Epson TM-T20X': 'https://ftp.epson.com/latin/drivers/pos/APD_601_T20X_WM.zip',
        'Epson TM-T70II': 'https://encr.pw/vhaRp',
        'Epson Térmica TM-T88VII': 'https://epson.com.br/Suporte/Ponto-de-venda/Impressoras-térmicas/Epson-TM-T88VII-Series/s/SPT_C31CJ57052',
        'Epson L375': 'https://ftp.epson.com/latin/drivers/inkjet/L375_Lite_LA.exe',
        'Epson L1250': 'https://ftp.epson.com/latin/drivers/inkjet/L1250_Lite_LA.exe',
        'Epson L3110': 'https://ftp.epson.com/latin/drivers/Multi/l3110/L3110_Lite_LA.exe',
        'Epson L3210': 'https://ftp.epson.com/latin/drivers/inkjet/L3210_Lite_LA.exe',
        'Epson L3250': 'https://ftp.epson.com/latin/drivers/inkjet/L3250_L3251_Lite_LA.exe',
        'Epson L3251': 'https://epson.com.br/c/Epson-L3251/s/SPT_C11CJ67302',
        'Epson L3252': 'https://www.epson.co.in/Support/Printers/All-In-One/L-Series/Epson-L3252/s/SPT_C11CJ67511',
        'Epson L4160': 'https://ftp.epson.com/latin/drivers/inkjet/L4160_Lite_LA.exe',
        'Epson L4260': 'https://ftp.epson.com/latin/drivers/inkjet/L4260_Lite_LA.exe',
        # ELGIN
        'Elgin i7/i9': 'https://www.elgin.com.br/assets/arquivos/imgCard_4ce638a5-22e5-4a0d-a820-0108152ced91_imgCard_3969ab8d-70ab-4b53-ac90-d84cc55ddd70_ELGIN%20i9%20Printer%20Driver_v-1.7.3.rar',

        # Impressoras HP
        'HP DeskJet 2774': 'https://arquivos.blogdainformatica.com.br/drivers/impressoras/hp/hp-deskjet-ink-2770/HPEasyStart-13.6.5-DJ2700_51_4_4865_1_Webpack.exe?md5=7Rcm0COquWIQHQax9e1pLA&expires=1681620578',
        'HP Ink Tank Wireless 416': 'https://ftp.ext.hp.com/pub/softlib/software13/printers/ITW410/Full_Webpack-45.4.2608-ITW410_Full_Webpack.exe',
        # ARQUIVOS DE INSTALAÇÃO
        'Samsung ML-2160': 'https://ftp.hp.com/pub/softlib/software13/printers/SS/SL-M3370FD/SamsungUniversalPrintDriver3.exe',
        # impressoras Xerox
        'Xerox Phaser 3020': 'https://www.support.xerox.com/pt-br/product/phaser-3020/downloads?language=pt_BR#',
        # Impressoras Zebra
        'Zebra Z800': 'https://www.zebra.com/br/pt/support-downloads/eula/unrestricted-eula.7b8a235653193b4c72c440110c25661656f56f5180957c98e7c0bc2144149cd156a1bc6e684725abae8eaa3b64ee1090a63134434792cf7fe7ebd953120a60cd367633fe9f513f4ae43f722b47f328b04e84f768a150ebe0.html#',

        # Impressoras de Etiquetas
        'Argox All Driver': 'https://drive.google.com/uc?id=134HjCgrHHWQ9CArgcSUUowsK0H3nrxR6&export=download',
        'Elgin L42 PRO FULL': 'https://l1nq.com/N6Ju1',

        'Zebra ZD420': 'https://l1nq.com/lS9Ok',

        'Zebra ZD421': 'https://l1nq.com/lS9Ok',

        'Zebra ZD621': 'https://l1nq.com/lS9Ok',

        'Zebra ZD621R RFID': 'https://l1nq.com/lS9Ok',

        'Zebra GK420T': 'https://l1nq.com/xSIlz',

        'Bematech LB-1000': 'https://l1nq.com/6ASQV',
    }

    sg.theme('DarkBlue13')
    # Lista do autocomplet
    # Diretório onde os arquivos .txt estão localizados
    diretorio_scripts = os.path.join(os.path.dirname(__file__), 'scripts_txt')

    # Listar os arquivos .txt no diretório
    arquivos_txt = [arquivo for arquivo in os.listdir(
        diretorio_scripts) if arquivo.endswith('.txt')]
    # Layout Da tela de Utilitários
    layout = [
        
        [sg.Text('Busque por um Script:',font=('Helvetica',9,'bold'), text_color="#f0ffff",background_color="#104e8b")],
        [sg.Combo(arquivos_txt, size=(61, 1), key='-ARQUIVO-'),
         sg.Button("Mostrar Script", font=('Helvetica', 9, 'bold'), size=(35, 0), button_color="#44ab4c", pad=(5, 0))],
        [sg.Column([[sg.Text('ARQUIVOS DE INSTALAÇÃO', font=('Arial', 8, 'bold'), text_color='#ffffff', background_color="#104e8b", pad=(0, 0))],
                    [sg.Combo(['Hiper.Setup', 'E-Trade instalador', 'E-Trade versão stable', 'Bancos de Dados dos Estados', 'SQL Server 2014 + SSMS x86', 'SQL Server 2014 + SSMS x64', 'SQL Server 2019 Express'],
                              font=('Helvetica', 10, 'bold'), key='combo2', text_color='black', pad=(0, 0))],

                    [sg.HorizontalSeparator(
                        pad=((0, 0), (10, 10)), color='black')],

                    [sg.Text('DRIVERS IMPRESSORAS', font=('Arial', 8, 'bold'),
                     text_color='#ffffff', background_color="#104e8b", pad=(0, 0))],

                    # Combo das Impressoras----------------------------------------------------------------------------------------------------------------------------------------
                    [sg.Combo(['--Impressoras de Cupons--', 'Bematech MP-100S TH 32bits', 'Bematech MP-100S TH 64bits', 'Bematech MP-2800 TH 32 bits', 'Bematech MP-2800 TH 64 bits',
                               'Bematech MP-4200 TH 32 bits', 'Bematech MP-4200 TH 64 bits', 'Diebold Todos os Drivers', 'Daruma DR-800', 'Epson TM-T20', 'Epson TM-T20X', 'Epson TM-T70II', 'Epson Térmica TM-T88VII', 'Epson L375',
                               'Epson L1250', 'Epson L3110', 'Epson L3210', 'Epson L3250', 'Epson L3251', 'Epson L3252', 'Epson L4160', 'Epson L4260', 'Elgin i7/i9',
                               'HP DeskJet 2774', 'HP Ink Tank Wireless 416', 'Samsung ML-2160', 'Xerox Phaser 3020',

                               '--Impressoras de Etiquetas--', 'Argox All Driver', 'Bematech LB-1000', 'Elgin L42 PRO FULL', 'Zebra ZD420', 'Zebra ZD421', 'Zebra GK420T', 'Zebra ZD621', 'Zebra ZD621R RFID', 'Zebra Z800'],
                              font=('Helvetica', 10, 'bold'), background_color='', key='combo', text_color='black', pad=(0, 0))],

                    [sg.Button('Baixar', size=(15, 1), font=(
                        'Helvetica', 9, 'bold'), key='bx', button_color="#e69138", pad=(40, 10))],
                    ], background_color="#104e8b"),
            [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],
            sg.VerticalSeparator(),

            sg.Column([
                [sg.Text(text='ARQUIVOS DIVERSOS', font=('Arial', 8, 'bold'),
                      text_color='#ffffff', background_color="#104e8b", pad=(10, 0))],

                [sg.Combo(["Advanced_IP_Scanner", "Driver's de Rede", 'Pré-Implantação Hiper', "AnyDesk", "Rufus Botável", 'Crystal Disk Info', 'WinToHDD_Clonar HD'], size=25, font=('Helvetica', 9, 'bold'), key='combo3', pad=(10, 0)),

                    sg.Button('Baixar', size=(15, 0), font=('Helvetica', 9, 'bold'), key='bx2', button_color="#e69138", pad=(0, 0))],

                [sg.HorizontalSeparator(
                 pad=((0, 0), (10, 10)), color='black')],

                [sg.Text('ATIVADORES', font=('Helvetica', 8, 'bold'),
                         text_color='#ffffff', background_color="#104e8b", pad=(100, 10))],
                [sg.Text('Obs:Ativador Reloader Ativa(win: 8,10 - Office: 14,15,16)', font=('Helvetica 8'), text_color="#f0ffff",
                         background_color="#104e8b", pad=(0, 0))],
                [sg.Button('Reloader', size=(10), font=('Helvetica', 8, 'bold'), key='reloader', button_color="#e69138", pad=(10, 0)),
                    sg.Button('Windows 11', size=(10), font=(
                        'Helvetica', 8, 'bold'), key='wim11', button_color="#e69138", pad=(10, 0)),
                    sg.Button('Office 2021', size=(10), font=('Helvetica', 8, 'bold'), key='2021', button_color="#e69138", pad=(10, 0))],


            ], background_color="#104e8b")
         ],
        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)), color='black')],
        [sg.Button('Verificar Atualizações', key='atualizacao',font=('Helvetica', 7, 'bold'), size=(20, 0), button_color="#44ab4c")],

    ]

    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'IMG.ico')
    reloader_process = None
    win11_process = None
    office_process = None
    driversrede_process = None
    hiper_process = None
    anydesk_process = None
    rufus_process = None
    cristal_process = None
    hdd_process = None
    ipscaner_process = None
    # Cria a janela
    janela1 = sg.Window('Minhas Ferramentas', layout=layout, size=(600, 280), background_color="#104e8b", finalize=True,
                        icon=(icon_path))

    # Cria o loop responsável por ler os eventos da tela
    while True:
        evento, valores = janela1.read()
        if evento == sg.WIN_CLOSED:
            break

        # Cria janela que mostra os arquivos de scripts
        if evento == "Mostrar Script":
            # Verificar se um arquivo foi selecionado
            if valores['-ARQUIVO-']:
                nome_arquivo = valores['-ARQUIVO-']
                caminho_arquivo = os.path.join(diretorio_scripts, nome_arquivo)

                # Ler o conteúdo do arquivo selecionado
                with open(caminho_arquivo, "r") as f:
                    conteudo = f.read()
                layout_script = [
                    [sg.Multiline(default_text=conteudo, size=(
                        80, 20), text_color='#e32636', disabled=True)],
                    [sg.Button('Voltar', button_color='#e32636', font=(
                        'Helvetica', 10, 'bold'), size=(15, 0))],

                ]
                # Criar uma nova janela para exibir o conteúdo do arquivo
                janela_script = sg.Window(
                    f"Conteúdo do Arquivo: {nome_arquivo}", layout=layout_script, icon=(icon_path))
                while True:
                    event_script, values_script = janela_script.read()
                    if event_script == sg.WINDOW_CLOSED or event_script == 'Voltar':
                        break
                janela_script.close()
            else:
                sg.popup_error("Nenhum arquivo selecionado.")

        elif evento == 'bx':
            if valores['combo']:
                # Recupera o link correspondente à opção selecionada
                link = links[valores['combo']]
                webbrowser.open(link)

        if evento == 'bx':
            if valores['combo2']:
                # Recupera o link correspondente à opção selecionada
                link1 = links1[valores['combo2']]
                # Abre o link no navegador
                webbrowser.open(link1)

        if evento == 'bx2':
            if valores['combo3'] == "Rufus Botável":
                # pega o caminho do arquivo em qualquer outra máquina
                verificador_rufus = os.path.join(
                    os.path.dirname(__file__), 'resources', 'rufus.exe')

                # não permite que a execução do arquivo se torne um loop
                if rufus_process is None or not psutil.pid_exists(rufus_process.pid):
                    rufus_process = subprocess.Popen(verificador_rufus)
                else:
                    sg.popup('Rufus já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == "AnyDesk":
                # pega o caminho do arquivo em qualquer outra máquina
                verificador_anydesk = os.path.join(
                    os.path.dirname(__file__), 'resources', 'AnyDesk.exe')

                # não permite que a execução do arquivo se torne um loop
                if anydesk_process is None or not psutil.pid_exists(anydesk_process.pid):
                    anydesk_process = subprocess.Popen(verificador_anydesk)
                else:
                    sg.popup('AnyDesk já está em execução!')

        if evento == 'reloader':
            # pega o caminho do arquivo em qualquer outra máquina
            verificador_reloader = os.path.join(
                os.path.dirname(__file__), 'resources', 'RELOAD.exe')

            # não permite que a execução do arquivo se torne um loop
            if reloader_process is None or not psutil.pid_exists(reloader_process.pid):
                reloader_process = subprocess.Popen(verificador_reloader)
            else:
                sg.popup('Reloader já está em execução!')

        if evento == 'wim11':
            ativador_win11 = os.path.join(
                os.path.dirname(__file__), 'resources', 'win11.cmd')

            # não permite que a execução do arquivo se torne um loop
            if win11_process is None or not psutil.pid_exists(win11_process.pid):
                win11_process = subprocess.Popen(ativador_win11)
            else:
                sg.popup('Ativador Windows 11 já está em execução!')

        if evento == '2021':
            ativador_winoffice = os.path.join(os.path.dirname(
                __file__), 'resources', 'office2021.cmd')

            # não permite que a execução do arquivo se torne um loop
            if office_process is None or not psutil.pid_exists(office_process.pid):
                office_process = subprocess.Popen(ativador_winoffice)
            else:
                sg.popup('Ativador Windows e Office já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == "Driver's de Rede":
                driver_rede = os.path.join(os.path.dirname(
                    __file__), 'resources', '3DP.exe')

                # não permite que a execução do arquivo se torne um loop
                if driversrede_process is None or not psutil.pid_exists(driversrede_process.pid):
                    driversrede_process = subprocess.Popen(driver_rede)
                else:
                    sg.popup('O 3DPn já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == 'Pré-Implantação Hiper':
                # pega o caminho do arquivo em qualquer outra máquina
                arquivo_hiper = os.path.join(os.path.dirname(
                    __file__), 'resources', 'Hiper.bat')

                # não permite que a execução do arquivo se torne um loop
                if hiper_process is None or not psutil.pid_exists(hiper_process.pid):
                    hiper_process = subprocess.Popen(arquivo_hiper)
                else:
                    sg.popup('Verificador de ambiente Hiper já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == 'Crystal Disk Info':
                # pega o caminho do arquivo em qualquer outra máquina
                arquivo_cristal = os.path.join(os.path.dirname(
                    __file__), 'resources', 'CrystalDiskInfo.exe')

                # não permite que a execução do arquivo se torne um loop
                if cristal_process is None or not psutil.pid_exists(cristal_process.pid):
                    cristal_process = subprocess.Popen(arquivo_cristal)
                else:
                    sg.popup(
                        'Verificador de ambiente Cristal Disk Info  já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == 'WinToHDD_Clonar HD':
                # pega o caminho do arquivo em qualquer outra máquina
                arquivo_wintohdd = os.path.join(os.path.dirname(
                    __file__), 'resources', 'WinToHDD_Free.exe')

                # não permite que a execução do arquivo se torne um loop
                if hdd_process is None or not psutil.pid_exists(hdd_process.pid):
                    hdd_process = subprocess.Popen(arquivo_wintohdd)
                else:
                    sg.popup(
                        'Verificador de ambiente WinToHDD  já está em execução!')

        if evento == 'bx2':
            if valores['combo3'] == 'Advanced_IP_Scanner':
                # pega o caminho do arquivo em qualquer outra máquina
                arquivo_ipscaner = os.path.join(os.path.dirname(
                    __file__), 'resources', 'Advanced_IP_Scanner.exe')

                # não permite que a execução do arquivo se torne um loop
                if ipscaner_process is None or not psutil.pid_exists(ipscaner_process.pid):
                    ipscaner_process = subprocess.Popen(arquivo_ipscaner)
                else:
                    sg.popup(
                        'Verificador de ambiente WinToHDD  já está em execução!')

        if evento == 'atualizacao':
             verificar_atualizacoes()

    janela1.close()
