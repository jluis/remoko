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
        <text enconding="hex" value="05010906a1018501050719e029e71500250175019508810295017508810395057501050819012905910295017503910395067508150025650507190029658100c005010902a10185020901a100050919012903150025019503750181029501750581030501093009311581257f750895028106c0c0" />		\
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
