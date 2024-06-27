import socket
import sys
import threading


port = 9999 # Se elige un numero elevado de puerto
ip = '127.0.0.1' # Se setea la direccion ip del servidor, para el caso de prueba utilizar localhost

try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creacion del socket de conexion
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#setsockopt() permite activar o desactivar una característica especial de un socket 
# o de un protocolo. El 1 final indica que se está activando, en este caso.
# SO_REUSEADDR es una opción del socket. 
#Indica que si cuando más adelante se intente 
# hacer la operación .bind((ip, puerto)) 
# se descubre que esa ip y ese puerto ya estaban siendo usados, 
# se reusen de todas formas. Sin esa opción el 
# intento de hacer .bind() sobre una IP y puerto en uso 
# causaría una excepción y que el programa abortara.

    server_sock.bind((ip, port))  # bind del socket a la direccion
    server_sock.listen()#Queda en escucha el socket 
except socket.error as msg:
	print ('Fallo en la creacion del socket. Codigo de Error: ' + str(msg[0]) + ' , Mensaje de Error : ' + msg[1])
	sys.exit()

print('Servidor Activo!!')

clients = []  # lista de clientes
c_addr = []  # lista de las direcciones de los clientes que se van conectando

def broadcast(msg):   # envia los mensajes a todos los clientes  conectados al server
    for c in clients:
        c.send(msg)


def event_check(client):  # chequeo de evento, si el cliente ingresa 'exit', cierra el cliente
    # y envia un mensaje a todos los conectados
    
    
    while True:
       
        try:
            msg = client.recv(1024)
            
            if msg.decode('utf-8') == "exit":
                index = clients.index(client)
                clients.remove(client)
                temp = c_addr[index]
                del c_addr[index]
                client.close()
                broadcast("{} Desconectado!".format(temp).encode('utf-8'))
               
                print("Cantidad de Clientes Conectados: ", len(clients))
                break
            else:
                broadcast(msg)

        except:
            index = clients.index(client)
            clients.remove(client)
            temp = c_addr[index]
            del c_addr[index]
            client.close()
            broadcast("{} Desconectado!".format(temp).encode('utf-8'))
            
            
            
            break


while True:
    
    
    clientsock, addr = server_sock.accept()
    print("Conectado en ", addr)
    clients.append(clientsock)
    c_addr.append(addr)
    clientsock.send('Conectado al Servidor'.encode('utf-8'))
    
    
    thread = threading.Thread(target=event_check, args=(clientsock,))#Se pasa como argumento el socket al momento del threading
    thread.start()
    
    print ("Cantidad de Clientes Conectados: ", len(clients)) 


   