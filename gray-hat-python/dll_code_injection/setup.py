from distutils.core import setup

setup(console=['backdoor.py'], options={'py2exe': {'bundle_files': 1}}, zipfile=None)
