import imp
import sys


print(sys.modules[name])
fp,path, desc = imp.find_module(conftest)
print("module found")

