import socket
import threading
import time

HOST    = ''     
PORT    = 5001 #int(input("Digite uma porta: "))
s       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
orig    = (HOST, PORT)
s.bind(orig)
s.listen(2)

global vControle                                #variavel de controle

def passagemLivre():
  global vControle
  return (vControle == 0)  

def handle(conn_addr):
  global vControle                              #explicitamente informa que a variavel global sera usada
  con, cliente = conn_addr  
  print ("\nConectado por .: ", cliente)
  con.send("Conectado ...\n".encode())  
  while not passagemLivre(): 
    con.send("WAIT".encode())                   #Envia ao cliente WAIT (espera)
    time.sleep(2)

  vControle = 1
  con.send("INI".encode())                      #Envia ao cliente INI (inicio da comunicacao)
  while True:                                   #Laço que serve para receber o comando do cliente
    msg = con.recv(1024).decode()
    if (msg.startswith("fim")):                 #Cliente sinaliza que deseja finalizar 
      print ("\n", cliente , " diz: " , msg)
      break        
  con.close()
  vControle = 0

#main do programa
vControle = 0
while True:
  threading.Thread(target=handle, args=(s.accept(),)).start()
