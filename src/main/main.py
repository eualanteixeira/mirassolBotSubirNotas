#teste
import pyautogui
import time
import pandas
from datetime import datetime
from botcity.core import DesktopBot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from multiprocessing import Process
from selenium.webdriver.common.keys import Keys

#Alimentando todos os arquivos do diretório numa variavel


# class MeuBot(DesktopBot):
#     def action(self, execution=None):
#         while True:
#             if self.find("ok", matching=0.87, waiting_time=10000):
#                 self.click()
#                 time.sleep(5)
#                 print("achamos o OK")
#             if self.find("precisaF5", matching=0.87, waiting_time=5000):
#                 print("Dar F5")
#                 if self.find("aberturaEdge", matching=0.87, waiting_time=5000):
#                     self.click()
#                     print("Dei F5") 
#             else:
#                 print("Botão não encontrado.")
#             time.sleep(15)
# def monitorar_popup():
#     bot = MeuBot()
#     bot.action()

def automacao_selenium():
    root = tk.Tk()
    root.withdraw()

    # Abre o seletor de arquivos
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.set_capability("acceptInsecureCerts", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://service-2.ariba.com/Supplier.aw/')
    
    Logando = True
    wait = WebDriverWait(driver, 10)
    #Rodando a pasta
    #Ler a lista de faturas a extrair
    listaFaturas = pandas.read_excel(caminho_arquivo)
    feitos = pd.DataFrame(columns=listaFaturas.columns)
    for Faturas in range(len(listaFaturas)):
        contador = 0
        login=""
        senha=""
        def pegar_valor(coluna):
            try:
                return str(listaFaturas[coluna][Faturas])
            except Exception as e:
                pyautogui.alert(f"Erro ao acessar a coluna '{coluna}'. Verifique se ela existe na planilha.")
                raise e
        #Informar o código inicial da fatura
        contrato = pegar_valor('Contrato').split('.')[0]
        rm = pegar_valor('RM')
        CNPJMir = pegar_valor('CNPJ')
        CNPJPetro = '33.000.167/0001-01'
        valorRetencao = pegar_valor('Valor Retencao')
        municipio_raw = pegar_valor('Cidade Origem')
        ValorSAP = pegar_valor('Valor do Frete - SAP')
        Nota = pegar_valor('N° NF')
        Filial = pegar_valor('FILIAL')
        serie = pegar_valor('Serie')
        print("agora vem o primeiro bot")
        if "/" in municipio_raw:
            cidade, uf = municipio_raw.split("/", 1)
            municipio = f"{cidade.strip()} ({uf.strip()})"
        else:
            municipio = municipio_raw
        NumeroNota = Nota.split(serie)[1] 
        print(Nota)
        while Logando:
            try:
                                                
                wait.until(EC.visibility_of_element_located((By.ID, 'userid')))
                campoUsuario = driver.find_element(By.ID, 'userid')
                if CNPJMir == '14.937.348/0004-67':
                    login="petrobras000467@expressomirassol.com.br"
                    senha="Mirassol@23"
                elif CNPJMir == '14.937.348/0008-90':
                    login="petrobras000890@expressomirassol.com.br"
                    senha="Comercial@22"
                elif CNPJMir == '14.937.348/0011-96':
                    login="petrobras001196@expressomirassol.com.br"
                    senha="Comercial@22"
                elif CNPJMir== '14.937.348/0001-14':
                    login="petrobras000114Hom@expressomirassol.com.br"
                    senha="Mirassol@2024"
                elif CNPJMir== '14.937.348/0011-96':
                    login="petrobras001196@expressomirassol.com.br"
                    senha="Comercial@22"
                elif CNPJMir== '14.937.348/0007-00':
                    login="petrobras000700@expressomirassol.com.br"
                    senha="Comercial@22"
                campoUsuario.send_keys(login)
                break
            except:
                print("Campo de usuário não encontrado")
                
        
        while Logando:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_sy6frd')))
                btnAvancar = driver.find_element(By.ID, '_sy6frd')
                btnAvancar.click()
                break
            except: 
                print("Botão entrar usuário não encontrado")
        
        while Logando:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, 'Password')))
                campoSenha = driver.find_element(By.ID, 'Password')
                campoSenha.send_keys(senha)
                break
            except:
                
                print("Campo de senha não encontrado")
        
        while Logando:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'submitButton')))
                btnEntrar = driver.find_element(By.ID, 'submitButton')
                btnEntrar.click()
                break
            except:
                print("Botão entrar senha não encontrado")
                
        
        while True:
            try:
                driver.execute_script("""
    var overlay = document.getElementById('trustarc-banner-overlay');  // Replace with the actual ID of the banner
    if (overlay) {
    overlay.style.display = 'none';  // Hides the banner
    }
    """)
            except:
                print("aaa")
            try:
                time.sleep(5)
                wait.until(EC.element_to_be_clickable((By.ID, 'truste-consent-button')))
                btnCookies = driver.find_element(By.ID, 'truste-consent-button')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnCookies)
                btnCookies.click()
                time.sleep(5)
            except:
                print("Não achei os cookies")             
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'create-btn')))
                btnCriar = driver.find_element(By.ID, 'create-btn')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnCriar)
                btnCriar.click()
                Logando = False
                break
            except:
                print("Botão criar não encontrado")
        while True:
            try:
                driver.execute_script("""
    var overlay = document.getElementById('trustarc-banner-overlay');  // Replace with the actual ID of the banner
    if (overlay) {
    overlay.style.display = 'none';  // Hides the banner
    }
    """)
            except:
                print("aaa")
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'an.non_po_invoice')))
                btnFaturaForadaPO = driver.find_element(By.ID, 'an.non_po_invoice')
                btnFaturaForadaPO.click()
                break
            except:
                print("Botão fatura fora da PO não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_lsd8ld')))
                btnAvancarFatura = driver.find_element(By.ID, '_lsd8ld')
                btnAvancarFatura.click()
                break
            except:
                print("Botão avançar fatura não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_sarwgb')))
                inputNotaFiscal = driver.find_element(By.ID, '_sarwgb')
                inputNotaFiscal.send_keys(NumeroNota)
                break
            except:
                print("Campo de nota fiscal não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_rqrdvc')))
                btnModeloDocumentoFiscal = driver.find_element(By.ID, '_rqrdvc')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnModeloDocumentoFiscal)
                btnModeloDocumentoFiscal.click()
                drop93 = driver.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                for item in drop93[::-1]:
                    if "56 - NF Serviço Eletrônica" in item.text:
                        item.click()
                        break
                break
            except:
                print("Botão modelo documento fiscal não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_2h2c5c')))
                btnAdicionarAnexo= driver.find_element(By.ID, '_2h2c5c')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAdicionarAnexo)
                btnAdicionarAnexo.click()
                break
            except:
                print("Botão adicionar anexo não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_jbqvrb')))
                btnAnexo = driver.find_element(By.ID, '_jbqvrb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAnexo)
                btnAnexo.click()
                break
            except:
                print("Botão anexo não encontrado")
        contando=0
        while True:
            try:
                print(Filial)
                print(Nota)
                contando+=1
                file_input = driver.find_element(By.NAME, "_lqy5hc")
                driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
                file_input.send_keys(r'C:\Visual_Rodopar\NFs ' + Nota + '.pdf')
                break
            except:
                print("Campo de arquivo não encontrado")
                if contando > 100:
                    pyautogui.alert(f"Arquivo-{Nota}.pdf não encontrado")
                    sys.exit()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_ucj$3')))
                btnAdicionarAnexo = driver.find_element(By.ID, '_ucj$3')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAdicionarAnexo)
                btnAdicionarAnexo.click()
                break
            except:
                print("Botão adicionar anexo não encontrado") 
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_8wvuvc')))
                btnLastroObrigracao = driver.find_element(By.ID, '_8wvuvc')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnLastroObrigracao)
                btnLastroObrigracao.click()
                time.sleep(3)
                dropRM = btnLastroObrigracao.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                for item in dropRM:
                    if "Número do Contrato + Número do RM (Relatório de Medição)" in item.text:
                        item.click()
                        break
                break
            except:
                print("Botão Lastro Obrigacao não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_hal28')))
                btnIdentificacao = driver.find_element(By.ID, '_hal28')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnIdentificacao)
                btnIdentificacao.click()
                dropCNPJ = btnIdentificacao.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                time.sleep(3)
                for item in dropCNPJ:
                    if "CNPJ" in item.text:
                        item.click()
                        break
                break
            except:
                print("Botão Identificação não encontrado")
        while True:
            try:
                driver.implicitly_wait(10)
                wait.until(EC.visibility_of_element_located((By.ID, '_yush9d')))
                btnAtualizar = driver.find_element(By.ID, '_yush9d')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAtualizar)
                btnAtualizar.click()
                break
            except:
                print("Botão atualizar não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_sm64zb')))
                inputContrato = driver.find_element(By.ID, '_sm64zb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputContrato)
                inputContrato.send_keys(contrato)
                break
            except:
                print("Campo de contrato não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '__rpqab')))
                inputRM = driver.find_element(By.ID, '__rpqab')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputRM)
                inputRM.send_keys(str(rm).split('.')[0])
                break
            except:
                print("Campo de RM não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_ggf0yb')))
                inputCNPJ = driver.find_element(By.ID, '_ggf0yb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputCNPJ)
                inputCNPJ.send_keys(CNPJMir)
                break
            except:
                print("Campo de CNPJ não encontrado")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_ed1r0b')))
                inputTomador = driver.find_element(By.ID, '_ed1r0b')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputTomador)
                inputTomador.send_keys(CNPJPetro)
                break
            except:
                print("Campo de tomador não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_nsg0hd')))
                btnMunicipio = driver.find_element(By.ID, '_nsg0hd')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnMunicipio)
                btnMunicipio.click()
                # Monta o XPath procurando pelo texto do município
                # Aqui eu assumo que municipio é exatamente o texto visível no dropdown
                xpath_opcao = (
                    f"//div[contains(@class,'w-dropdown-item') "
                    f"and normalize-space(.) = '{municipio}']"
                )

                opcao = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcao)))
                opcao.click()
                # Pressiona ENTER para selecionar o primeiro item filtrado
                # drop93 = driver.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                # for item in drop93:
                #     if municipio.lower() in item.text.lower():
                #         item.click()
                #         break
                # btnMunicipio.send_keys(Keys.ENTER)
                break
            except:
                print("Escolha de Município não encontrada")
        # while True:
        #     try:
        #         wait.until(EC.element_to_be_clickable((By.ID, '_nsg0hd')))
        #         btnMunicipio = driver.find_element(By.ID, '_nsg0hd')
        #         driver.execute_script("arguments[0].scrollIntoView(true);", btnMunicipio)
        #         btnMunicipio.click()
        #         drop93 = driver.find_elements(By.CLASS_NAME, 'w-dropdown-item')
        #         for item in drop93[::-1]:
        #             print(municipio)
        #             if municipio in item.text:
        #                 item.click()
        #                 break
        #         break
        #     except:
        #         print("Escolha de Município não encontrada")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_z2jfab')))
                btnLC = driver.find_element(By.ID, '_z2jfab')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnLC)
                btnLC.click()
                drop93 = driver.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                for item in drop93[::-1]:
                    if '16.02 Outros serviços de transporte de natureza municipal. (Incluído pela Lei Complementar nº 157, de 2016)' in item.text:
                        item.click()
                        break
                break
            except:
                print("Escolha de classificação LC não encontrada")
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_$dddb')))
                inputTomador = driver.find_element(By.ID, '_$dddb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputTomador)
                inputTomador.send_keys(str(valorRetencao).replace('.',',').replace('-', ''))
                break
            except:
                print("Campo de valor retencao não encontrado")

        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_g053ud')))
                btnAdicionar = driver.find_element(By.ID, '_g053ud')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAdicionar)
                btnAdicionar.click()
                break
            except:
                print("Botão Adicionar não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_ipc3qb')))
                btnGeral = driver.find_element(By.ID, '_ipc3qb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnGeral)
                btnGeral.click()
                break
            except:
                print("Botão Geral não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_xayoyc')))
                inputQt = driver.find_element(By.ID, '_xayoyc')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputQt)
                inputQt.send_keys('1')
                break
            except:
                print("Input Quantidade de Itens não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_29vmnb')))
                inputPreco = driver.find_element(By.ID, '_29vmnb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputPreco)
                inputPreco.send_keys(str(ValorSAP).replace('.',',').replace('-', ''))
                break
            except:
                print("Input Preço não encontrado")
        while True:
            try:
                div_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-chk.w-chk-dsize")))
                total_divs = len(div_elements)
                print(f"Total de <div> encontrados: {total_divs}")
                for div_element in div_elements:
                    try:
                        WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(div_element))
                        div_element.click()
                        print("Elemento clicado com sucesso.")
                    except Exception as e:
                        print("Erro ao clicar no elemento:", e)
                break
            except Exception as e:
                print("Erro ao localizar os elementos:", e)
        while True:
            try:
                time.sleep(3)
                div_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-chk.w-chk-dsize")))
                total_divs = len(div_elements)
                print(f"Total de <div> encontrados: {total_divs}")
                if total_divs > 0:
                    last_div = div_elements[-1]
                    try:
                        WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(last_div))
                        last_div.click()
                        print("Último elemento clicado com sucesso.")
                    except Exception as e:
                        print("Erro ao clicar no último elemento:", e)
                else:
                    print("Nenhum elemento foi encontrado para clicar.")
                break
            except Exception as e:
                print("Erro ao localizar os elementos:", e)
        time.sleep(5)
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_w_slkb')))
                btnAvancar = driver.find_element(By.ID, '_w_slkb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAvancar)
                btnAvancar.click()
                break
            except:
                print("Botão Avançar não encontrado")
        while True:
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "multiDivContainer")))
                wait.until(EC.element_to_be_clickable((By.ID, '_jsl7tb')))
                btnEnviar = driver.find_element(By.ID, '_jsl7tb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnEnviar)
                time.sleep(1)
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
                btnEnviar.click()
                break
            except:
                print("Botão Enviar não encontrado")
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_qfivt')))
                btnSair = driver.find_element(By.ID, '_qfivt')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnSair)
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
                btnSair.click()
                # driver.get('https://portal.us.bn.cloud.ariba.com/dashboard/home')
                break
            except:
                print("Botão Sair não encontrado")
        # with open(r'C:\Visual_Rodopar\Sub\Enviados.txt', 'a') as file:
        #     file.write("Fatura " + 'se' + '-'+ NumeroNota + ", em " + datetime.now().strftime('%d/%m/%Y %H:%M:%S \n'))                    
        # driver.get('https://portal.us.bn.cloud.ariba.com/dashboard/home')
        first_line = listaFaturas.iloc[0]
        listaFaturas = listaFaturas.iloc[1:]
        listaFaturas.to_excel(caminho_arquivo, index=False)

if __name__ == "__main__":
    # Inicia o processo do bot que fecha popups
    # p = Process(target=monitorar_popup)
    # p.start()

    try:
        # Roda sua automação normalmente
        automacao_selenium()
    finally:
        # Encerra o processo do bot depois que a automação terminar
        # p.terminate()
        # p.join()
        print('ok')