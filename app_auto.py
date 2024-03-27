import pyautogui
from time import sleep
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


listVolumes = ['Volume','Pallet','Container','Unidade','Tambor',
               'Balde','Granel']

finaliza = True

def pegarInfo():
    global transportadora, redespacho, volume, especie, itens
    transportadora = entrada_trans.get()
    redespacho = entrada_redespacho.get()
    volume = entrada_volume.get()
    especie = cb_especie.get()
    itens = entrada_volume_item.get()

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

def limpar():
    entrada_trans.delete(0, END)
    entrada_redespacho.delete(0, END)
    entrada_volume.delete(0, END)
    cb_especie.set('')
    entrada_volume_item.delete(0, END)

while finaliza:
    finaliza = False
    
    janela = Tk()
    janela.title('Informações do Pedido')
    janela.resizable(False, False)
    janela.iconbitmap(default='') # informar a imagem da janela .ico
    janela.focus()

    largura = 380
    altura = 175
    largura_tela = janela.winfo_screenwidth()
    altura_tela =  janela.winfo_screenheight()
    posix = largura_tela/2 - largura/2
    posiy = altura_tela/2 - altura/2
    janela.geometry("%dx%d+%d+%d" % (largura,altura,posix,posiy))


    label_trans = Label(janela, text = "    Código da Transportadora:")
    label_trans.grid(column=0, row = 0, padx=0, pady=5, sticky='e')
    entrada_trans = Entry(janela,width=14, justify='center')
    entrada_trans.grid(column=1, row=0, padx=5, pady=5, sticky='e')

    label_redesp = Label(janela, text = "Código do Redespacho:")
    label_redesp.grid(column=0, row=1, pady=5, sticky='e')
    entrada_redespacho = Entry(janela,width=14, justify='center')
    entrada_redespacho.grid(column=1, row=1, padx=5, pady=5, sticky='e')

    label_qtd = Label(janela, text = "Qtd. total de Volumes:")
    label_qtd.grid(column=0, row=2, pady=5, sticky='e')
    entrada_volume = Entry(janela,width=14, justify='center')
    entrada_volume.grid(column=1, row=2, padx=5, pady=5, sticky='e')

    label_esp = Label(janela, text = "Tipo de Volume:")
    label_esp.grid(column=0, row=3, pady=5, sticky='e')
    cb_especie=ttk.Combobox(janela,values=listVolumes, width=14, state='readonly')
    cb_especie.grid(column=1, row=3, padx=5, pady=5, sticky='e')

    label_qtd_item = Label(janela, text = "Volumes por item:")
    label_qtd_item.grid(column=0, row=4, pady=5, sticky='e')
    entrada_volume_item = Entry(janela,width=17, justify='center')
    entrada_volume_item.grid(column=1, row=4, padx=5, pady=5, sticky='e')
        
    btn_iniciar = Button(janela, text="Iniciar",command=pegarInfo, width=10)
    btn_iniciar.grid(column=3, row=2, padx=5, pady=5)

    btn_sair = Button(janela, text="Limpar",command=limpar, width=10)
    btn_sair.grid(column=3, row=3, padx=5, pady=5)

    btn_sair = Button(janela, text="Sair",command=quit, width=10)
    btn_sair.grid(column=3, row=4, padx=5, pady=5)

    janela.mainloop()

    aviso = messagebox.showinfo('Atenção', 'Favor não tocar no mouse e teclado durante o processo!')

           
    # Preparação para NF
    try:
        sleep(1)
        #pyautogui.click(1200,317,duration=0.5) # Mostrar
        pyautogui.click(1197,342,duration=0.5) # Processar
        sleep(0.5)
        pyautogui.click(pyautogui.locateCenterOnScreen('img/sim.png', minSearchTime=5),duration=0.2) # Transferir itens
        sleep(0.5)
        pyautogui.moveTo(642,500, duration=0.2)
        pyautogui.click(pyautogui.locateCenterOnScreen('img/nao.png', minSearchTime=10),duration=0.2) # Não fechar NF
        sleep(0.5)
        pyautogui.click(pyautogui.locateCenterOnScreen('img/nf.png', minSearchTime=2),duration=0.2) # Abrir NF
        sleep(2)

        # Localizar tipo de produtos para selecionar frase
        try:
            pvc = pyautogui.locateCenterOnScreen('img/pvc.png', minSearchTime=1)
            pyautogui.moveTo(pvc, duration=0.2)
            frase_pvc = '71'
        except:
            frase_pvc = ''

        try:
            espuma = pyautogui.locateCenterOnScreen('img/espuma.png')
            pyautogui.moveTo(espuma, duration=0.2)
            frase_espuma = '70'
        except:
            frase_espuma = ''

        try:
            perc_icms = pyautogui.locateOnScreen('img/perc_icms.png')
            area = pyautogui.locateOnScreen('img/icms.png', region=(perc_icms[0],perc_icms[1],perc_icms[0]+40,perc_icms[1]+250))
            pyautogui.moveTo(area, duration=0.2)
            frase_icms = '75'
        except:
            frase_icms = '0'

        
        # Monta as frases dependendo dos itens na nota
        if frase_espuma != '' or frase_pvc != '':
            frases = [frase_espuma, frase_pvc, frase_icms]
            for frase in frases:
                if frase == '':
                    frases.remove('')
        else:
            frases = ['33',frase_icms]
        
        # Confere e completa os volumes de cada item
        if itens != '':
            try:
                qtd_item = pyautogui.locateOnScreen('img/qtde.png', minSearchTime=1)
                pyautogui.doubleClick(qtd_item[0]+77, qtd_item[1] + 30)
                item_sep = itens.split(',')
                for item in item_sep:
                    pyautogui.write(str(item))
                    pyautogui.press('down')
                    sleep(0.7)
                pyautogui.press('esc')
            except:
                messagebox.showwarning('Aviso', 'Execução encerrada! Volume não encontrado')
            

        sleep(0.5)
        
        # Tela da NF
        pyautogui.click(64,144,duration=0.2) # Diversos
        sleep(1.3)
        
        pyautogui.doubleClick(225,87,duration=0.2) # Transportadora
        pyautogui.write(transportadora)

        if redespacho == '0' or redespacho == '':
            tem_redespacho = False
        else:
            tem_redespacho = True
            pyautogui.click(220,163,duration=0.2) # Redespacho
            pyautogui.write(redespacho)

        pyautogui.click(190,211,duration=0.2) # Quantidade de volumes
        pyautogui.write(volume)

        pyautogui.click(229,211,duration=0.2) # Tipo de volume
        pyautogui.write(especie)

        pyautogui.doubleClick(173,266,duration=0.2) # Frase
        for frase in frases:        
            pyautogui.write(str(frase))
            pyautogui.keyDown('enter')
            pyautogui.keyDown('enter')
            sleep(0.3)

        messagebox.showinfo('Atenção', 'Confira os dados!')

        pyautogui.click(1324,38,duration=0.2) # Processar

        # Frete do redespacho
        if tem_redespacho: 
            pyautogui.click(1244,109,duration=0.2) 
            pyautogui.doubleClick(519,340,duration=0.5)
            pyautogui.write('F')
            pyautogui.keyDown('enter')
            pyautogui.click(998,234,duration=0.5)

        pyautogui.click(1246,61,duration=0.3) # Fechar NF
        sleep(0.5)
        
        fechar = True
        sim = True
        continuar = True
        certificado = True
        
        while fechar: # Clica em sim, continuar ou imprimir certificado enquanto for verdadeiro
            pyautogui.moveTo(642,500,duration=0.1)
            try:
                clica_sim = pyautogui.locateOnScreen('img/sim.png', minSearchTime=3.5, region=(524,333,842,429))
                pyautogui.click(clica_sim, duration=0.2) # Sim
                sim = True
            except:
                sim = False
            
            pyautogui.moveTo(642,500,duration=0.1)
            try:
                if continuar == True:
                    clica_continuar = pyautogui.locateOnScreen('img/continuar.png', minSearchTime=0.6, region=(524,333,842,429))
                    pyautogui.click(clica_continuar, duration=0.2) # Continuar
                    sleep(1)
            except:
                continuar = False
                        
            try:
                clica_imprimir = pyautogui.locateOnScreen('img/imprimir.png', minSearchTime=1.2, region=(418,0,656,63))
                pyautogui.click(clica_imprimir, duration=0.2)
                certificado=True
            except:
                certificado = False
            if certificado==True:
                #clica_ok = pyautogui.locateOnScreen('img/ok.png', minSearchTime=1, region=(807,188,1037,352))
                pyautogui.click(935,252, duration=0.3)
                clica_sair = pyautogui.locateOnScreen('img/sair.png', minSearchTime=1.5, region=(418,0,656,63))
                pyautogui.click(clica_sair, duration=0.2)
            

            if sim == False and continuar == False and certificado == False:
                fechar = False


        clica_ok = pyautogui.locateOnScreen('img/ok-1.png', minSearchTime=0.3, region=(1193, 0, 1361, 271)) # Ok
        pyautogui.click(clica_ok, duration=0.2)
        sleep(2)

        fechar_nota = messagebox.askyesno('Confirmação','Posso fechar a nota?')

        clica_sair = pyautogui.locateOnScreen('img/sair.png', minSearchTime=1.5, region=(418,0,656,63))
        pyautogui.click(clica_sair, duration=0.2)
        
        if fechar_nota == True:
            clica_sim = pyautogui.locateOnScreen('img/sim.png', minSearchTime=1, region=(505,301,877,449))
            pyautogui.click(clica_sim, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            clica_ok = pyautogui.locateOnScreen('img/ok.png', minSearchTime=1, region=(505,301,877,449))
            pyautogui.click(clica_ok, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            clica_nao = pyautogui.locateOnScreen('img/nao.png', minSearchTime=1, region=(505,301,877,449))
            pyautogui.click(clica_nao, duration=0.3)
        else:
            clica_nao = pyautogui.locateOnScreen('img/nao.png', minSearchTime=1, region=(505,301,877,449))
            pyautogui.click(clica_nao, duration=0.3)
            pyautogui.moveTo(642,500,duration=0.1)
            pyautogui.click(clica_nao, duration=0.3)

        finaliza = messagebox.askyesno('Confirmação','Faturar novamente?')

    except:
        messagebox.showwarning('Aviso', 'Execução encerrada!')