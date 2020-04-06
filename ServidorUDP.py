# Código se basa en: https://pythontic.com/modules/socket/udp-client-server-example
# https://www.binarytides.com/programming-udp-sockets-in-python/
# Hashing: https://www.pythoncentral.io/hashing-files-with-python/
# Transferencia: https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# https://wiki.python.org/moin/UdpCommunication#Using_UDP_for_e.g._File_Transfers
import math
import os
import socket
import hashlib
import tqdm
from pip._vendor.distlib.compat import raw_input

# Tamanio en el que se va a fragmentar los archivos.
# Punto 2
tamanioBuffer = raw_input('Defina el tamanio de los mensajes en que se van a fragmentar los archivos. Ingrese un numero '
                          'entre 1 - 65536 ')
tamanioBuffer = 1024

# Ubicar archivos

# Nombre archivo multimedia
archivoMultimedia = "Archivos a Transferir/Multimedia.mov"

# Tamanio archivo multimedia
tamanioMultimedia = os.path.getsize(archivoMultimedia)

# Nombre archivo driver sonido
archivoDriver = "Archivos a Transferir/224MB.exe"

# Tamanio archivo
tamanioDriver = os.path.getsize(archivoDriver)

# Punto 3
# Numero de fragmentos
fragmentosMultimedia = math.ceil(tamanioMultimedia/tamanioBuffer)
fragmentosDriver = math.ceil(tamanioDriver/tamanioBuffer)

# Calcular Hash de archivo utilizando MD5
# Multimedia
hashMultimedia = hashlib.md5()
with open('Archivos a Transferir/Multimedia.mov', 'rb') as aMultimedia:
    buf = aMultimedia.read(tamanioBuffer)
    while len(buf) > 0:
        hashMultimedia.update(buf)
        buf = aMultimedia.read(tamanioBuffer)
valorHashMultimedia = hashMultimedia.hexdigest()

# Driver
hashDriver = hashlib.md5()
with open('Archivos a Transferir/224MB.exe', 'rb') as aDriver:
    buf = aDriver.read(tamanioBuffer)
    while len(buf) > 0:
        hashDriver.update(buf)
        buf = aDriver.read(tamanioBuffer)
valorHashDriver = hashDriver.hexdigest()

# Punto 1
ipLocal = "127.0.0.1"

puertoLocal = 20001

# Crear socket

socketServidorUDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Vincular socket a dirección e ip

socketServidorUDP.bind((ipLocal, puertoLocal))


# Esperar mensajes de clientes
numClientesConectados = 0
print("Servidor UDP abierto a conexiones")
while (True):
    # Punto 5
    seleccionaArchivoyNumeroClientes = False
    while (not seleccionaArchivoyNumeroClientes):
        # Seleccionar archivo
        archivoSeleccionado = int(raw_input('Seleccione el archivo a enviar: 0: Multimedia (117 MB) 1: Driver (224 MB) '))
        # Numero de clientes a enviar archivo
        numClientes = int(raw_input('Indique el numero de clientes a los que se les va a enviar el archivo en simultaneo '))
        if((archivoSeleccionado == 1 or archivoSeleccionado == 0) and numClientes > 0):
            seleccionaArchivoyNumeroClientes = True

    bytesAddressPair = socketServidorUDP.recvfrom(tamanioBuffer)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    if(message == 'Inicio'):
        print('Inicio')

    clientMsg = "Message from Client:{}".format(message)

    print(clientMsg)



