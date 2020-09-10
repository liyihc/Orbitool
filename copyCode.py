import os
import shutil

from utils.files import FolderTraveler

dsts = [
    "C:/CODE/Python/Orbitool",
    "../codeexport" ]

shutil.rmtree("../codeexport")
os.mkdir("../codeexport")

notRecurrent = "."
recurrent = ["utils","functions"]

exts = [".py", ".pyx", ".pyd", ".dll", ".md"]

def iterator(*args):
    for i in args:
        for j in i:
            yield j

def checkBuildFolder(path):
    folder = os.path.dirname(path)
    if not os.path.isdir(folder):
        checkBuildFolder(folder)
        os.mkdir(folder)

def copyFileTo(file, dst):
    checkBuildFolder(dst)
    if not os.path.isfile(dst) or os.path.getmtime(file) > os.path.getmtime(dst):
        shutil.copyfile(file,dst)

def copyTo(folder):
    ftNot = FolderTraveler(notRecurrent, exts, False)
    ftRec = FolderTraveler(recurrent, exts, True)
    for file in iterator(ftNot, ftRec):
        if file != "copy.py":
            copyFileTo(file, os.path.join(folder,file))

if __name__ == "__main__":
    for dst in dsts:
        copyTo(dst)
    