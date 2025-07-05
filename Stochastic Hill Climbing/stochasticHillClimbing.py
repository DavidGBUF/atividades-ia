import random
import copy

# Função para calcular conflitos em uma solução
def calcularConflitos(tabuleiro):
    conflitos = 0
    n = len(tabuleiro) 

    for i in range(n):
        for j in range(i + 1, n): 
            if tabuleiro[i] == tabuleiro[j]: # Conflito na mesma linha
                conflitos += 1
            if abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j): # Conflito na mesma diagonal
                conflitos += 1

    return conflitos

# Gera novos vizinhos
def gerarVizinho(tabuleiro):
    n = len(tabuleiro)
    novoTabuleiro = copy.copy(tabuleiro) 

    coluna = random.randint(0, n - 1) # Escolhe aleatoriamente uma coluna para mover a rainha
    linha = random.randint(0, n - 1) # Escolhe aleatoriamente uma nova linha para a rainha na coluna selecionada

    while novoTabuleiro[coluna] == linha: # Garante que a nova linha seja diferente da linha atual da rainha na coluna escolhida
        linha = random.randint(0, n - 1)
    
    novoTabuleiro[coluna] = linha
    return novoTabuleiro

def stochasticHillClimbing(iteracoes=500):
    tabuleiro = [random.randint(0, 7) for _ in range(8)]
    conflitos = calcularConflitos(tabuleiro)

    for i in range(iteracoes):
        if conflitos == 0:  # Se encontrou uma solução sem conflitos, para
            break

        vizinho = gerarVizinho(tabuleiro)
        novosConflitos = calcularConflitos(vizinho)

        if novosConflitos <= conflitos:
            return vizinho, novosConflitos
    
    return tabuleiro, conflitos

solucao, totalConflitos = stochasticHillClimbing()

if totalConflitos == 0:
    print(f"Solução encontrada: {solucao}")
else:
    print(f"Solução parcial encontrada com {totalConflitos} conflitos: {solucao}")