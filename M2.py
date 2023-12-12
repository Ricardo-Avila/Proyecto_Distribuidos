import socket
from datetime import datetime
import threading
import time

def conectar_al_servidor():
    while True:
        try:
            # Dirección IP y puerto del servidor al que se conectará el cliente
            host = '192.168.183.136'
            port = 12345

            # Crear un objeto socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar al servidor
            s.connect((host, port))
            print(f'Conectado al servidor en {host}:{port}')

            while True:
                # Solicitar al usuario que ingrese un mensaje personalizado
                user_input = input("Ingrese su mensaje (o escriba 'quit' para cerrar el programa): ")

                if user_input.lower() == 'quit':
                    return  # Terminar el hilo y cerrar el programa

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

            # Cerrar la conexión
            s.close()

        except Exception as e:
            print(f"Error de conexión: {e}")

        # Esperar antes de intentar nuevamente (por ejemplo, 5 segundos)
        time.sleep(5)

# Iniciar un hilo para manejar la conexión al servidor
thread = threading.Thread(target=conectar_al_servidor)
thread.start()

# Esperar a que el hilo termine (puedes implementar una lógica diferente para manejar esto)
thread.join()
