# Server program
import socket
import thread
import threading
import time

#Minhas configuracoes
HOST_origem = '127.0.0.1' #meu IP


#Configuracoes do servidor geral
HOST = '127.0.0.1'  # Endereco IP do Servidor do chat
PORT = 5007           # Porta que o Servidor do chat

#Configuracao chat p2p
PORT_p2p = 5004
HOST_p2p = '127.0.0.1'

opcao = '0'

#Thread do cliente para enviar mensagem
def enviar():
	while True:
		msg = raw_input()
		if (msg != 'exit'):
			udp.sendall(msg.encode())
		else:
			udp.sendall(msg.encode())
			print('Voce saiu do chat em grupo...\n')
			break
	thread.exit()
			
#Thread do cliente para receber mensagem
def receber(): 
	msg = udp.recv(1024)
	while (msg != None and msg != 'exit'):
		print msg
		msg = udp.recv(1024)
	thread.exit()

#Thread do servidor para enviar mensagem (chat p2p)		
def enviar_p2p(con, nickname):
	while (True):
		msg = raw_input()
		if (msg != 'exit'):
			con.sendall(msg.encode())
		else:
			print('Voce saiu do chat...\n')
			con.sendall('exit')
			break
	thread.exit()
	
#Thread do servidor para receber mensagem (chat p2p)
def receber_p2p(t, con, nickname):
	con.setblocking(False)
	t.signal = True
	msg = ''
	while (t.isAlive()):
		try:
			if t.isAlive():
				msg = con.recv(1024)
			else:
				break
		except socket.error:
			continue
		if(msg != None and msg != 'exit'):
			print nickname,'>',msg
		if msg == 'exit':
			print nickname, 'saiu do chat...\nPara sair digite exit.\n'
			con.close()
			break
		else:
			continue
	thread.exit()

			
#main
print('Pronto...')
while(opcao != '3'):
	print('1 - Criai um Chat\n2 - Entrar no Chat\n3 - Sair\n10 - Conectar com o Servidor\nQual a opcao? ')
	opcao = raw_input()
	udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.SOCK_STREAM conexao de udp;
	if(opcao == '10'):
		try:
			udp.connect((HOST, PORT)) # abre conexao com o servidor para verificar se nickname esta no chat em grupo
			udp.sendall(opcao.encode()) #manda a opcao para o servidor geral
			resposta2 = udp.recv(1024) # true ou false
			if(resposta2 == 'true'): # se consegui entrar no chat
				msg = udp.recv(1024) # true ou false
				print msg
				msg = raw_input() #digita nickname
				print('\nVoce esta no chat em grupo.\nPara sair digite exit.\n')
				udp.sendall(msg.encode()) #manda o nickname para o servidor
				thread_enviar = threading.Thread(target = enviar)
				thread_receber = threading.Thread(target = receber)
				thread_enviar.start()
				thread_receber.start()
				thread_enviar.join()
				thread_receber.join()
			else: # se nao consegui entrar no chat
				print "A sala esta cheia. Tente novamente mais tarde.\n"
				udp.close()
		except:
			print 'PORTA errada. Ajeite e tente novamente.\n'

	elif(opcao == '2'): #Cliente quer entrar no chat

		try:
			print('Digite o seu nickname: ')
			nickname = raw_input()
			time.sleep(1) #delay
			udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria conexao
			udp.connect((HOST_p2p, PORT_p2p))               # abre conexao
			nickname2 = udp.recv(1024) #recebe nickname de quem esta na sala
			udp.send(nickname) #envia seu nickname
			print 'Chat iniciado, ', nickname2, ' esta no chat...\nPara sair do chat use exit.\n'
			thread_enviar_p2p = threading.Thread(target = enviar_p2p, args = (udp, nickname))
			thread_receber_p2p = threading.Thread(target = receber_p2p, args = (thread_enviar_p2p, udp, nickname2))
			thread_enviar_p2p.start()
			thread_receber_p2p.start()
			thread_enviar_p2p.join()
			thread_receber_p2p.join() 
			udp.close()
		except socket.error: #else
			print nickname, "algum problema tente mais tarde...\n"
		
	elif(opcao == '1'): # Abre servidor nessa maquina para receber mensagem
		print('Digite o seu nickname: ')
		nickname = raw_input()
		server_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		orig = (HOST_origem, PORT_p2p)
		server_p2p.bind(orig)
		server_p2p.listen(1)
		print "Aguardando conexao...\n"
		con, cliente = server_p2p.accept() #aceita a conexao
		con.send(nickname.encode()) #envia seu nickname
		nickname2 = con.recv(1024) #recebe nickname da pessoa que quer participar
		
		print 'Use exit para sair do chat.\nChat aberto ', nickname2, ' acabou de entrar...\n'
		#criando as threads para iniciar conversa
		thread_enviar_p2p = threading.Thread(target = enviar_p2p, args = (con, nickname))
		thread_receber_p2p = threading.Thread(target = receber_p2p, args = (thread_enviar_p2p,con, nickname2))
		thread_enviar_p2p.start()
		thread_receber_p2p.start()
		thread_enviar_p2p.join()
		thread_receber_p2p.join() 
		server_p2p.close()   #fecha o servidor
    	
	elif(opcao == '3'):
		print 'Obrigado.\n'
		udp.close()

	else:
		print 'ERRO: Opcao invalida! Tente novamente!\n'

