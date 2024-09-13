import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# Configurações iniciais otimizadas
num_particulas = 1000  # Número de partículas
limites_iniciais = [-10, 10]  # Limites do cubo onde as partículas se movem
velocidade_max = 1  # Velocidade máxima inicial das partículas
volume_inicial = (limites_iniciais[1] - limites_iniciais[0]) ** 3  # Volume inicial do recipiente
num_frames = 100  # Número de frames
num_fatias_x = 100  # Número de fatias ao longo do eixo X

# Inicializa as posições e velocidades das partículas em 3D
posicoes = np.random.uniform(limites_iniciais[0], limites_iniciais[1], (num_particulas, 3)) # O 3 é para as componentes x, y e z
velocidades = np.random.uniform(-velocidade_max, velocidade_max, (num_particulas, 3))

# Parâmetros para armazenar os dados de energia cinética e pressão ao longo do tempo
tempos = []
energia_cinetica = []
pressao = []
volume_atual = volume_inicial  # Volume atual começa como o volume inicial

# Função para calcular a energia cinética de todas as partículas
def calcular_energia_cinetica():
    return 0.5 * np.sum(np.linalg.norm(velocidades, axis=1) ** 2)
    # Fórmula da energia cinética: Ec = 1/2 * ∑(v^2) onde v é a velocidade de cada partícula

# Função para calcular a pressão do sistema baseada na energia cinética e volume
def calcular_pressao():
    return (2 / 3) * (calcular_energia_cinetica() / volume_atual)
    # Fórmula da pressão: P = (2/3) * (Ec / V), onde Ec é a energia cinética e V é o volume do recipiente

# Função para calcular o centro de massa
def calcular_centro_massa():
    return np.mean(posicoes, axis=0) # Calcula a posição média de todas as partículas, ou seja, o centro de massa do sistema.

# Função para plotar o histograma das velocidades das partículas
def plotar_histograma_velocidades():
    # Calcula a magnitude das velocidades das partículas
    magnitudes_velocidades = np.linalg.norm(velocidades, axis=1)

    # Magnitude da Velocidade: As magnitudes das velocidades das partículas são calculadas como a norma dos vetores de velocidade em 3D. 
    # Para cada partícula, a velocidade tem três componentes: vx, vy e vz. A magnitude da velocidade é então dada pela fórmula: v = sqrt(vx² + vy² + vz²)
    # Valor Máximo Teórico: O valor máximo teórico para a magnitude da velocidade ocorre quando vx = vy = vz = 1, o que resulta em: v_máximo = sqrt(1² + 1² + 1²) = sqrt(3) ≈ 1.732

    # Define o número de bins para o histograma
    num_bins = num_fatias_x
    fig, ax = plt.subplots(figsize=(6, 4))  # Cria explicitamente o eixo para o histograma

    # Cria o histograma das magnitudes das velocidades e obtém os valores para as barras
    contagem, bordas, _ = ax.hist(magnitudes_velocidades, bins=num_bins, color='blue', edgecolor='black')

    # Normaliza as magnitudes das velocidades para o intervalo do colormap
    norm = plt.Normalize(vmin=magnitudes_velocidades.min(), vmax=magnitudes_velocidades.max())
    cores = cm.coolwarm(norm((bordas[:-1] + bordas[1:]) / 2))  # Cor baseada no ponto médio de cada intervalo

    # Limpa o gráfico e redesenha o histograma com as cores
    ax.cla()
    for i in range(num_bins):
        ax.bar(bordas[i], contagem[i], width=bordas[i+1] - bordas[i], color=cores[i], edgecolor='black')

    # Adiciona títulos e rótulos
    ax.set_title('Histograma de Velocidades das Partículas')
    ax.set_xlabel('Magnitude da Velocidade')
    ax.set_ylabel('Número de Partículas')

    # Adiciona a barra de cores para referência
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Magnitude da Velocidade')  # Passa explicitamente o eixo

    # Exibe o gráfico
    plt.show()

