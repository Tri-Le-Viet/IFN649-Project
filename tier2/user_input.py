from bluetooth_functions import *

def enable(threads, clusters, index):
    cluster = clusters[index]
    if (cluster.connect() == 0):
        cluster.running = True
        new_thread = threading.Thread(target=cluster.read, args=(cluster,))
        threads[index] = new_thread
        new_thread.start()

""" Terminates existing thread for a cluster by disconnecting
    the MQTT client. Messages for the particular cluster are then
    ignored until a new thread is started again

    Parameters:
        threads (list[threading.Thread]): list of currently running threads
        clusters (list[cluster]): list of predefined clusters
        index (int): cluster number to disable
"""
def disable(threads, clusters, index):
    cluster = clusters[index]
    cluster.running = False
    cluster.disconnect()
    threads[index].join()

""" Alters the status of a cluster (enabling/disabling)

    Parameters:
        command (string): a u command starting in either
            "disable" or "enable"

        threads (list[
    clusters (list[cluster]): list of clusters to subscribe to
        disab (bool): indicates that a disable or enable command
"""
def altercluster(command, threads, clusters, disab=True):
    if (disab):
        alter = disable
        type = "Disabled"
    else:
        alter = enable
        type = "Enabled"

    command = command.split(' ')
    if (len(command) != 2):
        print("Please enter a single cluster number")
    elif(command[1] == "all"):
        for i in range(len(threads)):
            alter(threads, clusters, i)
        print(f"Successfully {type} all")
    else:
        try:
            n = int(command[1]) - 1
            if (n < 0 or n >= len(clusters)):
                print("No such cluster")
            elif (clusters[n].connected == disab):
                print(f"{n + 1} is already {type}")
            else:
                alter(threads, clusters, n)
                print(f"Successfully {type} {n + 1}")
        except ValueError: #not an int
            print("Please enter an integer")

def search(command, threads, clusters):
    commmand = command.split(' ')
    if (len(command != 2)):
        print("Please enter a single cluster number")
    else:
        try:
            n = int(command[1]) - 1
            if (n < 0 or n >= len(clusters)):
                print("No such cluster")
            elif (cluster[n].found and cluster[n].connected):
                print(f"{n + 1} is already found and connected")
            else:
                address = search_specific(cluster[n].name)
                if address == "":
                    print("Not found, check sensor is powered")
                else:
                    cluster.set_address(address)
                    ans = ""

                    while (ans != "Y" and ans != "N"):
                        ans = input("Sensor found, do you want to connect? Y/N")
                        if (ans == "Y"):
                            enable(threads, clusters, n)

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
    Display: displays all received data from clusters
    Disable (n or 'all'): disables either specified cluster or all clusters
    Enable (n or 'all'): enables either specified cluster or all clusters
    Kill: quits the program and shuts down all threads
    Search n: searches all bluetooth devices for the specified cluster, only use if device is shown as "Not Found"
    Status: prints the current status (i.e. connected/disconnected) of sensors
    """)

""" Prints the current status
    Parameters:
        clusters (list[cluster]): list of clusters being monitored
"""
def status(clusters):
    for i in range(len(clusters)):
        cluster = clusters[i]
        if not cluster.running.is_set()
            if cluster.connected:
                print(f"{i + 1}: {cluster.name} - Connected")
            else:
                print(f"{i + 1}: {cluster.name} - Disconnected, attempting reconnect")
        elif not self.found:
            print(f"{i + 1}: {cluster.name} - Not found")
        else:
            print(f"{i + 1}: {cluster.name} - Disabled")

def display(clusters, weatherAPI):
    print("Displaying data, press enter to stop...")
    for cluster in clusters:
        cluster.display = True
    weatherAPI.display = True

    stop = input()
    for cluster in clusters:
        cluster.display = False
    weatherAPI.display = False

""" Respond to user commands
    Parameters:
        threads (list[threading.Thread]): list of currently running threads
        clusters (list[cluster]): list of predefined clusters
"""
def handle_input(threads, clusters, weatherAPI, lock, logger):
    command = input("Enter command: ")
    if (type(command) == str):
        if (command == "help"):
            printHelp()
        elif (command == "status"):
            status(clusters)
        elif (command == "display"):
            display(clusters, weatherAPI)
        elif (command == "kill"):
            for i in range(len(clusters)):
                disable(threads, clusters, i)
            threads[-1].running.set()
            exit()
        elif (command.startswith("disable")):
            altercluster(command, threads, clusters)
        elif (command.startswith("enable")):
            altercluster(command, threads, clusters, disab=False)
        else:
            invalid()
    else:
        invalid()
