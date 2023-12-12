import socket
from datetime import datetime

# Dirección IP y puerto del servidor al que se conectará el cliente
host = '192.168.183.136'
port = 12345

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
s.connect((host, port))
print(f'Conectado al servidor en {host}:{port}')

# Enviar una serie de mensajes al servidor
messages = ["Hola, servidor!", "¿Cómo estás?", "Este es otro mensaje."]
for message in messages:
    # Obtener la hora actual
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Crear el mensaje con la hora
    full_message = f"[{current_time}] {message}"
    
    # Enviar el mensaje al servidor
    s.sendall(full_message.encode())
    print(f'Mensaje enviado: {full_message}')

# Cerrar la conexión
s.close()
