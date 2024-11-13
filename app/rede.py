import socket
import pygame
class Rede:
    def __init__(self):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endereco_host = 'localhost'
        self.porta = 4343
        self.endereco = (self.endereco_host, self.porta)
        self.id = self.estabelecer_conexao()
    
    def estabelecer_conexao(self):
        self.servidor.connect(self.endereco)
        return self.servidor.recv(8192).decode()
    def enviar(self, dados):
        try:
            self.servidor.send(dados.encode('utf-8'))
            resposta = self.servidor.recv(8192).decode()
            return resposta
        except socket.error as erro:
            return str(erro)
def aguardar_jogador(rede, tela):
    fonte_arial = pygame.font.SysFont('arial', 70)
    texto = fonte_arial.render('Espere (...)', True, (255, 216, 110))
    tela.fill((0, 0, 0))  # Cor de fundo preta
    tela.blit(texto, (115, 265)) 
    pygame.display.flip()
    
    jogador = 2
    while True:
        requisicao = "players"
        resposta = rede.enviar(requisicao)
        while resposta == '1':
            resposta = rede.enviar(requisicao)
            jogador = 1
        break
    tela.fill(0) 
    return jogador