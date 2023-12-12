import socket
from datetime import datetime
import threading

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

# Lista para almacenar conexiones activas
conexiones = []

def manejar_cliente(conn, addr):
    try:
        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si la máquina2 se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Máquina2 desconectada desde {addr} a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de Máquina2 ({addr}): {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje de Máquina2 ({addr}) recibido por el servidor el {current_datetime}."
            conn.sendall(confirmation_message.encode())

        # Cerrar la conexión después de salir del bucle interno
        conn.close()
        conexiones.remove(conn)

    except Exception as e:
        print(f"Error de conexión con Máquina2 ({addr}): {e}")
        conexiones.remove(conn)

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
s.bind((host, port))

# Escuchar conexiones entrantes (máximo 5 conexiones en este ejemplo)
s.listen(5)

print(f'Esperando conexiones en {host}:{port}...')

while len(conexiones) < 5:
    # Aceptar la conexión entrante
    conn, addr = s.accept()
    conexiones.append(conn)

    # Iniciar un hilo para manejar el cliente
    thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()

# Cerrar el socket principal después de salir del bucle principal
s.close()
