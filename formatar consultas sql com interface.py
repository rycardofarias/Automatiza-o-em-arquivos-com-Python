import re
import json
import tkinter as tk
from tkinter import scrolledtext

def formatar_sql_com_valores(sql_com_valores, substituir_tb=False):
    partes = re.split(r'\s*\+->\s*', sql_com_valores)
    sql_original = partes[0]

    valores_str = re.search(r'\[([^\[\]]*)\]', partes[1]).group(1)
    valores = [v.strip() for v in valores_str.split(',')]

    marcadores = re.findall(r'\?', sql_original)
    if len(marcadores) != len(valores):
        raise ValueError('A quantidade de valores não corresponde à quantidade de marcadores de posição')

    for valor in valores:
        marcador_posicao = sql_original.find('?')
        if valor.isdigit():
            sql_original = sql_original[:marcador_posicao] + valor + sql_original[marcador_posicao + 1:]
        else:
            sql_original = sql_original[:marcador_posicao] + f"'{valor}'" + sql_original[marcador_posicao + 1:]

    if substituir_tb:
        sql_original = sql_original.replace('tb', 'sate.tb')

    return sql_original

def executar_consulta():
    entrada = entrada_texto.get("1.0", tk.END)  # Obter texto da entrada
    substituir_tb = substituir_tb_var.get()  # Verificar se deve substituir 'tb' por 'sat.tb'
    
    try:
        sql_formatado = formatar_sql_com_valores(entrada, substituir_tb)
        resultado_texto.delete(1.0, tk.END)  # Limpar o campo de resultado
        resultado_texto.insert(tk.END, sql_formatado)  # Exibir o resultado formatado
    except Exception as e:
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, f"Erro: {str(e)}")

# Criar a janela principal
janela = tk.Tk()
janela.title("Formatador de Consultas SQL")
janela.geometry("800x800")

label_rodape = tk.Label(janela, text="Desenvolvido por Ricardo Farias", relief=tk.SUNKEN, anchor=tk.W)
label_rodape.pack(side=tk.BOTTOM, fill=tk.X)

# Criar entrada de texto para a consulta
entrada_texto = scrolledtext.ScrolledText(janela, width=150, height=20)
entrada_texto.pack(padx=10, pady=10)

# Criar botão de execução
botao_executar = tk.Button(janela, text="Executar Consulta", command=executar_consulta)
botao_executar.pack(pady=5)

# Criar checkbox para substituir 'tb' por 'sat.tb'
substituir_tb_var = tk.BooleanVar()
check_substituir_tb = tk.Checkbutton(janela, text="Substituir 'tb' por 'sate.tb'", variable=substituir_tb_var)
check_substituir_tb.pack(pady=5)

# Criar campo de texto para exibir o resultado
resultado_texto = scrolledtext.ScrolledText(janela, width=150, height=20)
resultado_texto.pack(padx=10, pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
