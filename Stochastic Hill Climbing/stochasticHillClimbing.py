import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt

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

def stochasticHillClimbing(iteracoes=1000):
    tabuleiro = [random.randint(0, 7) for _ in range(8)]
    conflitos = calcularConflitos(tabuleiro)
    tempo_inicial = time.time()
    tempo_execucao = 0

    for i in range(iteracoes):
        if conflitos == 0:  # Se encontrou uma solução sem conflitos, para
            break
        
        vizinho = gerarVizinho(tabuleiro)
        novosConflitos = calcularConflitos(vizinho)

        if novosConflitos < conflitos: # Se encontrou uma combinação diferente com menos conflitos, atualiza o tabuleiro
            tabuleiro = vizinho
            conflitos = novosConflitos
    tempo_execucao = time.time() - tempo_inicial
    return tabuleiro, conflitos, tempo_execucao, i

# Executar 50 vezes
solucoes = []
conflitos = []
tempos = []
iteracoes = []

for i in range(50):
    print(f"Execução {i}")
    solucao, totalConflitos, tempo, i = stochasticHillClimbing()
    solucoes.append(solucao)
    conflitos.append(totalConflitos)
    tempos.append(tempo)
    iteracoes.append(i)

# Calcular médias e desvios padrão
media_conflitos = np.mean(conflitos)
desvio_conflitos = np.std(conflitos)

media_tempos = np.mean(tempos)
desvio_tempos = np.std(tempos)

media_iteracoes = np.mean(iteracoes)
desvio_iteracoes = np.std(iteracoes)

print(f'Média de conflitos: {media_conflitos}')
print(f'Desvio padrão de conflitos: {desvio_conflitos}')

print(f'Média do tempo de execução: {media_tempos:.4f} segundos')
print(f'Desvio padrão do tempo de execução: {desvio_tempos:.4f} segundos')

print(f'Média de iterações: {media_iteracoes}')
print(f'Desvio padrão de iterações: {desvio_iteracoes}')


# Gráfico do número de conflitos
plt.figure(figsize=(10, 5))
plt.hist(conflitos, bins=15, color='salmon', edgecolor='black')
plt.title("Distribuição do número de conflitos")
plt.xlabel("Conflitos")
plt.ylabel("Frequência")
plt.show()

# Gráfico do tempo de execução
plt.figure(figsize=(10, 5))
plt.hist(tempos, bins=15, color='salmon', edgecolor='black')
plt.title("Distribuição do tempo de execução")
plt.xlabel("Tempo (segundos)")
plt.ylabel("Frequência")
plt.show()

# Gráfico do número de iterações
plt.figure(figsize=(10, 5))
plt.hist(iteracoes, bins=15, color='skyblue', edgecolor='black')
plt.title("Distribuição do número de iterações")
plt.xlabel("Número de iterações")
plt.ylabel("Frequência")
plt.show()

solucoes_otimas = sorted(zip(solucoes, conflitos), key= lambda x: x[1])
sol = []
for s in solucoes_otimas:
    if s[0] not in sol:
        sol.append(s)

print("Soluções ótimas")
sol = sol[:5]
for i in range(len(sol)):
    print(f"Solução {i+1}: {sol[i]}")