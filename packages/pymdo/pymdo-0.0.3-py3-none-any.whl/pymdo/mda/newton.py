from typing import List, Dict 

from numpy import ndarray
from scipy.sparse.linalg import spsolve

from pymdo.core.discipline import Discipline
from pymdo.core.derivative_assembler import DerivativeAssembler
from .mda import MDA

class MDANewton(MDA):
    """

    This MDA sub-class uses the Newton iteration 
    for a system of non-linear equations:
    
    dR^k/dY * Ycorr^(k) = R^k

    Y^(k+1) = Y^k + Ycorr^k

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDANewton",
                 _nIterMax: int = 15,
                 _relTol=0.0001) -> None:

        super().__init__(_disciplines, 
                         _name, 
                         _nIterMax, 
                         _relTol = _relTol)

    def _Eval(self) -> None:

        self.status = self.MDA_FAIL

        self.residualLog = []

        assembler = DerivativeAssembler(self.disciplines,
                                        self.outputVars,
                                        self.diffInputs,
                                        self.diffOutputs)

        while self._TerminateCondition() == False:

            currentOutputs: Dict[str, ndarray] = {}

            for disc in self.disciplines:

                disc.Eval(self.values,
                          _checkValues=True,
                          _cacheValues=False)
                
                disc.Differentiate()

                currentOutputs.update(disc.GetOutputValues())

            R = self._ComputeResidual(currentOutputs,
                                  self.values)

            assembler.UpdateJac()

            dRdY = assembler.dYdY().tocsr()

            Ycorr = spsolve(dRdY, R)

            r = 0 

            for var in self.outputVars:

                self.values[var.name] = self.values[var.name] + Ycorr[r: r + var.size]

                r += var.size