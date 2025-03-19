import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

def criar_no(chave):
    return [chave, None, None] # [chave, None, None] / [valor nó, pt filho esquerda, pt filho direita]

def inserir(raiz, chave):
    if raiz is None:
        return criar_no(chave) # se não houver raiz, a raiz será criada
    if chave < raiz[0]:
        raiz[1] = inserir(raiz[1], chave) # se menor que a raiz, o nó sera o inserido à esquerda
    else:
        raiz[2] = inserir(raiz[2], chave) # se menor que a raiz, o nó sera o inserido à direita
    return raiz

def excluir_no(raiz, chave):
    if raiz is None: # se a árvore for vazia, retornará vazio
        return raiz
    if chave < raiz[0]: # se a chave for menor que a raiz, chama recursivamente a função no filho esquerdo
        raiz[1] = excluir_no(raiz[1], chave)
    elif chave > raiz[0]: # se a chave for maior que a raiz, chama recursivamente a função no filho direito
        raiz[2] = excluir_no(raiz[2], chave)
    else:
        if raiz[1] is None: # se o nó não tem filhos a esquerda, o filho direito substitui o nó removido
            return raiz[2]
        elif raiz[2] is None: # se o nó não tem filhos a direita, o filho esquerdo substitui o nó removido
            return raiz[1]
        temp = menor_no(raiz[2])  # se o nó tiver os dois filhos, é encontrado o menor valor da subárvore a direita
        raiz[0] = temp[0] # é substituido o valor do nó a ser removido com o valor do seu sucessor
        raiz[2] = excluir_no(raiz[2], temp[0]) # chama recursivamente a função para remover o sucessor
    return raiz

def menor_no(raiz): # retorna o menor valor da árvore, percorre a subárvore à esquerda até encontrar o menor valor a esquerda
    atual = raiz    # começa a busca pelo nó raiz
    while atual[1] is not None: # enquanto o filho atual tiver um nó a esquerda, a função segue para o filho a esquerda
        atual = atual[1]
    return atual

def contar_nos(raiz): # conta os nós da árvore por meio de recursão
    if raiz is None:
        return 0
    return 1 + contar_nos(raiz[1]) + contar_nos(raiz[2]) # soma a raiz + filhos à esquerda + filhos à direita

def contar_nao_folhas(raiz): # conta os nós não folha da árvore por meio de recursão
    if raiz is None:
        return 0
    if raiz[1] is not None or raiz[2] is not None: # verifica se há filhos à direita e à esquerda
        return 1 + contar_nao_folhas(raiz[1]) + contar_nao_folhas(raiz[2])
    return contar_nao_folhas(raiz[1]) + contar_nao_folhas(raiz[2])

def atualizar_contagem():
    total_nos = contar_nos(raiz) # conta o total de nós
    total_nao_folhas = contar_nao_folhas(raiz) # conta os nós não folhas
    contagem_label.config(text=f"Nós: {total_nos} | Não-folhas: {total_nao_folhas}") # exibe os valores

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
    if raiz is None: # se a árvore for vazia, retornará vazio
        return None
    if raiz[0] == chave: # se a chave for igual ao nó, esse nó será retornado
        return raiz
    elif chave < raiz[0]: # se chave é menor que o nó, a busca continua à esquerda
        return buscar_no(raiz[1], chave)
    else: # se a chave é maior que o nó, a busca contiuna à direita
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
    plt.close('all')
    G = nx.DiGraph()
    pos = {}
    plt.figure(figsize=(8, 5))
    adicionar_arestas(raiz, G, pos)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()

def desenhar_arvore_destacado(no_destacado):
    plt.close('all') 
    G = nx.DiGraph()
    pos = {}
    adicionar_arestas(raiz, G, pos)
    pos = nx.get_node_attributes(G, 'pos')
    # se o nó for destacado ele ficará colorido em amarelo
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
janela = tk.Tk() # cria a janela de interação 
janela.title("Arvore Binária")

entrada = tk.Entry(janela) # cria o campo para inserir valores
entrada.pack()

botao_inserir = tk.Button(janela, text="Inserir", command=adicionar_valor) # cria o botão de inserir
botao_inserir.pack()

botao_remover = tk.Button(janela, text="Remover", command=remover_valor) # cria o botão de excluir
botao_remover.pack()

botao_localizar = tk.Button(janela, text="Localizar", command=localizar_valor) # cria o botão de localizar
botao_localizar.pack()

contagem_label = tk.Label(janela, text="Nós: 0 | Não-folhas: 0") # cria a exibição da contagem
contagem_label.pack()

janela.mainloop() # mantém a janela em execução até ser fechada pelo usuários
 
