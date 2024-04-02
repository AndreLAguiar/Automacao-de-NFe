import pyautogui
from time import sleep
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


# Função que inicia a aplicação chamada pelo botão iniciar
def iniciar():

    global transportadora, redespacho, volume, especie, itens
    
    # Adiciona os valores informados no campo da janela em uma variável
    transportadora = entrada_trans.get()
    redespacho = entrada_redespacho.get()
    volume = entrada_volume.get()
    especie = cb_especie.get()
    itens = entrada_volume_item.get()

    # Compara o tipo de volume escolhido pelo usuário e altera a variável para o código do tipo
    match especie:
        case 'Volume':
            especie='13'
        case 'Pallet':
            especie='15'
        case 'Container':
            especie='4'
        case 'Granel':
            especie='8'
        case 'Unidade':
            especie='12'
        case 'Balde':
            especie='16'
        case 'Tambor':
            especie='14'

    janela.destroy()
    
    messagebox.showinfo('Atenção', 'Favor não tocar no mouse e teclado durante o processo! \
    Caso precise parar arraste o mouse para o campo superior esquerdo até encerrar o processo.')

    
    # Preparação para NF
    try:
        sleep(1)
        # Mostra os itens do pedido na tela de preparação
        #pyautogui.click(pyautogui.locateCenterOnScreen('img/mostrar.png', minSearchTime=2),duration=0.2)
        
        # Processa os itens conferindo se tem os lotes informados
        pyautogui.click(pyautogui.locateCenterOnScreen('img/processar.png', minSearchTime=2),duration=0.2)
        sleep(0.5)

        # Transfere os itens para a nota
        pyautogui.click(pyautogui.locateCenterOnScreen('img/sim.png', minSearchTime=5),duration=0.2)
        sleep(0.5)

        # Movimenta o mouse para baixo para sair de cima do botão
        pyautogui.moveTo(642,500, duration=0.2)

        # Opção de não fechar a nota pois falta informar transportadora, volumes, frases e etc.
        pyautogui.click(pyautogui.locateCenterOnScreen('img/nao.png', minSearchTime=10),duration=0.2)
        sleep(0.5)

        # Abrir a tela da nota para preencher a informações
        pyautogui.click(pyautogui.locateCenterOnScreen('img/nf.png', minSearchTime=2),duration=0.2)
        sleep(2)

        # Procura na coluna de descrição do produto por pvc, caso encontre a frase é 71 senão será vazio
        try:
            pvc = pyautogui.locateCenterOnScreen('img/pvc.png', minSearchTime=1)
            pyautogui.moveTo(pvc, duration=0.2)
            frase_pvc = '71'
        except:
            frase_pvc = ''

        # Procura na coluna de descrição do produto por espuma, caso encontre a frase é 75 senão será vazio
        try:
            espuma = pyautogui.locateCenterOnScreen('img/espuma.png')
            pyautogui.moveTo(espuma, duration=0.2)
            frase_espuma = '70'
        except:
            frase_espuma = ''

        # Procura se algum produto na coluna de percentual de icms tem o icms com 4%, caso tenha a frase é a 75 senão é 0
        try:
            perc_icms = pyautogui.locateOnScreen('img/perc_icms.png')
            area = pyautogui.locateOnScreen('img/icms.png', region=(perc_icms[0],perc_icms[1],perc_icms[0]+40,perc_icms[1]+250))
            pyautogui.moveTo(area, duration=0.2)
            frase_icms = '75'
        except:
            frase_icms = '0'

        
        # Se as frases da espuma ou pvc estiverem vazias, então:
        if frase_espuma != '' or frase_pvc != '':
            frases = [frase_espuma, frase_pvc, frase_icms]
            # Monta a lista de frases removendo as vazias
            for frase in frases:
                if frase == '':
                    frases.remove('')
        # Senão, monta a lista de frases somente com a padrão 33 mais a de icms
        else:
            frases = ['33',frase_icms]
        
        # Se o volume por item for diferente de vazio, então:
        if itens != '':
            try:
                # Clica na coluna de volume dos itens
                qtd_item = pyautogui.locateOnScreen('img/qtde.png', minSearchTime=1)
                pyautogui.doubleClick(qtd_item[0]+77, qtd_item[1] + 30)
                
                # Separa a quantidade informada retirando a vírgula
                item_sep = itens.split(',')

                # Preenche cada linha com os volumes informados 
                for item in item_sep:
                    pyautogui.write(str(item))
                    pyautogui.press('down', interval=0.5)
                
                # Pressiona Esc para sair da última linha criada em branco
                pyautogui.press('esc')

            except:
                # Mensagem de erro caso não encontre a coluna de volume
                messagebox.showwarning('Aviso', 'Execução encerrada! Volume não encontrado')
            

        sleep(0.5)
        
        # Tela da NF
        # Clica em diversos para preencher transportadora, redespacho, volumes, e frases
        pyautogui.click(pyautogui.locateCenterOnScreen('img/diversos.png', minSearchTime=2),duration=0.2) 
        sleep(1.3)
        
        # Transportadora
        camp_transp = pyautogui.locateCenterOnScreen('img/campo_transportadora.png', minSearchTime=1)
        pyautogui.doubleClick(camp_transp[0]+120,camp_transp[1],duration=0.2)
        pyautogui.write(transportadora)
        pyautogui.press('enter', presses=4, interval=0.1)
        
        # Verifica se tem transportadora informada como redespacho e preenche no campo
        if redespacho == '0' or redespacho == '':
            tem_redespacho = False
        else:
            tem_redespacho = True
            pyautogui.write(redespacho)

        pyautogui.press('enter', presses=4, interval=0.1)
        
        # Quantidade de volumes
        pyautogui.write(volume)
        pyautogui.press('enter')

        # Tipo de volume
        pyautogui.write(especie)
        pyautogui.press('enter', presses=3, interval=0.1)
        
        # Preenche as frases 
        for frase in frases:        
            pyautogui.write(str(frase))
            pyautogui.press('enter', presses=2, interval=0.1)
        
        # Confirmação de preenchimento
        messagebox.showinfo('Atenção', 'Confira os dados!')

        # Processar
        pyautogui.click(pyautogui.locateCenterOnScreen('img/processar.png', minSearchTime=2),duration=0.2)

        # Adiciona o tipo de frete do redespacho caso tenha transportadora informada
        if tem_redespacho: 
            pyautogui.click(pyautogui.locateCenterOnScreen('img/person.png', minSearchTime=2),duration=0.2) 
            pyautogui.write('F')
            pyautogui.press('enter', interval=0.3)
            pyautogui.hotkey('alt','s')

        # Fechar NF
        pyautogui.click(pyautogui.locateCenterOnScreen('img/fechar.png', minSearchTime=2),duration=0.2) 
        sleep(0.5)
        
        # Variáveis condicionais do looping
        fechar = True
        sim = True
        continuar = True
        certificado = True
        
        # Looping para clicar em sim, continuar ou imprimir certificado enquanto for verdadeiro
        while fechar: 
            pyautogui.moveTo(642,500,duration=0.1)
            
            # Sim
            try:
                clica_sim = pyautogui.locateOnScreen('img/sim.png', minSearchTime=3, region=(524,333,842,429))
                pyautogui.click(clica_sim, duration=0.2)
                sim = True
            except:
                sim = False
            
            pyautogui.moveTo(642,500,duration=0.1)
            
            # Continuar
            try:
                if continuar == True:
                    clica_continuar = pyautogui.locateOnScreen('img/continuar.png', minSearchTime=0.6, region=(524,333,842,429))
                    pyautogui.click(clica_continuar, duration=0.2) 
                    sleep(1)
            except:
                continuar = False

            # Imprimir certificado caso tenha         
            try:
                clica_imprimir = pyautogui.locateOnScreen('img/imprimir.png', minSearchTime=2, region=(418,0,656,63))
                pyautogui.click(clica_imprimir, duration=0.2)
                certificado=True
            except:
                certificado = False
            if certificado==True:
                clica_ok = pyautogui.locateOnScreen('img/ok-cert.png', minSearchTime=1, region=(807,188,1037,352))
                pyautogui.click(clica_ok, duration=0.3) # posição do ok 935,252
                clica_sair = pyautogui.locateOnScreen('img/sair.png', minSearchTime=1.5, region=(418,0,656,63))
                pyautogui.click(clica_sair, duration=0.2)
            
            # Verifica se continua ou sai do looping
            if sim == False and continuar == False and certificado == False:
                fechar = False

        # clica no Ok para continuar
        clica_ok = pyautogui.locateOnScreen('img/ok-esp.png', minSearchTime=0.3, region=(1193, 0, 1361, 271))
        pyautogui.click(clica_ok, duration=0.2)
        sleep(2)

        # Confirmação para fechar a nota
        fechar_nota = messagebox.askyesno('Confirmação','Posso fechar a nota?')

        # Sair do espelho da nota
        clica_sair = pyautogui.locateOnScreen('img/sair.png', minSearchTime=1.5, region=(418,0,656,63))
        pyautogui.click(clica_sair, duration=0.2)
                
        if fechar_nota == True:
            clica_sim = pyautogui.locateOnScreen('img/sim.png', minSearchTime=2, region=(505,301,877,449))
            pyautogui.click(clica_sim, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            clica_ok = pyautogui.locateOnScreen('img/ok.png', minSearchTime=2, region=(505,301,877,449))
            pyautogui.click(clica_ok, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            clica_nao = pyautogui.locateOnScreen('img/nao.png', minSearchTime=2, region=(505,301,877,449))
            pyautogui.click(clica_nao, duration=0.3)
        else:
            clica_nao = pyautogui.locateOnScreen('img/nao.png', minSearchTime=2, region=(505,301,877,449))
            pyautogui.click(clica_nao, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            pyautogui.click(clica_nao, duration=0.3)

        # Confirmação para reabrir a tela e reiniciar o processo
        reiniciar = messagebox.askyesno('Confirmação','Faturar novamente?')

        if reiniciar:
            abrirJanela()
        else:
            messagebox.showinfo('Aviso', 'Finalizado com sucesso!')

    except:
        messagebox.showwarning('Aviso', 'Execução encerrada!')

# Função para limpar os campos da tela
def limpar():
    entrada_trans.delete(0, END)
    entrada_trans.focus()
    entrada_redespacho.delete(0, END)
    entrada_volume.delete(0, END)
    cb_especie.set('')
    entrada_volume_item.delete(0, END)

# Função para criar a janela
def abrirJanela():

    # Variáveis globais dos campos e tela
    global entrada_trans, entrada_redespacho, entrada_volume, cb_especie, entrada_volume_item, janela

    listVolumes = ['Volume','Pallet','Container','Unidade','Tambor',
               'Balde','Granel']

    janela = Tk()
    janela.title('Informações do Pedido')
    janela.resizable(False, False)
    janela.iconbitmap(default='') # Adicionar a imagem de icone .ICO
    janela.focus()

    # Dimensões e posição da tela
    largura = 345
    altura = 180
    largura_tela = janela.winfo_screenwidth()
    altura_tela =  janela.winfo_screenheight()
    posix = largura_tela/2
    posiy = altura_tela/2 - altura
    janela.geometry("%dx%d+%d+%d" % (largura,altura,posix,posiy))

    # Label e campo de preenchimento da transportadora
    label_trans = Label(janela, text = "    Código da Transportadora:")
    label_trans.grid(column=0, row = 0, padx=0, pady=5, sticky='e')
    entrada_trans = Entry(janela,width=12, justify='center')
    entrada_trans.grid(column=1, row=0, padx=5, pady=5, sticky='e')

    # Label e campo de preenchimento da transportadora de redespacho
    label_redesp = Label(janela, text = "Código do Redespacho:")
    label_redesp.grid(column=0, row=1, pady=5, sticky='e')
    entrada_redespacho = Entry(janela,width=12, justify='center')
    entrada_redespacho.grid(column=1, row=1, padx=5, pady=5, sticky='e')

    # Label e campo de preenchimento da quantidade de volumes total
    label_qtd = Label(janela, text = "Qtd. total de Volumes:")
    label_qtd.grid(column=0, row=2, pady=5, sticky='e')
    entrada_volume = Entry(janela,width=12, justify='center')
    entrada_volume.grid(column=1, row=2, padx=5, pady=5, sticky='e')

    # Label e campo de preenchimento do tipo de volume
    label_esp = Label(janela, text = "Tipo de Volume:")
    label_esp.grid(column=0, row=3, pady=5, sticky='e')
    cb_especie=ttk.Combobox(janela,values=listVolumes, width=9, state='readonly')
    cb_especie.grid(column=1, row=3, padx=5, pady=5, sticky='e')

    # Label e campo de preenchimento da quantidade de volumes por item separados somente por vírgula
    label_qtd_item = Label(janela, text = "Volumes por item:")
    label_qtd_item.grid(column=0, row=4, pady=5, sticky='e')
    entrada_volume_item = Entry(janela,width=26, justify='left')
    entrada_volume_item.grid(column=1, row=4, padx=5, pady=5, columnspan='3')

    # Botão que inicia a aplicação    
    btn_iniciar = Button(janela, text="Iniciar",command=iniciar, width=10)
    btn_iniciar.grid(column=3, row=0, padx=1, pady=5)

    # Botão de limpar os campos
    btn_limpar = Button(janela, text="Limpar",command=limpar, width=10)
    btn_limpar.grid(column=3, row=1, padx=1, pady=5)

    # Botão de sair da aplicação
    btn_sair = Button(janela, text="Sair",command=janela.destroy, width=10)
    btn_sair.grid(column=3, row=2, padx=1, pady=5)

    entrada_trans.focus()
    janela.mainloop()

abrirJanela()