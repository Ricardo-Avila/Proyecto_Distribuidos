import socket
from datetime import datetime

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

# Lista para almacenar conexiones de Máquina2 y sus nombres
maquinas2_conectadas = []

while True:
    try:
        # Crear un objeto socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular el socket al host y puerto
        s.bind((host, port))

        # Escuchar conexiones entrantes (máximo 2 conexiones en este ejemplo)
        s.listen(2)

        print(f'Esperando conexiones en {host}:{port}...')

        for i in range(2):
            # Aceptar la conexión entrante
            conn, addr = s.accept()
            print(f'Conexión establecida desde {addr}')

            # Solicitar al usuario un nombre para la Máquina2
            nombre_maquina = input(f'Ingrese un nombre para Máquina2_{i + 1}: ')

            # Agregar la conexión y el nombre a la lista
            maquinas2_conectadas.append((conn, nombre_maquina))

            # Obtener la fecha y hora actual de la conexión
            connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'Máquina2_{i + 1} ({nombre_maquina}) conectada a las {connection_datetime}')

        while True:
            for conn, nombre_maquina in maquinas2_conectadas:
                data = conn.recv(1024)
                if not data:
                    # Si Máquina2 se desconecta, mostrar el mensaje y la hora
                    disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f'{nombre_maquina} desconectada a las {disconnection_datetime}')
                    maquinas2_conectadas.remove((conn, nombre_maquina))
                    break

                # Mostrar el mensaje recibido
                print(f'Datos recibidos de {nombre_maquina}: {data.decode()}')

                # Obtener la fecha y hora actual
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Crear el mensaje de confirmación con la fecha y hora
                confirmation_message = f"Mensaje de {nombre_maquina} recibido por el servidor el {current_datetime}."
                conn.sendall(confirmation_message.encode())

            # Preguntar al usuario si desea reiniciar el servidor o cerrar el programa
            user_input = input("¿Desea reiniciar el servidor? (y/n): ")
            if user_input.lower() != 'y':
                break  # Terminar el programa

    except Exception as e:
        print(f"Error de conexión: {e}")

# Cerrar el socket principal antes de salir del bucle principal
s.close()
