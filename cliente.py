import socket
import time
import random

def ler(dest): 
  servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  servidor.connect(dest)
  comando = "ler;0"
  servidor.send(comando.encode())
  res = servidor.recv(1024).decode()
  servidor.close()
  return int(res) 

def escreve(x, dest): 
  servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  servidor.connect(dest)
  comando = "escrever;" + str(x)
  servidor.send(comando.encode())
  time.sleep(1)
  servidor.close()
  return True

def realizaOperacao(server_d):
  for i in range(1, random.randint(1,10) * 5):         
      x = ler(server_d)
      x = x + 1
      escreve(x, server_d)
      print ("Valor de x: ", x)
      
def permissaoPassagem(controlador_d, server_d):
  controlador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  controlador.connect(controlador_d)
  print(controlador.recv(1024).decode())      #mensagem se houve conexao
  while True:
    perm = controlador.recv(1024).decode()    #mensagem INI ou WAIT    
    if perm.startswith("WAIT"):
      print ("Controlador: Aguarde ...\n")
    else:
      print ("Controlador: \n", perm)
      realizaOperacao(server_d)
      controlador.send("fim".encode())
      break
  controlador.close()
  return True
    
#main do programa
#Controlador
HOST_CONTROL = "127.0.0.1"
PORT_CONTROL = 5001          
DEST_CONTROL = (HOST_CONTROL, PORT_CONTROL)
#Servidor
HOST_SERVER = "127.0.0.1"
PORT_SERVER = 5002          
DEST_SERVER = (HOST_SERVER, PORT_SERVER)

permissaoPassagem(DEST_CONTROL, DEST_SERVER)
  
print ("\nfim")
