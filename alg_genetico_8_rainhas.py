import random
import time
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o valor de conflito de uma solução (quantidade de conflitos)
def calcular_valor_solucao(solucao):
    """Calcula o valor total de 'conflitos' de rainhas numa solução."""
    n = len(solucao)
    valor_total = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Conflitos: mesma coluna (linha é garantida pela codificação)
            if solucao[i] == solucao[j]:
                valor_total += 1
            # Conflitos diagonais
            if abs(solucao[i] - solucao[j]) == abs(i - j):
                valor_total += 1
    return valor_total

# Função para gerar a população inicial
def gerar_populacao(tamanho_populacao, n):
    populacao = []
    for _ in range(tamanho_populacao):
        # Garante que as rainhas estão em colunas distintas
        individuo = random.sample(range(n), n)  # Gera uma lista única de n números, sem repetições
        populacao.append(individuo)
    return populacao

# Função para calcular a aptidão (quanto menor o valor de conflito, melhor)
def calcular_aptidao(individuo):
    valor_conflito = calcular_valor_solucao(individuo)
    return 28 - valor_conflito  # A solução ótima tem aptidão 28 e a solução ruim tem aptidão 0

# Função para realizar a seleção por roleta
def selecao_por_roleta(populacao, n):
    tamanho_roleta = sum(calcular_aptidao(ind) for ind in populacao)
    selecionados = []
    for _ in range(2):  # Seleciona dois pais
        sorteio = random.randint(1, tamanho_roleta)
        soma = 0
        for individuo in populacao:
            soma += calcular_aptidao(individuo)
            if soma >= sorteio:
                selecionados.append(individuo)
                break
    return selecionados

# Função para realizar o cruzamento (corte de um ponto)
def cruzamento(pai1, pai2):
    n = len(pai1)
    ponto_corte = random.randint(1, n-1)  # Ponto de corte aleatório
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Função para realizar a mutação (bit flip)
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = random.randint(0, len(individuo)-1)  # Inverte o valor da posição
    return individuo

# Função elitista para seleção dos sobreviventes
def selecao_elitista(populacao, tamanho_populacao, n):
    # Ordena a população pela aptidão (quanto menor o valor de conflito, melhor)
    populacao.sort(key=lambda ind: calcular_aptidao(ind), reverse=True)
    return populacao[:tamanho_populacao]  # Os melhores sobrevivem

# Função para mostrar o tabuleiro como matriz 8x8
def mostrar_tabuleiro(solucao):
    """Exibe a solução como um tabuleiro 8x8"""
    tabuleiro = [[0 for _ in range(8)] for _ in range(8)]  # Cria um tabuleiro vazio 8x8
    for linha, coluna in enumerate(solucao):
        tabuleiro[linha][coluna] = 1  # Marca a posição da rainha
    for linha in tabuleiro:
        print(' '.join(str(x) for x in linha))  # Exibe o tabuleiro de forma legível

# Função principal do algoritmo genético
def algoritmo_genetico(tamanho_populacao=20, n=8, max_geracoes=1000, taxa_crossover=0.8, taxa_mutacao=0.03):
    populacao = gerar_populacao(tamanho_populacao, n)
    geracao = 0
    tempo_inicial = time.time()
    
    while geracao < max_geracoes:
        nova_populacao = []

        # Verifica se a solução ótima foi encontrada
        for individuo in populacao:
            if calcular_valor_solucao(individuo) == 0:
                tempo_execucao = time.time() - tempo_inicial
                return individuo, geracao, tempo_execucao

        # Selecione os pais
        while len(nova_populacao) < tamanho_populacao:
            pais = selecao_por_roleta(populacao, n)

            # Cruzamento
            if random.random() < taxa_crossover:
                filho1, filho2 = cruzamento(pais[0], pais[1])
                nova_populacao.append(filho1)
                nova_populacao.append(filho2)
            else:
                nova_populacao.append(pais[0])
                nova_populacao.append(pais[1])

        # Aplicar mutação
        for i in range(len(nova_populacao)):
            nova_populacao[i] = mutacao(nova_populacao[i], taxa_mutacao)

        # Selecione os sobreviventes (elitista)
        populacao = selecao_elitista(populacao + nova_populacao, tamanho_populacao, n)

        geracao += 1

    tempo_execucao = time.time() - tempo_inicial
    return populacao[0], geracao, tempo_execucao  # Retorna a melhor solução encontrada

# Executa o algoritmo 50 vezes
resultados = []
solucoes = []
for _ in range(5):
    print("Execução ", _)
    solucao, geracoes, tempo_execucao = algoritmo_genetico()
    resultados.append((geracoes, tempo_execucao))
    solucoes.append(solucao)

# Calculando a média e desvio padrão do número de gerações e do tempo de execução
geracoes = [resultados[i][0] for i in range(len(resultados))]
tempos = [resultados[i][1] for i in range(len(resultados))]
media_geracoes = np.mean(geracoes)
desvio_geracoes = np.std(geracoes)
media_tempos = np.mean(tempos)
desvio_tempos = np.std(tempos)

print(f'Média de gerações: {media_geracoes}')
print(f'Desvio padrão de gerações: {desvio_geracoes}')
print(f'Média do tempo de execução: {media_tempos:.4f} segundos')
print(f'Desvio padrão do tempo de execução: {desvio_tempos:.4f} segundos')

# Encontrando as cinco melhores soluções distintas
melhores_solucoes = sorted(solucoes, key=lambda x: calcular_valor_solucao(x))
melhores_solucoes = melhores_solucoes[:5]

print("Cinco melhores soluções encontradas:")
for i in range(len(melhores_solucoes)):
    print(f"Solucao {i}: {melhores_solucoes[i]}")

# Gráficos
# Gráfico do número de gerações
plt.figure(figsize=(10, 5))
plt.hist(geracoes, bins=15, color='skyblue', edgecolor='black')
plt.title("Distribuição do número de gerações")
plt.xlabel("Número de gerações")
plt.ylabel("Frequência")
plt.show()

# Gráfico do tempo de execução
plt.figure(figsize=(10, 5))
plt.hist(tempos, bins=15, color='salmon', edgecolor='black')
plt.title("Distribuição do tempo de execução")
plt.xlabel("Tempo (segundos)")
plt.ylabel("Frequência")
plt.show()

