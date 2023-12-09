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

    def iniciar(self):
        # Configurar hilo para aceptar conexiones entrantes
        hilo_aceptar = threading.Thread(target=self.aceptar_conexiones)
        hilo_aceptar.start()

        # Conectar a otros nodos
        self.conectar_a_nodos()

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

    def conectar_a_nodos(self):
        # Configurar conexiones a otros nodos
        for i in range(1, 4):  # Conectar a nodos en el rango del puerto 5556 al 5558
            if i != self.puerto % 5555:
                try:
                    self.cliente_socket.connect((self.host, (self.puerto + i) % 5555))
                    self.conexiones.append(self.cliente_socket)
                    print(f"Conectado a nodo en el puerto {(self.puerto + i) % 5555}")
                except Exception as e:
                    print(f"No se pudo conectar al nodo en el puerto {(self.puerto + i) % 5555}: {str(e)}")

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
host = '127.0.0.1'
puerto = 5555

nodo = Nodo(host, puerto)
nodo.iniciar()
