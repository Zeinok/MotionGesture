import subprocess

class WindowAction:
    @staticmethod
    def nextDesktop():
        subprocess.call(["qdbus", "org.kde.KWin", "/KWin", "nextDesktop"])
    @staticmethod
    def previousDesktop():
        subprocess.call(["qdbus", "org.kde.KWin", "/KWin", "previousDesktop"])
    @staticmethod
    def toggleDashboard():
        subprocess.call(["qdbus", "org.kde.plasmashell", "/PlasmaShell", "toggleDashboard"])
    @staticmethod
    def minimizeWindow():
        subprocess.call(['qdbus', 'org.kde.kglobalaccel', '/component/kwin', 'org.kde.kglobalaccel.Component.invokeShortcut', 'Window Minimize'])
    @staticmethod
    def maximizeWindow():
        subprocess.call(['qdbus', 'org.kde.kglobalaccel', '/component/kwin', 'org.kde.kglobalaccel.Component.invokeShortcut', 'Window Maximize'])