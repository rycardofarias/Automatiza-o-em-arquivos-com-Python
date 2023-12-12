import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time

def contem_registro(caminho_arquivo, filtros):
    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
        for linha in arquivo:
            linha = linha.lower()
            for filtro in filtros:
                if filtro.lower() in linha:
                    return True
    return False

def buscar_e_copiar_arquivos(diretorio_raiz, filtros, diretorio_destino, barra_progresso, label_quantidade, label_progresso, button_executar):
    if not os.path.isdir(diretorio_raiz):
        tk.messagebox.showerror("Erro", "Diretório raiz inválido.")
        button_executar.config(state=tk.NORMAL)
        return

    if not os.path.isdir(diretorio_destino):
        tk.messagebox.showerror("Erro", "Diretório de destino inválido.")
        button_executar.config(state=tk.NORMAL)
        return

    arquivos_txt = [arquivo for arquivo in os.listdir(diretorio_raiz) if arquivo.endswith('.txt')]

    total_arquivos = len(arquivos_txt)
    barra_progresso["maximum"] = total_arquivos

    quantidade_encontrada = 0
    arquivos_encontrados = []
    arquivos_falha = []

    for indice, arquivo in enumerate(arquivos_txt, start=1):
        caminho_arquivo_txt = os.path.join(diretorio_raiz, arquivo)
        label_progresso.config(text=f"Arquivo atual: {arquivo}")
        if contem_registro(caminho_arquivo_txt, filtros):
            quantidade_encontrada += 1
            arquivos_encontrados.append(arquivo)
            shutil.copy(caminho_arquivo_txt, diretorio_destino)
        else:
            arquivos_falha.append(arquivo)
        barra_progresso["value"] = indice
        root.update_idletasks()

    with open('log_busca.txt', 'w') as log:
        log.write("Arquivos Encontrados:\n")
        for arquivo_encontrado in arquivos_encontrados:
            log.write(f"{arquivo_encontrado}\n")
        log.write("\nArquivos que não contêm os filtros:\n")
        for arquivo_falha in arquivos_falha:
            log.write(f"{arquivo_falha}\n")

    label_quantidade.config(text=f"Quantidade de arquivos encontrados: {quantidade_encontrada}")
    label_progresso.config(text="Busca Concluída!")
    button_executar.config(state=tk.NORMAL)

def buscar_arquivos():
    diretorio_raiz = filedialog.askdirectory()
    if diretorio_raiz:
        entry_diretorio.delete(0, tk.END)
        entry_diretorio.insert(0, diretorio_raiz)

def colar_caminho(event=None):
    diretorio_raiz = root.clipboard_get()
    entry_diretorio.delete(0, tk.END)
    entry_diretorio.insert(0, diretorio_raiz)

def escolher_diretorio_saida():
    diretorio_destino = filedialog.askdirectory()
    if diretorio_destino:
        entry_diretorio_destino.delete(0, tk.END)
        entry_diretorio_destino.insert(0, diretorio_destino)

def executar_busca():
    diretorio_raiz = entry_diretorio.get()
    filtros = entry_filtro.get()
    diretorio_destino = entry_diretorio_destino.get()

    if not diretorio_raiz or not diretorio_destino or not filtros:
        tk.messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if not os.path.isdir(diretorio_raiz) or not os.path.isdir(diretorio_destino):
        tk.messagebox.showerror("Erro", "Diretórios inválidos.")
        return

    filtros = filtros.split(',')
    button_executar.config(state=tk.DISABLED)
    buscar_e_copiar_arquivos(diretorio_raiz, filtros, diretorio_destino, barra_progresso, label_quantidade, label_progresso, button_executar)
    tk.messagebox.showinfo("Concluído", "Busca e cópia de arquivos concluídas com sucesso!")

# Criação da interface gráfica
root = tk.Tk()
root.title("Busca de Arquivos")

label_instrucao = tk.Label(root, text="Selecione um diretório raiz:")
label_instrucao.pack()

entry_diretorio = tk.Entry(root)
entry_diretorio.pack()
entry_diretorio.bind("<Button-3>", colar_caminho)  # Opção de colar com botão direito do mouse

button_selecionar_dir = tk.Button(root, text="Selecionar Diretório", command=buscar_arquivos)
button_selecionar_dir.pack()

label_filtro = tk.Label(root, text="Filtros:")
label_filtro.pack()

label_explicativo = tk.Label(root, text="Se mais de um filtro, separe por vírgula (ex: filtro1, filtro2)")
label_explicativo.pack()

entry_filtro = tk.Entry(root)
entry_filtro.pack()

label_diretorio_destino = tk.Label(root, text="Diretório de Saída:")
label_diretorio_destino.pack()

entry_diretorio_destino = tk.Entry(root)
entry_diretorio_destino.pack()

button_selecionar_saida = tk.Button(root, text="Escolher Diretório de Saída", command=escolher_diretorio_saida)
button_selecionar_saida.pack()

button_executar = tk.Button(root, text="Executar", command=executar_busca)
button_executar.pack()

barra_progresso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
barra_progresso.pack()

label_quantidade = tk.Label(root, text="Quantidade de arquivos encontrados: 0")
label_quantidade.pack()

label_progresso = tk.Label(root, text="")
label_progresso.pack()

root.mainloop()