import socket
import threading
import SocketServer
import time
import random
import sys
import os

list_ip = []

def init_list_ip():
    list_ip = []
    return None

def remove_client_ip(ip_client):
    list_ip.remove(ip_client)
    if len(list_ip) == 0:
        return 1
    else:
        return None
    
def add_client_ip(ip_client):
    list_ip.append(ip_client)
    return None

def remove_file(ddrr):
    print 'Deleted ' + ddrr
    os.remove(ddrr)
    return None

def send_list(f, connection):     
    #print len(f)
    for i in f:
        element_length(connection, i)
	connection.sendall(str(len(i)))
        connection.sendall(i)
    return None

def element_length(connection, nm):
    if len(nm) > 9:
        connection.sendall('2')
    elif len(nm) > 99:
        connection.sendall('3')
    elif len(nm) > 999:
        connection.sendall('4')
    elif len(nm) > 9999:
        connection.sendall('5')
    else:
        connection.sendall('1')
    return None

def list_all(connection):
    for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\McNapster\Server_Database'):
        nm = print_name(f_1)

        element_length(connection, nm)
        connection.sendall(str(len(nm)))
        connection.sendall(nm)

        element_length(connection, f_2)
        connection.sendall(str(len(f_2)))
	if len(f_2) != 0:
            send_list(f_2, connection)

        element_length(connection, f_3)
        connection.sendall(str(len(f_3)))
	if len(f_3) != 0:
	    send_list(f_3, connection)

    element_length(connection, 'DONE***DONE***DONE')
    connection.sendall('18')
    connection.sendall('DONE***DONE***DONE')
    return None
    
def check_file_name_exist(arg_n):
    f_dir = []
    drr = None
    actual_name = None
    for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\McNapster\Server_Database'):
        if len(f_2) != 0:
            for d in f_2:
                f_dir.append(d)

    for dr in f_dir:   
        f_dir = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\%s' % (dr)
        f = os.listdir(f_dir)
        for fl in f:
            if arg_n == fl:
                drr = dr
                actual_name = fl
                return 1, drr, actual_name

    return 0, drr, actual_name

def print_name(f):
    f_dir = ''
    n = 1 
    for i in f:
        if n > (len('C:\Users\Coordinator\Desktop\S\McNapster')+ 1):
            f_dir = f_dir + i
            n = n + 1
        n = n + 1
    #print f_dir + ':'
    return f_dir

def send_file(connection, arg_n, ddrr):
	# Send a file over a socket
	
    print 'Server openning file : %s' % (arg_n)
    name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\%s' % (ddrr) + '\%s' % (arg_n)

    if ('wma' in arg_n) or('mp3' in arg_n) or ('mp4' in arg_n)or ('mov' in arg_n)or ('wmv' in arg_n):
        nn = 'rb'
    elif ('bmp' in arg_n)or ('jpg' in arg_n):
        nn = 'rb'
    else:
        nn = 'rb'

    try:
        f1 = open(name, nn)
        f1.seek(0, os.SEEK_END)
        size = f1.tell()
        print size
        connection.sendall(str(size))
        f1.seek(0, 0)
  
        i = 1
        sum_bytes = 0
        lines = f1.readlines()
        for line in lines:
            print 'Sending Line', i, ' with ', len(line), ' bytes. sum_bytes = ', sum_bytes
            #connection.sendall('CONTINUESENDING')
            connection.sendall(line)
            i = i+1
            sum_bytes = sum_bytes + len(line)
        print '------'
        print ' sum_bytes = ', sum_bytes
        #connection.sendall('PLZCEASESENDING')
        connection.sendall('^^DONE+DONE/DONE-DONE^^')
        f1.close()
        if(size == sum_bytes):
            #connection.sendall(('SERVER: Server sent file with ' + str(size) +  ' bytes'))
            print 'Server sent file with ', sum_bytes/(1000*1000), ' Megabytes'
            return 1
        else:
            print 'ERROR'
            return 0
    except SystemError:
        print ' Except Error'
        #connection.sendall(" Error. Something went wrong somewhere. Try Again")
        return 0
    return 0

