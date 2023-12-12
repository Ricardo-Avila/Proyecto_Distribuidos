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

# Aceptar la conexión entrante
conn, addr = s.accept()

# Obtener la fecha y hora actual de la conexión
connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'Conexión establecida desde {addr} a las {connection_datetime}')

# Recibir y mostrar datos del cliente
while True:
    data = conn.recv(1024)
    if not data:
        break
    
    # Mostrar el mensaje recibido
    print(f'Datos recibidos del cliente: {data.decode()}')
    
    # Obtener la fecha y hora actual
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Crear el mensaje de confirmación con la fecha y hora
    confirmation_message = f"Mensaje recibido por el servidor el {current_datetime}."
    conn.sendall(confirmation_message.encode())

# Cerrar la conexión después de salir del bucle
conn.close()
