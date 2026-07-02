#teste
import pyautogui
import time
import os
import logging
import keyboard
from plyer import notification
from datetime import datetime
from botcity.core import DesktopBot
from selenium import webdriver
from selenium.common import TimeoutException
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

base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "log")
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ControleExecucao:
    """Controla pausa/retomada e encerramento da automação via hotkeys globais."""

    def __init__(self):
        self.pausado = False
        self.rodando = True
        self.driver = None

    def alternar_pausa(self):
        self.pausado = not self.pausado
        if self.pausado:
            print("Automação pausada")
            logger.info("Automação pausada (ctrl+shift+space)")
            self.notificar("Automação pausada")
        else:
            print("Automação retomada")
            logger.info("Automação retomada (ctrl+shift+space)")
            self.notificar("Automação retomada")

    def finalizar(self):
        print("Encerrando automação")
        logger.info("Encerramento solicitado (ctrl+shift+q)")
        self.notificar("Encerrando automação")
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Erro ao encerrar o driver do Chrome: {e}")
        os.system("taskkill /f /im chromedriver.exe")
        self.rodando = False

    def checkpoint(self):
        while self.pausado and self.rodando:
            time.sleep(0.2)
        if not self.rodando:
            raise SystemExit("Automação encerrada pelo usuário")

    def iniciar_hotkeys(self):
        keyboard.add_hotkey('ctrl+shift+space', self.alternar_pausa)
        keyboard.add_hotkey('ctrl+shift+q', self.finalizar)

    def notificar(self, mensagem):
        try:
            notification.notify(
                title="Bot Subir NF",
                app_name="Bot Subir NF",
                message=mensagem,
                timeout=3,
            )
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")


controle = ControleExecucao()


