from xmlparser.xmlbuilder       import XMLBuilder

class PomBuilder:
    def __init__(self, modelVersion = '4.0.0'):
        self.builder = XMLBuilder()

        xmlns = "http://maven.apache.org/POM/4.0.0".format(modelVersion)
        xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        xsi_schemaLocation = "{0} http://maven.apache.org/maven-v4_0_0.xsd".format(xmlns)

        self.root = self.builder.Root('project')

        self.root.SetProperty('xmlns', xmlns)
        self.root.SetProperty('xmlns:xsi', xmlns_xsi)
        self.root.SetProperty('xsi:schemaLocation', xsi_schemaLocation)

        self.modules = None
        self.dependencies = None
        self.build = None
        self.pluginManagement = None

        modelVersion = self.root.Child('modelVersion', modelVersion)

    def AddModulesRoot(self):
        self.modules = self.root.Child('modules')
        return self.modules

    def AddModule(self, text = ''):
        if not self.modules:
            self.AddModulesRoot()

        m = self.modules.Child('module', text)
        return m

    def AddBuildRoot(self):
        self.build = self.root.Child('build')
        return self.build

    def AddDependenciesRoot(self):
        self.dependencies = self.root.Child('dependencies')
        return self.dependencies

    def AddPluginManagementRoot(self):
        if not self.build:
            self.AddBuildRoot()

        self.pluginManagement = self.build.Child('pluginManagement')

    def AddPlugin(self, groupId, artifactId, configuration = {}):
        if not self.pluginManagement:
            self.AddPluginManagementRoot()

        plugin = self.pluginManagement.Child('plugin')
        plugin.Child('groupId', groupId)
        plugin.Child('artifactId', artifactId)

        conf = plugin.Child('configuration')
        conf.Childs(configuration)

        return plugin

    def AddDependency(self, groupId, artifactId, version, scope):
        if not self.dependencies:
            self.AddDependenciesRoot()

        d = self.dependencies.Child('dependency')

        d.Child('groupId', groupId)
        d.Child('artifactId', artifactId)
        d.Child('version', version)
        d.Child('scope', scope)

        return d

    def SetGroupId(self, groupId):
        return self.root.Child('groupId', groupId)

    def SetArtifactId(self, artifactId):
        return self.root.Child('artifactId', artifactId)

    def SetPackaging(self, packaging):
        return self.root.Child('packaging', packaging)

    def SetVersion(self, version):
        return self.root.Child('version', version)

    def SetName(self, name):
        return self.root.Child('name', name)

    def ToString(self):
        return self.builder.ToString()

