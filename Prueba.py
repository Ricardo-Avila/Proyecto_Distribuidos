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

            # Configurar hilo para manejar la conexión entrante
            hilo_cliente = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            hilo_cliente.start()

    def conectar_a_nodos(self, nodos_destino):
        # Configurar conexiones a otros nodos
        for i, direccion_ip in enumerate(nodos_destino):
            if i != self.puerto % 5555:
                try:
                    self.cliente_socket.connect((direccion_ip, (self.puerto + i) % 5555))
                    self.conexiones.append(self.cliente_socket)
                    print(f"Conectado a nodo en la dirección IP {direccion_ip}, puerto {(self.puerto + i) % 5555}")
                except Exception as e:
                    print(f"No se pudo conectar al nodo en la dirección IP {direccion_ip}, puerto {(self.puerto + i) % 5555}: {str(e)}")

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

    def enviar_a_todos(self, mensaje):
        for conexion in self.conexiones:
            try:
                conexion.send(mensaje.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje: {str(e)}")

# Configuración del nodo
host = 'dirección_IP_local'  # Reemplazar con la dirección IP de la máquina local
puerto = 5555

# Lista de direcciones IP de los nodos destino
nodos_destino = ['dirección_IP_nodo1', 'dirección_IP_nodo2']

# NODO 1 : 192.168.183.136
# NODO 2 : 192.168.183.147
# NODO 3 : 192.168.183.148

nodo = Nodo(host, puerto)
nodo.iniciar(nodos_destino)
