import socket
from datetime import datetime
import threading
import time

def conectar_al_servidor():
    while True:
        try:
            # Solicitar al usuario que ingrese la dirección IP del servidor
            server_ip = input("Ingrese la dirección IP del servidor (o escriba 'quit' para cerrar el programa): ")
            
            if server_ip.lower() == 'quit':
                return  # Terminar el hilo y cerrar el programa

            # Solicitar al usuario que ingrese el puerto del servidor
            server_port = input("Ingrese el puerto del servidor: ")

            # Crear un objeto socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar al servidor
            s.connect((server_ip, int(server_port)))

            # Obtener la fecha y hora actual de la conexión
            connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'Conectado al servidor en {server_ip}:{server_port} a las {connection_datetime}')

            while True:
                # Solicitar al usuario que ingrese un mensaje personalizado
                user_input = input("Ingrese su mensaje (o escriba 'quit' para cerrar el programa): ")

                if user_input.lower() == 'quit':
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
