import socket
import sys
import time
import os

def remove_file(ddrr):
    #name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\%s' % (ddrr) + '\%s' % (actual_n)
    print 'Deleted ' + ddrr
    os.remove(ddrr)
    return None

def print_list(f):  
    if len(f) == 0:
        return None
    for i in f:
	print i
    return None	

def list_all(sock):
	f = []
	ff = []
	i = 1
	
	while True:
            data_number = sock.recv(1)
	    print '----------------------------'
            data_size = sock.recv(int(data_number))
            #print data_size
            data = sock.recv(int(data_size))
            if 'DONE***DONE***DONE' in data:
                break
            print data
            print '----------------------------'

            data_number = sock.recv(1)
            data_size = sock.recv(int(data_number))
            #print data_size
            if int(data_size) != 0:
                #n = n + data_size + sock.recv(1)
                while True:
                    data_number_1 = sock.recv(1)
                    data_size_1 = sock.recv(int(data_number_1))
                    #print data_size_1
                    data = sock.recv(int(data_size_1))
                    f.append(data)
                    print data
                    if int(data_size) == i:
                        break
                    else:
                        i = i + 1
                    #print '-----------------'
            #print_list(f)
            i = 1
            data_number = sock.recv(1)
            data_size = sock.recv(int(data_number))
            #print data_size
            if int(data_size) != 0:
                #n = n + data_size + sock.recv(1)
                while True:
                    data_number_1 = sock.recv(1)
                    data_size_1 = sock.recv(int(data_number_1))
                    #print data_size_1
                    data = sock.recv(int(data_size_1))
                    ff.append(data)
                    print data
                    if int(data_size) == i:
                        break
                    else:
                        i = i + 1
                    #print '-----------------'
            #print_list(ff)
	return None

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
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Vidoes\%s' % (arg_n)
    elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Music\%s' % (arg_n)
    elif mss == 'jpg' or mss == 'bmp':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Pictures\%s' % (arg_n)
    elif mss == 'txt' or mss == 'py' or mss == 'c':
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Files\%s' % (arg_n)
    else:
        nn = 'wb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Files\%s' % (arg_n)
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
            print '**E-R-R-O-R**'
            return 0, name
    except SystemError:
        #data = sock.recv(64)
        #print data
        print " Error. Something went wrong somewhere. Try Again"
        
        return 0, name
    return None, name

def send_file(connection, arg_n):
    iss = 0
    mss = ''
    nn = ''
    
    for i in arg_n:
        if iss == 1:
            mss = mss + i
        if i == '.':
            iss = 1
	# Send a file over a socket
    if mss == 'mov' or mss == 'wmv':
        nn = 'rb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Vidoes\%s' % (arg_n)
    elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
        nn = 'rb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Music\%s' % (arg_n)
    elif mss == 'jpg' or mss == 'bmp':
        nn = 'rb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\CLient_Database\Pictures\%s' % (arg_n)
    elif mss == 'txt' or mss == 'py' or mss == 'c':
        nn = 'rb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Files\%s' % (arg_n)
    else:
        nn = 'rb'
        name = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\Files\%s' % (arg_n)
    
    print 'Client openning file : %s' % (arg_n)
    
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
            print 'Client sent file with ', sum_bytes/(1000*1000), ' Megabytes'
            return 1
        else:
            print 'ERROR'
            return 0
    except SystemError:
        print ' Except Error'
        #connection.sendall(" Error. Something went wrong somewhere. Try Again")
        return 0
    return 0

def check_file_name_exist(arg_n):
    f_dir = []
    drr = None
    actual_name = None
    for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\McNapster\Client_Database'):
        if len(f_2) != 0:
            for d in f_2:
                f_dir.append(d)

    for dr in f_dir:   
        f_dir = 'C:\Users\Coordinator\Desktop\S\McNapster\Client_Database\%s' % (dr)
        f = os.listdir(f_dir)
        for fl in f:
            if arg_n in fl:
                drr = dr
                actual_name = fl
                return 1, actual_name

    return 0, None
		
