import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['kbibtex/0.9'] = 'git://anongit.kde.org/kbibtex|kbibtex/0.9'
        self.svnTargets['master'] = 'git://anongit.kde.org/kbibtex|master'
        self.defaultTarget = 'kbibtex/0.9'

        self.description = "An editor for bibliographies used with LaTeX"
        self.webpage = "https://userbase.kde.org/KBibTeX"
        self.displayName = "KBibTeX"

    def setDependencies(self):
        self.runtimeDependencies['qt-libs/poppler'] = None
        self.runtimeDependencies['libs/icu'] = None
        self.runtimeDependencies['kdesupport/qca'] = None
        self.runtimeDependencies['kde/applications/okular'] = None
        self.runtimeDependencies["kde/applications/kate"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["productname"] = "KBibTeX"
        self.defines["website"] = "https://userbase.kde.org/KBibTeX"
        self.defines["executable"] = "bin\\kbibtex.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kbibtex.ico")

        return TypePackager.createPackage(self)
