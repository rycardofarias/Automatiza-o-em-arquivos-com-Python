import os
import shutil

# Diretório raiz onde estão os diretórios
diretorio_raiz = r'C:\diretorio'

versao_layout = '010'
filtro = "-"+versao_layout+"-"
nome_arquivo_saida = f'arquivos_encontrados-versao{versao_layout}.txt'

# Caminho para o arquivo de texto
caminho_arquivo_saida = fr'C:\diretorio\{nome_arquivo_saida}'

# Lista para armazenar os nomes dos arquivos
arquivos_encontrados = []

print(f'Executando - '+ versao_layout)

# Percorre os diretórios
for diretorio, subdiretorios, arquivos in os.walk(diretorio_raiz):
    for arquivo in arquivos:
        if arquivo.endswith('.txt') and filtro in arquivo:
            # Adiciona o nome do arquivo à lista
            arquivos_encontrados.append(arquivo)

# Cria um arquivo de texto para armazenar os nomes
with open(caminho_arquivo_saida, 'w') as arquivo_saida:
    for arquivo in arquivos_encontrados:
        arquivo_saida.write(arquivo + '\n')

# Cria a pasta para mover os arquivos
pasta_versao = os.path.join(diretorio_raiz, versao_layout)
os.makedirs(pasta_versao, exist_ok=True)

# Move os arquivos para a pasta de versão
for arquivo in arquivos_encontrados:
    caminho_origem = os.path.join(diretorio_raiz, arquivo)
    caminho_destino = os.path.join(pasta_versao, arquivo)
    shutil.move(caminho_origem, caminho_destino)

print(f'Busca finalizada. Nomes dos arquivos foram salvos em {caminho_arquivo_saida}')
print(f'Arquivos movidos para a pasta {versao_layout}.')