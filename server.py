# Server side GUI chat room (admin)
import tkinter, socket, threading, json
from tkinter import DISABLED, VERTICAL, END, NORMAL


# Define window
root = tkinter.Tk()
root.title("Chat Server")
root.iconbitmap("message_icon.ico")
root.geometry("800x650")
root.resizable(False, False)

# Define fonts and colors
my_font = ('Sim sun', 14)
black = "#010101"
light_green = "#1fc742"
red = "#ff3855"
root.config(bg=black)


# Create a connection class for server socket
class Connection():
    """Create a connection class for server socket - a sever socket and pertinent methods"""

    def __init__(self):
        """Initialize a server socket"""
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.encoder = 'utf-8'
        self.bytesize = 1024

        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []


# Define functions
def start_server(connection):
    """Start the server socket"""
    # Get the port number from the server and attach it to the connection object
    connection.port = int(port_entry.get())

    # Create a server socket
    connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.server_socket.bind((connection.host_ip, connection.port))
    connection.server_socket.listen()

    # update the GUI
    history_listbox.delete(0, END)
    history_listbox.insert(0, f"Server started on {connection.host_ip}:{connection.port}")
    end_button.config(state=NORMAL)
    stat_button.config(state=DISABLED)
    self_broadcast_button.config(state=NORMAL)
    message_button.config(state=NORMAL)
    kick_button.config(state=NORMAL)
    ban_button.config(state=NORMAL)

    # Create a thread to accept incoming connections
    connect_thread = threading.Thread(target=connect_client, args=(connection,))
    connect_thread.start()


def end_server(connection):
    """Begin the shutdown process for the server socket"""
    # Alert all clients that the server is shutting down
    message_packet = create_message("DISCONNECT", "Admin (Broadcast)", "Server is shutting down!", red)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Update the GUI
    history_listbox.insert(0, f"Server is shutting down on port {connection.port}!")
    end_button.config(state=DISABLED)
    stat_button.config(state=NORMAL)
    self_broadcast_button.config(state=DISABLED)
    message_button.config(state=DISABLED)
    kick_button.config(state=DISABLED)
    ban_button.config(state=DISABLED)

    # Close all client sockets
    connection.server_socket.close()


def connect_client(connection):
    """Connect a client to the server socket"""
    while True:
        try:
            client_socket, client_address = connection.server_socket.accept()

            # Check if the client is banned
            if client_address[0] in connection.banned_ips:
                message_packet = create_message("DISCONNECT", "Admin (Private)",
                                                "You are banned from this server...BYE", red)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                # Close the client socket
                client_socket.close()

            else:
                # Send a message packet to receive the client's info
                message_packet = create_message("INFO", "Admin (Private)",
                                                "Please enter your name and color...", light_green)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                # wait for the confirmation message to be sent validating the connection
                message_json = client_socket.recv(connection.bytesize)
                process_message(connection, message_json, client_socket, client_address)

        except:
            break


def create_message(flag, name, message, color):
    """Create and return a message to be broadcast to all clients"""
    message_package = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color
    }
    return message_package


def process_message(connection, message_json, client_socket, client_address=(0, 0)):
    """Process a message received from a client"""
    message_packet = json.loads(message_json)

    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        # Add the client to the client list
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])

        # Broadcast the message to all clients that new client has connected
        message_packet = create_message("MESSAGE", "Admin (Broadcast)",
                                        f"{name} has joined the chat!", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Update the server GUI
        client_listbox.insert(END, f"Name: {name}   IP Addr: {client_address[0]}")

        # Create a thread to receive messages from the client
        receive_thread = threading.Thread(target=receive_message, args=(connection, client_socket,))
        receive_thread.start()

    elif flag == "MESSAGE":
        # Broadcast the message to all clients
        message_packet = create_message("MESSAGE", name, message, color)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Update the server GUI
        history_listbox.insert(0, f"{name}: {message}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        # Close the client socket and remove
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()

        # Broadcast the message to all clients
        message_packet = create_message("MESSAGE", "Admin (Broadcast)",
                                        f"{name} has left the chat!", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Update the server UI
        history_listbox.insert(0, f"Admin (Broadcast): {name} has left the chat!")

    else:
        # Catch all for invalid messages
        history_listbox.insert(0, f"Invalid message received!  {flag} is not a valid flag!")


def broadcast_message(connection, message_json):
    """Broadcast a message to all clients...All clients will receive the message
    ...ALL JSON ARE ENCODED"""
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)


def receive_message(connection, client_socket):
    """Receive an incoming message from a client"""
    while True:
        # Get a message from the client
        try:
            message_json = client_socket.recv(connection.bytesize)
            process_message(connection, message_json, client_socket)
        except:
            break


def self_broadcast_message(connection):
    """Broadcast a message to the server GUI"""
    # Create a message packet
    message_packet = create_message("MESSAGE", "Admin (Broadcast)", input_entry.get(), light_green)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Clear the input field
    input_entry.delete(0, END)


def private_message(connection):
    """Send a private message to a client"""
    # Select the client from the client listbox and access the client's socket
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]

    # Create a message packet
    message_packet = create_message("MESSAGE", "Admin (Private)", input_entry.get(), light_green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    # Clear the input field
    input_entry.delete(0, END)


def kick_client(connection):
    """Kick a client from the server"""
    # Select the client from the client listbox and access the client's socket
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]

    # Create a message packet
    message_packet = create_message("DISCONNECT", "Admin (Private)", "You have been kicked from the server!", red)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))


