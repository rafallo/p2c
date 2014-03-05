from cx_Freeze import setup, Executable
import sys, os

base = None
path_platforms = []
target_name = "p2c"
path = None
if sys.platform == "win32":
    base = "Win32GUI"
    target_name += ".exe"
    path_platforms = [( "C:\\Qt\\5.2.1\\msvc2012\\plugins\\platforms\\qwindows.dll", "platforms\qwindows.dll" ),
        ( "C:\\Qt\\5.2.1\\msvc2012\\bin\\libEGL.dll", "libEGL.dll" ),
        ( "C:\\Qt\\5.2.1\\msvc2012\\bin\\Qt5MultimediaQuick_p.dll", "Qt5MultimediaQuick_p.dll" ),
        ( "C:\\Qt\\5.2.1\\msvc2012\\bin\\Qt5MultimediaWidgets.dll", "Qt5MultimediaWidgets.dll" ),
        ( "C:\\Qt\\5.2.1\\msvc2012\\bin\\d3dcompiler_46.dll", "d3dcompiler_46.dll" ),
        ( "gui\\qml\\resources", "resources" )
        ,]
    # get all dlls from qml dir
    path = "C:\\Qt\\5.2.1\\msvc2012\\qml"
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".pdb"):
                abs_path = os.path.join(root,file)
                path_platforms.append((abs_path, os.path.join("qml", os.path.relpath(abs_path, path))))

    # get all imageformats
    path = "C:\\Qt\\5.2.1\\msvc2012\\plugins\\imageformats"
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".pdb"):
                abs_path = os.path.join(root,file)
                path_platforms.append((abs_path, os.path.join("imageformats", os.path.relpath(abs_path, path))))


exe = Executable(
    script=os.path.join('gui','qml','main.py'),
    base = base,
    initScript=None,
    targetName=target_name,
    compress=True,
    path=["qml"]
)


options = dict(
    includes=['p2c', "atexit", "PyQt5.QtCore", "PyQt5.QtGui",
              "PyQt5.QtWidgets", "PyQt5.QtNetwork",
              "PyQt5.QtMultimedia","PyQt5.QtSvg",
              "PyQt5.QtQml", "sip"],
    include_files=path_platforms,
    packages=["os"],
    path=[],
    excludes=[
        '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
        'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
        'Tkconstants', 'Tkinter'
    ]
)

setup(
    name="P2C",
    version="0.1",
    description="Peer 2 cinema",
    executables=[exe],
    options={'build_exe': options}
)