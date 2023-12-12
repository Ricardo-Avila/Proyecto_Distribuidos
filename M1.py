import socket

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
print(f'Conexión establecida desde {addr}')

# Recibir datos del cliente
data = conn.recv(1024)
print(f'Datos recibidos: {data.decode()}')

# Cerrar la conexión
conn.close()
