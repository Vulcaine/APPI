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
        self.plugins = None
        self.properties = None
        self.dependencyManagement = None
        self.dependencyManagementDependencies = None

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

    def AddDependencyManagementRoot(self):
        self.dependencyManagement = self.root.Child('dependencyManagement')
        return self.dependencyManagement

    def AddDependencyManagementDependenciesRoot(self):
        if not self.dependencyManagement:
            self.AddDependencyManagementRoot()

        self.dependencyManagementDependencies = self.dependencyManagement.Child('dependencies')
        return self.dependencyManagementDependencies

    def AddDependencyManagementDependency(self, groupId, artifactId, dtype, version, scope):
        if not self.dependencyManagementDependencies:
            self.AddDependencyManagementDependenciesRoot()

        dependency = self.dependencyManagementDependencies.Child('dependency')
        dependency.Child('groupId', groupId)
        dependency.Child('artifactId', artifactId)
        dependency.Child('type', dtype)
        dependency.Child('version', version)
        dependency.Child('scope', scope)

        return dependency

    def AddParent(self, groupId, artifactId, version, isRelativePath = False):
        parent = self.root.Child('parent')
        parent.Child('groupId', groupId)
        parent.Child('artifactId', artifactId)
        parent.Child('version', version)

        if isRelativePath:
            parent.Child('relativePath')

    def AddPluginsRoot(self):
        if not self.pluginManagement:
	        self.AddPluginManagementRoot()

        self.plugins = self.pluginManagement.Child("plugins")
        return self.plugins

    def AddPropertiesRoot(self):
        self.properties = self.root.Child('properties')
        return self.properties

    def AddProperty(self, propertyKey, propertyValue):
        if not self.properties:
            self.AddPropertiesRoot()

        prop = self.properties.Child(propertyKey, propertyValue)
        return prop

    def AddPluginManagementRoot(self):
        if not self.build:
            self.AddBuildRoot()

        self.pluginManagement = self.build.Child('pluginManagement')

    def AddPlugin(self, groupId, artifactId, configuration = {}):
        if not self.plugins:
            self.AddPluginsRoot()

        plugin = self.plugins.Child('plugin')
        plugin.Child('groupId', groupId)
        plugin.Child('artifactId', artifactId)

        conf = plugin.Child('configuration')
        conf.Childs(configuration)

        return plugin

    def AddDependency(self, groupId, artifactId, version, scope = None):
        if not self.dependencies:
            self.AddDependenciesRoot()

        d = self.dependencies.Child('dependency')

        d.Child('groupId', groupId)
        d.Child('artifactId', artifactId)
        d.Child('version', version)

        if scope:
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

