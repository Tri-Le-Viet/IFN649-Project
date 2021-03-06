from bluetooth_functions import *

def enable(threads, nodes, index):
    node = nodes[index]
    if (node.connect() == 0):
        node.running.clear()
        new_thread = threading.Thread(target=node.read, args=(node,))
        threads[index] = new_thread
        new_thread.start()

""" Terminates existing thread for a node by disconnecting
    the MQTT client. Messages for the particular node are then
    ignored until a new thread is started again

    Parameters:
        threads (list[threading.Thread]): list of currently running threads
        nodes (list[node]): list of predefined nodes
        index (int): node number to disable
"""
def disable(threads, nodes, index):
    node = nodes[index]
    node.running.set()
    node.disconnect()
    threads[index].join()

""" Alters the status of a node (enabling/disabling)

    Parameters:
        command (string): a u command starting in either
            "disable" or "enable"

        threads (list[
    nodes (list[node]): list of nodes to subscribe to
        disab (bool): indicates that a disable or enable command
"""
def alternode(command, threads, nodes, disab=True):
    if (disab):
        alter = disable
        type = "Disabled"
    else:
        alter = enable
        type = "Enabled"

    command = command.split(' ')
    if (len(command) != 2):
        print("Please enter a single node number")
    elif(command[1] == "all"):
        for i in range(len(threads)):
            alter(threads, nodes, i)
        print(f"Successfully {type} all")
    else:
        try:
            n = int(command[1]) - 1
            if (n < 0 or n >= len(nodes)):
                print("No such node")
            elif (nodes[n].connected == disab):
                print(f"{n + 1} is already {type}")
            else:
                alter(threads, nodes, n)
                print(f"Successfully {type} {n + 1}")
        except ValueError: #not an int
            print("Please enter an integer")

def search(command, threads, nodes):
    commmand = command.split(' ')
    if (len(command != 2)):
        print("Please enter a single node number")
    else:
        try:
            n = int(command[1]) - 1
            if (n < 0 or n >= len(nodes)):
                print("No such node")
            elif (node[n].found and node[n].connected):
                print(f"{n + 1} is already found and connected")
            else:
                address = search_specific(node[n].name)
                if address == "":
                    print("Not found, check sensor is powered")
                else:
                    node.set_address(address)
                    ans = ""

                    while (ans != "Y" and ans != "N"):
                        ans = input("Sensor found, do you want to connect? Y/N")
                        if (ans == "Y"):
                            enable(threads, nodes, n)

        except ValueError: #not an int
            print("Please enter an integer")


""" Prints error message then instructions
"""
def invalid():
    print("Invalid command")
    printHelp()

""" Prints instructions
"""
def printHelp():
    print("""Commands are:
    Help: prints help
    Display: displays all received data from nodes
    Disable (n or 'all'): disables either specified node or all nodes
    Enable (n or 'all'): enables either specified node or all nodes
    Kill: quits the program and shuts down all threads
    Search n: searches all bluetooth devices for the specified node, only use if device is shown as "Not Found"
    Status: prints the current status (i.e. connected/disconnected) of sensors
    """)

""" Prints the current status
    Parameters:
        nodes (list[node]): list of nodes being monitored
"""
def status(nodes):
    for i in range(len(nodes)):
        node = nodes[i]
        if not node.running.is_set():
            if node.connected:
                print(f"{i + 1}: {node.name} - Connected")
            elif not node.found:
                print(f"{i + 1}: {node.name} - Not found")
            else:
                print(f"{i + 1}: {node.name} - Disconnected, attempting reconnect")
        else:
            print(f"{i + 1}: {node.name} - Disabled")

def display(nodes, weatherAPI):
    print("Displaying data, press enter to stop...")
    for node in nodes:
        node.display = True
    weatherAPI.display = True

    stop = input()
    for node in nodes:
        node.display = False
    weatherAPI.display = False

""" Respond to user commands
    Parameters:
        threads (list[threading.Thread]): list of currently running threads
        nodes (list[node]): list of predefined nodes
"""
def handle_input(threads, nodes, weatherAPI, lock, logger):
    command = input("Enter command: ")
    if (type(command) == str):
        if (command == "help"):
            printHelp()
        elif (command == "status"):
            status(nodes)
        elif (command == "display"):
            display(nodes, weatherAPI)
        elif (command == "kill"):
            for i in range(len(nodes)):
                disable(threads, nodes, i)
            threads[-1].running.set()
            exit()
        elif (command.startswith("disable")):
            alternode(command, threads, nodes)
        elif (command.startswith("enable")):
            alternode(command, threads, nodes, disab=False)
        else:
            invalid()
    else:
        invalid()
