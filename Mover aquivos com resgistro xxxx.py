import os

# Função para verificar se o arquivo contém a informação |xxxx|
def contem_registro_xxxx(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
        for linha in arquivo:
            if '|xxxx|' in linha:
                return True
    return False

diretorio_raiz = r'diretorio'

# Percorre os diretórios
for diretorio, subdiretorios, arquivos in os.walk(diretorio_raiz):
    for arquivo in arquivos:
        if arquivo.endswith('.txt'):
            caminho_arquivo_txt = os.path.join(diretorio, arquivo)
            
            # Verifica se o arquivo contém o registro |xxxx|
            if contem_registro_xxxx(caminho_arquivo_txt):
                print(f'Arquivo: {arquivo}\n')