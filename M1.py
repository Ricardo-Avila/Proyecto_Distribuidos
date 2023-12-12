import socket
from datetime import datetime
import threading

def manejar_cliente(conn_enviar, conn_recibir, addr):
    try:
        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            # Recibir mensajes del cliente para el servidor
            data_enviar = conn_enviar.recv(1024)
            if not data_enviar:
                break

            # Mostrar el mensaje recibido del cliente para el servidor
            print(f'Datos recibidos del cliente para el servidor: {data_enviar.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje del cliente para el servidor recibido el {current_datetime}."
            conn_enviar.sendall(confirmation_message.encode())

        # Cerrar la conexión del cliente para enviar mensajes al servidor
        conn_enviar.close()

    except Exception as e:
        print(f"Error de conexión al manejar cliente para enviar mensajes al servidor: {e}")

    finally:
        # Cerrar la conexión del cliente para recibir mensajes del servidor
        conn_recibir.close()

def recibir_del_cliente(conn_recibir, addr):
    try:
        while True:
            # Recibir mensajes del cliente para el servidor
            data_recibir = conn_recibir.recv(1024)
            if not data_recibir:
                break

            # Mostrar el mensaje recibido del cliente para el servidor
            print(f'Datos recibidos del cliente para el servidor: {data_recibir.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje del cliente para el servidor recibido el {current_datetime}."
            conn_recibir.sendall(confirmation_message.encode())

        # Cerrar la conexión del cliente para recibir mensajes del servidor
        conn_recibir.close()

    except Exception as e:
        print(f"Error de conexión al manejar cliente para recibir mensajes del servidor: {e}")

def iniciar_servidor():
    # Dirección IP y puerto en el que el servidor escuchará para enviar mensajes al servidor
    host_enviar = '192.168.183.136'
    port_enviar = 12345

    # Dirección IP y puerto en el que el servidor escuchará para recibir mensajes del servidor
    host_recibir = '192.168.183.136'
    port_recibir = 12346

    try:
        # Crear un objeto socket para enviar mensajes al servidor
        s_enviar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_enviar.bind((host_enviar, port_enviar))
        s_enviar.listen(1)

        # Crear un objeto socket para recibir mensajes del servidor
        s_recibir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_recibir.bind((host_recibir, port_recibir))
        s_recibir.listen(1)

        print(f'Esperando conexiones en {host_enviar}:{port_enviar} para enviar mensajes al servidor...')
        print(f'Esperando conexiones en {host_recibir}:{port_recibir} para recibir mensajes del servidor...')

        while True:
            # Aceptar conexiones entrantes para enviar mensajes al servidor
            conn_enviar, addr_enviar = s_enviar.accept()

            # Aceptar conexiones entrantes para recibir mensajes del servidor
            conn_recibir, addr_recibir = s_recibir.accept()

            # Iniciar un hilo para manejar cada conexión por separado
            thread_cliente = threading.Thread(target=manejar_cliente, args=(conn_enviar, conn_recibir, addr_enviar))
            thread_servidor = threading.Thread(target=recibir_del_cliente, args=(conn_recibir, addr_recibir))

            # Iniciar los hilos
            thread_cliente.start()
            thread_servidor.start()

    except Exception as e:
        print(f"Error de conexión al iniciar el servidor: {e}")

    finally:
        # Cerrar los sockets principales después de salir del bucle principal
        s_enviar.close()
        s_recibir.close()

# Iniciar el servidor
iniciar_servidor()
