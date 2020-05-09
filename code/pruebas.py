import connection

def main():
    print("start")
    addrs = connection.search_available_devices('names.txt', 3)
    print (addrs)
    for addr in addrs:
        client_socket = connection.send_info(addr, "Hola", 3)

        data, addr, client_socket, server_socket = connection.receive_info(3)
        print (data)


        client_socket = connection.send_info(addr, "Muy bien. Adiós", 3)
        close_sockets(client_socket, server_socket)


if __name__ == '__main__':
    main()

