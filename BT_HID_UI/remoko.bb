DESCRIPTION = "Remoko"
AUTHOR = "Valerio Valerio"
SECTION = "application"
PRIORITY = "optional"
LICENSE = "GPL"
DEPENDS = "python-ecore python-edbus python-edje python-evas python-dbus"
SRCDATE = "20080728"
PN = "remoko"
PV = "0.1"
PR = "r1"
SRC_URI = "file://README.txt "

S = "${WORKDIR}/remoko/"


do_install() {
        install -m 0755 -d ${D}${bindir} ${D}${docdir}/remoko
        install -m 0755 ${S}/remoko ${D}${bindir}
        #install -m 0644 ${WORKDIR}/README.txt ${D}${docdir}/remoko
	#copy python files and xml to /usr/local/pakages = WORKDIR
	#install -d ${D}${datadir}/applications/
	#install -m 0644 ${WORKDIR}/remoko.desktop ${D}${datadir}/applications/remoko.desktop
}	

