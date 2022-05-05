import sys
import threading
import time

import PySimpleGUI as sg
from iqoptionapi.stable_api import IQ_Option
import configparser
from datetime import datetime
from pytz import timezone
from time import sleep



sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Text('Nome do ativo:'), sg.Combo(
        ['EURUSD-OTC', 'EURUSD', 'USDJPY-OTC', 'USDJPY', 'USDCHF-OTC', 'USDCHF', 'GBPUSD-OTC', 'GBPUSD','GBPJPY','GBPJPY-OTC', 'EURJPY-OTC',
         'EURJPY', 'AUDCAD-OTC', 'AUDCAD', 'AUDUSD-OTC', 'AUDUSD',], key='telaativo', size=(20, 0))],
    [sg.Text('Porcetagem maxima de perda:'), sg.Combo(['10', '20','30','40','50','60','70','80','90','100'], key='maxperda')],
    #[sg.Text('Porcetagem maxima de ganho:'), sg.Combo(['10', '20','30'], key='maxganho')],
    [sg.Text('Multiplicador:'), sg.Combo(['2.1', '2.2','2.3','2.4','2.5','2.6','2.7','2.8','2.9','3.0'], key='multipli')],
    [sg.Text('Valor da operação'), sg.Input(key='telalote', size=(8, 0))],
    [sg.Text('Compra ou venda:'), sg.Combo(['call', 'put'], key='teladirecao')],
    [sg.Text('Tipo de conta:'), sg.Combo(['PRACTICE', 'REAL'], key='tipoc')],
    #[sg.Output(size=(50,10))],
    [sg.Submit(), sg.Exit()]
]

janela = sg.Window('MARTINGALE BOT', layout)

def novajanela():

    layout=[
        [sg.Output(size=(50, 10))]
    ]
    return sg.Window("RESULTADOS", layout=layout, finalize=True)


while True:





    eventos, valores = janela.read()

    perda = float(valores['maxperda'])

    #ganho = float(valores['maxganho'])

    multi = float(valores['multipli'])

    nomeativo = valores['telaativo']
    ativo = str(nomeativo)

    # numerolote=valores['telalote']
    # lotes = float(numerolote)
    lotes = float(valores['telalote'])

    nomedirecao = valores['teladirecao']
    direcao = str(nomedirecao)

    nomeconta = valores['tipoc']
    tipoconta = str(nomeconta)

    if eventos == sg.WIN_CLOSED or eventos == 'Exit':

        janela.hide()
        break

    if eventos == 'Submit':

        # print(valores, eventos)

        #janela.hide()
        #novajanela()

        arq = configparser.RawConfigParser()
        arq.read('config.txt')

        email = arq.get('LOGIN', 'email')
        password = arq.get('LOGIN', 'password')


        def timestamp2dataHora(x, timezone_='America/Sao_Paulo'):

            d = datetime.fromtimestamp(x, tz=timezone(timezone_))
            return str(d)


        def infoContaIQ(api):

            conta = api.get_profile_ansyc()
            nome = conta['name']
            moeda = conta['currency']
            data_criacao = timestamp2dataHora(conta['created'])
            return conta, nome, moeda, data_criacao


        def Conexao(email, password, tipoconta=valores['tipoc']):


            API = IQ_Option(email, password)

            API.connect()

            API.change_balance(tipoconta)  # REAL

            conectado = False
            if API.check_connect() == True:
                # print("Conexão estabelecida")
                #sg.popup('Conectado')
                sg.popup_auto_close('Conectado')
                conectado = True
            else:
                # print("Não conectado")
                #sg.popup('Não conectado')
                sg.popup_auto_close('Não conectado')
                conectado = False

            return API, conectado


        def payout(lotes, ativo, direcao, timeframe=1):


            status, ID = API.buy(lotes, ativo, direcao, timeframe)

            dez = baa * 0.9
            vinte = baa * 0.8
            trinta = baa * 0.7
            quarenta = baa * 0.6
            cinquenta = baa * 0.5
            sessenta = baa * 0.4
            setenta = baa * 0.3
            oitenta = baa * 0.2
            noventa = baa * 0.1

            perda = float(valores['maxperda'])

            if perda == 10.0:
                perda = float(dez)

            elif perda == 20.0:
                perda = float(vinte)

            elif perda == 30.0:
                perda = float(trinta)

            elif perda == 40.0:
                perda = float(quarenta)

            elif perda == 50.0:
                perda = float(cinquenta)

            elif perda == 60.0:
                perda = float(sessenta)

            elif perda == 70.0:
                perda = float(setenta)

            elif perda == 80.0:
                perda = float(oitenta)

            elif perda == 90.0:
                perda = float(noventa)

            elif perda == 100.0:
                perda = 2

            baa2 = API.get_balance()
            print("\n Saldo atualizado:  ", baa2)


            if status:
                print("\n")
                print(API.check_win_v3(ID))
                print("\n")

            lucro = API.check_win_v3(ID)



            while perda <= baa2:




                #if lucro <= 0 and baa2 > dez and baa2 > vinte and baa2 > trinta and baa2 > quarenta and baa2 > cinquenta and baa2 > sessenta and baa2 > setenta and baa2 > oitenta and baa2 > noventa:
                if lucro <= 0:
                    multi = float(valores['multipli'])
                    lotes = lotes * multi



                    payout(lotes, ativo, direcao)


                    time.sleep(63)
                    baa2 = API.get_balance()

                    print("\n Saldo atualizado:  ", baa2)

                else:


                    # numerolote=valores['telalote']
                    # lotes = float(numerolote)
                    lotes = float(valores['telalote'])
                    # ID = API.buy(lotes , ativo, direcao, timeframe)



                    payout(lotes, ativo, direcao)

                    time.sleep(63)
                    baa2 = API.get_balance()
                    print("\n Saldo atualizado:  ", baa2)


                    return status, ID, lucro
            else:
                quit()
                sys.exit()
                janela.close()









        API, conectado = Conexao(email, password, tipoconta)

        info = API.get_profile_ansyc()

        ##global baa

        baa = API.get_balance()
        baa2 = API.get_balance()
        conta, nome, moeda, data_criacao = infoContaIQ(API)

        payout(lotes, ativo, direcao)











