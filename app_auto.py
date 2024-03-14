import pyautogui
from time import sleep
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

listVolumes = ['Volume(s)','Pallet(s)','Container(s)','Granel','Unidades(s)','Balde(s)','Tambor(es)']
listIcms = ['Sim','Não']

def pegarInfo():
    global transportadora, volume, especie, redespacho, icms
    transportadora = entrada_trans.get()
    volume = entrada_volume.get()
    especie = cb_especie.get()
    redespacho = entrada_redespacho.get()
    icms = cb_icms.get()

    match especie:
        case 'Volume(s)':
            especie='13'
        case 'Pallet(s)':
            especie='15'
        case 'Container(s)':
            especie='4'
        case 'Granel':
            especie='8'
        case 'Unidades(s)':
            especie='12'
        case 'Balde(s)':
            especie='16'
        case 'Tambor(es)':
            especie='14'

    janela.destroy()

   
janela = Tk()
janela.title('Informações do Pedido')
janela.geometry('295x198')
janela.resizable(False, False)
# janela.iconbitmap(default='') # informar a imagem da janela .ico


label_trans = Label(janela, text = "Código da Transportadora:")
label_trans.grid(column=0, row = 0, padx=5, pady=5)
entrada_trans = Entry(janela,width=15, justify='center')
entrada_trans.grid(column=1, row=0, padx=10, pady=5)

label_redesp = Label(janela, text = "Código do Redespacho:", justify='right')
label_redesp.grid(column=0, row=1, padx=5, pady=5)
entrada_redespacho = Entry(janela,width=15, justify='center')
entrada_redespacho.grid(column=1, row=1, padx=10, pady=5)

label_qtd = Label(janela, text = "Quantidade de Volumes:", justify='right')
label_qtd.grid(column=0, row=2, padx=5, pady=5)
entrada_volume = Entry(janela,width=15, justify='center')
entrada_volume.grid(column=1, row=2, padx=10, pady=5)

label_esp = Label(janela, text = "Tipo de Volume:", justify='right')
label_esp.grid(column=0, row=3, padx=5, pady=5)
cb_especie=ttk.Combobox(janela,values=listVolumes, width=12, state='readonly')
cb_especie.grid(column=1, row=3, padx=10, pady=5)

label_icms = Label(janela, text = "Tem ICMS de 4%:", justify='right')
label_icms.grid(column=0, row=4, padx=5, pady=5)
cb_icms=ttk.Combobox(janela,values=listIcms, width=12, state='readonly')
cb_icms.set(listIcms[1])
cb_icms.grid(column=1, row=4, padx=10, pady=5)

    
btn_iniciar = Button(janela, text="Iniciar",command=pegarInfo, width=12)
btn_iniciar.grid(column=0, row=5, padx=5, pady=5)

btn_sair = Button(janela, text="Sair",command=quit, width=12)
btn_sair.grid(column=1, row=5, padx=0, pady=5)

janela.mainloop()


aviso = messagebox.showinfo('Atenção', 'Favor não tocar no mouse e teclado durante o processo!')


