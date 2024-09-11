import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

#Configurações iniciais otimizadas
num_particulas = 100
limites_iniciais = [-10, 10]
velocidade_max = 2
volume_inicial = (limites_iniciais[1] - limites_iniciais[0]) ** 3
raio_colisao = 0.5  #Raio de colisão para detecção

#Inicializa as posições e velocidades das partículas em 3D
posicoes = np.random.uniform(limites_iniciais[0], limites_iniciais[1], (num_particulas, 3))
velocidades = np.random.uniform(-velocidade_max, velocidade_max, (num_particulas, 3))

#Parâmetros do gráfico de energia cinética e pressão
tempos = []
energia_cinetica = []
pressao = []
volume_atual = volume_inicial

#Função para calcular energia cinética
def calcular_energia_cinetica():
    return 0.5 * np.sum(np.linalg.norm(velocidades, axis=1)**2)

#Função para calcular pressão baseada na energia cinética e volume
def calcular_pressao():
    return (2/3) * (calcular_energia_cinetica() / volume_atual)

#Função para detectar colisões entre partículas
def detectar_colisoes():
    global velocidades
    for i in range(num_particulas):
        for j in range(i + 1, num_particulas):
            distancia = np.linalg.norm(posicoes[i] - posicoes[j])
            if distancia < raio_colisao:
                #Calcula a velocidade média após a colisão
                direcao = (posicoes[i] - posicoes[j]) / distancia
                v1 = velocidades[i]
                v2 = velocidades[j]
                velocidades[i] = v1 - np.dot(v1 - v2, direcao) * direcao
                velocidades[j] = v2 + np.dot(v1 - v2, direcao) * direcao

#Função para atualizar as posições das partículas e detectar colisões
def atualizar(frame):
    global posicoes, velocidades, volume_atual

    #Atualiza as posições de forma vetorizada para maior eficiência
    posicoes += velocidades

    #Detecta colisões com as paredes (evita loops aninhados)
    colisao_menor = posicoes <= limites[0]
    colisao_maior = posicoes >= limites[1]
    velocidades[colisao_menor | colisao_maior] *= -1
    posicoes = np.clip(posicoes, limites[0], limites[1])

    #Detecta colisões entre partículas
    detectar_colisoes()

    #Atualiza o gráfico 3D de forma otimizada sem recriar o scatter plot
    scatter._offsets3d = (posicoes[:, 0], posicoes[:, 1], posicoes[:, 2])

    #Atualiza apenas os dados de energia cinética e pressão
    tempo = frame / 20
    tempos.append(tempo)
    energia_cinetica.append(calcular_energia_cinetica())
    pressao.append(calcular_pressao())

    #Atualiza os gráficos 2D sem recriá-los
    linha_energia.set_data(tempos, energia_cinetica)
    ax1.set_xlim(0, max(tempos))
    ax1.set_ylim(0, max(energia_cinetica) * 1.1)

    linha_pressao.set_data(tempos, pressao)
    ax2.set_xlim(0, max(tempos))
    ax2.set_ylim(0, max(pressao) * 1.1)

#Função para atualizar a velocidade das partículas com base na temperatura
def atualizar_temperatura(val):
    global velocidades
    nova_velocidade_max = val
    velocidades = np.random.uniform(-nova_velocidade_max, nova_velocidade_max, (num_particulas, 3))

#Função para atualizar os limites e o volume com base na compressão/expansão
def atualizar_limites(val):
    global limites, volume_atual, velocidades, velocidade_max
    novo_limite = limites_iniciais[1] * val
    limites = [-novo_limite, novo_limite]
    ax0.set_xlim(limites)
    ax0.set_ylim(limites)
    ax0.set_zlim(limites)
    volume_atual = (limites[1] - limites[0]) ** 3
    
    #Ajusta a velocidade conforme a compressão
    escala_velocidade = (volume_inicial / volume_atual)**(1/3)
    velocidade_max = 2 * escala_velocidade
    velocidades *= escala_velocidade
    slider_temp.set_val(velocidade_max)

#Criação da figura para as animações
fig = plt.figure(figsize=(12, 4))
ax0 = fig.add_subplot(131, projection='3d')
ax1 = fig.add_subplot(132)
ax2 = fig.add_subplot(133)

#Configuração do gráfico de partículas 3D
limites = limites_iniciais
ax0.set_xlim(limites)
ax0.set_ylim(limites)
ax0.set_zlim(limites)
ax0.set_box_aspect([1, 1, 1])
ax0.set_title('Colisão de Moléculas de Gás')

#Criação do scatter plot 3D (mantido fixo para otimização)
scatter = ax0.scatter(posicoes[:, 0], posicoes[:, 1], posicoes[:, 2], color='blue')

#Inicializa as linhas dos gráficos 2D sem recriar a cada frame
linha_energia, = ax1.plot([], [], color='red')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xlabel('Tempo')
ax1.set_ylabel('Energia Cinética')
ax1.set_title('Energia Cinética em Tempo Real')

linha_pressao, = ax2.plot([], [], color='blue')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_xlabel('Tempo')
ax2.set_ylabel('Pressão')
ax2.set_title('Pressão em Tempo Real')

#Criação do slider para ajustar a temperatura
ax_slider_temp = plt.axes([0.25, 0.01, 0.50, 0.03], facecolor='lightgoldenrodyellow')
slider_temp = Slider(ax_slider_temp, 'Velocidade', 0, 5.0, valinit=velocidade_max)
slider_temp.on_changed(atualizar_temperatura)

#Criação do slider para ajustar a compressão/expansão do recipiente
ax_slider_limite = plt.axes([0.25, 0.06, 0.50, 0.03], facecolor='lightgoldenrodyellow')
slider_limite = Slider(ax_slider_limite, 'Tamanho do Recipiente', 0.5, 2.0, valinit=1.0)
slider_limite.on_changed(atualizar_limites)

#Animação com menos frames por segundo para reduzir o processamento
ani = FuncAnimation(fig, atualizar, frames=np.arange(0, 5000), interval=50)
plt.show()
