from typing import List, Dict 

from numpy import ndarray

from pymdo.core.discipline import Discipline
from .mda import MDA

class MDAJacobi(MDA):
    """
    
    This MDA sub-class implements the generalized 
    or non-linear Jacobi iteration:

    Yi^(k+1) = Yi(Xi^k),

    where Xi^k = [xi^k z^k y1i^k ... yni^k], j =/= i

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDAJacobi",
                 _nIterMax: int = 15,
                 _relaxFact: float = 0.9,
                 _relTol=0.0001) -> None:

        super().__init__(_disciplines,
                         _name,
                         _nIterMax,
                         _relaxFact,
                         _relTol)

    def _Eval(self) -> None:

        self.status = self.MDA_FAIL

        self.residualLog = []

        while self._TerminateCondition() == False:

            currentOutputs: Dict[str, ndarray] = {}

            for disc in self.disciplines:

                discInputs = {
                    var.name: self.values[var.name] for var in disc.inputVars}

                disc.Eval(discInputs,
                            _checkValues=True,
                            _cacheValues=False)
                
                currentOutputs.update({var.name: disc.values[var.name] for var in disc.outputVars})
                
            for var in self.outputVars:
                currentOutputs[var.name] = self.relaxFact * currentOutputs[var.name] + \
                    (1 - self.relaxFact) * self.values[var.name]
            
            self._ComputeResidual(currentOutputs,
                                  self.values)

            self.values.update(currentOutputs)