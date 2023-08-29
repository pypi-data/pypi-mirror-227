from typing import List, Dict 

from numpy import ndarray

from pymdo.core.discipline import Discipline
from .mda import MDA


class MDAGaussSeidel(MDA):
    """
    
    This MDA sub-class implements the generalized 
    or non-linear Gauss-Seidel iteration:

    Yi^(k+1) = Yi(Xi^k),

    where Xi^k = [xi^(k+1) z^(k+1) y1i^(k+1) ... y(i-1)i^(k+1)  y(i+1)i^k yni^k]

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDAGaussSeidel",
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

                discInputs = {var.name: self.values[var.name] if var.name not in currentOutputs
                              else currentOutputs[var.name] for var in disc.inputVars}

                discOutputs = disc.Eval(discInputs,
                                        _checkValues=True,
                                        _cacheValues=False)

                for var in disc.outputVars:

                    currentOutputs[var.name] = self.relaxFact * discOutputs[var.name] + \
                        (1 - self.relaxFact) * self.values[var.name]

            self._ComputeResidual(currentOutputs,
                                  self.values)

            self.values.update(currentOutputs)