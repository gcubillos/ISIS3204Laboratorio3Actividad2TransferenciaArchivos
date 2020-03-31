# Código se basa en: https://pythontic.com/modules/socket/udp-client-server-example
# https://www.binarytides.com/programming-udp-sockets-in-python/

import socket

# Punto 1: Conectarse a servidor y mostrar estado de conexión. Dado que UDP no está orientado a la conexión, se verifica
# la comunicación entre el cliente y servidor mediante un mensaje que manda el cliente y el servidor responde.
from pip._vendor.distlib.compat import raw_input

ipServidor = raw_input('Ingrese la dirección IP del servidor con el que se va a realizar la conexión: ')
ipServidor = "127.0.0.1"

puertoServidor = raw_input('Ingrese el puerto del servidor: ')
puertoServidor = 20001

direccionServidor = (ipServidor, puertoServidor)

mensajeBasico = ('Hola Servidor')

bytesEnviar = str.encode(mensajeBasico)

tamanioBuffer = 1024

# Crear socket UDP

socketClienteUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enviar mensaje a servidor UDP

socketClienteUDP.sendto(bytesEnviar, direccionServidor)

respuestaServidor = socketClienteUDP.recvfrom(tamanioBuffer)

msg = "Message from Server {}".format(respuestaServidor[0])

print(msg)

# Punto 2: Notificación de preparado para recibir datos.
recibirDatos = int(raw_input('¿Está preparado para recibir datos? 0: No 1: Sí'))

while(recibirDatos != 1):
    recibirDatos = int(raw_input('¿Está preparado para recibir datos? 0: No 1: Sí'))

# Se envía la notificación al servidor

notificacion = ('Listo')

bytesEnviar = str.encode(notificacion)

tamanioBuffer = 1024

# Send to server using created UDP socket

socketClienteUDP.sendto(bytesEnviar, direccionServidor)