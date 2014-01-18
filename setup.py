from distutils.core import setup
import warnings
"""
Following Segment of this file was taken from the Pandas 
project(https://github.com/pydata/pandas) 
"""
# Version Check

MAJOR = 0
MINOR = 1
MICRO = 0
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'
    try:
        import subprocess
        try:
            pipe = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"],
                                    stdout=subprocess.PIPE).stdout
        except OSError:
            # msysgit compatibility
            pipe = subprocess.Popen(
                ["git.cmd", "rev-parse", "--short", "HEAD"],
                stdout=subprocess.PIPE).stdout
        rev = pipe.read().strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        FULLVERSION += "-%s" % rev
    except:
        warnings.warn("WARNING: Couldn't get git revision")
else:
    FULLVERSION += QUALIFIER


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'nilmtk', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()
# write_version_py()
# End of Version Check

setup(
    name='iiit_disagg',
    version=FULLVERSION,
    author='Nipun Batra',
    author_email='nipunb@iiitd.ac.in',
    packages=['iiit_disagg'],
    scripts=[],
    url='https://github.com/nipunreddevil/iiit_disagg',
    license='',
    description='Non Intrusive Load Monitoring',
)
