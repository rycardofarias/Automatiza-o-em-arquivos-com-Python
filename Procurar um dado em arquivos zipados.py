import os
import zipfile

# Função para ler o conteúdo do arquivo documento.txt e verificar a sigla
def verificar_sigla(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linha = arquivo.readline()
        dados = linha.split('|')
        sigla = dados[7]  # A posição 7 contém a sigla

        return sigla != 'SP'

# Diretório raiz onde estão os diretórios
diretorio_raiz = r'C:\diretorio'

# Percorre os diretórios
for diretorio, subdiretorios, arquivos in os.walk(diretorio_raiz):
    for arquivo in arquivos:
        if arquivo == 'documento.zip':
            caminho_zip = os.path.join(diretorio, arquivo)
            caminho_extracao = os.path.join(diretorio, 'extracao')
            
            # Extrai o conteúdo do arquivo zip
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(caminho_extracao)
            
            # Verifica se a sigla é diferente de "SP"
            caminho_arquivo_txt = os.path.join(caminho_extracao, 'documento.txt')
            if verificar_sigla(caminho_arquivo_txt):
                print(f'Diretório: {diretorio}\nArquivo: {arquivo}\n')
