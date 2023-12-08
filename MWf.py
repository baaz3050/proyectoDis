import socket
import threading
import sqlite3
import time

def cliente(conn, addr, bd):
    print(f'Conectado por {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_message = data.decode()
        str = received_message.split(sep=' ')
        if str[1] == 'cliente':
            c = bd.cursor()
            n = str[2]
            p = str[3]
            m = str[4]
            id = str[5]
            c.execute('INSERT INTO CLIENTE (idCliente, nombre, apPaterno, apMaterno) VALUES (?,?,?,?)',(id,n,p,m))
            bd.commit()
            print("Se agrego el cliente ",n," "," ",p," ",m," correctamente")
        elif str[1] == 'producto':
            print("")
        elif str[1] == 'compra':
            print("")
        #print(f'Mensaje recibido de {addr}: {received_message}')
        
        # Almacenar mensaje recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d_%H:%M:%S')} - {received_message}\n")
        
        # Enviar un mensaje de confirmación al cliente
        confirmation_message = "El mensaje fue recibido"
        conn.sendall(confirmation_message.encode())
        print(f'Mensaje de confirmación enviado a {addr}: {confirmation_message}')

    conn.close()

def servidor(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Servidor escuchando en {host}:{port}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=cliente, args=(conn, addr))
            client_thread.start()

def mensaje(server_ip, server_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        t = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        mt = f"[{t}] {message}"
        s.sendall(mt.encode())
        print(f"Mensaje enviado a {server_ip}:{server_port}: {mt}")
        
        # Almacenar mensaje enviado en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Enviado] {t} - {message}\n")
        
        response = s.recv(1024)
        decoded_response = response.decode()
        print(f"Respuesta del servidor {server_ip}:{server_port}: {decoded_response}")
        
        # Almacenar mensaje de confirmación recibido en un archivo
        with open(f"/home/eduardo/msgs.txt", "a") as file:
            file.write(f"[Recibido] {time.strftime('%Y-%m-%d_%H:%M:%S')} - {decoded_response}\n")

#if __name__ == "__main__":
    # Configuración de los servidores en cada máquina virtual
    #hosts = [
        #"192.168.153.128",
        #"192.168.153.129",
        #"192.168.153.130",
        #"192.168.153.131"
    #]
    #port = [      # Puerto para la comunicación entre las máquinas
        #1111,
        #2222,
        #3333,
        #4444
    #]
    # Iniciar los servidores en cada máquina virtual
    #vm1 = threading.Thread(target=servidor, args=(hosts[0], port[0]))
    #vm1.start()
    #vm2 = threading.Thread(target=servidor, args=(hosts[1], port[1]))
    #vm2.start()
    #vm3 = threading.Thread(target=servidor, args=(hosts[2], port[2]))
    #vm3.start()
    #vm4 = threading.Thread(target=servidor, args=(hosts[3], port[3]))
    #vm4.start()

    # Menú del cliente para enviar mensajes
    #while True:
        #print("\nSeleccione a qué servidor desea enviar un mensaje:")
        #for i, host in enumerate(hosts, start=1):
            #print(f"{i}. {host}")

        #choice = input("Ingrese el número correspondiente al servidor o '0' para salir: ")
        #if choice == '0':
            #break

        #try:
            #choice_idx = int(choice) - 1
            #if 0 <= choice_idx < len(hosts):
                #server_ip = hosts[choice_idx]
                #port_i = port[choice_idx]
                #message = input("Ingrese el mensaje a enviar: ")
                #mensaje(server_ip, port_i, message)
            #else:
                #print("Opción inválida. Intente de nuevo.")
        #except ValueError:
            #print("Entrada inválida. Ingrese un número válido o '0' para salir.")
