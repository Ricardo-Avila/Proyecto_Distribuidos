import socket
from datetime import datetime
import threading

# Obtener la dirección IP de la interfaz de red deseada
def obtener_direccion_ip():
    try:
        # Crear un socket de prueba para obtener la dirección IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        direccion_ip = s.getsockname()[0]
        s.close()
        return direccion_ip
    except Exception as e:
        print(f"Error al obtener la dirección IP: {e}")
        return None

# Dirección IP de la máquina actual
hostname = obtener_direccion_ip()

# Verificar si se obtuvo la dirección IP correctamente
if hostname:
    print(f"Dirección IP de la máquina actual: {hostname}")
else:
    print("No se pudo obtener la dirección IP. Saliendo del programa.")
    exit()

# Objeto compartido para rastrear el estado de conexión y el número de clientes conectados
estado_conexion = {'conectado': False, 'clientes_conectados': 0}
servidores = ['192.183.168.136', '192.183.168.147', '192.183.168.148', '192.183.168.149', '192.183.168.150']
# Filtrar la lista para excluir la dirección IP de la máquina actual
servidores = [ip for ip in servidores if ip != hostname]


def manejar_cliente(conn, addr):
    try:
        # Incrementar el contador de clientes conectados
        estado_conexion['clientes_conectados'] += 1

        # Establecer la variable conectado en True
        estado_conexion['conectado'] = True

        # Obtener la fecha y hora actual de la conexión
        connection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Conexión establecida desde {addr} a las {connection_datetime}')

        while True:
            data = conn.recv(1024)
            if not data:
                # Si el cliente se desconecta, mostrar el mensaje y la hora
                disconnection_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Cliente desconectado desde {addr} a las {disconnection_datetime}')
                break

            # Mostrar el mensaje recibido
            print(f'Datos recibidos de {addr}: {data.decode()}')

            # Obtener la fecha y hora actual
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el mensaje de confirmación con la fecha y hora
            confirmation_message = f"Mensaje recibido por el servidor desde {addr} el {current_datetime}."
            conn.sendall(confirmation_message.encode())

        # Decrementar el contador de clientes conectados
        estado_conexion['clientes_conectados'] -= 1

        # Si no hay más clientes conectados, establecer conectado en False
        if estado_conexion['clientes_conectados'] == 0:
            estado_conexion['conectado'] = False

    except Exception as e:
        print(f"Error de conexión con {addr}: {e}")

    finally:
        # Cerrar la conexión después de salir del bloque try
        conn.close()

def conectar_al_servidor():
    global conectado

    while True:
        try:
            # Solicitar al usuario que ingrese un mensaje personalizado
            user_input = input("Ingrese su mensaje (o escriba 'quit' para cerrar el programa): ")

            if user_input.lower() == 'quit':
                # Si el usuario escribe 'quit', salir del bucle
                break

            # Obtener la hora actual
            current_time = datetime.now().strftime("%H:%M:%S")

            # Crear el mensaje con la hora
            full_message = f"[{current_time}] {user_input}"

            # Iterar sobre la lista de servidores y enviar el mensaje a cada uno
            for servidor in servidores:
                try:
                    # Crear un objeto socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    # Conectar al servidor
                    s.connect((servidor, puerto_servidor))

                    # Enviar el mensaje al servidor
                    s.sendall(full_message.encode())
                    print(f'Mensaje enviado a {servidor}: {full_message}')

                    # Recibir la confirmación del servidor
                    confirmation = s.recv(1024)
                    print(f'Confirmación del servidor {servidor}: {confirmation.decode()}')

                    # Cerrar la conexión
                    s.close()

                except Exception as e:
                    print(f"Error de conexión con {servidor}: {e}")

            # Establecer conectado en False después de enviar los mensajes
            conectado = False

        except Exception as e:
            print(f"Error de entrada: {e}")


#Creacion de la tienda
class Tienda:
    def __init__(self):
        self.articulos = []
        self.clientes = []

    def mostrar_menu(self):
        print("----- Menú -----")
        print("1) Comprar un artículo")
        print("2) Agregar artículo")
        print("3) Eliminar cliente")
        print("4) Agregar cliente")
        print("5) Salir")

    def comprar_articulo(self):
        conectar_al_servidor()
        pass

    def agregar_articulo(self):
        conectar_al_servidor()
        pass

    def eliminar_cliente(self):
        conectar_al_servidor()
        pass

    def agregar_cliente(self):
        conectar_al_servidor()
        pass

# Instancia de la tienda
tienda = Tienda()

while True:
    tienda.mostrar_menu()

    opcion = input("Selecciona una opción (1-5): ")

    if opcion == "1":
        tienda.comprar_articulo()
    elif opcion == "2":
        tienda.agregar_articulo()
    elif opcion == "3":
        tienda.eliminar_cliente()
    elif opcion == "4":
        tienda.agregar_cliente()
    elif opcion == "5":
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción valida.")