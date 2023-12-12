import socket
import threading

class Nodo:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.conexiones = []

        # Configurar socket como servidor y cliente
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.puerto))
        self.servidor_socket.listen(5)
        print(f"Nodo creado exitosamente.....")

    def iniciar(self, nodos_destino):
        # Configurar hilo para aceptar conexiones entrantes
        hilo_aceptar = threading.Thread(target=self.aceptar_conexiones)
        hilo_aceptar.start()

        # Conectar a otros nodos
        self.conectar_a_nodos(nodos_destino)

        # Enviar mensajes desde la consola
        while True:
            mensaje = input("Mensaje: ")
            self.enviar_a_todos(mensaje)

    def aceptar_conexiones(self):
        while True:
            cliente, addr = self.servidor_socket.accept()
            self.conexiones.append(cliente)
            print(f"Socket aceptado.......")
            sys.stdout.flush()

            # Configurar hilo para manejar la conexión entrante
            hilo_cliente = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            hilo_cliente.start()
            print(f"Hilo iniciado.....")
            sys.stdout.flush()

    def conectar_a_nodos(self, nodos_destino, puertos_destino):
        min_length = min(len(nodos_destino), len(puertos_destino))
        for i in range(min_length):
            direccion_ip = nodos_destino[i]
            puerto_destino = puertos_destino[i]
            if puerto_destino != self.puerto:
                try:
                    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cliente_socket.connect((direccion_ip, puerto_destino))
                    self.conexiones.append(cliente_socket)
                    print(f"Conectado a nodo en la dirección IP {direccion_ip}, puerto {puerto_destino}")
                except Exception as e:
                    print(f"No se pudo conectar al nodo en la dirección IP {direccion_ip}, puerto {puerto_destino}: {str(e)}")

    def manejar_cliente(self, cliente):
        while True:
            try:
                datos = cliente.recv(1024)
                if not datos:
                    break
                print(f"Mensaje recibido: {datos.decode('utf-8')}")
            except Exception as e:
                print(f"Error al recibir mensajes: {str(e)}")
                break
        # Cerrar el socket al salir del bucle
        cliente.close()
        
    def enviar_a_todos(self, mensaje):
        for conexion in self.conexiones:
            try:
                conexion.send(mensaje.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje: {str(e)}")

# Configuración del nodo
host = '192.168.183.'  # Reemplazar con la dirección IP de la máquina local
puerto = 5555

# Lista de direcciones IP de los nodos destino
nodos_destino = ['192.168.183.', '192.168.183.']
puertos_destino = [5555, 5556, 5557]

# NODO 1 : 192.168.183.136
# NODO 2 : 192.168.183.147
# NODO 3 : 192.168.183.148

nodo = Nodo(host, puerto)
nodo.iniciar(nodos_destino)
