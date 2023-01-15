import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(__file__) + '/src')
print(sys.path) # DEBUG

wsgi = imp.load_source('wsgi', 'src/main.py')
application = wsgi.tchoupibot