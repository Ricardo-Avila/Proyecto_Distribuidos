#VICENTE URILE RICARDO

import socket
import threading
import pickle

class Nodo:
    def __init__(self, nombre, ip, puerto):
        self.nombre = nombre
        self.ip = ip
        self.puerto = puerto
        self.inventario = {}  
        self.clientes = set()
        self.mutex_inventario = threading.Lock()
        self.mutex_clientes = threading.Lock()

    def enviar_datos(self, data, ip_destino, puerto_destino):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_destino, puerto_destino))
            s.sendall(pickle.dumps(data))

    def recibir_datos(self, conn):
        data = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
        return pickle.loads(data)

    def manejar_cliente(self, conn, addr, contenido):
       
        pass

    def manejar_sucursal(self, conn, addr, contenido):
        
        pass

    def manejar_conexion(self, conn, addr):
        data = self.recibir_datos(conn)

        if data['tipo'] == 'cliente':
            self.manejar_cliente(conn, addr, data['contenido'])
        elif data['tipo'] == 'sucursal':
            self.manejar_sucursal(conn, addr, data['contenido'])

    def iniciar_servidor(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.puerto))
            s.listen()

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.manejar_conexion, args=(conn, addr)).start()

    def distribuir_articulos(self):
        
        pass

    def consultar_actualizar_clientes(self):
        
        pass

    def comprar_articulo(self):
        # Lógica para comprar un artículo con exclusión mutua
        pass

    def generar_guia_envio(self, id_articulo, serie, id_cliente):
        # Lógica para generar y guardar la guía de envío y actualizar inventario distribuido
        pass

    def agregar_articulos_inventario(self):
        # Lógica para agregar artículos al inventario general distribuido
        pass

    def consenso(self):
        # Lógica para lograr consenso en las actualizaciones de datos
        pass

    def redistribuir_articulos(self):
        # Lógica para redistribuir artículos en caso de falla de sistema en una sucursal
        pass

    def eleccion(self):
        # Lógica para llevar a cabo una elección en caso de falla del nodo maestro
        pass

# Configuración de los nodos
nodo_maestro = Nodo("Maestro", "127.0.0.1", 5000)
sucursal_1 = Nodo("Sucursal1", "127.0.0.1", 5001)
sucursal_2 = Nodo("Sucursal2", "127.0.0.1", 5002)

# Iniciar los servidores en hilos separados
threading.Thread(target=nodo_maestro.iniciar_servidor).start()
threading.Thread(target=sucursal_1.iniciar_servidor).start()
threading.Thread(target=sucursal_2.iniciar_servidor).start()

# Iniciar la lógica del sistema (puede ser en un bucle infinito)
# nodo_maestro.distribuir_articulos()
# nodo_maestro.consultar_actualizar_clientes()
# nodo_maestro.comprar_articulo()
# nodo_maestro.generar_guia_envio()
# nodo_maestro.agregar_articulos_inventario()
# nodo_maestro.consenso()
# nodo_maestro.redistribuir_articulos()
# nodo_maestro.eleccion()

