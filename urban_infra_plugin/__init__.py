def classFactory(iface):
    from .main_plugin import UrbanInfraPlugin
    return UrbanInfraPlugin(iface)
