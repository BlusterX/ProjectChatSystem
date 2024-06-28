#!/usr/bin/env python3
"""
Concurrent Chat Server Script
Course: Network Programming - University of Bologna
"""

import socket
from threading import Thread

def accetta_connessioni_client():
    """Gestisce l'ascolto delle connessioni in ingresso dai client."""
    while True:
        try:
            client_conn, client_addr = server_socket.accept()  # Accetta una nuova connessione
            print(f"Nuova connessione da {client_addr}")
            client_conn.send("Benvenuto! Per favore, inserisci il tuo nome:".encode("utf8"))
            client_addresses[client_conn] = client_addr  # Memorizza l'indirizzo del client
            Thread(target=gestore_client, args=(client_conn,)).start()  # Avvia un thread per gestire il client
        except Exception as e:
            print(f"Errore nell'accettare la connessione: {e}")

def gestore_client(client_conn):
    """Gestisce i messaggi provenienti da un singolo client."""
    try:
        nome = client_conn.recv(BUFFER_SIZE).decode("utf8")  # Riceve il nome del client
        benvenuto = f"Ciao {nome}! Digita (quit) per uscire dalla chat."
        client_conn.send(benvenuto.encode("utf8"))
        notifica_tutti(f"{nome} si è unito alla chat!".encode("utf8"))  # Notifica a tutti che il client si è unito
        clients[client_conn] = nome  # Memorizza il nome del client

        while True:
            messaggio = client_conn.recv(BUFFER_SIZE)  # Riceve un messaggio dal client
            if messaggio.decode("utf8") != "(quit)":
                notifica_tutti(messaggio, f"{nome}: ")  # Invia il messaggio a tutti i client
            else:
                client_conn.send("(quit)".encode("utf8"))
                client_conn.close()
                del clients[client_conn]  # Rimuove il client dalla lista
                notifica_tutti(f"{nome} ha lasciato la chat.".encode("utf8"))  # Notifica a tutti che il client ha lasciato la chat
                break
    except Exception as e:
        print(f"Errore nel gestire il client: {e}")
        client_conn.close()
        if client_conn in clients:
            del clients[client_conn]
            notifica_tutti(f"{nome} ha lasciato la chat a causa di un errore.".encode("utf8"))  # Notifica a tutti che il client ha lasciato a causa di un errore

def notifica_tutti(messaggio, prefisso=""):
    """Invia un messaggio a tutti i client connessi."""
    for sock in clients:
        try:
            sock.send(prefisso.encode("utf8") + messaggio)  # Invia il messaggio con un prefisso
        except Exception as e:
            print(f"Errore nell'invio del messaggio a un client: {e}")

clients = {}  # Dizionario per memorizzare i client connessi
client_addresses = {}  # Dizionario per memorizzare gli indirizzi dei client

HOST = ''
PORT = 53000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Imposta SO_REUSEADDR
server_socket.bind(ADDRESS)

if __name__ == "__main__":
    server_socket.listen(5)
    print("Server in esecuzione, in attesa di connessioni...")
    try:
        accept_thread = Thread(target=accetta_connessioni_client)
        accept_thread.start()
        accept_thread.join()
    except KeyboardInterrupt:
        print("Server interrotto dall'utente")
    except Exception as e:
        print(f"Errore nel thread di accettazione: {e}")
    finally:
        server_socket.close()
