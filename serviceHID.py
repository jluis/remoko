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
 <attribute id="0x0006">						\
    <sequence>									\
        <uint16 value="0x656e"/>				\
        <uint16 value="0x006a"/>				\
        <uint16 value="0x0100"/>				\
    </sequence>									\
  </attribute>									\
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
   <uint8 value="0xc0"/>                    \
  </attribute>									\
  <attribute id="0x0203">                       \
   <uint8 value="0x016"/>                    \
  </attribute>									\
  <attribute id="0x0204">                       \
   <boolean value="true"/>                    \
  </attribute>									\
   <attribute id="0x0205">                       \
   <boolean value="true"/>                    \
  </attribute>									\
  <attribute id="0x0206">                       \
    <sequence>                                  \
   <sequence>                                \
        <uint8 value="0x22"/>                  \
        <text enconding="hex" value="05 01 09 05 a1 01 85 01 15 00 26 ff 00 75 08 95 0b 06 00 ff 09 01 81 00 85 01 95 0b 09 01 b1 00 85 02 95 0b 09 01 b1 00 85 03 95 0b 09 01 b1 00 85 04 95 0b 09 01 b1 00 85 05 95 0b 09 01 b1 00 85 06 95 0b 09 01 b1 00 c0 00" />		\
      </sequence>                               \
  </sequence>								    \
  </attribute>                                  \
  <attribute id="0x0207">                       \
    <sequence>                                  \
   <sequence>                                   \
   		<uint16 value="0x0409" />               \
   		<uint16 value="0x0100" />				\
   </sequence>                                  \
  </sequence>								    \
  </attribute>                                  \
  <attribute id="0x0208">                       \
   <boolean value="false"/>                    \
  </attribute>									\
   <attribute id="0x0209">                       \
   <boolean value="true"/>                    \
 </attribute>									\
  <attribute id="0x020a">                       \
  <boolean value="true"/>                    \
  </attribute>									\
  <attribute id="0x020b">                       \
  <uint16 value="0x0100"/>                    \
  </attribute>									\
  <attribute id="0x020d">                       \
  <boolean value="true"/>                    \
  </attribute>									\
  <attribute id="0x020e">                       \
   <boolean value="false"/>                    \
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