# Função para atualizar as posições das partículas e detectar colisões
def atualizar(frame):
    global posicoes, velocidades, volume_atual

    # Atualiza as posições das partículas com base nas suas velocidades
    posicoes += velocidades

    # Detecta colisões com as paredes e inverte a direção da velocidade
    colisao_menor = posicoes <= limites[0]
    colisao_maior = posicoes >= limites[1]
    velocidades[colisao_menor | colisao_maior] *= -1  # Inverte a velocidade ao colidir com as paredes
    posicoes = np.clip(posicoes, limites[0], limites[1])  # Garante que as partículas não ultrapassem os limites

    # Calcula a magnitude das velocidades
    magnitudes = np.linalg.norm(velocidades, axis=1)

    # Atualiza o gráfico 3D com base nas novas posições e cores
    scatter._offsets3d = (posicoes[:, 0], posicoes[:, 1], posicoes[:, 2])
    scatter.set_array(magnitudes)  # Atualiza as cores das partículas com base nas magnitudes das velocidades

    # Calcula o centro de massa
    centro_massa = calcular_centro_massa()

    # Atualiza a posição da partícula do centro de massa
    centro_massa_point.set_data([centro_massa[0]], [centro_massa[1]])
    centro_massa_point.set_3d_properties([centro_massa[2]])

    # No último frame, calcular o histograma das partículas e das velocidades
    if frame == num_frames - 1:
        # Fatiar o cubo ao longo do eixo X e contar as partículas em cada fatia
        x_fatias = np.linspace(limites_iniciais[0], limites_iniciais[1], num_fatias_x + 1)
        histograma, _ = np.histogram(posicoes[:, 0], bins=x_fatias)

        # Calcular a velocidade média em cada fatia
        velocidade_media_fatia = []
        for i in range(num_fatias_x):
            particulas_fatia = (posicoes[:, 0] >= x_fatias[i]) & (posicoes[:, 0] < x_fatias[i + 1])
            if np.sum(particulas_fatia) > 0:
                velocidade_media_fatia.append(np.mean(np.linalg.norm(velocidades[particulas_fatia], axis=1)))
            else:
                velocidade_media_fatia.append(0)  # Caso não haja partículas na fatia

        # Normalizar as velocidades médias para usar no colormap
        velocidade_media_fatia = np.array(velocidade_media_fatia)
        norm = plt.Normalize(vmin=velocidade_media_fatia.min(), vmax=velocidade_media_fatia.max())
        cores = cm.coolwarm(norm(velocidade_media_fatia))

        # Criar nova figura para o histograma
        fig_hist, ax_hist = plt.subplots(figsize=(6, 4))

        # Plotar o gráfico de histograma com as cores
        for i in range(num_fatias_x):
            ax_hist.bar(x_fatias[i], histograma[i], width=np.diff(x_fatias)[i], align='edge', color=cores[i], edgecolor='black')

        ax_hist.set_xlabel('Posição ao longo do eixo X')
        ax_hist.set_ylabel('Número de partículas')
        ax_hist.set_title('Distribuição das partículas ao longo do eixo X no último frame')

        # Adicionar a colorbar na nova figura
        fig_hist.colorbar(cm.ScalarMappable(norm=norm, cmap='coolwarm'), ax=ax_hist, label='Velocidade média')

        plt.show()

        # Também exibe o histograma das magnitudes das velocidades
        plotar_histograma_velocidades()

# Criação da figura para as animações
fig = plt.figure(figsize=(6, 6))  # Tamanho menor da figura, focando no gráfico 3D
ax0 = fig.add_subplot(111, projection='3d')  # Apenas o gráfico 3D é exibido inicialmente

# Configuração do gráfico de partículas 3D
limites = limites_iniciais
ax0.set_xlim(limites)
ax0.set_ylim(limites)
ax0.set_zlim(limites)
ax0.set_box_aspect([1, 1, 1])  # Mantém a proporção igual entre os eixos
ax0.set_title('Colisão de Moléculas de Gás')

# Nomeando os eixos
ax0.set_xlabel('Eixo X')
ax0.set_ylabel('Eixo Y')
ax0.set_zlabel('Eixo Z')

# Criação do scatter plot 3D com colormap
magnitudes_iniciais = np.linalg.norm(velocidades, axis=1)
scatter = ax0.scatter(posicoes[:, 0], posicoes[:, 1], posicoes[:, 2], c=magnitudes_iniciais, cmap='coolwarm')

# Adiciona a barra de cores para referência
fig.colorbar(scatter, ax=ax0, label='Magnitude da Velocidade')

# Adiciona a partícula verde para o centro de massa
centro_massa = calcular_centro_massa()
centro_massa_point, = ax0.plot([centro_massa[0]], [centro_massa[1]], [centro_massa[2]], 'o', color='green', markersize=10)

# Animação com menos frames por segundo para reduzir o processamento
ani = FuncAnimation(fig, atualizar, frames=np.arange(0, num_frames), interval=100, repeat=False)  # Intervalo aumentado para suavizar
plt.show()
