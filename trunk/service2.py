import dbus
import time

from bluetooth import *

xml = ' \
<?xml version="1.0" encoding="UTF-8" ?>\
<record> \
        <attribute id="0x0000">\
                <uint32 value="0x00010002" />\
        </attribute>\
        <attribute id="0x0001">\
                <sequence>\
                        <uuid value="0x1124" />\
                </sequence>\
        </attribute>\
        <attribute id="0x0004">\
                <sequence>\
                        <sequence>\
                                <uuid value="0x0100" />\
                                <uint8 value="0x11" />\
                        </sequence>\
                        <sequence>\
                                <uuid value="0x0011" />\
                        </sequence>\
                </sequence>\
        </attribute>\
        <attribute id="0x0005">\
                <sequence>\
                        <uuid value="0x1002" />\
                </sequence>\
        </attribute>\
        <attribute id="0x0006">\
                <sequence>\
                        <uint16 value="0x656e" /> \
                        <uint16 value="0x006a" />\
                        <uint16 value="0x0100" />\
                </sequence>\
        </attribute>\
        <attribute id="0x0009">\
                <sequence>\
                        <sequence>\
                                <uuid value="0x1124" />\
                                <uint16 value="0x0100" />\
                        </sequence>\
                </sequence>\
        </attribute>\
        <attribute id="0x000d">\
                <sequence>\
                        <sequence>\
                                <sequence>\
                                        <uuid value="0x0100" />\
                                        <uint8 value="0x13" />\
                                </sequence>\
                                <sequence>\
                                        <uuid value="0x0011" />\
                                </sequence>\
                        </sequence>\
                </sequence>\
        </attribute>\
        <attribute id="0x0100">\
                <text value="BluetoothKeyboard" />\
        </attribute>\
        <attribute id="0x0101">\
                <text value="BluetoothVirtual Keyboard" />\
        </attribute>\
        <attribute id="0x0102">\
                <text value="VDVsx Inc." />\
        </attribute>\
        <attribute id="0x0200">\
                <uint16 value="0x0100" />\
        </attribute>\
        <attribute id="0x0201">\
                <uint16 value="0x0111" />\
        </attribute>\
        <attribute id="0x0202">\
                <uint16 value="0x0040" />\
        </attribute>\
        <attribute id="0x0203">\
                <uint16 value="0x000d" />\
        </attribute>\
        <attribute id="0x0204">\
                <uint16 value="0x0001" />\
        </attribute>\
        <attribute id="0x0205">\
                <uint16 value="0x0001" />\
        </attribute>\
        <attribute id="0x0206">\
                <sequence>\
                        <sequence>\
                                <uint8 value="0x22" />\
                                <text encoding="hex" value="05010906a1018501050719e029e71500250175019508810275089501810175019505050819012905910275039501910175089506150026ff00050719002aff0081007501950115002501050c09b8810609e2810609e9810209ea8102750195048101c0" />\
                        </sequence>\
                </sequence>\
        </attribute>\
        <attribute id="0x0207">\
                <sequence>\
                        <sequence>\
                                <uint16 value="0x0409" />\
                                <uint16 value="0x0100" />\
                        </sequence>\
                </sequence>\
        </attribute>\
        <attribute id="0x0208">\
                <uint16 value="0x0000" />\
        </attribute>\
        <attribute id="0x020a">\
                <uint16 value="0x0001" />\
        </attribute>\
        <attribute id="0x020b">\
                <uint16 value="0x0100" />\
        </attribute>\
        <attribute id="0x020c">\
                <uint16 value="0x1f40" />\
        </attribute>\
        <attribute id="0x020d">\
                <uint16 value="0x0001" /> \
        </attribute> \
        <attribute id="0x020e"> \
                <uint16 value="0x0001" /> \
        </attribute> \
</record> \
'\

bus = dbus.SystemBus()
database = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
                                                        'org.bluez.Database')
handle = database.AddServiceRecordFromXML(xml)

print "Service record with handle 0x%04x added" % (handle)

print "Press CTRL-C to remove service record"

#interrupt_sock= BluetoothSocket( L2CAP )
#control_sock= BluetoothSocket( L2CAP )



#interrupt_port = 19
#control_port = 17

#interrupt_sock.bind(("",interrupt_port))
#interrupt_sock.listen(1)

#control_sock.bind(("",control_port))
#control_sock.listen(1)

                   
#client_sock,address = interrupt_sock.accept()
#print "Accepted connection from ",address

#client_sock_C,address_C = control_sock.accept()
#print "Accepted connection from ",address_C

#data = client_sock.recv(1024)
#print "Data received:", data

#data = client_sock_C.recv(1024)
#print "Data received:", data


#client_sock.close()
#interrupt_sock.close()

#client_sock_C.close()
#control_sock.close()


try:
        time.sleep(1000)
        print "Terminating session"
except:
        pass

database.RemoveServiceRecord(handle)
