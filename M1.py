import socket
from datetime import datetime
import threading

def manejar_conexion(conn, addr):
    try:
        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si la máquina2 se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Máquina2 ({addr}) desconectada a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de Máquina2 ({addr}): {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje de Máquina2 ({addr}) recibido por el servidor el {current_datetime}."
            conn.sendall(confirmation_message.encode())

    except Exception as e:
        print(f"Error de conexión con Máquina2 ({addr}): {e}")

    finally:
        # Cerrar la conexión después de salir del bloque try
        conn.close()

def iniciar_servidor():
    # Dirección IP y puerto en el que el servidor escuchará
    host = '192.168.183.136'
    port = 12345

    # Crear un objeto socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular el socket al host y puerto
    s.bind((host, port))

    # Escuchar conexiones entrantes (máximo 5 conexiones en este ejemplo)
    s.listen(5)

    print(f'Esperando conexiones en {host}:{port}...')

    try:
        while True:
            # Aceptar la conexión entrante
            conn, addr = s.accept()

            # Iniciar un hilo para manejar la conexión
            threading.Thread(target=manejar_conexion, args=(conn, addr)).start()

    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")

    finally:
        # Cerrar el socket principal después de salir del bucle principal
        s.close()

# Iniciar el servidor
iniciar_servidor()
