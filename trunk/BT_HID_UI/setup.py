from distutils.core import setup
from distutils.extension import Extension

# compile theme files
import subprocess
result = subprocess.call( "cd themes; edje_cc -v -fd ../fonts -id ../images remoko.edc", shell=True )
if result != 0:
    raise Exception( "Can't build theme files. Built edje_cc?" )

setup(
    name = "remoko UI",
    version = "0.1",
    author = "See AUTHORS",
    author_email = "",
    url = "",
		packages = [ "remoko/" ],
    scripts = [ "remoko/remoko" ],
    data_files = [
        ( "remoko/", ["themes/remoko.edj", "data/service_record.xml"] ),
        ( "pixmaps", ["images/remoko.png"] ),
        ( "applications", ["data/remoko.desktop"] ),
        ]
)
