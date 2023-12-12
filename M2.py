import socket

# Dirección IP y puerto del servidor al que se conectará el cliente
host = '192.168.183.136'
port = 12345

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
s.connect((host, port))
print(f'Conectado al servidor en {host}:{port}')

# Solicitar al usuario que ingrese un mensaje personalizado
message = input("Ingrese su mensaje: ")

# Enviar el mensaje al servidor
s.sendall(message.encode())

# Cerrar la conexión
s.close()
