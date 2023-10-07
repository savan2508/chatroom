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
root.config(bg=black)


# Create a connection class for server socket
class Connection():
    """Create a connection class for server socket - a sever socket and pertinent methods"""

    def __init__(self):
        """Initialize a server socket"""
        pass


# Define functions
def start_server(connection):
    """Start the server socket"""
    pass


def end_server(connection):
    """Begin the shutdown process for the server socket"""
    pass


def connect_client(connection):
    """Connect a client to the server socket"""
    pass


def create_message(flag, name, message, color):
    """Create and return a message to be broadcast to all clients"""
    pass


def process_message(connection, message_json, client_socket, client_address=(0, 0)):
    """Process a message received from a client"""
    pass


def broadcast_message(connection, message_json):
    """Broadcast a message to all clients"""
    pass


def receive_message(connection, client_socket):
    """Receive an incoming message from a client"""
    pass


def self_broadcast_message(connection):
    """Broadcast a message to the server GUI"""
    pass


def private_message(connection):
    """Send a private message to a client"""
    pass


def kick_client(connection):
    """Kick a client from the server"""
    pass


def ban_client(connection):
    """Ban a client from the server based on the IP address"""
    pass


def unban_client(connection):
    """Unban a client's IP address from the server"""
    pass


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
                             borderwidth=3, width=15)
end_button = tkinter.Button(connection_frame, text="End Server", font=my_font, bg=light_green, fg=black,
                            borderwidth=3, width=15, state=DISABLED)

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
                                       borderwidth=3, width=8)

input_entry.grid(row=0, column=0, padx=10, pady=10)
self_broadcast_button.grid(row=0, column=1, padx=10, pady=10, ipadx=20)

# Admin frame layout
message_button = tkinter.Button(admin_frame, text="PM", font=my_font, bg=light_green, fg=black,
                                borderwidth=3, width=10)
kick_button = tkinter.Button(admin_frame, text="Kick", font=my_font, bg=light_green, fg=black,
                             borderwidth=3, width=10)
ban_button = tkinter.Button(admin_frame, text="Ban", font=my_font, bg=light_green, fg=black,
                            borderwidth=3, width=10)
unban_button = tkinter.Button(admin_frame, text="Unban", font=my_font, bg=light_green, fg=black,
                              borderwidth=3, width=10)

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)
unban_button.grid(row=0, column=3, padx=5, pady=5)

# Run the root window's main loop
root.mainloop()
