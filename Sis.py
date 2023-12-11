import socket
import threading
import sqlite3
import random
import MWf

bd = sqlite3.connect('/home/eduardo/base.sqlite')
cur = bd.cursor()
ipl = MWf.obtener_ip()

if __name__ == "__main__":
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

    # Iniciar los servidores en cada máquina virtual
    vm1 = threading.Thread(target=MWf.servidor, args=(hosts[0], port[0]))
    vm1.start()
    vm2 = threading.Thread(target=MWf.servidor, args=(hosts[1], port[1]))
    vm2.start()
    vm3 = threading.Thread(target=MWf.servidor, args=(hosts[2], port[2]))
    vm3.start()
    vm4 = threading.Thread(target=MWf.servidor, args=(hosts[3], port[3]))
    vm4.start()
    
    while True:
        # Menu de seleccion
        hn = socket.gethostbyname(socket.gethostname())
        print(hn)
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
                msj = "cliente "+n+" "+p+" "+m
                MWf.mensaje(hosts[0],port[0],msj)
                MWf.mensaje(hosts[1],port[1],msj)
                MWf.mensaje(hosts[2],port[2],msj)
                MWf.mensaje(hosts[3],port[3],msj)
        
            elif choice == '3':
               print("")
            elif choice == '4':
                a = input("\nCuál es el nombre del nuevo articulo?: ")
                p = input("\nCuál es la cantidad total del articulo?: ")
                msj = "articulo "+a+" "+p
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
