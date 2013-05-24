#!/usr/bin/python
import time

def read_netstat():
    fd = open("/proc/net/dev", "r")
    for line in fd.readlines():
        if line.find("eth0") > 0:
            field = line.split()
            recv = field[1]
            send = field[9]
    fd.close()
    return (float(recv), float(send))
 
def put_info():
    (recv, send) = read_netstat()
    while True:
        time.sleep(1)
        (new_recv, new_send) = read_netstat()
        print "recv: %.3f MB, send %.3f MB" % ((new_recv -recv)/1024/1024, (new_send - send)/1024/1024)
        (recv, send) = (new_recv, new_send)
 
if __name__ == '__main__':
    put_info()
