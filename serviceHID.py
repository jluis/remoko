import dbus
import time

xml = ' \
<?xml version="1.0" encoding="UTF-8" ?>         \
<record>                                        \
  <attribute id="0x0001">                       \
    <sequence>                                  \
      <uuid value="0x1124"/>                    \
    </sequence>                                 \
  </attribute>                                  \
  <attribute id="0x0004">                       \
    <sequence>                                  \
     <sequence>                                \
        <uuid value="0x0100"/>                  \
        <uint16 value="0x0011"/>				\
      </sequence>                               \
    <sequence>								  	\
       <uuid value="0x0011"/>					\
     </sequence>								\
  </sequence>								    \
 </attribute>                                  \
 <attribute id="0x0009">						\
    <sequence>									\
      <sequence>								\
        <uuid value="0x1124"/>					\
        <uint16 value="0x0100"/>				\
      </sequence>								\
    </sequence>									\
  </attribute>									\
  <attribute id="0x000d">                       \
    <sequence>                                  \
     <sequence>                                \
        <uuid value="0x01124"/>                  \
        <uint16 value="0x0100"/>				\
      </sequence>                               \
    <sequence>								  	\
       <uuid value="0x0011"/>					\
     </sequence>								\
   </sequence>								    \
  </attribute>                                  \
  <attribute id="0x0100">                       \
      <text value="BluetoothKeyboard" name="name"/>            \
  </attribute>									\
  <attribute id="0x0101">                       \
   <text value="BluetoothVirtual Keyboard" name="name"/>            \
  </attribute>									\
  <attribute id="0x0102">                       \
   <text value="VDVsx Inc." name="name"/>            \
  </attribute>									\
  <attribute id="0x0200">                       \
   <uint16 value="0x0100"/>                    \
  </attribute>									\
  <attribute id="0x0201">                       \
   <uint16 value="0x0111"/>                    \
  </attribute>									\
  <attribute id="0x0202">                       \
   <uint8 value="0x0c"/>                    \
  </attribute>									\
  <attribute id="0x0203">                       \
   <uint8 value="0x016"/>                    \
  </attribute>									\
  <attribute id="0x0204">                       \
    <boolean value="0x01"/>                    \
  </attribute>									\
</record>                                       \
'
bus = dbus.SystemBus()
database = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
                                                        'org.bluez.Database')
handle = database.AddServiceRecordFromXML(xml)

print "Service record with handle 0x%04x added" % (handle)

print "Press CTRL-C to remove service record"

try:
        time.sleep(1000)
        print "Terminating session"
except:
        pass

database.RemoveServiceRecord(handle)
