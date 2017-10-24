# -*- coding: utf-8 -*-
import socket
import select
import sys
from thread import *
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
## google-re csatlakozás, ennek a socketnek a hostname-jét kéri le 
try:
    IP_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_socket.connect(('google.com', 0))
    IP_address = IP_socket.getsockname()[0]
    print ('Szerver IP-címe: ' + IP_address)
except:
    # Ha nincs internet kapcsolat, kérjünk el a felhasználótol
    # egyet.
    print('Nem sikerült lekérni az IP-címet')
    IP_address = raw_input('Kérlek addj meg egyet: ')

# Port lekérdezése, ha nem adott meg a felhasználó portot,
# legyen az 5000.
Port = raw_input('Port: (alapértelmezett:5000) ')
if Port == '':
	Port = 5000
# Vonja össze az ip-t és a portot ebben a socketben.
server.bind((IP_address,int(Port)))
# Fogadjon el maximum 100 kapcsolatot egyszerre.
server.listen(100)
# Kliens listájának inicializálása
list_of_clients = []
print ("Szerver elindult\n")
# Ez a funkció azt meséli el, mi történjen egy kliens csatlakozásakor,
# valamint írja ki, mi történik a csetszobában.
def clientthread(conn, addr):

        # some üdvözlőüzenet
	conn.send("""
            _           _   
           | |         | |  
 _ __   ___| |__   __ _| |_ 
| '_ \ / __| '_ \ / _` | __|
| |_) | (__| | | | (_| | |_ 
| .__/ \___|_| |_|\__,_|\__|
| |                         
|_|                         
Üdvözöllek, """ + str(addr[0]) + '\n')
        # amíg true true, próbáljon elkérni egy üzenetet.
	while True:
		try:
			message = conn.recv(2048)
                        # Ha kaptunk valamit
			if message:
	
                                # Mutassa meg, mit kaptunk 
				print ("<" + addr[0] + "> " + message)
	
                                # Csapja össze a kapott üzenetet az kliens IP-címével
				message_to_send = "<" + addr[0] + ">" + message
                                # Broadcas az egy nagyon fancy client.send
				broadcast(message_to_send, conn)
	
			else:
                                # Ha nincs semmi életjel egy klienstől,
                                # akkor zárja be a kapcsolatot
				remove(conn)
						
		except:
                        # Ha 1 tickben nem kapott semmit,
                        # ne szomorkodjon, hanem próbáljon meg még sokszor üzenetet szerezni
			continue
		time.sleep(0.2)
# clients.send, csak ha nem működik, zárja be a kapcsolatot.
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message)
			except:
				clients.close()

				remove(clients)

# Szakítsa meg a paraméterben megadott kapcsolatot,
# és írja ki, hogy melyik kliens lépett ki
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)
		quitstring = str(addr[0]) + ' kilépett.' 
		broadcast(quitstring, conn)
		print (quitstring)

# Amíg fut a program, fogadjon el minden beérkező kérelmet,
# írja ki, ki csatlakozott, hozzon létre minden új kapcsolatnak egy új 
# párhuzamos folyamatot (nem tudom mi a threadnek a magyar megfelelője) 
try:
	while True:
	
		conn, addr = server.accept()
		list_of_clients.append(conn)
		connectedstring = str(addr[0]) + " csatlakozott"
		broadcast(connectedstring, conn)
		print (connectedstring) 
	
		start_new_thread(clientthread,(conn,addr)) 
		time.sleep(0.2) # 0,1 másodpercig várakozik, hogy csökkentse a CPU-használatot
	
except KeyboardInterrupt:
	try:
		# Ha senki nem csatlakozott, nem jön létre
		# a conn objektum, hibát ír ki
		conn.close() 		
	except:
		server.close()
	else:
		conn.close()
		server.close()

