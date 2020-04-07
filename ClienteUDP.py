# Código se basa en: https://pythontic.com/modules/socket/udp-client-server-example
# https://www.binarytides.com/programming-udp-sockets-in-python/

import socket
from pip._vendor.distlib.compat import raw_input
import tqdm

# Punto 1: Conectarse a servidor y mostrar estado de conexión. Dado que UDP no está orientado a la conexión, se verifica
# la comunicación entre el cliente y servidor mediante un mensaje que manda el cliente y el servidor responde.
ipServidor = raw_input('Ingrese la dirección IP del servidor con el que se va a realizar la conexión:\n')
ipServidor = "127.0.0.1"

puertoServidor = raw_input('Ingrese el puerto del servidor:\n')
puertoServidor = 20001

direccionServidor = (ipServidor, puertoServidor)

mensajeInicio = str.encode('Inicio')

tamanioBuffer = 1024

# Crear socket UDP

socketClienteUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enviar mensaje a servidor UDP

# Asignar direccion de servidor
socketClienteUDP.connect(direccionServidor)

socketClienteUDP.send(mensajeInicio)

respuestaServidor = socketClienteUDP.recvfrom(tamanioBuffer)

msg = "Mensaje de Servidor: "+ respuestaServidor[0].decode("utf-8")

print(msg)

# Punto 2: Notificación de preparado para recibir datos.
preparado = False
while(not preparado):
    recibirDatos = int(raw_input('¿Está preparado para recibir datos? 0: No 1: Sí\n'))
    if(recibirDatos == 1):
        preparado = True


# Se envía la notificación al servidor
mensajeListo = ('Listo')

# Enviar mensaje a servidor
socketClienteUDP.sendto(str.encode(mensajeListo), direccionServidor)