# -*- coding: utf-8 -*-
# importok
import socket
import re
import select
import sys
import time
import errno
from AESCipher import AESCipher
# server socket (objektum) létrehozása
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ip-cím lekérése
IP_address = raw_input('Szerver IP címe: ')
# Port lekérése, ha nem adott meg semmit a felhasználó, akkor legyen 5000
Port = raw_input('Szerver port: (alapértelmezett:5000)')
if Port == '':
	Port = 5000
# Kulcs bekérése
Key = raw_input('Kulcs: ')
# AESCipher objektum létrehozása az elöbb bekért key-jel
aes = AESCipher(Key)
# Ha a felhasználó rossz IP-címet adott meg,
# vagy nem fut a szerver azon az IP-n
# beszéljen vissza
try:		
	server.connect((str(IP_address), int(Port)))
except socket.error, v:
    errorcode=v[0]
    if errorcode==errno.ECONNREFUSED:
        print "Kapcsolat elutasítva." 
	exit()

char1 = '<'
char2 = '>' 
# Egyetlen while loop,
# figyeljen, hogy mikor a szervertől
# üzenet érkezik, írja ki azt.
# Valamint a felhasználótól kérje el az üzenetet.
# Kiírja az elküldött üzenet utf8 és enkódolt változatát.
# Ha nincs egyáltalán szóköz a fogadott üzenetben, nagy valószínüséggel
# enkódolt 
while True:
	try:
		sockets_list = [sys.stdin, server]
		
		read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
		
		for socks in read_sockets:
			if socks == server:
				try:
					message = socks.recv(2048)
				except socket.error, v:
					errorcode=v[0]
					if errorcode==errno.ENOTCONN:
						print("Hibás IP-cím")
						exit()

				# Létrehozza az ipsubstr-t a message-ból a < és > közötti szöveget
				ipsubstr = message[message.find(char1)+1 : message.find(char2)]
				# Leválasztja az IP - t 
				noipmess = re.sub('<.*?>', '', message)
				# Az előző parancs szóközzel tömte ki a kidobott részt,
				# ez teljesen levágja a szóközt a szöveg elött, és után
				noipmess.strip(' ')
				messnospc = message.strip(' ')
				if ' ' not in noipmess:
					# Ha siránkozik azzal, hogy nem 16bites a message, 
					# akkor nincs kapcsolat a szerver és a kliens között
					try:
						# dekódolás
						decrmes = aes.decrypt(noipmess)
					except ValueError:
						print('A szerver bezárt.')
						exit()
					# Írja ki az IP-vel együtt a dekódolt messaget
					allstr = '<' + ipsubstr +'>: '+ decrmes
					print (allstr.rstrip())
				else:
					# Ha nincs enkódolva a message, 
					# akkor valószínüleg a szervertől kapott üzenetet
					# pl.: valaki kilépett
					print (message)
			else:
				# Folyamatosan olvassa be a küldendő üzenetet
				message = sys.stdin.readline()
				# Enkódolja a bekért message stringet
				encrmes = aes.encrypt(message)
				# Küldje ki a szervernek az enkódolt üzenetet
				server.send(encrmes)
				# Írja ki az enkódolt, elüldött message-t
				# Nem tudom, mire jó ez
				#sys.stdout.write('<Te>: ' + encrmes + '\n\n')
				# Törölje az ideiglenes puffert
				sys.stdout.flush()
	# Ha ki akarunk lépni, ne jöjjön hibaüzenettel
	except KeyboardInterrupt:
		exit()
	time.sleep(0.2)
server.close()

