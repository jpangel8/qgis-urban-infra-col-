"""
Urban Infrastructure Colombia - QGIS Plugin
Autor: jpangel8 | Licencia: MIT
"""
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField,
    QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer
)
from PyQt5.QtCore import QVariant
import os

class UrbanInfraPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.actions = []
        self.menu = None
        self.toolbar = None

    def initGui(self):
        self.menu = QMenu("Infraestructura Urbana COL", self.iface.mainWindow().menuBar())
        menu_bar = self.iface.mainWindow().menuBar()
        menu_bar.insertMenu(menu_bar.actions()[-1], self.menu)
        self.toolbar = self.iface.addToolBar("Urban Infra COL")

        for nombre, metodo, tooltip in [
            ("Analizar Red de Servicios", self.run_network_analysis, "Analiza redes de acueducto, alcantarillado y energia"),
            ("Visualizar Infraestructura", self.run_infrastructure_visualization, "Aplica simbologia estandar a capas de infraestructura"),
            ("Gestion Activos Viales", self.run
cat > urban_infra_plugin/main_plugin.py << 'PYEOF'
"""
Urban Infrastructure Colombia - QGIS Plugin
Autor: jpangel8 | Licencia: MIT
"""
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField,
    QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer
)
from PyQt5.QtCore import QVariant
import os

class UrbanInfraPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.actions = []
        self.menu = None
        self.toolbar = None

    def initGui(self):
        self.menu = QMenu("Infraestructura Urbana COL", self.iface.mainWindow().menuBar())
        menu_bar = self.iface.mainWindow().menuBar()
        menu_bar.insertMenu(menu_bar.actions()[-1], self.menu)
        self.toolbar = self.iface.addToolBar("Urban Infra COL")

        for nombre, metodo, tooltip in [
            ("Analizar Red de Servicios", self.run_network_analysis, "Analiza redes de acueducto, alcantarillado y energia"),
            ("Visualizar Infraestructura", self.run_infrastructure_visualization, "Aplica simbologia estandar a capas de infraestructura"),
            ("Gestion Activos Viales", self.run_road_asset_management, "Crea capa con esquema estandar INVIAS"),
        ]:
            action = QAction(nombre, self.iface.mainWindow())
            action.setToolTip(tooltip)
            action.triggered.connect(metodo)
            self.menu.addAction(action)
            self.toolbar.addAction(action)
            self.actions.append(action)

        self.menu.addSeparator()
        about = QAction("Acerca de", self.iface.mainWindow())
        about.triggered.connect(self.show_about)
        self.menu.addAction(about)

    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run_network_analysis(self):
        layer = self.iface.activeLayer()
        if not layer or layer.type() != layer.VectorLayer:
            QMessageBox.warning(None, "Seleccion requerida", "Selecciona una capa vectorial de red de servicios.")
            return
        total = sum(f.geometry().length() for f in layer.getFeatures() if f.geometry())
        QMessageBox.information(None, "Analisis completado",
            f"Red: {layer.name()}\nTramos: {layer.featureCount()}\nLongitud total: {total/1000:.2f} km\n\nRevisa Log Messages para detalle.")

    def run_infrastructure_visualization(self):
        layer = self.iface.activeLayer()
        if not layer or layer.type() != layer.VectorLayer:
            QMessageBox.warning(None, "Seleccion requerida", "Selecciona una capa vectorial.")
            return
        if "tipo" not in [f.name().lower() for f in layer.fields()]:
            QMessageBox.warning(None, "Campo faltante", "La capa necesita un campo 'tipo'.")
            return
        colores = {
            "acueducto":"#1E90FF","alcantarillado":"#8B4513",
            "energia":"#FFD700","vias":"#808080",
            "telecomunicaciones":"#9400D3","gas":"#FF8C00",
        }
        from qgis.PyQt.QtGui import QColor
        categorias = []
        for tipo in layer.uniqueValues(layer.fields().indexOf("tipo")):
            color = colores.get(str(tipo).lower(), "#AAAAAA")
            sym = QgsSymbol.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            categorias.append(QgsRendererCategory(tipo, sym, str(tipo)))
        layer.setRenderer(QgsCategorizedSymbolRenderer("tipo", categorias))
        layer.triggerRepaint()
        QMessageBox.information(None, "Simbologia aplicada", f"Visualizacion aplicada a: {layer.name()}")

    def run_road_asset_management(self):
        from qgis.core import QgsFields, QgsWkbTypes
        fields = QgsFields()
        for nombre, tipo in [
            ("id_activo",QVariant.String),("nombre_via",QVariant.String),
            ("tipo_via",QVariant.String),("material",QVariant.String),
            ("longitud_m",QVariant.Double),("ancho_m",QVariant.Double),
            ("pci",QVariant.Int),("estado",QVariant.String),
            ("ultimo_mant",QVariant.String),("costo_mant",QVariant.Double),
            ("municipio",QVariant.String),("responsable",QVariant.String),
        ]:
            fields.append(QgsField(nombre, tipo))
        layer = QgsVectorLayer("LineString?crs=EPSG:4686", "Activos_Viales_Municipal", "memory")
        layer.dataProvider().addAttributes(fields)
        layer.updateFields()
        QgsProject.instance().addMapLayer(layer)
        layer.startEditing()
        QMessageBox.information(None, "Capa creada",
            "Capa 'Activos_Viales_Municipal' creada.\nCRS: MAGNA-SIRGAS (EPSG:4686)\nEsquema INVIAS listo para digitalizar.")

    def show_about(self):
        QMessageBox.about(None, "Urban Infrastructure Colombia v1.0",
            "Plugin QGIS para ingenieros civiles del sector publico colombiano.\n\n"
            "Herramientas:\n1. Analisis de redes de servicios\n"
            "2. Visualizacion de infraestructura critica\n"
            "3. Gestion de activos viales (INVIAS)\n\n"
            "github.com/jpangel8/qgis-urban-infra-col\nLicencia: MIT")
