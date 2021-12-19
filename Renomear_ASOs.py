#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# codigo criado no ambiente linux
# usando ocrmypdf instalado na propria maquina
# apt-get install ocrmypdf -q
# usa tesseract


# In[ ]:


print('Iniciando...')
import os 
import pathlib
import pdfplumber
import shutil
# import fnmatch as fn # para buscar data com caracteres coringa: ??-??-????


# In[ ]:


# TODO: incluir data de resultado do exame no nome do arquivo (fnmatch ?)
# TODO: criar procedimento para separar os arquivos nao renomeados para a pasta 'Falhas'
# TODO: testar com arquivos de diferentes qualidades
# TODO: ciar planilha com nomes e datas dos arquivos copiados e nao copiados
# TODO: simplificar mensagens
# TODO: fazer com que as mensagens do bloco 'criar pastas' aparecem apenas uma vez


# In[ ]:


# pegar current working directory
pasta_atual = os.getcwd()
caminho = pathlib.Path(r'{}'.format(pasta_atual))

# iterar sobre os arquivos da pasta
for arquivo in caminho.iterdir():
    nome_arquivo = arquivo.name #capturar nome do arquivo
    if '.pdf' in nome_arquivo:
        print(f'Criando copia de {nome_arquivo} ...')

        # criar novo pdf com OCR
        os.system(f'ocrmypdf {nome_arquivo} output.pdf') # comando do proprio sistema atraves do terminal

        # pegar nome do funcionário no novo PDF
        with pdfplumber.open('output.pdf') as pdf_OCR:
            pagina = pdf_OCR.pages[0]
            texto_pagina = pagina.extract_text(x_tolerance=2)

        # tratar texto e transformar em lista
        print('Extraindo texto...')
        texto_final = texto_pagina
        texto_final = texto_final.upper()
        texto_final = texto_final.replace(' \n', '\n')
        texto_final = texto_final.replace('  ', ' ')
        texto_final = texto_final.replace('\n ', '\n')
        texto_final = texto_final.replace('\n\n', '\n')
        texto_final = texto_final.replace('/', '-')
        texto_final = texto_final.replace(':', '_')
        texto_final = texto_final.replace('[', '')
        texto_final = texto_final.replace(']', '')
        texto_final = texto_final.splitlines()

        # iterar sobre a lista texto_final para pegar nome do funcionario
        for indice, item in enumerate(texto_final):
            if 'Funcio' in item or 'funcio' in item:
                nome_funcionario = texto_final[indice+1] # item logo após a palavra Funcionario
                nome_funcionario = nome_funcionario.split('_', 1) # retorna lista com 2 itens
                nome_funcionario = nome_funcionario[1].strip()
                break
              
        # Renomear output.pdf
        print('Renomeando arquivo...')
        arquivo_renomeado = f'ASO {nome_funcionario}.pdf'
        os.rename('output.pdf', arquivo_renomeado)

        # criar pastas Renomeados (para os novos PDFs), Originais (para os antigos)
        # e Falhas (para os que não deu pra renomear)

        # criar pastas
        
        try:
            print('Criando pastas...')
            os.mkdir(f'{caminho}/Renomeados OCR')
            os.mkdir(f'{caminho}/Originais')
            os.mkdir(f'{caminho}/Falhas')
            # se as pastas ja existem, pular etapa
        except FileExistsError:
                print('Criacao cancelada, as pastas ja existem')
            pass

        # mover arquivo
        print('Movendo arquivo')
        shutil.move(f'{caminho}/{arquivo_renomeado}',f'{caminho}/Renomeados OCR/{arquivo_renomeado}')
        shutil.move(f'{caminho}/{nome_arquivo}',f'{caminho}/Originais/{nome_arquivo}')
        
print('Concluído!')

