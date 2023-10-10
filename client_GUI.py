# Client side GUI chat room
import json
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL

# Define window
root = tkinter.Tk()
root.title("Chat Client")
root.iconbitmap("message_icon.ico")
root.geometry("800x650")
root.resizable(False, False)

# Define fonts and colors
my_font = ('Sim sun', 14)
black = "#010101"
light_green = "#1fc742"
white = "#ffffff"
red = "#ff3855"
orange = "#ff9a00"
yellow = "#fff700"
green = "#00ff2b"
blue = "#00b4ff"
purple = "#9966ff"
root.config(bg=black)

# Define socket constants
ENCODER = 'utf-8'
BYTESIZE = 1024
global client_socket


class Connection():
    """Create a connection class for client socket - a client socket and pertinent methods"""

    def __init__(self):
        """Initialize a client socket"""
        self.encoder = ENCODER
        self.bytesize = BYTESIZE


# Define functions
def connect(connection):
    """Connect to a server at a given ip/port address"""
    # Clear any previous messages
    my_listbox.delete(0, END)

    # Get required information from a connection object
    connection.name = name_entry.get()
    connection.target_ip = ip_entry.get()
    connection.port = int(port_entry.get())
    connection.color = color.get()

    try:
        # Create a client socket
        connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.client_socket.connect((connection.target_ip, connection.port))

        # Create a thread to receive messages
        message_json = connection.client_socket.recv(connection.bytesize)
        process_message(connection, message_json)

    except:
        # Update the GUI
        my_listbox.insert(0, "Error connecting to server")


def disconnect(connection):
    """Disconnect from the current server"""
    pass


def gui_start():
    """Start the connection process by updating the GUI"""
    connect_button.config(state=DISABLED)
    disconnect_button.config(state=NORMAL)
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)
    send_button.config(state=NORMAL)

    for button in color_buttons:
        button.config(state=DISABLED)


def gui_end():
    """Disconnect from the server by updating the GUI"""
    pass


def create_message(flag, name, message, color):
    """Create and return a message to be broadcast to all clients"""
    pass


def process_message(connection, message_json):
    """Process a message received from a client"""
    # Update the chat history by unpacking the json message
    message_packet = json.loads(message_json)
    message = message_packet['message']
    flag = message_packet['flag']
    name = message_packet['name']
    color = message_packet['color']

    if flag == "INFO":
        # Server is asking for information to varify connection. Send the info.
        message_packet = create_message("INFO", connection.name, "Joins the server", connection.color)
        message_json = json.dumps(message_packet)
        connection.client_socket.send(message_json.encode(connection.encoder))

        # Enable the GUI buttons
        gui_start()


def send_message(connection):
    """Send a message to the server"""
    pass


def receive_message(connection):
    """Receive an incoming message from the server"""
    pass


# Define GUI Layout
# Creates frames
info_frame = tkinter.Frame(root, bg=black)
color_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Info Frame Layout
name_label = tkinter.Label(info_frame, text="Client Name:", font=my_font, fg=light_green, bg=black)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(info_frame, text="Host IP:", font=my_font, fg=light_green, bg=black)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(info_frame, text="Port Num:", font=my_font, fg=light_green, bg=black)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green,
                                borderwidth=5, width=10, command=lambda: connect(my_connection))
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=light_green,
                                   borderwidth=5, width=10, state=DISABLED, command=disconnect)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=10, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

# Color Frame Layout
color = tkinter.StringVar()
color.set(white)
white_button = tkinter.Radiobutton(color_frame, width=5, text="White",
                                   variable=color, value=white, font=my_font, bg=white, fg=light_green)
red_button = tkinter.Radiobutton(color_frame, width=5, text="Red", variable=color, value=red, font=my_font, bg=red,
                                 fg=light_green)
orange_button = tkinter.Radiobutton(color_frame, width=5, text="Orange", variable=color, value=orange, font=my_font,
                                    bg=orange, fg=light_green)
yellow_button = tkinter.Radiobutton(color_frame, width=5, text="Yellow", variable=color, value=yellow, font=my_font,
                                    bg=yellow, fg=light_green)
green_button = tkinter.Radiobutton(color_frame, width=5, text="Green", variable=color, value=green, font=my_font,
                                   bg=green, fg=light_green)
blue_button = tkinter.Radiobutton(color_frame, width=5, text="Blue", variable=color, value=blue, font=my_font,
                                  bg=blue, fg=light_green)
purple_button = tkinter.Radiobutton(color_frame, width=5, text="Purple", variable=color, value=purple, font=my_font,
                                    bg=purple, fg=light_green)

color_buttons = [white_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

white_button.grid(row=1, column=0, padx=2, pady=2)
red_button.grid(row=1, column=1, padx=2, pady=2)
orange_button.grid(row=1, column=2, padx=2, pady=2)
yellow_button.grid(row=1, column=3, padx=2, pady=2)
green_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
purple_button.grid(row=1, column=6, padx=2, pady=2)

# Output frame layout
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=18, width=68, borderwidth=3, bg=black, fg=light_green,
                             font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Input frame Layout
input_entry = tkinter.Entry(input_frame, width=55, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="send", borderwidth=5, width=10, font=my_font,
                             bg=light_green, command=send_message)

input_entry.grid(row=0, column=0, padx=10, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)

# Create a connection instance and start the GUI
my_connection = Connection()
root.mainloop()
