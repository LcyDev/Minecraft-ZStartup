import pathlib
from manager_config import *
from typing import List
from flags_module import *


class ModuleMan:
    modulesPath: pathlib.Path
    modulesLoaded: List[FlagsModule]
    
    def __init__( self ):
        self.setModulesPath( MODULES_DEFAULT_PATH )
    
    def setModulesPath( self, path ):
        self.modulesPath = path
    
    def getModuleList( self ) -> List[pathlib.Path]:
        modules = []
        for file in self.modulesPath.glob( f"*{MODULES_DEFAULT_EXT}" ):
            modules.append( file )
        return modules
    
    def loadModule( self, path ):
        self.modulesLoaded.append( FlagsModule(path) )
        
if __name__ == "__main__":
    moduleLoader = ModuleMan()
    print( moduleLoader.getModuleList() )