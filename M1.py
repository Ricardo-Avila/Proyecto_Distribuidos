import socket
from datetime import datetime

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
s.bind((host, port))

# Escuchar conexiones entrantes (máximo 1 conexión en este ejemplo)
s.listen(1)

print(f'Esperando una conexión en {host}:{port}...')

try:
    # Aceptar la conexión entrante
    conn, addr = s.accept()

    # Obtener la fecha y hora actual de la conexión
    connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'Conexión establecida desde {addr} a las {connection_datetime}')

    # Recibir y mostrar datos del cliente
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                # Si el cliente se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Cliente desconectado a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos del cliente: {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje recibido por el servidor el {current_datetime}."
            conn.sendall(confirmation_message.encode())

        except ConnectionResetError:
            # Si la conexión se reinicia abruptamente (por ejemplo, cuando se apaga la máquina cliente),
            # mostrar el mensaje y la hora
            disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'Cliente desconectado abruptamente a las {disconnection_datetime}')
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar la conexión después de salir del bloque try
    if 'conn' in locals():
        conn.close()
