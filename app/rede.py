import socket
import pygame

# Classe para lidar com a comunicação pela rede
class Rede:
    def __init__(self):

        # Classe para lidar com a comunicação pela rede
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Define o endereco do servidor
        self.endereco_host = 'localhost'

        #Define uma porta para o servidor
        self.porta = 4343

        #Endereco completo ID + PORTA
        self.endereco = (self.endereco_host, self.porta)

        # Conecta ao servidor e recebe o ID do jogador
        self.id = self.estabelecer_conexao()
    
    def estabelecer_conexao(self):
        """
        Conecta ao servidor e recebe o ID do jogador.
        """
        
        self.servidor.connect(self.endereco) # Conecta ao servidor usando o endereço definido (IP e porta)

        # Recebe o identificador do jogador do servidor:
        # - O método `recv` recebe dados enviados pelo servidor, com um tamanho máximo de 8192 bytes.
        # - O identificador é decodificado de bytes para string.
        return self.servidor.recv(8192).decode()

    def enviar(self, dados):
        """
        Envia dados para o servidor e recebe uma resposta.
        """
        
        try:
            # Envia uma mensagem codificada em UTF-8 para o servidor.
            # - O método `send` transmite os dados ao servidor.
            self.servidor.send(dados.encode('utf-8'))

            # Recebe a resposta do servidor (até 8192 bytes).
            # - O método `recv` espera a resposta e a decodifica.
            resposta = self.servidor.recv(8192).decode()
            return resposta
            
        except socket.error as erro:
            # Caso ocorra um erro de conexão, o erro é retornado como string.
            return str(erro)


# Função para exibir mensagem de espera e aguardar o segundo jogador
def aguardar_jogador(rede, tela):
    # Define a fonte para o texto exibido na tela (Arial, tamanho 70)
    fonte_arial = pygame.font.SysFont('arial', 70)

    # Renderiza o texto "Espere (...)" na cor amarelo claro (255, 216, 110)
    texto = fonte_arial.render('Espere (...)', True, (255, 216, 110))

    # Preenche a tela com cor de fundo preta
    tela.fill((0, 0, 0))

    # Desenha o texto na posição especificada (115, 265)
    tela.blit(texto, (115, 265))
    
    # Atualiza a tela para mostrar o texto
    pygame.display.flip()

    # Define o jogador como 2 (por padrão, esperando o segundo jogador)
    jogador = 2

    # Loop para aguardar a conexão de outro jogador
    while True:
        requisicao = "players"  # Mensagem para verificar quantos jogadores estão conectados
        resposta = rede.enviar(requisicao)  # Envia a requisição para o servidor
        
        # Continua verificando enquanto a resposta indica apenas 1 jogador conectado
        while resposta == '1':
            resposta = rede.enviar(requisicao)  # Envia a requisição novamente

            # Se a resposta mudar, significa que o segundo jogador está presente
            jogador = 1  # Define o jogador como 1 (indicando o primeiro jogador)
        
        break  # Sai do loop quando há 2 jogadores conectados

    # Limpa a tela antes de retornar o valor do jogador
    tela.fill(0)
    return jogador
