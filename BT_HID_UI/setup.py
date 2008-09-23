from distutils.core import setup
from distutils.extension import Extension

from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
import os

class my_build(_build):
    def run(self):
        _build.run(self)

        # compile theme files
        import subprocess
        result = subprocess.call( "cd themes; edje_cc -v -id ../images -fd ../fonts remoko.edc", shell=True )
        if result != 0:
            raise Exception( "Can't build theme files. Built edje_cc?" )

class my_clean(_clean):
    def run(self):
        _clean.run(self)

        if os.path.exists('./themes/remoko.edj'):
            os.remove('./themes/remoko.edj')

setup(
    name = "remoko UI",
    version = "0.3.2",
    author = "Valerio Valerio",
    author_email = "vdv100@gmail.com",
    cmdclass = { 'build'    : my_build  ,
                 'clean'    : my_clean  },
    url = "http://code.google.com/p/remoko/",
    packages = [ "remoko" ],
    scripts = [ "remoko/remoko" ],
    data_files = [
        ( "remoko", ["themes/remoko.edj", "data/service_record.xml", "data/settings.cfg"] ),
        ( "pixmaps", ["images/remoko.png"] ),
        ( "applications", ["data/remoko.desktop"] ),
        ]
)

