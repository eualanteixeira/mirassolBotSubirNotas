# Bot Subir NF

Automação em Python que faz login no portal SAP Ariba (Petrobras) e sobe faturas
(notas fiscais de serviço) a partir de uma planilha Excel, anexando o PDF
correspondente de cada nota. O script principal está em
[src/main/main.py](../src/main/main.py).

## Visão geral do fluxo

1. Abre duas janelas de seleção (`tkinter.filedialog`):
   - Planilha Excel com a lista de faturas a processar.
   - Pasta onde estão os PDFs das notas fiscais (anexos).
2. Registra hotkeys globais para controlar a execução (ver [Controles em tempo de execução](#controles-em-tempo-de-execução)).
3. Abre o Chrome via Selenium (WebDriver gerenciado automaticamente pelo `webdriver_manager`) e navega até `https://service-2.ariba.com/Supplier.aw/`.
4. Para cada linha da planilha:
   1. Lê os campos necessários (contrato, RM, CNPJ, valor de frete, cidade, número da NF, série, filial, classificação LC 116/2003, valor de retenção).
   2. Faz login escolhendo usuário/senha conforme o CNPJ da Mirassol (`CNPJMir`) — ver [Credenciais por CNPJ](#credenciais-por-cnpj).
   3. Fecha banners de cookies/pop-ups da Ariba.
   4. Clica em "Criar" → "Fatura fora da PO" → avança.
   5. Preenche número da nota, modelo do documento fiscal ("56 - NF Serviço Eletrônica"), anexa o PDF correspondente (`<pasta>\<serie>-<Nota>.pdf`).
   6. Preenche lastro de obrigação, identificação (CNPJ), contrato, RM, CNPJ tomador (Petrobras, fixo), município, classificação LC 116/2003 e valor de retenção.
   7. Adiciona o item da fatura (quantidade fixa "1", preço = valor do frete SAP) e marca o(s) checkbox(es) relacionados.
   8. Avança e envia a fatura, depois sai da tela.
   9. Remove a linha processada da planilha e salva o Excel (checkpoint de progresso — evita reprocessar faturas já enviadas se o bot for reiniciado).
5. O processo é resiliente a elementos que ainda não carregaram: cada etapa fica em um laço `while True` tentando localizar o elemento até conseguir, chamando `controle.checkpoint()` a cada tentativa falha (o que também permite pausar/encerrar o bot nesse ponto).

## Credenciais por CNPJ

O login/senha usados no Ariba são escolhidos com base no CNPJ da Mirassol (`CNPJMir`) lido da planilha:

| CNPJ Mirassol         | Login                                          |
|-----------------------|-------------------------------------------------|
| 14.937.348/0004-67    | petrobras000467@expressomirassol.com.br         |
| 14.937.348/0008-90    | petrobras000890@expressomirassol.com.br         |
| 14.937.348/0011-96    | petrobras001196@expressomirassol.com.br         |
| 14.937.348/0001-14    | petrobras000114Hom@expressomirassol.com.br      |
| 14.937.348/0007-00    | petrobras000700@expressomirassol.com.br         |

> ⚠️ As senhas estão gravadas diretamente no código-fonte (texto puro). Isso é um risco de
> segurança: qualquer pessoa com acesso ao `.py` ou ao executável gerado (via engenharia
> reversa) consegue extraí-las. O ideal é migrar para variáveis de ambiente, um arquivo
> `.env` (fora do controle de versão) ou um cofre de segredos.

## Colunas esperadas na planilha Excel

| Coluna                          | Uso                                                             |
|----------------------------------|------------------------------------------------------------------|
| `Classificação LC 116/2003`     | Define o texto do serviço prestado (`16.02` ou `11.04`)         |
| `Contrato`                      | Número do contrato (parte antes do primeiro `.`)                 |
| `RM`                             | Número do Relatório de Medição                                   |
| `CNPJ MIRASSOL`                 | CNPJ da filial Mirassol, define login/senha usados                |
| `Valor Retencao`                | Valor de retenção da fatura                                       |
| `Cidade Origem`                 | Município (formato `Cidade/UF` é convertido para `Cidade (UF)`)  |
| `Valor do Frete - SAP`          | Preço do item da fatura                                          |
| `N° NF`                         | Número da nota fiscal (usado no nome do arquivo PDF)              |
| `FILIAL`                        | Filial (usado apenas em log)                                     |
| `Serie`                         | Série da nota (usado no nome do arquivo PDF)                     |

O PDF de cada nota deve estar na pasta selecionada com o nome
`<Serie>-<N° NF>.pdf`.

## Controles em tempo de execução

A classe `ControleExecucao` ([src/main/main.py:37](../src/main/main.py#L37)) registra
hotkeys globais (via `keyboard`) que funcionam mesmo com o Chrome em foco:

- **Ctrl+Shift+Space** — pausa/retoma a automação (`alternar_pausa`).
- **Ctrl+Shift+Q** — encerra a automação (`finalizar`): fecha o driver do Chrome,
  mata processos `chromedriver.exe` residuais e interrompe o laço principal.

Notificações do sistema (via `plyer.notification`) informam pausa/retomada/encerramento.
Enquanto pausado, o bot fica bloqueado no método `checkpoint()`, que também é o ponto em
que o encerramento (`SystemExit`) é lançado para parar a execução de forma limpa.

## Logging

Cada execução gera um arquivo de log `AAAA_MM_DD_HH_MM_SS.log` no diretório de trabalho
(nome baseado no horário de início), além de exibir as mensagens no console
(`logging.StreamHandler`).

## Dependências principais

Definidas em [pyproject.toml](../pyproject.toml):

- `selenium` + `webdriver-manager` — automação do navegador Chrome.
- `botcity-framework-core` — importado (`DesktopBot`) mas não utilizado no fluxo atual.
- `pandas` + `openpyxl` — leitura/escrita da planilha Excel.
- `keyboard` — hotkeys globais de pausa/encerramento.
- `plyer` — notificações nativas do sistema.
- `pyautogui` — alertas (`pyautogui.alert`) em cenários de erro.
- `auto-py-to-exe` — geração do executável Windows (ver seção abaixo).

## Gerando o executável (PyInstaller / auto-py-to-exe)

O executável Windows "Subir NFS" é gerado com o PyInstaller através do comando abaixo
(equivalente ao que a interface do `auto-py-to-exe` produz):

```bash
pyinstaller --noconfirm --onefile --windowed --name "Subir NFS" --add-data "C:\Users\automacao\Documents\botSubirNF\resources;resources/" --collect-all "botcity" --collect-all "plyer" --collect-all "keyboard" --collect-all "selenium" --collect-all "webdriver_manager"  "C:\Users\automacao\Desktop\Bot Subir NFS\main.py"
```

Detalhes das flags:

- `--noconfirm` — sobrescreve a saída anterior (`dist/`, `build/`) sem pedir confirmação.
- `--onefile` — empacota tudo em um único `.exe`.
- `--windowed` — não abre um terminal/console junto com a aplicação (modo GUI).
- `--name "Subir NFS"` — nome do executável gerado (`dist/Subir NFS.exe`).
- `--add-data "...resources;resources/"` — inclui a pasta [resources/](../resources)
  (imagens usadas por automações baseadas em reconhecimento de imagem, como `botcity`/`pyautogui`)
  dentro do pacote, mantendo o caminho relativo `resources/`.
- `--collect-all "<pacote>"` — garante que todos os submódulos, dados e binários dos
  pacotes `botcity`, `plyer`, `keyboard`, `selenium` e `webdriver_manager` sejam incluídos
  (esses pacotes costumam usar importação dinâmica/plugins que o PyInstaller não detecta
  automaticamente).

Após a build, o executável fica em `dist/Subir NFS.exe`. Para reproduzir a build pela
interface gráfica, basta abrir `auto-py-to-exe` (já incluído nas dependências do projeto)
e configurar as mesmas opções acima.

## Limitações e pontos de atenção conhecidos

- Seletores de elementos da página Ariba (IDs como `_sy6frd`, `_lsd8ld`, etc.) são gerados
  pelo framework do site e podem mudar em atualizações do Ariba, quebrando a automação.
- Não há tratamento de timeout máximo nos laços `while True` de busca de elementos — se um
  elemento nunca aparecer, o bot tenta indefinidamente até ser encerrado manualmente
  (Ctrl+Shift+Q). A única exceção é o upload do anexo, que aborta após 100 tentativas.
- Senhas em texto puro no código-fonte (ver [Credenciais por CNPJ](#credenciais-por-cnpj)).
