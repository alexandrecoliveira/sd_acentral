import socket
import threading
import time

HOST    = ''     
PORT    = int(input("Digite uma porta: "))
s       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
orig    = (HOST, PORT)
s.bind(orig)
s.listen(2)

global x              #variavel compartilhada
global vControle      #variavel de controle

def passagemLivre():
  global vControle
  if vControle == 0:
    return True
  else:
    return False

def handle(conn_addr):
  global vControle
  con, cliente = conn_addr  
  print ("\nConectado por .: ", cliente)
  con.send("Conectado ...\n".encode())
  while not passagemLivre(): 
    con.send("Aguarde a liberacao ...\n".encode())
    time.sleep(2)

  vControle = 1
  con.send("Ok, sua vez...\nDigite algo: ".encode())    
  msg = con.recv(1024).decode()
  print (msg + "\n")
  con.send("bye\n".encode())
  con.close()
  vControle = 0

#main do programa
vControle = 0

while True:
  threading.Thread(target=handle, args=(s.accept(),)).start()
  #msg = con.recv(1024).decode()
  #[comando, numero] = msg.split(";")
  #if (comando == "ler"):
  #  print (msg + "\n")
  #  msg = str(x)
  #else:
  #  if (comando == "escrever"):
  #    print (msg + "\n")
  #    x = int(numero)
  #    msg = numero
  #print (msg + "\n")
  #con.send(msg.encode())
  #con.close()