def file_receive(sock, arg_n):
    iss = 0
    mss = ''
    nn = ''
    
    for i in arg_n:
        if iss == 1:
            mss = mss + i
        if i == '.':
            iss = 1
    if mss == 'mov' or mss == 'wmv':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\Vidoes\%s' % (arg_n)
    elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\Music\%s' % (arg_n)
    elif mss == 'jpg' or mss == 'bmp':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\Pictures\%s' % (arg_n)
    elif mss == 'txt' or mss == 'py' or mss == 'c':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\Files\%s' % (arg_n)
    else:
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Server_Database\Files\%s' % (arg_n)
    try:
        size = sock.recv(64)
        print size

        f1 = open(name, nn)   

        i = 1
        quit_bit = 0
        sum_bytes = 0
        # Receive the data in small chunks and write it to a file
        # the file is is known in advance to be 16,958,907 bytes
        while True:
            data = sock.recv(4096)
            if '^^DONE+DONE/DONE-DONE^^' in data:
                new_data = ''
                n = 0

                for iii in data:
                    if n < (len(data) - 23):
                        new_data = new_data + iii
                    n = n + 1
                data = new_data
                quit_bit = 1
            #print '----------------'
            if data:
            # write the data to the file
                f1.write(data)
                i = i + 1
                sum_bytes = sum_bytes + len(data)
                print 'received chunk ', i, 'with ', len(data), ' bytes, ', \
                ' sum_bytes = ', sum_bytes, ' size', size
                if quit_bit:
                    break
            else:
                print 'received line with no data ?? '
                print ' sum_bytes = ', sum_bytes
                break
        print '------'
        print 'sum_bytes = ', sum_bytes
        f1.close
        if(quit_bit == 1):
            #data = sock.recv(128)
            #print data
            print 'Received file with', sum_bytes, ' bytes, Closing file ', arg_n
            return 1, name
        else:
            print '**ERROR**'
            return 0, name
    except SystemError:
        #data = sock.recv(64)
        #print data
        print " Error. Something went wrong somewhere. Try Again"
        return 0, name
    return None, name

def get_command(connection, client_address):
    while True:
        try:
            data = connection.recv(64)		
            #print 'Received data : "%s"' % data
            if data == 'LIST-ALL':
                connection.sendall('\nSERVER: Received LIST-ALL command from client')
		list_all(connection)
            elif data == 'READ':
                connection.sendall('\nSERVER: Received READ command from client')
					
                #receive the arguments
                arg_name = connection.recv(128)
                ixi, ddrr, actual_n = check_file_name_exist(arg_name)
                #print ixi
                if ixi == 0:
                    connection.sendall('SERVER: $ERROR$ File ' + arg_name + ' does not exist')
                    #return 0
		else:
                    connection.sendall('SERVER: Recieved File name ' + arg_name + ' to be transferred')
                    xx = send_file(connection, arg_name, ddrr)
                    print '^^----******+++++*******----^^'
                    if xx == 1:
                        connection.sendall('SERVER: File ' + arg_name + ' has been sent successfully')
                    #print '1'
                    else:
                        connection.sendall('SERVER: **ERROR**: File transfer unsuccessful, Try Again')
                    #print '0'
                    print '^^----******+++++*******----^^'
            elif data == 'WRITE':
                connection.sendall('\nSERVER: Received WRITE command from client')
					
                #receive the arguments
                data = connection.recv(64)
                if 'ERROR$' in data:
                    print data
                else:
                    arg_name = data
                    connection.sendall('\nSERVER: Recieved name ' + arg_name)
					
                    sx, nname = file_receive(connection, arg_name)
                    if sx == 1:
                        connection.sendall('\nSERVER: File ' + arg_name + ' has been recieved succesfully')
                    else:
                        remove_file(nname)
                        connection.sendall('SERVER: $ERROR$: File transfer unsuccessful, Try Again')
            elif data == 'BYE':
                print '\nSERVER: Client left the Server: ', client_address
                quit_check = remove_client_ip(client_address)
                #print list_ip
                #print quit_check
                #This method will remove this client ip address from a list containing all ip addresses of clients that are conneted to server
                #When there are no elements left in the list then  server knows that no clients are connected to server and thus it QUITs n close server
                if quit_check == 1:
                    return 1
                else:
                    connection.close()
                    return None
            elif data == 'CONNECT':
                connection.sendall('\nClient is now connected to the server')
                add_client_ip(client_address)
            else:
                connection.sendall('\nSERVER: Invalid Command')
        except SystemError:
            connection.sendall(" Error. Something went wrong somewhere")
            break

    return 0

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    
        cur_thread = threading.current_thread()  # identify current thread

        thread_name = cur_thread.name   # get thread-number in python     
    
        print '\nServer Thread %s receives request' % thread_name
        a = 0
        while a == 0:        
            try:
                print 'Server receives connection from ', self.client_address
                a = get_command(self.request, self.client_address)
                if a:
                    break
            
            finally:
                # Clean up the connection
                # this section 'finally' is 'ALWAYS' executed        
                print '******************************************************'
                print 'Server  Thread %s terminating connection' % thread_name
                self.request.close()  
        
        #print '\nServer Thread %s sleeping for 30 seconds'
        #time.sleep(30)
        
        #print '\nServer Thread %s terminating' % thread_name


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 4000

    print "\nStart Threaded-Server on PORT %s " % PORT

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # Terminate the server when the main thread terminates 
    # by setting daemon to True
    server_thread.daemon = True
    server_thread.start()
    print "Main Server using thread %s " % server_thread.name

    # sleeping the server thread will keep the server alive
    print 'Main Server thread sleeping'
    while True:
        answer = raw_input(">>")
        if answer.upper() == 'QUIT':
            print "Shutting Down Server for upgrade..\n%s clients need to be closed" % str(len(threading.enumerate())-2)
            #server_thread.close()
            break
    
    print 'Main server thread shutting down the server and terminating'
    server.shutdown()

