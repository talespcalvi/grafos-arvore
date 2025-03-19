import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

def criar_no(chave):
    return [chave, None, None]

def inserir(raiz, chave):
    if raiz is None:
        return criar_no(chave)
    if chave < raiz[0]:
        raiz[1] = inserir(raiz[1], chave)
    else:
        raiz[2] = inserir(raiz[2], chave)
    return raiz

def excluir_no(raiz, chave):
    if raiz is None:
        return raiz
    if chave < raiz[0]:
        raiz[1] = excluir_no(raiz[1], chave)
    elif chave > raiz[0]:
        raiz[2] = excluir_no(raiz[2], chave)
    else:
        if raiz[1] is None:
            return raiz[2]
        elif raiz[2] is None:
            return raiz[1]
        temp = menor_no(raiz[2])
        raiz[0] = temp[0]
        raiz[2] = excluir_no(raiz[2], temp[0])
    return raiz

def menor_no(raiz):
    atual = raiz
    while atual[1] is not None:
        atual = atual[1]
    return atual

def contar_nos(raiz):
    if raiz is None:
        return 0
    return 1 + contar_nos(raiz[1]) + contar_nos(raiz[2])

def contar_nao_folhas(raiz):
    if raiz is None:
        return 0
    if raiz[1] is not None or raiz[2] is not None:
        return 1 + contar_nao_folhas(raiz[1]) + contar_nao_folhas(raiz[2])
    return contar_nao_folhas(raiz[1]) + contar_nao_folhas(raiz[2])

def atualizar_contagem():
    total_nos = contar_nos(raiz)
    total_nao_folhas = contar_nao_folhas(raiz)
    contagem_label.config(text=f"Nós: {total_nos} | Não-folhas: {total_nao_folhas}")

def adicionar_valor():
    global raiz
    try:
        valor = int(entrada.get())
        raiz = inserir(raiz, valor)
        atualizar_contagem()
        desenhar_arvore()
    except ValueError:
        messagebox.showerror("Erro", "Digite um número")

def remover_valor():
    global raiz
    try:
        valor = int(entrada.get())
        raiz = excluir_no(raiz, valor)
        atualizar_contagem()
        desenhar_arvore()
    except ValueError:
        messagebox.showerror("Erro", "Digite um número")

def buscar_no(raiz, chave):
    if raiz is None:
        return None
    if raiz[0] == chave:
        return raiz
    elif chave < raiz[0]:
        return buscar_no(raiz[1], chave)
    else:
        return buscar_no(raiz[2], chave)

def adicionar_arestas(raiz, G, pos, x=0, y=0, layer=1):
    if raiz is not None:
        G.add_node(raiz[0], pos=(x, y))
        if raiz[1] is not None:
            G.add_edge(raiz[0], raiz[1][0])
            adicionar_arestas(raiz[1], G, pos, x - 1 / layer, y - 1, layer + 1)
        if raiz[2] is not None:
            G.add_edge(raiz[0], raiz[2][0])
            adicionar_arestas(raiz[2], G, pos, x + 1 / layer, y - 1, layer + 1)

def desenhar_arvore():
    plt.close('all')  # Fecha todas as janelas de gráfico abertas
    G = nx.DiGraph()
    pos = {}
    plt.figure(figsize=(8, 5))
    adicionar_arestas(raiz, G, pos)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()

def desenhar_arvore_destacado(no_destacado):
    plt.close('all')  # Fecha todas as janelas de gráfico abertas
    G = nx.DiGraph()
    pos = {}
    adicionar_arestas(raiz, G, pos)
    pos = nx.get_node_attributes(G, 'pos')
    
    node_colors = ['lightblue' if node != no_destacado else 'yellow' for node in G.nodes()]
    
    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')
    plt.show()

def localizar_valor():
    global raiz
    try:
        valor = int(entrada.get())
        no_encontrado = buscar_no(raiz, valor)
        
        if no_encontrado:
            desenhar_arvore_destacado(no_encontrado[0])
        else:
            messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
    except ValueError:
        messagebox.showerror("Erro", "Digite um número")

# Interface
raiz = None
janela = tk.Tk()
janela.title("Arvore Binária")

entrada = tk.Entry(janela)
entrada.pack()

botao_inserir = tk.Button(janela, text="Inserir", command=adicionar_valor)
botao_inserir.pack()

botao_remover = tk.Button(janela, text="Remover", command=remover_valor)
botao_remover.pack()

botao_localizar = tk.Button(janela, text="Localizar", command=localizar_valor)
botao_localizar.pack()

contagem_label = tk.Label(janela, text="Nós: 0 | Não-folhas: 0")
contagem_label.pack()

janela.mainloop()
