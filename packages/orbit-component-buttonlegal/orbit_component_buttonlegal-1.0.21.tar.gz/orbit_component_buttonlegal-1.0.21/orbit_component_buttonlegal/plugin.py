from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_buttonlegal.schema.MyTable import MyTableCollection
from loguru import logger as log


class Plugin (PluginBase):

    NAMESPACE = 'buttonlegal'
    COLLECTIONS = [MyTableCollection]


class Args (ArgsBase):
        
    def setup (self):
        return self
    
    def process (self):
        pass