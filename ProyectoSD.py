#VICENTE URILE RICARDO

import socket
import threading
import pickle

class Nodo:
    def __init__(self, nombre, ip, puerto): #Iniciacion de un nuevo objeto NODO
        self.nombre = nombre
        self.ip = ip
        self.puerto = puerto
        self.inventario = {}  
        self.clientes = set()
        self.mutex_inventario = threading.Lock() #Exclusion mutua para el inventario
        self.mutex_clientes = threading.Lock() #Exclusion mutua para los clientes
    
    #RICARDO 
    def enviar_mensaje(self, ip_destino, puerto_destino, tipo_destino):
        mensaje = input("Ingrese un mensaje: ")
        data = {'tipo': tipo_destino, 'contenido': mensaje}
        self.enviar_datos(data, ip_destino, puerto_destino)

    def enviar_datos(self, data, ip_destino, puerto_destino):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Crea un socket utilizando IPv4 (AF_INET) y TCP (SOCK_STREAM)
        # El uso de "with" garantiza que el socket se cierre correctamente después de su uso.
            s.connect((ip_destino, puerto_destino))
            # Establece una conexión con el nodo de destino especificado usando la dirección IP y el puerto.
            s.sendall(pickle.dumps(data))
            # Serializa los datos utilizando el módulo "pickle" y luego envía los datos serializados a través del socket.

    def recibir_datos(self, conn):
        # Inicializa una variable para almacenar los datos recibidos
        data = b""
        # Inicia un bucle infinito para recibir datos en bloques (chunks)
        while True:
            # Recibe un bloque de datos (máximo 1024 bytes) a través de la conexión 'conn'
            chunk = conn.recv(1024)
            # Verifica si el bloque recibido es vacío (indicando que la conexión se cerró)
            if not chunk:
                # Si el bloque es vacío, termina el bucle
                break
            # Concatena el bloque recibido a los datos existentes
            data += chunk
        # Deserializa los datos recibidos utilizando el módulo 'pickle' y los devuelve
        return pickle.loads(data)

    def manejar_cliente(self, conn, addr, contenido):
        try:
            print(f"Cliente conectado desde {addr}. Contenido recibido: {contenido}")
            # Puedes implementar aquí la lógica específica para manejar a los clientes

            # Envía una respuesta de vuelta al cliente (esto es un ejemplo, ajusta según tus necesidades)
            respuesta = {'mensaje': 'Mensaje recibido correctamente'}
            self.enviar_datos(respuesta, addr[0], addr[1])

        finally:
            conn.close()

    def manejar_sucursal(self, conn, addr, contenido):
        try:
            print(f"Sucursal conectado desde {addr}. Contenido recibido: {contenido}")
            # Puedes implementar aquí la lógica específica para manejar a los clientes

            # Envía una respuesta de vuelta al cliente (esto es un ejemplo, ajusta según tus necesidades)
            respuesta = {'mensaje': 'Mensaje recibido correctamente'}
            self.enviar_datos(respuesta, addr[0], addr[1])

        finally:
            conn.close()

    def manejar_conexion(self, conn, addr):
        try:
            # Recibe datos a través de la conexión utilizando el método recibir_datos
            data = self.recibir_datos(conn)

            # Verifica el tipo de datos recibidos
            if data['tipo'] == 'cliente':
                # Si el tipo es 'cliente', llama al método manejar_cliente
                self.manejar_cliente(conn, addr, data['contenido'])
            elif data['tipo'] == 'sucursal':
                # Si el tipo es 'sucursal', llama al método manejar_sucursal
                self.manejar_sucursal(conn, addr, data['contenido'])
        
        except Exception as e:
            print(f"Error al manejar la conexión: {e}")
        finally:
            conn.close()

    def iniciar_servidor(self):
        # Crea un socket para el servidor utilizando IPv4 (AF_INET) y TCP (SOCK_STREAM)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Asocia el socket con la dirección IP y el puerto especificados
            s.bind((self.ip, self.puerto))
            
            # Habilita el socket para aceptar conexiones entrantes
            s.listen()

            # Inicia un bucle infinito para esperar y manejar conexiones entrantes
            while True:
                # Acepta una conexión entrante y obtiene el objeto de conexión (conn) y la dirección del cliente (addr)
                conn, addr = s.accept()

                # Inicia un nuevo hilo para manejar la conexión utilizando el método manejar_conexion
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

    def conectar_con_nodos(self, nodos):
        for nodo in nodos:
            if nodo != self:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((nodo.ip, nodo.puerto))
                        data = {'tipo': 'nodo', 'contenido': f"Hola, soy {self.tipo} {self.nombre}"}
                        s.sendall(pickle.dumps(data))
                    except Exception as e:
                        print(f"Error al conectar con el nodo {nodo.nombre}: {e}")

# Configuración de los nodos
nodo_maestro = Nodo("Maestro", "127.0.0.1", 5000)
sucursal_1 = Nodo("Sucursal1", "127.0.0.1", 5001)
sucursal_2 = Nodo("Sucursal2", "127.0.0.1", 5002)
cliente_1 = Nodo("Cliente1", "127.0.0.1", 5003)
cliente_2 = Nodo("Cliente2", "127.0.0.1", 5004)

# Iniciar los servidores en hilos separados
threading.Thread(target=nodo_maestro.iniciar_servidor).start()
threading.Thread(target=sucursal_1.iniciar_servidor).start()
threading.Thread(target=sucursal_2.iniciar_servidor).start()
threading.Thread(target=cliente_1.iniciar_servidor).start()
threading.Thread(target=cliente_2.iniciar_servidor).start()

# Conectar todos los nodos entre sí
nodo_maestro.conectar_con_nodos([sucursal_1, sucursal_2, cliente_1, cliente_2])
sucursal_1.conectar_con_nodos([nodo_maestro, sucursal_2, cliente_1, cliente_2])
sucursal_2.conectar_con_nodos([nodo_maestro, sucursal_1, cliente_1, cliente_2])
cliente_1.conectar_con_nodos([nodo_maestro, sucursal_1, sucursal_2, cliente_2])
cliente_2.conectar_con_nodos([nodo_maestro, sucursal_1, sucursal_2, cliente_1])

# Iniciar la lógica del sistema (puede ser en un bucle infinito)
# nodo_maestro.distribuir_articulos()
# nodo_maestro.consultar_actualizar_clientes()
# nodo_maestro.comprar_articulo()
# nodo_maestro.generar_guia_envio()
# nodo_maestro.agregar_articulos_inventario()
# nodo_maestro.consenso()
# nodo_maestro.redistribuir_articulos()
# nodo_maestro.eleccion()

def main():
    while True:
        opcion = int(input("Seleccione un nodo para enviar un mensaje (1: Maestro, 2: Sucursal1, 3: Sucursal2, 0: Salir): "))
        if opcion == 1:
            nodo_maestro.enviar_mensaje("192.168.1.101", 5001, 'sucursal')
        elif opcion == 2:
            sucursal_1.enviar_mensaje("192.168.1.100", 5000, 'maestro')
        elif opcion == 3:
            sucursal_2.enviar_mensaje("192.168.1.100", 5000, 'maestro')
        elif opcion == 0:
            break
        else:
            print("Opción no válida. Intente nuevamente.")
