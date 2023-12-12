import socket
from datetime import datetime
import threading

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

# Diccionario para almacenar nombres de clientes
nombres_clientes = {}
contador_clientes = 1

def manejar_cliente(conn, addr):
    global contador_clientes

    try:
        # Asignar un nombre al cliente
        nombre_cliente = f"Cliente {contador_clientes:02d}"
        contador_clientes += 1
        nombres_clientes[conn] = nombre_cliente

        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} para {nombre_cliente} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si el cliente se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'{nombre_cliente} desconectado desde {addr} a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de {nombre_cliente} ({addr}): {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje de {nombre_cliente} ({addr}) recibido por el servidor el {current_datetime}."
            conn.sendall(confirmation_message.encode())

        # Cerrar la conexión después de salir del bucle interno
        conn.close()
        del nombres_clientes[conn]

    except Exception as e:
        print(f"Error de conexión con {nombre_cliente} ({addr}): {e}")
        del nombres_clientes[conn]

def reiniciar_servidor():
    global nombres_clientes, contador_clientes
    nombres_clientes = {}
    contador_clientes = 1

    # Preguntar al usuario si desea reiniciar el servidor
    reiniciar = input("¿Desea reiniciar el servidor? (y/n): ")
    return reiniciar.lower() == 'y'

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
s.bind((host, port))

while True:
    try:
        # Escuchar conexiones entrantes (máximo 5 conexiones en este ejemplo)
        s.listen(5)
        print(f'Esperando conexiones en {host}:{port}...')

        while len(nombres_clientes) < 5:
            # Aceptar la conexión entrante
            conn, addr = s.accept()

            # Iniciar un hilo para manejar el cliente
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()

        # Preguntar al usuario si desea reiniciar el servidor
        if not reiniciar_servidor():
            break

    except Exception as e:
        print(f"Error de servidor: {e}")

# Cerrar el socket principal después de salir del bucle principal
s.close()
