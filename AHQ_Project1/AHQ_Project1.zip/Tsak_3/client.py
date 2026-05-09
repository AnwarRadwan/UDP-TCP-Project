import socket
import threading

# Connection settings
SERVER_IP = '127.0.0.1'  # Change if testing from another device
TCP_PORT = 6000
UDP_PORT = 6001

username = ""
udpSock = None

def tcpListener(tcpSock):
    while True:
        try:
            data = tcpSock.recv(1024)
            if not data:
                break
            print("[Server] " + data.decode())
        except:
            break

def udpListener():
    while True:
        try:
            data, _ = udpSock.recvfrom(1024)
            print("[Feedback] " + data.decode())
        except:
            break

def main():
    global username, udpSock

    # Create TCP connection
    tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSock.connect((SERVER_IP, TCP_PORT))

    # Receive welcome message
    welcome = tcpSock.recv(1024).decode()
    print(welcome)

    # Enter username
    while True:
        username = input("Enter your player name: ").strip()
        joinMsg = f"JOIN {username}"
        tcpSock.sendall(joinMsg.encode())

        response = tcpSock.recv(1024).decode()
        print("[Server] " + response)
        if "Waiting for more players" in response:
            break
        elif "already taken" in response:
            continue
        else:
            print("Try again.")

    # Start TCP listener in the background
    threading.Thread(target=tcpListener, args=(tcpSock,), daemon=True).start()

    # Setup UDP
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind(('', 0))  # Random port

    # Start UDP listener in the background
    threading.Thread(target=udpListener, daemon=True).start()

    # Guessing loop
    print("\n You can now start guessing numbers...\n")
    while True:
        try:
            guess = input("Your guess (1-100): ").strip().lower()

            if guess == "exit":
                print(" Exiting game.")
                break
            elif guess == "no":
                try:
                    tcpSock.sendall(b"no\n")
                except:
                    pass
                print(" You chose not to continue. Disconnecting...")
                break
            elif guess == "yes":
                try:
                    tcpSock.sendall(b"yes\n")
                except:
                    pass
                continue
            elif not guess.isdigit():
                print(" Please enter a valid number.")
                continue

            # Send guess
            msg = f"{username}:{guess}"
            udpSock.sendto(msg.encode(), (SERVER_IP, UDP_PORT))

        except KeyboardInterrupt:
            print("\n Disconnected.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            break

    try:
        tcpSock.shutdown(socket.SHUT_RDWR)
        tcpSock.close()
    except:
        pass
    try:
        udpSock.close()
    except:
        pass

if __name__ == "__main__":
    main()