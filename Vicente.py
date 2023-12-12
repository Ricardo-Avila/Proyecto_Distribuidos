import socket
import datetime
import threading

def recibir_respuesta(client_socket):
    while True:
        respuesta = client_socket.recv(1024).decode('utf-8')
        print(f"\nRespuesta del servidor: {respuesta}\n")


def cliente(ip_servidor):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_servidor, 12345))  # Reemplazar 'ip_del_servidor' con la dirección IP del servidor

    hiloRespuesta = threading.Thread(target=recibir_respuesta, args=(client_socket,))
    hiloRespuesta.start()

    while True:
        # Enviar mensaje al servidor
        date = datetime.datetime.now().time()
        tiempo = f"{date.hour}:{date.min}:{date.second}"
        mensaje = input("Ingrese su mensaje (exit para salir):")

        if (mensaje != "exit"):
            mensaje += " " + tiempo
            client_socket.send(mensaje.encode('utf-8'))

            with open('mensajes.txt', 'a') as file:
                file.write(f"{address}: {mensaje}\n")

            # Recibir respuesta del servidor
            #respuesta = client_socket.recv(1024).decode('utf-8')
            #print(f"Respuesta del servidor: {respuesta}")
        else:
            client_socket.close()
            hiloRespuesta.join()
            break;

    #client_socket.close()

def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind a todas las interfaces en el puerto 12345
    server_socket.listen(5)

    print("Servidor esperando conexiones...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Cliente conectado desde: {address}")

        # Recibir mensaje del cliente
        mensaje = client_socket.recv(1024).decode('utf-8')
        print(f"Mensaje recibido: {mensaje}")

        # Almacenar el mensaje en un archivo
        with open('mensajes.txt', 'a') as file:
            file.write(f"{address}: {mensaje}\n")

        # Enviar respuesta al cliente
        respuesta = "Mensaje recibido correctamente"
        client_socket.send(respuesta.encode('utf-8'))

        # client_socket.close()


def main():

    maquina1 = '192.168.183.136'
    maquina2 = '192.168.183.147'
    maquina3 = '192.168.183.148'
    maquina4 = '192.168.183.137'
    maquina5 = '192.168.183.138'

    while True:
        maquina = input("Ingrese el numero de maquina al que quiere mandar un mensaje:")

        hiloServidor = threading.Thread(target=servidor, )


        if (maquina == '1'):
            hiloCliente = threading.Thread(target=cliente, args=(maquina1,))
            hiloServidor.start()
            hiloCliente.start()

        elif (maquina == '2'):
            hiloCliente = threading.Thread(target=cliente, args=(maquina2,))
            hiloServidor.start()
            hiloCliente.start()
        elif (maquina == '3'):
            hiloCliente = threading.Thread(target=cliente, args=(maquina3,))
            hiloServidor.start()
            hiloCliente.start()
        elif (maquina == '4'):
            hiloCliente = threading.Thread(target=cliente, args=(maquina4,))
            hiloServidor.start()
            hiloCliente.start()
        elif (maquina == '5'):
            hiloCliente = threading.Thread(target=cliente, args=(maquina5,))
            hiloServidor.start()
            hiloCliente.start()


    #hiloServidor.start()
    #hiloServidor.join()


if __name__ == '__main__':
    main()