def ban_client(connection):
    """Ban a client from the server based on the IP address"""
    # Select the client from the client listbox and access the client's socket
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]
    client_ip = connection.client_ips[index]

    # Add the IP to the banned list
    connection.banned_ips.append(client_ip)

    # Create a message packet
    message_packet = create_message("DISCONNECT", "Admin (Private)", "You have been banned from the server!", red)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))


def unban_client(connection):
    """Unban a client's IP address from the server"""
    # Select the client from the client listbox and access the client's socket
    index = client_listbox.curselection()[0]
    client_ip = connection.client_ips[index]

    # Remove the IP from the banned list
    connection.banned_ips.remove(client_ip)


# Define GUI Layout
# Creates frames
connection_frame = tkinter.Frame(root, bg=black)
history_frame = tkinter.Frame(root, bg=black)
client_frame = tkinter.Frame(root, bg=black)
message_frame = tkinter.Frame(root, bg=black)
admin_frame = tkinter.Frame(root, bg=black)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack(pady=5)

# Connection frame layout
port_label = tkinter.Label(connection_frame, text="Port:", font=my_font, bg=black, fg=light_green)
port_entry = tkinter.Entry(connection_frame, font=my_font, bg=black, fg=light_green, width=10, borderwidth=3)
stat_button = tkinter.Button(connection_frame, text="Start Server", font=my_font, bg=light_green, fg=black,
                             borderwidth=3, width=15, command=lambda: start_server(my_connection))
end_button = tkinter.Button(connection_frame, text="End Server", font=my_font, bg=light_green, fg=black,
                            borderwidth=3, width=15, state=DISABLED, command=lambda: end_server(my_connection))

port_label.grid(row=0, column=0, padx=2, pady=10)
port_entry.grid(row=0, column=1, padx=2, pady=10)
stat_button.grid(row=0, column=2, padx=5, pady=10)
end_button.grid(row=0, column=3, padx=5, pady=10)

# History frame layout
history_scroll = tkinter.Scrollbar(history_frame, orient=VERTICAL)
history_listbox = tkinter.Listbox(history_frame, width=70, height=7, bg=black, fg=light_green,
                                  font=my_font, yscrollcommand=history_scroll.set)
history_scroll.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
history_scroll.grid(row=0, column=1, sticky="NS")

# Client frame layout
client_scroll = tkinter.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tkinter.Listbox(client_frame, width=70, height=7, bg=black, fg=light_green,
                                 font=my_font, yscrollcommand=client_scroll.set)
client_scroll.config(command=client_listbox.yview)

client_listbox.grid(row=0, column=0)
client_scroll.grid(row=0, column=1, sticky="NS")

# Message frame layout
input_entry = tkinter.Entry(message_frame, width=50, font=my_font, bg=black, fg=light_green, borderwidth=3)
self_broadcast_button = tkinter.Button(message_frame, text="Broadcast", font=my_font, bg=light_green, fg=black,
                                       borderwidth=3, width=8, command=lambda: self_broadcast_message(my_connection))

input_entry.grid(row=0, column=0, padx=10, pady=10)
self_broadcast_button.grid(row=0, column=1, padx=10, pady=10, ipadx=20)

# Admin frame layout
message_button = tkinter.Button(admin_frame, text="PM", font=my_font, bg=light_green, fg=black,
                                borderwidth=3, width=10, command=lambda: private_message(my_connection))
kick_button = tkinter.Button(admin_frame, text="Kick", font=my_font, bg=light_green, fg=black,
                             borderwidth=3, width=10, command=lambda: kick_client(my_connection))
ban_button = tkinter.Button(admin_frame, text="Ban", font=my_font, bg=light_green, fg=black,
                            borderwidth=3, width=10, command=lambda: ban_client(my_connection))
unban_button = tkinter.Button(admin_frame, text="Unban", font=my_font, bg=light_green, fg=black,
                              borderwidth=3, width=10, command=lambda: unban_client(my_connection))

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)
unban_button.grid(row=0, column=3, padx=5, pady=5)

# Create a connection object and run the window loop
my_connection = Connection()
root.mainloop()
