#!/usr/bin/env python
#This file should be run in PC or other devices to working as COAP server
from coapthon.server.coap import CoAP   # need to install CoAPthon via pip
from dustResources import AdvancedResource

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('advanced/', AdvancedResource())

        print "CoAP Server start on " + host + ":" + str(port)


def main():  # pragma: no cover
    ip = "192.168.0.11"	#server IP
    port = 5683
    
    server = CoAPServer(ip, port)
    
    try:
        server.listen(1)
        
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."


if __name__ == "__main__":  # pragma: no cover
    main()
