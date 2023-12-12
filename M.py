import socket
import threading
from datetime import datetime

def manejar_conexion_entrante(socket_entrada, nombre):
    while True:
        data = socket_entrada.recv(1024)
        if not data:
            disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'{nombre} desconectada a las {disconnection_datetime}')
            break

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Datos recibidos de {nombre}: {data.decode()} a las {current_datetime}')

def conectar_a_otra_maquina(ip, port, nombre):
    try:
        # Crear un socket para enviar mensajes
        socket_envio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_envio.connect((ip, port))

        # Crear un socket para recibir mensajes
        socket_entrada = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_entrada.bind(('0.0.0.0', 0))
        socket_entrada.listen(1)

        # Enviar al otro extremo la información para conectarse
        local_ip, local_port = socket_entrada.getsockname()
        socket_envio.sendall(f"{local_ip},{local_port}".encode())

        # Aceptar la conexión entrante del otro extremo
        conn_entrada, addr_entrada = socket_entrada.accept()

        print(f'Conexión establecida con {nombre}')

        # Iniciar hilos para manejar la comunicación en ambas direcciones
        hilo_entrada = threading.Thread(target=manejar_conexion_entrante, args=(conn_entrada, nombre))
        hilo_entrada.start()

        while True:
            # Solicitar al usuario que ingrese un mensaje personalizado
            user_input = input(f'[{nombre}] Ingrese su mensaje (o escriba "quit" para cerrar el programa): ')

            if user_input.lower() == 'quit':
                break

            # Obtener la hora actual
            current_time = datetime.now().strftime("%H:%M:%S")

            # Crear el mensaje con la hora
            full_message = f"[{current_time}] {user_input}"

            # Enviar el mensaje al otro extremo
            socket_envio.sendall(full_message.encode())
            print(f'Mensaje enviado: {full_message}')

        # Cerrar las conexiones al salir del bucle
        socket_envio.close()
        conn_entrada.close()

    except Exception as e:
        print(f"Error de conexión: {e}")

# Obtener la dirección IP local de la máquina actual
local_ip = socket.gethostbyname(socket.gethostname())
print(f'Dirección IP local de esta máquina: {local_ip}')

# Configuración de la conexión a la otra máquina
ip_otra_maquina = input('Ingrese la dirección IP de la otra máquina: ')
port_otra_maquina = int(input('Ingrese el puerto para la conexión: '))

# Iniciar el hilo para conectar a la otra máquina
hilo_conexion = threading.Thread(target=conectar_a_otra_maquina, args=(ip_otra_maquina, port_otra_maquina, 'Máquina2'))
hilo_conexion.start()

# Esperar a que el hilo termine (puedes implementar una lógica diferente para manejar esto)
hilo_conexion.join()
