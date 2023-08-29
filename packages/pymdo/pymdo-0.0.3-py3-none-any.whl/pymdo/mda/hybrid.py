from typing import List 

from pymdo.core.discipline import Discipline
from .mda import MDA
from .gauss_seidel import MDAGaussSeidel
from .newton import MDANewton

class MDAHybrid(MDA):
    """
    
    A hybrid MDA consisting of a sequence of MDAs.

    By default a GaussSeidel MDA is followed by a
    Newton MDA. This combination uses the robust nature 
    of the former, with the fast convergence of the latter.

    Any user-defined sequence of MDAs can be used.

    """

    def __init__(self, 
                 _disciplines: List[Discipline],
                 _mdaSequence: List[MDA] = None, 
                 _name: str = "MDAHybrid") -> None:
        
        super().__init__(_disciplines,
                          _name)

        self.mdaSequence: List[MDA] 

        if _mdaSequence is None:

            self.mdaSequence = [MDAGaussSeidel(self.disciplines,
                                               _nIterMax = 2,
                                               _relaxFact = 0.8,
                                               _relTol = 10),
                                MDANewton(self.disciplines,)]
        else:
            self.mdaSequence = _mdaSequence
    
    def _Eval(self) -> None:
        
        self.residualLog = []

        for mda in self.mdaSequence:

            self.values.update(mda.Eval(self.values))

            self.residualLog.extend(mda.residualLog)