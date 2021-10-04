import bluetooth as bt

def search_devices(clusterNames, addresses):
    devices = bt.discover_devices(lookup_names=True)

    for dev in devices:
        for i in range(len(clusterNames)):
            if dev[1] == clusterNames[i]:
                addresses[i] = dev[0]

def search_specific(name):
    devices = bt.discover_devices(lookup_names=True)

    for dev in devices:
        if dev[1] == name:
            return dev[0]

    return ""
