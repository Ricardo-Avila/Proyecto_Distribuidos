import socket
from datetime import datetime
import threading

# Objeto compartido para rastrear el estado de conexión y el número de clientes conectados
estado_conexion = {'conectado': False, 'clientes_conectados': 0}

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

def iniciar_servidor():
    global estado_conexion

    # Código para el servidor
    host = input("Ingresa la direccion IP del servidor: ")
    port = 12345

    # Crear un objeto socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular el socket al host y puerto
    server_socket.bind((host, port))

    # Escuchar conexiones entrantes (máximo 2 conexiones concurrentes en este ejemplo)
    server_socket.listen(2)

    print(f'Esperando conexiones en {host}:{port}...')

    while estado_conexion['conectado']:
        try:
            # Aceptar la conexión entrante
            conn, addr = server_socket.accept()

            # Iniciar un hilo para manejar la conexión del cliente
            client_thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            client_thread.start()

        except Exception as e:
            print(f"Error de conexión: {e}")

    # Cerrar el socket principal antes de salir del bucle principal
    server_socket.close()

def conectar_al_servidor():
    while True:
        try:
            # Solicitar al usuario que ingrese la dirección IP del servidor
            server_ip = input("Ingrese la dirección IP del servidor (o escriba 'quit' para cerrar el programa): ")
            
            if server_ip.lower() == 'quit':
                return  # Terminar el hilo y cerrar el programa

            # Solicitar al usuario que ingrese el puerto del servidor
            server_port = 12345

            # Crear un objeto socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar al servidor
            s.connect((server_ip, int(server_port)))

            # Obtener la fecha y hora actual de la conexión
            connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'Conectado al servidor en {server_ip}:{server_port} a las {connection_datetime}')

            while True:
                # Solicitar al usuario que ingrese un mensaje personalizado
                user_input = input("Ingrese su mensaje (o escriba 'quit' para cerrar el programa): ")

                if user_input.lower() == 'quit':
                    break

                # Obtener la hora actual
                current_time = datetime.now().strftime("%H:%M:%S")

                # Crear el mensaje con la hora
                full_message = f"[{current_time}] {user_input}"

                # Enviar el mensaje al servidor
                s.sendall(full_message.encode())
                print(f'Mensaje enviado: {full_message}')

                # Recibir la confirmación del servidor
                confirmation = s.recv(1024)
                print(f'Confirmación del servidor: {confirmation.decode()}')

            # Cerrar la conexión
            s.close()

        except Exception as e:
            print(f"Error de conexión: {e}")
            
# Solicitar al usuario que elija ser servidor, cliente o finalizar programa
while True:
    opcion = input("¿Desea ser servidor (s), cliente (c) o finalizar programa (f)? ")

    if opcion.lower() == 's':
        # Iniciar el servidor en un hilo
        server_thread = threading.Thread(target=iniciar_servidor)
        server_thread.start()

    elif opcion.lower() == 'c':
        # Código para el cliente
        conectar_al_servidor()

    elif opcion.lower() == 'f':
        # Finalizar el programa
        estado_conexion['conectado'] = False
        break

    else:
        print("Opción no válida. Intente de nuevo.")
