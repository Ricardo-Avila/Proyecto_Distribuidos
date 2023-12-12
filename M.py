import socket
from datetime import datetime
import threading

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

def manejar_cliente(conn, addr):
    try:
        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si el cliente se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Cliente desconectado desde {addr} a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de {addr}: {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje recibido por el servidor desde {addr} el {current_datetime}."
            conn.sendall(confirmation_message.encode())

    except Exception as e:
        print(f"Error de conexión con {addr}: {e}")

    finally:
        # Cerrar la conexión después de salir del bloque try
        conn.close()

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
s.bind((host, port))

# Escuchar conexiones entrantes (máximo 2 conexiones concurrentes en este ejemplo)
s.listen(2)

print(f'Esperando conexiones en {host}:{port}...')

# Lista para almacenar los hilos de manejo de clientes
threads = []

while True:
    try:
        # Aceptar la conexión entrante
        conn, addr = s.accept()

        # Iniciar un hilo para manejar la conexión del cliente
        client_thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        client_thread.start()

        # Agregar el hilo a la lista
        threads.append(client_thread)

        # Eliminar hilos terminados
        threads = [thread for thread in threads if thread.is_alive()]

        # Si no hay más hilos activos, preguntar si se desea reiniciar o terminar el programa
        if not threads:
            user_input = input("Todos los clientes se han desconectado. ¿Desea reiniciar el servidor? (y/n): ")
            if user_input.lower() != 'y':
                break  # Terminar el programa

    except Exception as e:
        print(f"Error de conexión: {e}")

# Esperar a que todos los hilos terminen antes de cerrar el socket principal
for thread in threads:
    thread.join()

# Cerrar el socket principal
s.close()
