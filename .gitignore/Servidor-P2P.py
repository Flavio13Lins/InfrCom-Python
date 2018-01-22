import socket
import thread
import time

HOST = '127.0.0.1'   # Endereco IP do Servidor
PORT = 5007            # Porta que o Servidor esta
CLIENTES = {}
num_pessoas = 0 #numero de pessoas conectadas no chat
MAX_USUARIOS = 12
FALSE = 'false'
TRUE = 'true'


#configuracao do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(False)
orig = (HOST, PORT)
server.bind(orig)
server.listen(1) 


def broadcast(nome, msg): 
    print msg 
    for destinatario, con in CLIENTES.items(): 
        if destinatario != nome: 
            try: 
                con.send(msg) 
            except socket.error: 
                pass

def conectado(conn):
    while True: 
        conn.send("Digite seu nickname: ") 
        try: 
            name = conn.recv(1024).strip() 
        except socket.error: 
            continue 
        if name in CLIENTES: 
            conn.send("\nNickname ja existe.\n") 
        elif name: 
            conn.setblocking(False) 
            CLIENTES[name] = conn 
            broadcast(name, "%s entrou no chat..." % name) 
            break

opcao = '0'

#main
while True:
    while True:
        try:
            con, cliente = server.accept()
        except socket.error:
            break
        opcao = con.recv(1024) #recebe a opcao
        time.sleep(1)
        #print opcao
        if (opcao == '10' and len(CLIENTES) < MAX_USUARIOS):
            con.sendall(TRUE.encode()) #envio um true
            thread.start_new_thread(conectado, tuple([con]))
        elif (opcao == '10' and len(CLIENTES) >= MAX_USUARIOS):
            con.sendall(FALSE.encode()) #envio um false
        else: # opcao = 2
            continue
    msg = ""
    if (opcao == '10'):    # cliente quer entrar no chat
        if len(CLIENTES) <= MAX_USUARIOS:
            for nome, conn in CLIENTES.items():
                try:
                    msg = conn.recv(1024)
                except socket.error:
                    continue
                if msg == 'exit':
                    conn.sendall('exit')
                    del CLIENTES[nome]
                    broadcast(nome, "%s saiu do chat..." % nome)
                else:
                    if msg != "":
                        broadcast(nome, "%s> %s" % (nome, msg.strip()))
            time.sleep(.1)    
    elif (opcao == '2'): # msg = 2 cliente quer P2P
        try:
            msg = con.recv(1024) #pega o nickname
            #ve se ta no array e retorna true ou false
            esta_no_chat = (msg in CLIENTES)
            if(esta_no_chat == False):
                con.sendall(FALSE.encode())
            else:
                con.sendall(TRUE.encode())
            print cliente, 'desconectou do server'
            con.close() #fecha conxao com o servidor
        except socket.error:
            continue        
    else:
        continue

server.close()
sys.exit(0)
