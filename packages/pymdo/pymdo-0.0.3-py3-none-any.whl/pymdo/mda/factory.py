from typing import List

from pymdo.core.discipline import Discipline
from .mda import MDA 
from .gauss_seidel import MDAGaussSeidel
from .jacobi import MDAJacobi
from .newton import MDANewton
from .hybrid import MDAHybrid

class InvalidMDAName(Exception):

    def __init__(self, _invalidMDAType: str) -> None:

        self.message = f"Invalid MDA type: {_invalidMDAType}. Available types are: MDAGaussSeidel, MDAJacobi, MDANewton, MDAHybrid"

        super().__init__(self.message)
        
def MDAFactory(_disciplines: List[Discipline],
                _mdaType: str = "MDAGaussSeidel",
                **kwargs) -> MDA:
    
    if _mdaType == "MDAGaussSeidel":

        return MDAGaussSeidel(_disciplines, **kwargs)
    
    if _mdaType == "MDAJacobi":

        return MDAJacobi(_disciplines, **kwargs)
    
    if _mdaType == "MDANewton":

        return MDANewton(_disciplines, **kwargs)
    
    if _mdaType == "MDAHybrid":

        name = "MDAHybrid" if "_name" not in kwargs else kwargs["_name"]

        mdaSequence: List[MDA] = None if "_mdaSequence" not in kwargs else kwargs["_mdaSequence"]

        return MDAHybrid(_disciplines, mdaSequence, name)

    else:
        raise InvalidMDAName(_mdaType)