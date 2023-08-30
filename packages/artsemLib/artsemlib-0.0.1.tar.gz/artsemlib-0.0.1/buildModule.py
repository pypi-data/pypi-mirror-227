import os
import sys

__interpreter__ = 'python3' if sys.platform.find('linux') != -1 else 'python.exe'
__build_tools__ = ['twine', 'build']
print(__interpreter__)

if __name__ == '__main__':
    print(f"[INFO] Updating build tools {__build_tools__}...")
    os.system(f'{__interpreter__} -m pip install --upgrade {" ".join(__build_tools__)}')
    os.chdir(os.path.dirname(__file__))
    print(f"[INFO] Building module...")
    os.system(f'{__interpreter__} -m build')
    print(f"[INFO] Build completed. Exiting...")