# Preparação para NF
try:
    sleep(1)
    #pyautogui.click(1200,317,duration=0.5) # Mostrar
    pyautogui.click(1197,342,duration=0.5) # Processar
    sleep(1.5)
    pyautogui.click(pyautogui.locateCenterOnScreen('sim.png', minSearchTime=5),duration=0.5) # Transferir itens
    sleep(1)
    pyautogui.moveTo(642,500, duration=0.2)
    pyautogui.click(pyautogui.locateCenterOnScreen('nao.png', minSearchTime=10),duration=0.5) # Não fechar NF
    sleep(0.5)
    pyautogui.click(pyautogui.locateCenterOnScreen('nf.png', minSearchTime=2),duration=0.5) # Abrir NF
    sleep(1.5)

    # Localizar tipo de produtos para selecionar frase
    pyautogui.moveTo(1125,379, duration=0.5)
    try:
        try:
            pvc = pyautogui.locateCenterOnScreen('pvc.png', minSearchTime=1)
            pyautogui.moveTo(pvc, duration=0.4)
            frase_pvc = '71'
        except:
            frase_pvc = '0'

        try:
            espuma = pyautogui.locateCenterOnScreen('espuma.png')
            pyautogui.moveTo(espuma, duration=0.4)
            frase_espuma = '70'
        except:
            frase_espuma = '0'

        if icms == 'Sim':
            frase_icms = '75'
        else:
            frase_icms = '0'
        
    except:
        messagebox.showinfo('Aviso','Erro')
        quit()

    # Monta as frases dependendo dos itens na nota
    if frase_espuma != '0' or frase_pvc != '0':
        frases = [frase_pvc, frase_espuma, frase_icms]
        frases.sort(reverse=True)
    else:
        frases = ['33',frase_icms]
    
    
    # Tela da NF
    pyautogui.click(64,144,duration=0.5) # Diversos
    sleep(2)

    pyautogui.click(225,87,duration=0.5) # Transportadora
    pyautogui.write(transportadora)

    if redespacho == '0' or redespacho == '':
        tem_redespacho = False
    else:
        tem_redespacho = True
        pyautogui.click(220,163,duration=0.5) # Redespacho
        pyautogui.write(redespacho)

    pyautogui.click(190,212,duration=0.5) # Quantidade de volumes
    pyautogui.write(volume)

    pyautogui.click(229,211,duration=0.5) # Tipo de volume
    pyautogui.write(especie)

    pyautogui.doubleClick(173,266,duration=0.5) # Frase
    for frase in frases:        
        pyautogui.write(str(frase))
        pyautogui.keyDown('enter')
        pyautogui.keyDown('enter')
        sleep(0.5)

    sleep(0.5)
    pyautogui.click(1324,38,duration=0.5) # Processar

    # Frete do redespacho
    if tem_redespacho: 
        pyautogui.click(1244,109,duration=0.5) 
        pyautogui.doubleClick(519,340,duration=1)
        pyautogui.write('F')
        pyautogui.keyDown('enter')
        pyautogui.click(998,234,duration=1)

    pyautogui.click(1246,61,duration=0.5) # Fechar
    sleep(0.5)
    
    fechar = True
    sim = True
    continuar = True
    certificado = True
    
    while fechar: # Clica em sim, continuar ou imprimi certificado enquanto tiver
        try:
            clica_sim = pyautogui.locateCenterOnScreen('sim.png', minSearchTime=2)
            pyautogui.click(clica_sim.x, clica_sim.y, duration=0.3) # Sim
            pyautogui.moveTo(642,500,duration=0.2)
            sim = True
        except:
            sim = False
        
        try:
            if continuar == True:
                clica_continuar = pyautogui.locateCenterOnScreen('continuar.png', minSearchTime=1)
                pyautogui.click(clica_continuar.x, clica_continuar.y, duration=0.3) # Continuar
                pyautogui.moveTo(642,500,duration=0.2)
                sleep(2)
                continuar = True
            else:
                continuar = False
        except:
            continuar = False

        try:
            if certificado == True:
                clica_imprimir = pyautogui.locateCenterOnScreen('imprimir.png', minSearchTime=2)
                pyautogui.click(clica_imprimir.x, clica_imprimir.y, duration=0.5)
                clica_ok = pyautogui.locateCenterOnScreen('ok.png', minSearchTime=1)
                pyautogui.click(clica_ok.x, clica_ok.y, duration=0.3)
                clica_sair = pyautogui.locateCenterOnScreen('sair.png', minSearchTime=1.5)
                pyautogui.click(clica_sair.x, clica_sair.y, duration=1)
                certificado = True
        except:
            certificado = False


        if sim == True or continuar == True or certificado == True:
            fechar = True
        else:
            fechar = False


    pyautogui.click(1313,40,duration=0.5) # Ok
    sleep(2)

    messagebox.showinfo('Aviso','Finalizado com Sucesso!')
except:
    messagebox.showwarning('Aviso', 'Execução encerrada!')