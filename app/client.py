import pygame
from rede import Rede, aguardar_jogador
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
from sys import exit
# Função para desenhar o tabuleiro do jogo da velha
def desenhar_tabuleiro():
    # Desenha as linhas verticais e horizontais do tabuleiro
    pygame.draw.line(tela, (255, 216, 110), (200, 40), (200, 560), 10) 
    pygame.draw.line(tela, (255, 216, 110), (400, 40), (400, 560), 10)
    pygame.draw.line(tela, (255, 216, 110), (40, 200), (560, 200), 10)
    pygame.draw.line(tela, (255, 216, 110), (40, 400), (560, 400), 10)  
# Função para desenhar as peças no tabuleiro (X ou O) dependendo do jogador
def desenhar_peca(pos, quem_jogou): 
    x, y = pos
    if quem_jogou == 2:
        img = pygame.image.load('bola.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150)) 
        tela.blit(imgR, (x - 75, y - 75))
    else:
        img = pygame.image.load('x.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150))
        tela.blit(imgR, (x - 75, y - 75))
def testar_posicao():
    for p in rec:
        if e.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
            if p == rect1:
                confirmar(0, [100, 100])
            if p == rect2:
                confirmar(1, [300, 100])
            if p == rect3:
                confirmar(2, [500, 100])
            if p == rect4:
                confirmar(3, [100, 300])
            if p == rect5:
                confirmar(4, [300, 300])
            if p == rect6:
                confirmar(5, [500, 300])
            if p == rect7:
                confirmar(6, [100, 500])
            if p == rect8:
                confirmar(7, [300, 500])
            if p == rect9:
                confirmar(8, [500, 500])
def confirmar(indice, pos):
    global ESCOLHA, VEZ, espaco, rede, jogador
    if marca_tabuleiro[indice] == 'X':
        print('X')
    elif marca_tabuleiro[indice] == 'O':
        print('O')
    else:
        marca_tabuleiro[indice] = ESCOLHA
        desenhar_peca(pos, jogador)
        print(marca_tabuleiro)
        if VEZ == 1:
            VEZ = 2
        else:
            VEZ = 1
        espaco +=1
    # Avisando para o servidor que uma jogada foi feita
    rede.enviar(f"jogada {str(jogador)} {str(pos[0])} {str(pos[1])}")
def testar_vitoria(l):
    return ((marca_tabuleiro[0] == l and marca_tabuleiro[1] == l and marca_tabuleiro[2] == l) or
        (marca_tabuleiro[3] == l and marca_tabuleiro[4] == l and marca_tabuleiro[5] == l) or
        (marca_tabuleiro[6] == l and marca_tabuleiro[7] == l and marca_tabuleiro[8] == l) or
        (marca_tabuleiro[0] == l and marca_tabuleiro[3] == l and marca_tabuleiro[6] == l) or
        (marca_tabuleiro[1] == l and marca_tabuleiro[4] == l and marca_tabuleiro[7] == l) or
        (marca_tabuleiro[2] == l and marca_tabuleiro[5] == l and marca_tabuleiro[8] == l) or
        (marca_tabuleiro[0] == l and marca_tabuleiro[4] == l and marca_tabuleiro[8] == l) or
        (marca_tabuleiro[2] == l and marca_tabuleiro[4] == l and marca_tabuleiro[6] == l))
def texto_vitoria(v):
    opensans = pygame.font.SysFont('opensanscondensed', 45)
    mensagem = 'JOGADOR {} VENCEU'.format(v) 
    if v == 'EMPATE':
        mens_vitoria = opensans.render('DEU VELHA', True, (18, 19, 101), (255, 255, 255))
        tela.blit(mens_vitoria, (115, 265))
    else:
        mens_vitoria = opensans.render(mensagem, True, (18, 19, 101), (255, 255, 255)) 
        tela.blit(mens_vitoria, (100, 265))
def resetar():
        global ESCOLHA, ESTADO, VEZ, marca_tabuleiro, espaco
        ESTADO = 'JOGANDO'
        VEZ = 1
        ESCOLHA = 'X'
        espaco = 0
        marca_tabuleiro = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]
        tela.fill(0)  # Cor preta
pygame.init() 
rede = Rede()
tela = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Jogo da Velha') 
tela.fill((0, 0, 0))  # Cor preta
# Se conectando com o servidor e aguardando os dois jogadores se conectarem
jogador = aguardar_jogador(rede, tela)
print(f'jogador: {jogador}')
ESTADO = 'JOGANDO'
VEZ = 1
ESCOLHA = 'X'
espaco = 0
marca_tabuleiro = [
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
]
rect1 = Rect((0, 0), (200, 200))
rect2 = Rect((200, 0), (200, 200))
rect3 = Rect((400, 0), (200, 200))
rect4 = Rect((0, 200), (200, 200))
rect5 = Rect((200, 200), (200, 200))
rect6 = Rect((400, 200), (200, 200))
rect7 = Rect((0, 400), (200, 200))
rect8 = Rect((200, 400), (200, 200))
rect9 = Rect((400, 400), (200, 200))
rec = [
    rect1,rect2,rect3,rect4,
    rect5,rect6,rect7,rect8,rect9,
]
pontos1, pontos2 = 0, 0
tela.fill((0, 0, 0))  # Cor preta
while True:
    mouse_pos = pygame.mouse.get_pos()
    if ESTADO == 'JOGANDO':
        desenhar_tabuleiro()
        #pontos(pontos1, pontos2)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == MOUSEBUTTONDOWN:
                if VEZ == jogador:
                    if jogador == 1:
                        ESCOLHA = 'X'
                    else:
                        ESCOLHA = 'O'
                    testar_posicao()
        if testar_vitoria('X'):
            rede.enviar("vitoria 1")
            print('X VENCEU')
            texto_vitoria('X')
            ESTADO = 'RESET'
            pontos1 += 1
        elif testar_vitoria('O'):
            rede.enviar("vitoria 2")
            print('O VENCEU')
            texto_vitoria('O')
            ESTADO = 'RESET'
            pontos2 +=1
        elif espaco >= 9:
            print('EMPATE')
            texto_vitoria('EMPATE')
            ESTADO = 'RESET'
    else: 
        for u in pygame.event.get():
            if u.type == QUIT:
                pygame.quit()
                exit()
            if u.type == MOUSEBUTTONDOWN:
                resetar()
                desenhar_tabuleiro()
    pygame.display.flip()
    # Buscando por updates no estado do jogo 
    resposta = rede.enviar(f"updatevez {str(VEZ)}")
    resposta = resposta.split(' ')
    if resposta[0] == "venceu":
        if resposta[1] == '1':
            texto_vitoria('X')
        else:
            texto_vitoria('O')
    if resposta[0] == 'u':
        VEZ = int(resposta[1])
        quem_jogou = int(resposta[2])
        x = int(resposta[3])
        y = int(resposta[4])
        # Desenhando a jogada realizada pelo outro jogador
        desenhar_peca([x, y], quem_jogou)