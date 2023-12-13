import socket
import threading
import sqlite3
import time
import MWf

bd = sqlite3.connect('/home/eduardo/base.sqlite', check_same_thread=False)
cur = bd.cursor()
idP = 1
idC = 1

# Configuración de los servidores en cada máquina virtual
hosts = [
    "192.168.153.128",
    "192.168.153.129",
    "192.168.153.130",
    "192.168.153.131"
]
port = [      # Puerto para la comunicación entre las máquinas
    1111,
    2222,
    3333,
    4444
]
    
names = [    # Nombres dehost de las máquinas
    "VM1",
    "VM2",
    "VM3",
    "VM4"
]

def propaga(hn, msj):
    if (hn == names[0]):
        MWf.mensaje(hosts[1],port[1],msj)
        MWf.mensaje(hosts[2],port[2],msj)
        MWf.mensaje(hosts[3],port[3],msj)
    elif (hn == names[1]):
        MWf.mensaje(hosts[0],port[0],msj)
        MWf.mensaje(hosts[2],port[2],msj)
        MWf.mensaje(hosts[3],port[3],msj)
    elif (hn == names[2]):
        MWf.mensaje(hosts[0],port[0],msj)
        MWf.mensaje(hosts[1],port[1],msj)
        MWf.mensaje(hosts[3],port[3],msj)
    elif (hn == names[3]):
        MWf.mensaje(hosts[0],port[0],msj)
        MWf.mensaje(hosts[1],port[1],msj)
        MWf.mensaje(hosts[2],port[2],msj)
        
if __name__ == "__main__":
    # Borrado de tablas
    cur.execute('DROP TABLE IF EXISTS PRODUCTO')
    cur.execute('DROP TABLE IF EXISTS CLIENTE')
    cur.execute('DROP TABLE IF EXISTS INVENTARIO')
    
    # Creacion de tablas
    cur.execute('CREATE TABLE PRODUCTO (idProducto INTEGER, nombre TEXT, total INTEGER)')
    cur.execute('CREATE TABLE CLIENTE (idCliente INTEGER, nombre TEXT, apPaterno TEXT, apMaterno TEXT)')
    cur.execute('CREATE TABLE INVENTARIO (idSucursal, producto INTEGER, cantidad INTEGER)')

    #cur.execute('INSERT INTO PRODUCTOS (idProducto, nombre) VALUES (?, ?)', ('My Way', 15))
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Zapatos', 20))
    idP += 1
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Gorra', 16))
    idP += 1
    cur.execute('INSERT INTO PRODUCTO (idProducto, nombre, total) VALUES (?, ?, ?)',(idP,'Hoodie', 12))
    idP += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Brayan','Ambriz','Zuloaga'))
    idC += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Eduardo','Fajardo','Tellez'))
    idC += 1
    cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(idC,'Marcos','Vega','Alvarez'))
    idC += 1

    i = 1
    j = -1
    
    hn = socket.gethostname()
    while (i < idP):
        cur.execute('SELECT total FROM PRODUCTO WHERE idProducto = ?',(i, ))
        a = cur.fetchone()
        n = a[0]
        m = len(hosts)
        t = [n//m]*m
        r = n % m
        for x in range(r):
            t[x] += 1
        if (hn == names[0]):
            j = 1
        elif (hn == names[1]):
            j = 2
        elif (hn == names[2]):
            j = 3
        elif (hn == names[3]):
            j = 4
        cur.execute('INSERT INTO INVENTARIO (idSucursal, producto, cantidad) VALUES (?,?,?)',(j,i,t[j-1]))
        i += 1
    bd.commit()

    
    # Iniciar los servidores en cada máquina virtual
    if (hn == names[0]):
        vm1 = threading.Thread(target=MWf.servidor, args=(hosts[0], port[0]))
        vm1.start()
    elif (hn == names[1]):
        vm2 = threading.Thread(target=MWf.servidor, args=(hosts[1], port[1]))
        vm2.start()
    elif (hn == names[2]):
        vm3 = threading.Thread(target=MWf.servidor, args=(hosts[2], port[2]))
        vm3.start()
    elif (hn == names[3]):
        vm4 = threading.Thread(target=MWf.servidor, args=(hosts[3], port[3]))
        vm4.start()
    
    while True:
        # Menu de seleccion
        print("\nBienvenido al sistema de inventarios, que deseas hacer?:")
        print("\n1. Consultar clientes")
        print("\n2. Agregar nuevo cliente")
        print("\n3. Comprar articulo")
        print("\n4. Agregar articulo\n")

        choice = input("Ingrese el número de opción correspondiente o '0' para salir: ")
        if choice == '0':
            break
        try:
            if choice == '1':
                cur.execute('SELECT * FROM CLIENTE')
                print("(idCliente, nombre, apPaterno, apMaterno)")
                for fila in cur:
                    print(fila)
            elif choice == '2':
                n = input("\nCuál es el nombre del cliente?: ")
                p = input("\nCuál es el apellido paterno del cliente?: ")
                m = input("\nCuál es el apellido materno del cliente?: ")
                cur.execute('SELECT COUNT(*) FROM CLIENTE')
                id = cur.fetchone()[0]
                id += 1
                ids = str(id)
                msj = "cliente "+ids+" "+n+" "+p+" "+m
                cur.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(ids,n,p,m))
                propaga(hn,msj)

                #i = 0
                #while (i < len(hosts)):
                    #try:
                        #bd.execute('BEGIN EXCLUSIVE TRANSACTION')
                        #MWf.mensaje(hosts[i],port[i],msj)
                        #i += 1
                        #bd.commit()
                        #time.sleep(5) 
                    #except Exception as e:
                        #print(f"Error en la transacción: {e}")
                        #bd.rollback()
        
            elif choice == '3':
               print("")
            elif choice == '4':
                a = input("\nCuál es el nombre del nuevo articulo?: ")
                p = input("\nCuál es la cantidad total del articulo?: ")
                cur.execute('SELECT COUNT(*) FROM PRODUCTO')
                id = cur.fetchone()[0]
                id += 1
                ids = str(id)
                msj = "articulo "+ids+" "+a+" "+p
                MWf.mensaje(hosts[0],port[0],msj)
                MWf.mensaje(hosts[1],port[1],msj)
                MWf.mensaje(hosts[2],port[2],msj)
                MWf.mensaje(hosts[3],port[3],msj)
                
            elif choice == '5':
                cur.execute('SELECT * FROM INVENTARIO')
                print("(idSucursal, producto, cantidad)")
                for fila in cur:
                    print(fila)
            elif choice == '6':
                cur.execute('SELECT * FROM PRODUCTO')
                print("(idProducto, nombre, total)")
                for fila in cur:
                    print(fila)
        except ValueError:
            print("Entrada inválida. Ingrese un número válido o '0' para salir.")
