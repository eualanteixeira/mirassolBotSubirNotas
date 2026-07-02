# Bot Subir NF

Automação em Python (RPA) que faz login no portal **SAP Ariba** (Petrobras) e sobe
faturas — notas fiscais de serviço — a partir de uma planilha Excel, anexando o PDF
correspondente de cada nota.

Uma planilha é lida linha a linha; para cada linha o bot abre uma fatura no Ariba,
preenche os campos necessários (contrato, RM, CNPJ, valor de frete, cidade, etc.),
anexa o PDF da nota e envia. A linha é removida da planilha após o envio, servindo
como checkpoint de progresso caso o bot precise ser reiniciado.

Documentação completa do fluxo, credenciais, colunas da planilha, controles em
tempo de execução e geração do executável: **[docs/bot_subir_nf.md](docs/bot_subir_nf.md)**.

## Requisitos

- Python `3.12.13`
- Google Chrome instalado (o WebDriver é gerenciado automaticamente pelo `webdriver-manager`)
- [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências

## Instalação

```bash
uv sync
```

## Uso

```bash
uv run src/main/main.py
```

Ao iniciar, o bot pede a planilha Excel com as faturas e a pasta com os PDFs das
notas fiscais. Durante a execução, use **Ctrl+Shift+Space** para pausar/retomar e
**Ctrl+Shift+Q** para encerrar. Detalhes em
[Controles em tempo de execução](docs/bot_subir_nf.md#controles-em-tempo-de-execução).

## Gerando o executável

O executável Windows ("Subir NFS") é gerado via PyInstaller/`auto-py-to-exe`. Veja o
comando completo em
[Gerando o executável](docs/bot_subir_nf.md#gerando-o-executável-pyinstaller--auto-py-to-exe).

## Estrutura do projeto

```
src/main/main.py     # script principal da automação
resources/           # imagens usadas em automações baseadas em reconhecimento de imagem
docs/                # documentação detalhada
```

## Pontos de atenção

- Seletores de elementos do Ariba podem mudar em atualizações do site, quebrando a automação.
- Laços de busca de elementos não têm timeout máximo (exceto o upload de anexo, limitado a 100 tentativas).
- As senhas de acesso ao Ariba estão em texto puro no código-fonte — ver
  [Credenciais por CNPJ](docs/bot_subir_nf.md#credenciais-por-cnpj) para o risco e recomendação de mitigação.
