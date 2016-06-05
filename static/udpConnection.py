import socket
import sys
import os.path
import csv
from lxml import etree

HOST = ''
PORT_ON = 50000
filename = 'plot.csv'

loc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plot = os.path.join(loc, 'static/plot.csv')

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
    
except socket.error:
    print('Failed to create socket.')
    sys.exit()

try:
    s.bind((HOST, PORT_ON))

except socket.error:
    print('Bind failed')
    sys.exit()

while 1:
    data, addr = s.recvfrom(65535)
    print(addr)

    if not data:
        break
        
    root = etree.fromstring(data)
    header = root.xpath('//DataWord/Id/text()')
    content = root.xpath('//DataWord/Value/text()')

    PlotCmd = root.xpath('//PlotCmd/text()')
    print(PlotCmd)

    if PlotCmd[0] == '1':
        try:
            os.remove(plot)
        except IOError:
            print('~Data tidak ditemukan.')
    
    file_exists = os.path.isfile(filename)

    with open(filename, 'a') as csvfile:
        headers = header
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')

        if not file_exists:
            data = [header, content]
        else:
            data = [content]
        
        writer.writerows(data)

    csvfile.close()
s.close()
