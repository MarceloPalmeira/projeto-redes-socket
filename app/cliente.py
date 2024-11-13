# Importa as bibliotecas necessárias
import pygame  # Biblioteca para criação de jogos e interfaces gráficas
from rede import Rede, aguardar_jogador  # Funções de rede personalizadas para conexão e sincronização de jogadores
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT  # Eventos e constantes do Pygame
from sys import exit  # Para sair do programa de forma segura

# Função para desenhar o tabuleiro do jogo da velha
def desenhar_tabuleiro():
    # Desenha as linhas verticais e horizontais do tabuleiro
    pygame.draw.line(tela, (255, 216, 110), (200, 40), (200, 560), 10)  # Linha vertical esquerda
    pygame.draw.line(tela, (255, 216, 110), (400, 40), (400, 560), 10)  # Linha vertical direita
    pygame.draw.line(tela, (255, 216, 110), (40, 200), (560, 200), 10)  # Linha horizontal superior
    pygame.draw.line(tela, (255, 216, 110), (40, 400), (560, 400), 10)  # Linha horizontal inferior

# Função para desenhar as peças no tabuleiro (X ou O) dependendo do jogador
def desenhar_peca(pos, quem_jogou):
    x, y = pos  # Posição onde a peça será desenhada
    if quem_jogou == 2:
        # Se for o jogador 2, carrega e redimensiona a imagem de "O"
        img = pygame.image.load('bola.png').convert_alpha()
    else:
        # Se for o jogador 1, carrega e redimensiona a imagem de "X"
        img = pygame.image.load('x.png').convert_alpha()
    imgR = pygame.transform.scale(img, (150, 150))
    tela.blit(imgR, (x - 75, y - 75))  # Centraliza a imagem na posição desejada

# Função para verificar a posição onde o jogador clicou e fazer a jogada
def testar_posicao():
    for p in rec:  # Percorre todos os retângulos do tabuleiro
        if e.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
            # Verifica qual quadrado foi clicado e chama a função de confirmação de jogada
            if p == rect1: confirmar(0, [100, 100])
            if p == rect2: confirmar(1, [300, 100])
            if p == rect3: confirmar(2, [500, 100])
            if p == rect4: confirmar(3, [100, 300])
            if p == rect5: confirmar(4, [300, 300])
            if p == rect6: confirmar(5, [500, 300])
            if p == rect7: confirmar(6, [100, 500])
            if p == rect8: confirmar(7, [300, 500])
            if p == rect9: confirmar(8, [500, 500])

# Função para confirmar a jogada feita e atualizar o tabuleiro
def confirmar(indice, pos):
    global ESCOLHA, VEZ, espaco, rede, jogador
    if marca_tabuleiro[indice] == 'X' or marca_tabuleiro[indice] == 'O':
        # Se o espaço já estiver ocupado, não faz nada
        return
    else:
        # Marca o tabuleiro com a escolha do jogador (X ou O) e desenha a peça
        marca_tabuleiro[indice] = ESCOLHA
        desenhar_peca(pos, jogador)
        # Alterna a vez entre os jogadores
        VEZ = 2 if VEZ == 1 else 1
        espaco += 1  # Incrementa o contador de espaços ocupados
    # Envia ao servidor as coordenadas da jogada
    rede.enviar(f"jogada {str(jogador)} {str(pos[0])} {str(pos[1])}")

# Função para verificar se um jogador venceu
def testar_vitoria(l):
    return ((marca_tabuleiro[0] == l and marca_tabuleiro[1] == l and marca_tabuleiro[2] == l) or
            (marca_tabuleiro[3] == l and marca_tabuleiro[4] == l and marca_tabuleiro[5] == l) or
            (marca_tabuleiro[6] == l and marca_tabuleiro[7] == l and marca_tabuleiro[8] == l) or
            (marca_tabuleiro[0] == l and marca_tabuleiro[3] == l and marca_tabuleiro[6] == l) or
            (marca_tabuleiro[1] == l and marca_tabuleiro[4] == l and marca_tabuleiro[7] == l) or
            (marca_tabuleiro[2] == l and marca_tabuleiro[5] == l and marca_tabuleiro[8] == l) or
            (marca_tabuleiro[0] == l and marca_tabuleiro[4] == l and marca_tabuleiro[8] == l) or
            (marca_tabuleiro[2] == l and marca_tabuleiro[4] == l and marca_tabuleiro[6] == l))

# Função para exibir a mensagem de vitória na tela
def texto_vitoria(v):
    opensans = pygame.font.SysFont('opensanscondensed', 45)
    mensagem = 'JOGADOR {} VENCEU'.format(v)
    # Exibe uma mensagem diferente para empate
    if v == 'EMPATE':
        mens_vitoria = opensans.render('DEU VELHA', True, (18, 19, 101), (255, 255, 255))
    else:
        mens_vitoria = opensans.render(mensagem, True, (18, 19, 101), (255, 255, 255))
    tela.blit(mens_vitoria, (100, 265))  # Posiciona a mensagem centralmente

# Função para reiniciar o jogo
def resetar():
    global ESCOLHA, ESTADO, VEZ, marca_tabuleiro, espaco
    ESTADO, VEZ, ESCOLHA, espaco = 'JOGANDO', 1, 'X', 0
    marca_tabuleiro = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Reinicia o estado do tabuleiro
    tela.fill(0)  # Limpa a tela com a cor preta

# Inicializa o Pygame e configurações do jogo
pygame.init()
rede = Rede()  # Instancia a rede para comunicação com o servidor
tela = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Jogo da Velha')
tela.fill((0, 0, 0))  # Preenche a tela com preto
jogador = aguardar_jogador(rede, tela)  # Espera o jogador se conectar ao servidor

# Configurações iniciais do jogo
ESTADO, VEZ, ESCOLHA, espaco = 'JOGANDO', 1, 'X', 0
marca_tabuleiro = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Define os retângulos que representam cada espaço do tabuleiro
rect1 = Rect((0, 0), (200, 200))
rect2 = Rect((200, 0), (200, 200))
rect3 = Rect((400, 0), (200, 200))
rect4 = Rect((0, 200), (200, 200))
rect5 = Rect((200, 200), (200, 200))
rect6 = Rect((400, 200), (200, 200))
rect7 = Rect((0, 400), (200, 200))
rect8 = Rect((200, 400), (200, 200))
rect9 = Rect((400, 400), (200, 200))
rec = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9]  # Lista de todos os retângulos

# Laço principal do jogo
while True:
    mouse_pos = pygame.mouse.get_pos()  # Pega a posição do mouse
    if ESTADO == 'JOGANDO':
        desenhar_tabuleiro()  # Desenha o tabuleiro
        for e in pygame.event.get():  # Captura eventos do pygame
            if e.type == QUIT:
                pygame.quit()  # Fecha o Pygame ao sair
                exit()
            if e.type == MOUSEBUTTONDOWN and VEZ == jogador:
                # Define qual símbolo será usado pelo jogador atual
                ESCOLHA = 'X' if jogador == 1 else 'O'
                testar_posicao()  # Testa a posição clicada para ver se é válida

        # Testa se algum jogador venceu ou se deu empate
        if testar_vitoria('X'):
            rede.enviar("vitoria 1")  # Envia vitória para o servidor
            texto_vitoria('X')  # Exibe mensagem de vitória
            ESTADO = 'RESET'
        elif testar_vitoria('O'):
            rede
