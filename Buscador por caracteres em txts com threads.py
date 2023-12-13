import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread

# Variáveis globais para as entradas e botões
entry_diretorio = None
entry_diretorio_destino = None
entry_filtro = None
barra_progresso = None
label_quantidade = None
label_progresso = None
button_executar = None

def contem_registro(caminho_arquivo, filtros):
    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
        for linha in arquivo:
            linha = linha.lower()
            for filtro in filtros:
                if filtro.lower() in linha:
                    return True
    return False

def buscar_e_copiar_arquivos(diretorio_raiz, filtros, diretorio_destino, barra_progresso, label_quantidade, label_progresso, button_executar):
    def atualizar_progresso(valor):
        barra_progresso["value"] = valor
        barra_progresso.update_idletasks()

    def atualizar_log(arquivos_encontrados, arquivos_falha):
        with open('log_busca.txt', 'w') as log:
            log.write("Arquivos Encontrados:\n")
            for arquivo_encontrado in arquivos_encontrados:
                log.write(f"{arquivo_encontrado}\n")
            log.write("\nArquivos que não contêm os filtros:\n")
            for arquivo_falha in arquivos_falha:
                log.write(f"{arquivo_falha}\n")

    def processar_arquivos():
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

        lote_size = 100  # Tamanho do lote para atualização da barra de progresso
        for i in range(0, total_arquivos, lote_size):
            for indice, arquivo in enumerate(arquivos_txt[i:i+lote_size], start=i+1):
                caminho_arquivo_txt = os.path.join(diretorio_raiz, arquivo)
                if contem_registro(caminho_arquivo_txt, filtros):
                    quantidade_encontrada += 1
                    arquivos_encontrados.append(arquivo)
                    shutil.copy(caminho_arquivo_txt, diretorio_destino)
                else:
                    arquivos_falha.append(arquivo)

                atualizar_progresso(i + indice if i + indice < total_arquivos else total_arquivos)

            atualizar_progresso(i + lote_size if i + lote_size < total_arquivos else total_arquivos)

        atualizar_log(arquivos_encontrados, arquivos_falha)
        label_quantidade.config(text=f"Quantidade de arquivos encontrados: {quantidade_encontrada}")
        label_progresso.config(text="Busca Concluída!")
        button_executar.config(state=tk.NORMAL)

    thread_busca = Thread(target=processar_arquivos)
    thread_busca.start()

def contar_arquivos(diretorio_raiz):
    arquivos_txt = [arquivo for arquivo in os.listdir(diretorio_raiz) if arquivo.endswith('.txt')]
    quantidade_arquivos_txt = len(arquivos_txt)
    return quantidade_arquivos_txt

def buscar_arquivos():
    global entry_diretorio

    diretorio_raiz = filedialog.askdirectory()
    if diretorio_raiz:
        entry_diretorio.delete(0, tk.END)
        entry_diretorio.insert(0, diretorio_raiz)

        def contar_e_mostrar():
            quantidade_arquivos_txt = contar_arquivos(diretorio_raiz)
            tk.messagebox.showinfo("Informação", f"Quantidade de arquivos .txt neste diretório: {quantidade_arquivos_txt}")

        thread_contagem = Thread(target=contar_e_mostrar)
        thread_contagem.start()

def escolher_diretorio_saida():
    global entry_diretorio_destino

    diretorio_destino = filedialog.askdirectory()
    if diretorio_destino:
        entry_diretorio_destino.delete(0, tk.END)
        entry_diretorio_destino.insert(0, diretorio_destino)

def executar_busca():
    global entry_diretorio, entry_filtro, entry_diretorio_destino, barra_progresso, label_quantidade, label_progresso, button_executar

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

def criar_interface_grafica():
    global entry_diretorio, entry_diretorio_destino, entry_filtro, barra_progresso, label_quantidade, label_progresso, button_executar

    root = tk.Tk()
    largura_janela = 600
    altura_janela = 450

    root.geometry(f"{largura_janela}x{altura_janela}")
    root.title("Busca de caracteres em Arquivos .TXT")

    label_rodape = tk.Label(root, text="Desenvolvido por Ricardo Farias", relief=tk.SUNKEN, anchor=tk.W)
    label_rodape.pack(side=tk.BOTTOM, fill=tk.X)
    
    cor_principal = '#2c3e50'  # Azul escuro
    cor_secundaria = '#ecf0f1'  # Cinza claro
    cor_botao = '#3498db'  # Azul

    root.configure(bg=cor_principal)

    frame_principal = tk.Frame(root, bg=cor_secundaria)
    frame_principal.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    label_instrucao = tk.Label(frame_principal, text="Selecione um diretório raiz:", bg=cor_secundaria, fg=cor_principal)
    label_instrucao.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    entry_diretorio = tk.Entry(frame_principal)
    entry_diretorio.grid(row=1, column=0, padx=(10, 5), pady=5, sticky='ew')

    button_selecionar_dir = tk.Button(frame_principal, text="Selecionar Diretório", bg=cor_botao, fg=cor_secundaria, command=buscar_arquivos)
    button_selecionar_dir.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='w')

    label_filtro = tk.Label(frame_principal, text="Filtros (separados por vírgula): Ex: filtro1, filtro2", bg=cor_secundaria, fg=cor_principal)
    label_filtro.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    
    entry_filtro = tk.Entry(frame_principal)
    entry_filtro.grid(row=3, column=0, padx=(10, 5), pady=5, sticky='ew')

    label_diretorio_destino = tk.Label(frame_principal, text="Diretório de Saída:", bg=cor_secundaria, fg=cor_principal)
    label_diretorio_destino.grid(row=4, column=0, padx=10, pady=5, sticky='w')

    entry_diretorio_destino = tk.Entry(frame_principal)
    entry_diretorio_destino.grid(row=5, column=0, padx=(10, 5), pady=5, sticky='ew')

    button_selecionar_saida = tk.Button(frame_principal, text="Escolher Diretório de Saída", bg=cor_botao, fg=cor_secundaria, command=escolher_diretorio_saida)
    button_selecionar_saida.grid(row=5, column=1, padx=(5, 10), pady=5, sticky='w')

    button_executar = tk.Button(frame_principal, text="Executar", bg='#27ae60', fg=cor_secundaria, command=executar_busca)  # Mudando a cor para verde ('#27ae60')
    button_executar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    barra_progresso = ttk.Progressbar(frame_principal, orient="horizontal", length=300, mode="determinate")
    barra_progresso.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    label_quantidade = tk.Label(frame_principal, text="Quantidade de arquivos encontrados: 0", bg=cor_secundaria, fg=cor_principal)
    label_quantidade.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    label_progresso = tk.Label(frame_principal, text="", bg=cor_secundaria)
    label_progresso.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    criar_interface_grafica()
