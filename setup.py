from distutils.core import setup
import py2exe
setup(console=['gui.py'],skip_archive=True,data_files=[('',['organList.txt','cancerList.txt','stageKeys.yaml'])])
