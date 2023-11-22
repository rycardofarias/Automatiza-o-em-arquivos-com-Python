import re

# Função para extrair palavras que possui "tb"
def extrair_tabelas(linha):
    palavras = linha.split()
    tabelas = re.findall(r'\btb\w*', linha)
    return tabelas

# Função para ler o arquivo e extrair tabelas
def extrair_tabelas_do_arquivo(nome_arquivo):
    tabelas_encontradas = set()  # Usar um conjunto para evitar duplicatas

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            tabelas_encontradas.update(extrair_tabelas(linha))

    return list(tabelas_encontradas)

# Função para imprimir tabelas em ordem alfabética
def imprimir_tabelas_ordenadas(tabelas):
    tabelas_ordenadas = sorted(tabelas)
    for tabela in tabelas_ordenadas:
        print(tabela)

# Nome do arquivo que você deseja analisar
nome_arquivo = r'C:\diretorio\arquivo.txt'

tabelas_encontradas = extrair_tabelas_do_arquivo(nome_arquivo)

imprimir_tabelas_ordenadas(tabelas_encontradas)