def automacao_selenium():
    root = tk.Tk()
    root.withdraw()

    # Abre o seletor de arquivos
    # PATH =
    caminho_arquivo = filedialog.askopenfilename(title="Caminho do arquivo excel: ")
    caminho_arquivo_nfs = filedialog.askdirectory(title="Caminho da pasta dos anexos: ")
    # caminho_arquivo = 'C:\\Visual_Rodopar\\Bot_Subir_Notas\\Planilha NF.xlsx'
    controle.iniciar_hotkeys()
    logger.info("Hotkeys ativas: ctrl+shift+space pausa/retoma o bot, ctrl+shift+q encerra o bot.")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.set_capability("acceptInsecureCerts", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    controle.driver = driver
    driver.get('https://service-2.ariba.com/Supplier.aw/')

    Logando = True
    wait = WebDriverWait(driver, 10)
    #Rodando a pasta
    #Ler a lista de faturas a extrair
    listaFaturas = pd.read_excel(caminho_arquivo)
    feitos = pd.DataFrame(columns=listaFaturas.columns)
    for Faturas in range(len(listaFaturas)):
        controle.checkpoint()
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
        classificacao_lc = pegar_valor('Classificação LC 116/2003')
        contrato = pegar_valor('Contrato').split('.')[0]
        rm = pegar_valor('RM')
        CNPJMir = pegar_valor('CNPJ MIRASSOL')
        CNPJPetro = '33.000.167/0001-01'
        valorRetencao = pegar_valor('Valor Retencao')
        municipio_raw = pegar_valor('Cidade Origem')
        ValorSAP = pegar_valor('Valor do Frete - SAP')
        Nota = pegar_valor('N° NF')
        Filial = pegar_valor('FILIAL')
        serie = pegar_valor('Serie')
        logger.info("agora vem o primeiro bot")
        if "/" in municipio_raw:
            cidade, uf = municipio_raw.split("/", 1)
            municipio = f"{cidade.strip()} ({uf.strip()})"
        else:
            municipio = municipio_raw
        NumeroNota = Nota
        logger.info(Nota)
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
                logger.warning("Campo de usuário não encontrado")
                controle.checkpoint()


        while Logando:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_sy6frd')))
                btnAvancar = driver.find_element(By.ID, '_sy6frd')
                btnAvancar.click()
                break
            except:
                logger.warning("Botão entrar usuário não encontrado")
                controle.checkpoint()

        while Logando:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, 'Password')))
                campoSenha = driver.find_element(By.ID, 'Password')
                campoSenha.send_keys(senha)
                break
            except:

                logger.warning("Campo de senha não encontrado")
                controle.checkpoint()

        while Logando:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'submitButton')))
                btnEntrar = driver.find_element(By.ID, 'submitButton')
                btnEntrar.click()
                break
            except:
                logger.warning("Botão entrar senha não encontrado")
                controle.checkpoint()


        while True:
            try:
                driver.execute_script("""
    var overlay = document.getElementById('trustarc-banner-overlay');  // Replace with the actual ID of the banner
    if (overlay) {
    overlay.style.display = 'none';  // Hides the banner
    }
    """)
            except:
                logger.debug("aaa")
            try:
                time.sleep(5)
                wait.until(EC.element_to_be_clickable((By.ID, 'truste-consent-button')))
                btnCookies = driver.find_element(By.ID, 'truste-consent-button')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnCookies)
                btnCookies.click()
                time.sleep(5)
            except:
                logger.warning("Não achei os cookies")
                controle.checkpoint()

            try:
                btnFechar = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.target-lt-popupv2-close'))
                )
                btnFechar.click()
            except TimeoutException:
                logger.warning("Não achei o pop-up")
                controle.checkpoint()

            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'create-btn')))
                btnCriar = driver.find_element(By.ID, 'create-btn')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnCriar)
                btnCriar.click()
                Logando = False
                break
            except:
                logger.warning("Botão criar não encontrado")
                controle.checkpoint()
        while True:
            try:
                driver.execute_script("""
    var overlay = document.getElementById('trustarc-banner-overlay');  // Replace with the actual ID of the banner
    if (overlay) {
    overlay.style.display = 'none';  // Hides the banner
    }
    """)
            except:
                logger.debug("aaa")
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'an.non_po_invoice')))
                btnFaturaForadaPO = driver.find_element(By.ID, 'an.non_po_invoice')
                btnFaturaForadaPO.click()
                break
            except:
                logger.warning("Botão fatura fora da PO não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_lsd8ld')))
                btnAvancarFatura = driver.find_element(By.ID, '_lsd8ld')
                btnAvancarFatura.click()
                break
            except:
                logger.warning("Botão avançar fatura não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_sarwgb')))
                inputNotaFiscal = driver.find_element(By.ID, '_sarwgb')
                inputNotaFiscal.send_keys(NumeroNota)
                break
            except:
                logger.warning("Campo de nota fiscal não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão modelo documento fiscal não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_2h2c5c')))
                btnAdicionarAnexo= driver.find_element(By.ID, '_2h2c5c')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAdicionarAnexo)
                btnAdicionarAnexo.click()
                break
            except:
                logger.warning("Botão adicionar anexo não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_jbqvrb')))
                btnAnexo = driver.find_element(By.ID, '_jbqvrb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAnexo)
                btnAnexo.click()
                break
            except:
                logger.warning("Botão anexo não encontrado")
                controle.checkpoint()
        contando=0
        while True:
            try:
                logger.info(Filial)
                logger.info(Nota)
                contando+=1
                file_input = driver.find_element(By.NAME, "_lqy5hc")
                driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
                # caminho_arquivo_nfs = filedialog.askdirectory(title="Caminho dos anexos: ")
                file_input.send_keys(caminho_arquivo_nfs + '\\' + serie + '-' + Nota + '.pdf')
                break
            except:
                logger.warning("Campo de arquivo não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão adicionar anexo não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão Lastro Obrigacao não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão Identificação não encontrado")
                controle.checkpoint()
        while True:
            try:
                driver.implicitly_wait(10)
                wait.until(EC.visibility_of_element_located((By.ID, '_yush9d')))
                btnAtualizar = driver.find_element(By.ID, '_yush9d')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAtualizar)
                btnAtualizar.click()
                break
            except:
                logger.warning("Botão atualizar não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_sm64zb')))
                inputContrato = driver.find_element(By.ID, '_sm64zb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputContrato)
                inputContrato.send_keys(contrato)
                break
            except:
                logger.warning("Campo de contrato não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '__rpqab')))
                inputRM = driver.find_element(By.ID, '__rpqab')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputRM)
                inputRM.send_keys(str(rm).split('.')[0])
                break
            except:
                logger.warning("Campo de RM não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_ggf0yb')))
                inputCNPJ = driver.find_element(By.ID, '_ggf0yb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputCNPJ)
                inputCNPJ.send_keys(CNPJMir)
                break
            except:
                logger.warning("Campo de CNPJ não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_ed1r0b')))
                inputTomador = driver.find_element(By.ID, '_ed1r0b')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputTomador)
                inputTomador.send_keys(CNPJPetro)
                break
            except:
                logger.warning("Campo de tomador não encontrado")
                controle.checkpoint()
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
                logger.warning("Escolha de Município não encontrada")
                controle.checkpoint()
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
            
            if classificacao_lc == '16.02':
                classificacao = '16.02 Outros serviços de transporte de natureza municipal.'
            elif classificacao_lc == '11.04':
                classificacao = '11.04 Armazenamento, depósito, carga, descarga, arrumação e guarda de bens de qualquer espécie.'   

            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_z2jfab')))
                btnLC = driver.find_element(By.ID, '_z2jfab')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnLC)
                btnLC.click()
                drop93 = driver.find_elements(By.CLASS_NAME, 'w-dropdown-item')
                for item in drop93[::-1]:
                    if classificacao in item.text:
                        item.click()
                        break
                break
            except:
                logger.warning("Escolha de classificação LC não encontrada")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, '_$dddb')))
                inputTomador = driver.find_element(By.ID, '_$dddb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputTomador)
                inputTomador.send_keys(str(valorRetencao).replace('.',',').replace('-', ''))
                break
            except:
                logger.warning("Campo de valor retencao não encontrado")
                controle.checkpoint()

        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_g053ud')))
                btnAdicionar = driver.find_element(By.ID, '_g053ud')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAdicionar)
                btnAdicionar.click()
                break
            except:
                logger.warning("Botão Adicionar não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_ipc3qb')))
                btnGeral = driver.find_element(By.ID, '_ipc3qb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnGeral)
                btnGeral.click()
                break
            except:
                logger.warning("Botão Geral não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_xayoyc')))
                inputQt = driver.find_element(By.ID, '_xayoyc')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputQt)
                inputQt.send_keys('1')
                break
            except:
                logger.warning("Input Quantidade de Itens não encontrado")
                controle.checkpoint()
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_29vmnb')))
                inputPreco = driver.find_element(By.ID, '_29vmnb')
                driver.execute_script("arguments[0].scrollIntoView(true);", inputPreco)
                inputPreco.send_keys(str(ValorSAP).replace('.',',').replace('-', ''))
                break
            except:
                logger.warning("Input Preço não encontrado")
                controle.checkpoint()
            # try:
            #     div_elements = WebDriverWait(driver, 20).until(
            #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-chk.w-chk-dsize")))
            #     total_divs = len(div_elements)
            #     print(f"Total de <div> encontrados: {total_divs}")
            #     for div_element in div_elements:
            #         try:
            #             WebDriverWait(driver, 10).until(
            #             EC.element_to_be_clickable(div_element))
            #             div_element.click()
            #             print("Elemento clicado com sucesso.")
            #         except Exception as e:
            #             print("Erro ao clicar no elemento:", e)
            #     break
            # except Exception as e:
            #     print("Erro ao localizar os elementos:", e)
        while True:
            try:
                time.sleep(3)
                div_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-chk.w-chk-dsize")))
                total_divs = len(div_elements)
                logger.info(f"Total de <div> encontrados: {total_divs}")
                if total_divs > 0:
                    last_div = div_elements[-1]
                    try:
                        WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(last_div))
                        last_div.click()
                        logger.info("Último elemento clicado com sucesso.")
                    except Exception as e:
                        logger.error(f"Erro ao clicar no último elemento: {e}")
                else:
                    logger.warning("Nenhum elemento foi encontrado para clicar.")
                break
            except Exception as e:
                logger.error(f"Erro ao localizar os elementos: {e}")
        time.sleep(5)
        while True:
            try:
                wait.until(EC.element_to_be_clickable((By.ID, '_w_slkb')))
                btnAvancar = driver.find_element(By.ID, '_w_slkb')
                driver.execute_script("arguments[0].scrollIntoView(true);", btnAvancar)
                btnAvancar.click()
                break
            except:
                logger.warning("Botão Avançar não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão Enviar não encontrado")
                controle.checkpoint()
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
                logger.warning("Botão Sair não encontrado")
                controle.checkpoint()
        # with open(r'C:\Visual_Rodopar\Sub\Enviados.txt', 'a') as file:
        #     file.write("Fatura " + 'se' + '-'+ NumeroNota + ", em " + datetime.now().strftime('%d/%m/%Y %H:%M:%S \n'))
        # driver.get('https://portal.us.bn.cloud.ariba.com/dashboard/home')
        first_line = listaFaturas.iloc[0]
        listaFaturas = listaFaturas.iloc[1:]
        listaFaturas.to_excel(caminho_arquivo, index=False)

if __name__ == "__main__":
    logger.info("Inicia o processo do bot que fecha popups")

    try:
        automacao_selenium()
    except SystemExit as e:
        logger.info(str(e))
    except Exception as e:
        logger.error(f"Ocorreu um erro durante a execução do bot: {e}")

    finally:
        logger.info("Encerra o processo do bot depois que a automação terminar")
        logger.info('ok')
