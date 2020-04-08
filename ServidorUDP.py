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
tamanioBuffer = raw_input(
    'Defina el tamanio de los mensajes en que se van a fragmentar los archivos. Ingrese un numero '
    'entre 1 - 65536\n')
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
fragmentosMultimedia = math.ceil(tamanioMultimedia / tamanioBuffer)
fragmentosDriver = math.ceil(tamanioDriver / tamanioBuffer)

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


# Clase que representa un cliente
class Cliente:
    # Constructor
    def __init__(self, pDireccion):
        # Direccion del cliente
        self.direccion = pDireccion

    # Metodos
    def darDireccion(self):
        return self.direccion


# Arreglo de clientes conectados listos para recibir archivos
clientesConectados = []

# Esperar mensajes de clientes
print("Servidor UDP abierto a conexiones")

seleccionaArchivoyNumeroClientes = False
while (True):
    # Punto 5
    while (not seleccionaArchivoyNumeroClientes):
        # Seleccionar archivo
        archivoSeleccionado = int(
            raw_input('Seleccione el archivo a enviar: 0: Multimedia (117 MB) 1: Driver (224 MB)\n'))
        # Numero de clientes a enviar archivo
        numClientes = int(
            raw_input('Indique el numero de clientes a los que se les va a enviar el archivo en simultaneo\n'))
        if ((archivoSeleccionado == 1 or archivoSeleccionado == 0) and numClientes > 0):
            seleccionaArchivoyNumeroClientes = True

    # Recibe mensaje del cliente y la dirección IP del cliente
    mensaje, direccion = socketServidorUDP.recvfrom(tamanioBuffer)

    # Revisa el tipo de mensaje por el cliente y responde
    if (mensaje.decode("utf-8") == 'Inicio'):
        mensajeConexionExitosa = str.encode("Cliente {}".format(direccion) + " conectado exitosamente con servidor")
        socketServidorUDP.sendto(mensajeConexionExitosa, direccion)
    elif (mensaje.decode("utf-8") == 'Listo'):
        clientesConectados.append(Cliente(direccion))

    # Envia archivo y hash cuando el numero de clientes conectados es el deseado
    if (len(clientesConectados) == numClientes):
        # Determina la ruta del archivo a enviar, el hash a enviar y el número de fragmentos basado en el archivo escogido
        # para transferencia
        rutaArchivoEnviar = archivoMultimedia
        hashEnviar = valorHashMultimedia
        numFragmentosEnviar = fragmentosMultimedia
        if (archivoSeleccionado):
            rutaArchivoEnviar = archivoDriver
            hashEnviar = valorHashDriver
            numFragmentosEnviar = fragmentosDriver
        for i in clientesConectados:
            # Punto 3
            # Enviar tamaño buffer | Número fragmentos a enviar | Hash calculado de archivo
            socketServidorUDP.sendto(str.encode("Buffer {}".format(tamanioBuffer)), i.darDireccion())
            socketServidorUDP.sendto(str.encode("Fragmentos {}".format(numFragmentosEnviar)), i.darDireccion())
            socketServidorUDP.sendto(str.encode("Hash {}".format(hashEnviar)), i.darDireccion())

            # Enviar archivo
            # Barra de progreso
            progreso = tqdm.tqdm(range(numFragmentosEnviar), f"Sending {rutaArchivoEnviar}", unit="B",
                                 unit_scale=True, unit_divisor=tamanioBuffer)
            '''
            with open(rutaArchivoEnviar, 'rb') as archivoEnviar:
                for _ in progreso:
                    # Lectura de bytes del archivo
                    bytesLeidos = archivoEnviar.read(tamanioBuffer)
                    while (len(bytesLeidos) > 0):
                        socketServidorUDP.sendto(bytesLeidos,i.darDireccion())
                        # update the progress bar
                        progreso.update(len(bytesLeidos))'''

        #
        #for _ in progreso:
        #    # Lectura de bytes del archivo
        #    bytesLeidos = archivoEnviar.read(tamanioBuffer)
        #    while (len(bytesLeidos) > 0):
        #        socketServidorUDP.sendto(bytesLeidos, i.darDireccion())
        #        # update the progress bar
        #        progreso.update(len(bytesLeidos))
        # Reinicia valores de archivo seleccionado y numero clientes a enviar archivo
        archivoSeleccionado = -1
        numClientes = 0