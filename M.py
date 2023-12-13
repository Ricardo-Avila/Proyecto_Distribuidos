import socket
from datetime import datetime
import threading

# Objeto compartido para rastrear el estado de conexión y el número de clientes conectados
estado_conexion = {'conectado': False, 'clientes_conectados': 0}
servidores = ['192.183.168.136', '192.183.168.147', '192.183.168.148', '192.183.168.149', '192.183.168.150']
hostname = socket.gethostbyname(socket.gethostname())


def manejar_cliente(conn, addr):
    try:
        # Incrementar el contador de clientes conectados
        estado_conexion['clientes_conectados'] += 1

        # Establecer la variable conectado en True
        estado_conexion['conectado'] = True

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

        # Decrementar el contador de clientes conectados
        estado_conexion['clientes_conectados'] -= 1

        # Si no hay más clientes conectados, establecer conectado en False
        if estado_conexion['clientes_conectados'] == 0:
            estado_conexion['conectado'] = False

    except Exception as e:
        print(f"Error de conexión con {addr}: {e}")

    finally:
        # Cerrar la conexión después de salir del bloque try
        conn.close()

def conectar_al_servidor():
    global conectado

    while True:
        try:
            # Solicitar al usuario que ingrese un mensaje personalizado
            user_input = input("Ingrese su mensaje (o escriba 'quit' para cerrar el programa): ")

            if user_input.lower() == 'quit':
                # Si el usuario escribe 'quit', salir del bucle
                break

            # Obtener la hora actual
            current_time = datetime.now().strftime("%H:%M:%S")

            # Crear el mensaje con la hora
            full_message = f"[{current_time}] {user_input}"

            # Iterar sobre la lista de servidores y enviar el mensaje a cada uno
            for servidor in servidores:
                try:
                    # Crear un objeto socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    # Conectar al servidor
                    s.connect((servidor, puerto_servidor))

                    # Enviar el mensaje al servidor
                    s.sendall(full_message.encode())
                    print(f'Mensaje enviado a {servidor}: {full_message}')

                    # Recibir la confirmación del servidor
                    confirmation = s.recv(1024)
                    print(f'Confirmación del servidor {servidor}: {confirmation.decode()}')

                    # Cerrar la conexión
                    s.close()

                except Exception as e:
                    print(f"Error de conexión con {servidor}: {e}")

            # Establecer conectado en False después de enviar los mensajes
            conectado = False

        except Exception as e:
            print(f"Error de entrada: {e}")

# Solicitar al usuario que elija ser servidor, cliente o finalizar programa
while True:
    opcion = input("¿Desea ser servidor (s), cliente (c) o finalizar programa (f)? ")

    if opcion.lower() == 's':
        # Código para el servidor
        host = hostname
        print(f'Dirección IP de la máquina actual: {hostname}')
        port = 12345

        # Crear un objeto socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular el socket al host y puerto
        server_socket.bind((host, port))

        # Escuchar conexiones entrantes (máximo 2 conexiones concurrentes en este ejemplo)
        server_socket.listen(2)

        print(f'Esperando conexiones en {host}:{port}...')

        while True:
            try:
                # Aceptar la conexión entrante
                conn, addr = server_socket.accept()

                # Iniciar un hilo para manejar la conexión del cliente
                client_thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
                client_thread.start()

            except Exception as e:
                print(f"Error de conexión: {e}")

            # Si no hay más clientes conectados, salir del bucle principal
            if not estado_conexion['conectado']:
                break

    elif opcion.lower() == 'c':
        # Código para el cliente
        conectar_al_servidor()

    elif opcion.lower() == 'f':
        # Finalizar el programa
        break

    else:
        print("Opción no válida. Intente de nuevo.")
