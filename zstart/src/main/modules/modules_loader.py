import pathlib
from instances import ConfigData
from typing import List

class ModuleLoader:
    def getModuleList( self ) -> List[pathlib.Path]:
        modulesPath = pathlib.Path( ConfigData.java.flags.modules_path )
        modules = []
        
        for file in modulesPath.glob( "*.yml" ): modules.append( file )
        return modules

if __name__ == "__main__":
    moduleLoader = ModuleLoader()
    print( moduleLoader.getModuleList() )