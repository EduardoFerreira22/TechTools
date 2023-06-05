import PySimpleGUI as sg
import os
import subprocess
import psutil


def ibexpress():

    sg.theme('DarkBlue3')
    # Cria o Layout da tela
    layout = [[sg.Text('Após Clicar no botão por favor ', background_color="#104e8b")],
              [sg.Text('aguarde a instalação do Programa!',
                       background_color="#104e8b")],
              [sg.Checkbox('IB Expert', key='ibex',
                           background_color='#104e8b')],
              [sg.Button('Voltar', button_color="#e69138", key='voltar'), sg.Button('Baixar e executar', button_color="#e69138")]],

    # Define o caminho do ícone
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'IMG.ico')

    # Executa a criação da tela
    window = sg.Window('IB Expert', layout=layout, size=(300, 150), background_color="#104e8b", finalize=True,
                       icon=icon_path)

    ibexpert_process = None

    # Cria o loop responsável por ler os eventos da tela
    while True:
        event, values = window.read()
        if event == 'voltar' or event == sg.WIN_CLOSED:
            break
        elif event == 'Baixar e executar':
            if values['ibex'] == True:
                # pega o caminho do arquivo em qualquer outra máquina
                nome_arquivo = os.path.join(os.path.dirname(
                    __file__), 'IBExpert', 'ibexpert.exe')

                # não permite que a execução do arquivo se torne um loop
                if ibexpert_process is None or not psutil.pid_exists(ibexpert_process.pid):
                    ibexpert_process = subprocess.Popen(nome_arquivo)
                else:
                    sg.popup('IBExpert já está em execução!',icon=icon_path)

    window.close()

    
