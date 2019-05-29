import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/kde/kdeconnect-kde.git'
        self.defaultTarget = 'master'
        self.description = "KDE Connect adds communication between KDE and your smartphone"
        self.displayName = "KDE Connect"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\kdeconnect-indicator.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.defines["appname"] = "kdeconnect-indicator"

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # move everything to the location where Qt expects it
        pluginPath = os.path.join(archiveDir, "plugins")
        binPath = os.path.join(archiveDir, "bin")
        libPath = os.path.join(archiveDir, "lib")

        if CraftCore.compiler.isMacOS:
            # Move kdeconnect-cli and kdeconnectd to package
            defines = self.setDefaults(self.defines)
            appPath = self.getMacAppPath(defines)
            if not utils.copyFile(os.path.join(binPath, "kdeconnect-cli"), 
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False
            
            if not utils.copyFile(os.path.join(libPath, "libexec", "kdeconnectd"), 
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False
            
            # Fix all executable in Contents/MacOS except kdeconnect-indicator
            for executable in ["kdeconnect-cli", "kdeconnectd"]:
                fileToFix = os.path.join(appPath, "Contents", "MacOS", executable)
                for oldRef in utils.getLibraryDeps(fileToFix):
                    newRef = None
                    basename = os.path.basename(oldRef)
                    if f"{basename}.framework" in oldRef:
                        # Update dylib in framework
                        newRef = "@executable_path/../Frameworks/" + oldRef[oldRef.find(f"{basename}.framework"):]
                    else:
                        newRef = "@executable_path/../Frameworks/" + basename
                    with utils.makeWritable(fileToFix):
                        if not utils.system(["install_name_tool", "-change", oldRef, newRef, str(fileToFix)], logCommand=False):
                            CraftCore.log.error("%s: failed to update library dependency path from '%s' to '%s'",
                                                fileToFix, oldRef, newRef)
                            return False
        
        return utils.mergeTree(os.path.join(archiveDir, "lib/qca-qt5"), 
            pluginPath if CraftCore.compiler.isMacOS else binPath)
