import socket
from datetime import datetime

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

while True:
    try:
        # Crear un objeto socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular el socket al host y puerto
        s.bind((host, port))

        # Escuchar conexiones entrantes (máximo 1 conexión en este ejemplo)
        s.listen(1)

        print(f'Esperando una conexión en {host}:{port}...')

        # Aceptar la conexión entrante
        conn, addr = s.accept()

        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si la máquina2 se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Máquina2 desconectada a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de Máquina2: {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje de Máquina2 recibido por el servidor el {current_datetime}."
            conn.sendall(confirmation_message.encode())

        # Cerrar la conexión después de salir del bucle interno
        conn.close()

        # Preguntar al usuario si desea reiniciar el servidor o cerrar el programa
        user_input = input("¿Desea reiniciar el servidor? (y/n): ")
        if user_input.lower() != 'y':
            break  # Terminar el programa

    except Exception as e:
        print(f"Error de conexión: {e}")

# Cerrar el socket principal antes de salir del bucle principal
s.close()
