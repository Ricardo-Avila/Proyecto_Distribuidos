import socket
from datetime import datetime
import threading
import time

def enviar_al_servidor():
    try:
        # Dirección IP y puerto del servidor al que se conectará el cliente
        host = '192.168.183.136'
        port = 12345

        # Crear un objeto socket para enviar mensajes al servidor
        s_enviar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_enviar.connect((host, port))

        while True:
            # Solicitar al usuario que ingrese un mensaje personalizado
            user_input = input("Ingrese su mensaje para el servidor (o escriba 'quit' para cerrar el programa): ")

            if user_input.lower() == 'quit':
                break

            # Obtener la hora actual
            current_time = datetime.now().strftime("%H:%M:%S")

            # Crear el mensaje con la hora
            full_message = f"[{current_time}] {user_input}"

            # Enviar el mensaje al servidor
            s_enviar.sendall(full_message.encode())
            print(f'Mensaje enviado al servidor: {full_message}')

        # Cerrar la conexión para enviar mensajes al servidor
        s_enviar.close()

    except Exception as e:
        print(f"Error de conexión al enviar mensajes al servidor: {e}")

def recibir_del_servidor():
    try:
        # Dirección IP y puerto del servidor al que se conectará el cliente
        host = '192.168.183.136'
        port = 12346  # Puerto diferente para la conexión de recepción del servidor

        # Crear un objeto socket para recibir mensajes del servidor
        s_recibir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_recibir.connect((host, port))

        while True:
            # Recibir mensajes del servidor
            data = s_recibir.recv(1024)
            if not data:
                break

            # Mostrar el mensaje recibido del servidor
            print(f'Mensaje recibido del servidor: {data.decode()}')

        # Cerrar la conexión para recibir mensajes del servidor
        s_recibir.close()

    except Exception as e:
        print(f"Error de conexión al recibir mensajes del servidor: {e}")

# Iniciar dos hilos para manejar cada conexión por separado
thread_enviar = threading.Thread(target=enviar_al_servidor)
thread_recibir = threading.Thread(target=recibir_del_servidor)

# Iniciar los hilos
thread_enviar.start()
thread_recibir.start()

# Esperar a que ambos hilos terminen (puedes implementar una lógica diferente para manejar esto)
thread_enviar.join()
thread_recibir.join()
