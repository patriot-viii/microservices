import getopt, sys

def get_host_port():
    args, opts = getopt.getopt(sys.argv[1:], 'h:p:', ["host=", "port="])
    host, port = '', 0
    for a, v in args:
        if a in ("-h", "--host"):
            host = v
        elif a in ("-p", "--port"):
            port = int(v)
    return (host, port)