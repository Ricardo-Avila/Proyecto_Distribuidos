import socket
from datetime import datetime
import threading

# Dirección IP y puerto en el que el servidor escuchará
host = '192.168.183.136'
port = 12345

# Lista para almacenar las conexiones de los clientes
clientes = []

def manejar_cliente(cliente, addr):
    try:
        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = cliente.recv(1024)
            if not data:
                # Si el cliente se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Cliente desconectado ({addr}) a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de Cliente ({addr}): {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje de Cliente ({addr}) recibido por el servidor el {current_datetime}."
            cliente.sendall(confirmation_message.encode())

        # Cerrar la conexión después de salir del bucle interno
        cliente.close()

        # Eliminar la conexión del cliente de la lista
        clientes.remove((cliente, addr))

        # Verificar si todas las máquinas 02 se desconectaron
        if not clientes:
            reiniciar_servidor = input("¿Desea reiniciar el servidor? (y/n): ")
            if reiniciar_servidor.lower() != 'y':
                break  # Terminar el programa

    except Exception as e:
        print(f"Error de conexión con Cliente ({addr}): {e}")

def esperar_conexiones():
    while True:
        try:
            # Crear un objeto socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Vincular el socket al host y puerto
            s.bind((host, port))

            # Escuchar conexiones entrantes (hasta 5 conexiones en este ejemplo)
            s.listen(5)

            print(f'Esperando conexiones en {host}:{port}...')

            # Aceptar la conexión entrante
            cliente, addr = s.accept()

            # Agregar la conexión del cliente a la lista
            clientes.append((cliente, addr))

            # Iniciar un hilo para manejar la conexión del cliente
            thread = threading.Thread(target=manejar_cliente, args=(cliente, addr))
            thread.start()

        except Exception as e:
            print(f"Error al esperar conexiones: {e}")

# Iniciar un hilo para esperar conexiones
thread = threading.Thread(target=esperar_conexiones)
thread.start()

# Esperar a que el hilo termine (puedes implementar una lógica diferente para manejar esto)
thread.join()