def command_logic(arg_command, arg_1, arg_2, sock, connect_bit):
        server_address = ()
	try:
                if((arg_command.upper() == 'CONNECT')):
                        if arg_1 == None or arg_1 == '' or arg_2 == '':
                            print 'No arguments entered'
                            return None
			server_address = (arg_1, int(arg_2))
			if arg_1 != 'localhost' or arg_2 != str(4000):
                                print 'Invalid IP address or port number. Terminating'
				print 'If you do not have this information then you are an intruder'
				print '************Terminating************'
				return None#sys.exit()
			print 'Client connecting to ip-address %s port %s' % server_address
			sock.connect(server_address)
			connect_bit = 1
			sock.sendall('CONNECT')
			data = sock.recv(64)
			print data
			return 100
		elif((arg_command.upper() == 'BYE')):
                        if(connect_bit == 1):
                                print 'client closing socket to server at ip-address %s port %s' % (arg_1, arg_2)
                                sock.sendall('BYE')
                                sock.close()
                                return 1
                        else:
                                print 'Connection with server has to be established first'
		elif((arg_command.upper() == 'LIST-ALL')):
                        if(connect_bit == 1):
                                sock.sendall('LIST-ALL')
			#print 'client sent message LIST-ALL to server'
                                data = sock.recv(64)
                                print data
				list_all(sock)
				
                        else:
                                print 'Connection with server has to be established first'
		elif((arg_command.upper() == 'READ')):
                        if(connect_bit == 1):
                                if arg_1 == None or arg_1 == '':
                                    print 'No file name entered'
                                    return None
                                sock.sendall('READ')
			#print 'client sent message READ to server'
                                data = sock.recv(64)
                                print data
                                sock.sendall(arg_1)
                                data = sock.recv(128)
                                if '$ERROR$' in data:
                                    print data
                                    return 0
                                print data
				xsx, ddrrx = file_receive(sock, arg_1)
				if xsx != 1:                         
                                    remove_file(ddrrx)
				print '--***********----***********----***********--'
				data = sock.recv(128)
                                print data
                                print '--***********----***********----***********--'
                        else:
                                print 'Connection with server has to be established first'
		elif((arg_command.upper() == 'WRITE')):
                        if connect_bit == 1:
                                if arg_1 == None or arg_1 == '':
                                    print 'No file name entered'
                                    return None
                                sock.sendall('WRITE')
			#print 'client sent message WRITE to server'
                                data = sock.recv(64)
                                print data

                                exist_bit, argum_1 = check_file_name_exist(arg_1)
                                print exist_bit
                                if exist_bit == 0:
                                    print 'File Does not exist'
                                    sock.sendall('$ERROR$')
                                    return 0
                                sock.sendall(arg_1)
                                data = sock.recv(128)
                                print data
                                
				send_file(sock, arg_1)
                                data = sock.recv(128)
                                if '$ERROR$' in data:
                                    print data
                                    return 0
                                print data
                        else:
                                print 'Connection with server has to be established first'
		else:
			if(connect_bit == 1):
				sock.sendall(arg_command)
				data = sock.recv(128)
				print data
				print 'ERROR. No such command'
			else:
				print 'ERROR. No such command'
				print 'ERROR. No connection to server'
	except SystemError:
                print sock.recv(64)
		print("Error. Something went wrong somewhere")
	return 0

	
def get_args(a):
	arg_command = ''
	arg_1 = ''
	arg_2 = ''
	arg_number = 0
	
	try:
		for i in a:
			if arg_number == 0:
				if i == ' ':
					arg_number = arg_number + 1
				else:
					arg_command = arg_command + i
			elif arg_number == 1:
				if i == ' ':
					arg_number = arg_number + 1
				else:
					arg_1 = arg_1 + i
			elif arg_number == 2:
				if i == ' ':
					arg_number = arg_number + 1
				else:
					arg_2 = arg_2 + i
			else:
				print 'You have Entered too many arguments'
		#print arg_command
		#print arg_1
		#print arg_2
	except:
		print 'Usage Error!'
		print 'Usage : <IP> <PortNumber>'
		print ''
		print 'Ex: Connect 000.111.2.333 4000'
		sys.exit(-1)
		
	return arg_command, arg_1, arg_2
    
	
def main():
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 4000)
        # server_address = ('172.17.68.149', 9000)
        
        print ''
        print '------------------------------------------------------'
        print 'This is the McNapster Client Terminal'
        print '------------------------------------------------------'
	print 'You have to choose from one of the following commands:'
	print '------------------------------------------------------'
	print '1. CONNECT <ip-address> <port-number>'
	print '2. LIST-ALL'
	print '3. READ <file-name>'
	print '4. WRITE <filename>'
	print '5. BYE'
	print '------------------------------------------------------'
	print ' ' # print a blank line
	
	i = 0
	connect_bit = 0
	arg_command = ''
	arg_1 = ''
	arg_2 = ''
	
        try:
                while True:
                    answer = raw_input("Enter Your command: ")
                    arg_command, arg_1, arg_2 = get_args(answer)
                    i = command_logic(arg_command, arg_1, arg_2, sock, connect_bit)
                    if i == 1:
                        break
                    elif i == 100:
			connect_bit = 1
		    #time.sleep(5)
		    #print 'xx ', sock.getpeername()
		    print '         ***********************'
	except:
                print 'Error. The server is down'
        finally:
                print 'client closing socket to server at ip-address %s port %s' % server_address
                sock.close()
		print 'BYE BYE'


		
if __name__ == "__main__":
	main()
