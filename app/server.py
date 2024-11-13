import socket
from _thread import *
# Iniciando variáveis globais
posicao_x = '0'
posicao_y = '0'
numero_de_conexoes = 0
vez = '1'
jogador_atual = '1'
pronto = 0
vencedor = '0'
def principal():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco_servidor = 'localhost'
    porta = 4343
    endereco_servidor = (endereco_servidor, porta)
    try:
        #bind associa o servidor_socket com a porta 8080
        servidor_socket.bind(endereco_servidor) 
    except socket.error as erro:
        print(str(erro))
    #escuta somente 2 conexões, que é o máximo de jogadores existentes no jogo da velha
    servidor_socket.listen(2)
    print("NO AGUARDO DE UMA CONEXÃO")
    
    while True:
        conexao, endereco = servidor_socket.accept()
        print("VOCÊ ESTÁ CONECTADO A: ", endereco)
        global numero_de_conexoes
        numero_de_conexoes += 1
        start_new_thread(threaded, (conexao,))
def threaded(conexao):
    global numero_de_conexoes, vez, posicao_x, posicao_y, pronto, jogador_atual, vencedor
    conexao.send(str.encode('START'))
    resposta = ' '
    while True:
        try:
            requisicao = conexao.recv(4096).decode('utf-8')
            requisicao = requisicao.split(' ')
            # op = código de operação enviado pelo cliente
            op = requisicao[0]
            if op == "players":
                resposta = str(numero_de_conexoes)
            # Operação de recebimento de jogadas
            elif op == "jogada":
                jogador_atual = requisicao[1]
                print(f"Jogador {jogador_atual} fez uma jogada")
                posicao_x = requisicao[2]
                posicao_y = requisicao[3]
                if vez == '1':
                    vez = '2'
                elif vez == '2': 
                    vez = '1'
            # Atualizar os clientes das jogadas realizadas
            elif op == "updatevez":
                if vencedor != "0":
                    resposta = f"GANHOU {vencedor}"
                elif requisicao[1] != vez:
                    pronto = 1
                    resposta = f"u {vez} {jogador_atual} {posicao_x} {posicao_y}"
                else:
                    resposta = "OK"
            elif op == "vitoria":
                print(f"QUEM LEVOU OS 3 PONTOS PARA CASA: {requisicao[1]}")
                vencedor = requisicao[1]
            conexao.sendall(str.encode(resposta))
        except Exception as erro:
            print('ACONTECEU ALGO DE ERRADO', erro)
            break
    print("GAME OVER")
    conexao.close()
principal()