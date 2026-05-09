import socket
import threading
import random
import time

TCP_PORT = 6000
UDP_PORT = 6001
SERVER_IP = '0.0.0.0'
MIN_PLAYERS = 2
GAME_DURATION = 60

players = {}              # {name: (conn, addr)}
udpAddresses = {}        # {name: (ip, port)}
secretNumber = None
gameActive = False
lock = threading.Lock()

# Send a message to all players
def broadcastTcp(message, excludeName=None):
    for name, (conn, _) in list(players.items()):
        if name != excludeName:
            try:
                conn.sendall(message.encode())
            except:
                continue

# Handle each player
def handleTcpConnection(conn, addr):
    global gameActive
    name = ""

    try:
        conn.sendall(b"Welcome! Please send 'JOIN <your_name>'\n")
        nameMsg = conn.recv(1024).decode().strip()
        if not nameMsg.startswith("JOIN "):
            conn.sendall(b"Invalid format. Use: JOIN <your_name>\n")
            conn.close()
            return

        name = nameMsg.split(" ", 1)[1]

        with lock:
            if name in players:
                conn.sendall(b"Name already taken. Use another name.\n")
                conn.close()
                return
            players[name] = (conn, addr)

        print(f" Player '{name}' joined from {addr}")
        conn.sendall(b"Waiting for more players...\n")

        with lock:
            if len(players) >= MIN_PLAYERS and not gameActive:
                gameActive = True
                threading.Thread(target=startGame).start()

        # Listen to player messages (yes/no only)
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip().lower()

            if msg == "no":
                with lock:
                    print(f" Player '{name}' chose not to continue and was removed.")
                    if name in players:
                        del players[name]
                    if name in udpAddresses:
                        del udpAddresses[name]

                try:
                    conn.sendall(b"Goodbye! You have been disconnected.\n")
                    conn.shutdown(socket.SHUT_RDWR)
                except:
                    pass

                conn.close()
                checkIfGameShouldEnd()
                return

            elif msg == "yes":
                # No action needed
                continue

    except:
        pass

    # When a player suddenly disconnects
    with lock:
        if name in players:
            del players[name]
        if name in udpAddresses:
            del udpAddresses[name]
    print(f" Player '{name}' has left the game.")

    broadcastTcp(f" Player '{name}' has left the game.", excludeName=name)

    try:
        conn.close()
    except:
        pass

    checkIfGameShouldEnd()

# Check if the round should end
def checkIfGameShouldEnd():
    global gameActive
    with lock:
        if gameActive and len(players) == 0:
            print(" No players remaining. Ending game.")
            gameActive = False

# Start the round
def startGame():
    global secretNumber
    print(" Game is starting!")

    with lock:
        currentPlayers = list(players.keys())

    broadcastTcp(f"Game starting with players: {', '.join(currentPlayers)}\n")
    secretNumber = random.randint(1, 100)

    broadcastTcp("Guess a number between 1 and 100 (you have 60 seconds)...\n")

    threading.Thread(target=handleUdpGuesses).start()

    startTime = time.time()
    while time.time() - startTime < GAME_DURATION:
        time.sleep(1)
        with lock:
            if not gameActive:
                return

    if gameActive:
        broadcastTcp("\nGame Result")
        broadcastTcp(f"Secret number: {secretNumber} ")
        broadcastTcp("  , Time is up! No winner this round.\n")
        print("Game ended without a winner.")
    resetGame()

# Receive guesses from players
def handleUdpGuesses():
    global gameActive
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind((SERVER_IP, UDP_PORT))
    print(f"UDP server listening on {UDP_PORT}")

    while gameActive:
        try:
            udpSock.settimeout(1)
            data, addr = udpSock.recvfrom(1024)
            guessInfo = data.decode().strip().split(":")
            if len(guessInfo) != 2:
                continue

            name, guessStr = guessInfo
            guess = int(guessStr)

            with lock:
                udpAddresses[name] = addr

            if guess < 1 or guess > 100:
                udpSock.sendto(b"Warning Invalid guess. Out of bounds. miss your chance", addr)
            elif guess < secretNumber:
                udpSock.sendto(b"Higher", addr)
            elif guess > secretNumber:
                udpSock.sendto(b"Lower", addr)
            else:
                
                udpSock.sendto(b"Correct!", addr)
                print(f"Game Completed. Player '{name}' won!")
                broadcastTcp("\nGame Result")
                broadcastTcp(f"Secret number: {secretNumber} ")
                broadcastTcp(f" , Player '{name}' guessed the number {secretNumber} correctly!\n")
                gameActive = False
                break

        except socket.timeout:
            continue
        except Exception as e:
            print(f"[UDP ERROR] {e}")
            continue

    udpSock.close()

# Reset the game
def resetGame():
    global secretNumber, gameActive
    secretNumber = None
    gameActive = False
    udpAddresses.clear()
    print("Waiting for new players...")

# Start the server
def main():
    tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpSock.bind((SERVER_IP, TCP_PORT))
    tcpSock.listen()
    print(f" TCP server listening on {TCP_PORT}")

    while True:
        conn, addr = tcpSock.accept()
        threading.Thread(target=handleTcpConnection, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
