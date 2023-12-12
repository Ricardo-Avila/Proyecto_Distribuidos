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

# Solicitar al usuario que ingrese mensajes personalizados
messages = []
while True:
    user_input = input("Ingrese su mensaje (o escriba 'exit' para salir): ")
    
    if user_input.lower() == 'exit':
        break
    
    # Obtener la hora actual
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Crear el mensaje con la hora
    full_message = f"[{current_time}] {user_input}"
    
    # Agregar el mensaje a la lista
    messages.append(full_message)

# Enviar la serie de mensajes al servidor
for message in messages:
    s.sendall(message.encode())
    print(f'Mensaje enviado: {message}')

# Cerrar la conexión
s.close()
