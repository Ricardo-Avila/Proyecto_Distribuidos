import socket
from datetime import datetime
import threading

def enviar_mensajes():
    while True:
        user_input = input("Ingrese su mensaje (o escriba 'exit' para salir): ")
        
        if user_input.lower() == 'exit':
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

# Dirección IP y puerto del servidor al que se conectará el cliente
host = '192.168.183.136'
port = 12345

# Crear un objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
s.connect((host, port))
print(f'Conectado al servidor en {host}:{port}')

# Iniciar un hilo para manejar la entrada del usuario y enviar mensajes
thread = threading.Thread(target=enviar_mensajes)
thread.start()

# Esperar a que el hilo termine (cuando el usuario escribe 'exit')
thread.join()

# Cerrar la conexión
s.close()
