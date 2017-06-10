#! python2

import scapy.all as scapy
import sys
import socket
import random




localIP = ''
#localIP = '127.0.0.1'

def handshake(targetIP, targetPort):
    
    #scapy.conf.L3socket=scapy.L3RawSocket
    
    seqNum = random.randint(10000, 20000)
    sport = random.randint(1024, 65535)

    
    ipLayer = scapy.IP(src=localIP, dst=targetIP)
    tcpLayer1 = scapy.TCP(sport=sport, dport=targetPort, flags='S', seq=seqNum)
    p = scapy.sr1(ipLayer/tcpLayer1)    
    print(p.show())

    
    # Send ACK Packet
    tcpLayer2 = scapy.TCP(sport=sport, dport=targetPort, flags='A', seq=seqNum+1, ack=p.seq+1)
    scapy.send(ipLayer/tcpLayer2)



    # Send Payload
    payload = "hello"
    #payload = "GET /\n\n"
    tcpLayer3 = scapy.TCP(sport=sport, dport=targetPort, flags='PA', seq=seqNum+1, ack=p.seq+1)
    p = scapy.sr1(ipLayer/tcpLayer3/payload, inter=0.01)
    print(p.show())


    
    
def main(tHost, tPort):

    tIP = socket.gethostbyname(tHost)
    print('{0} {1}'.format(tIP, tPort))
    handshake(tIP, tPort)


    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('{0} host port'.format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]))



