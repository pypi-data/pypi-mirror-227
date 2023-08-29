from typing import Dict, List, Tuple
from warnings import warn

from numpy import ndarray, zeros, abs, mean
import matplotlib.pyplot as plt

from pymdo.core.discipline import Discipline
from pymdo.core.tools import SeperateInputsAndOutputs
from pymdo.core.derivative_assembler import DerivativeAssembler


class MDANotEvaluatedError(Exception):
    def __init__(self, _mdaName: str) -> None:
        self.message = f"{_mdaName} is not yet evaluated"
        super().__init__(self.message)


class MDANotConverged(Warning):
    def __init__(self, _mdaName: str, _nMaxIter: int, _res: float, _relTol: float) -> None:
        self.message = f"{_mdaName} has not converged in {_nMaxIter} iterations, (residual) {_res} > (tolerance) {_relTol}"
        super().__init__(self.message)


class MDA(Discipline):
    """

    Base MDA class 

    """

    MDA_SUCCESS = True

    MDA_FAIL = False

    MDA_STATUS = [MDA_SUCCESS,
                  MDA_FAIL]

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str,
                 _nIterMax: int = 15,
                 _relaxFact: float = 0.9,
                 _relTol: float = 0.0001
                 ) -> None:

        self.disciplines: List[Discipline] = _disciplines
        """ Disciplines to be included in the analysis """

        self.nIterMax = _nIterMax
        """ Maximum number of iterations """

        self.relaxFact = _relaxFact
        """ Relaxation factor """

        self.relTol = _relTol
        """ Relative tolerance """

        self.residualLog: List[Dict[str, float]] = []
        """ Residual log from last evaluation """

        self.status: bool = self.MDA_FAIL
        """ Whether the last execution converged """

        inputVars, outputVars = SeperateInputsAndOutputs(self.disciplines)

        super().__init__(_name,
                         inputVars,
                         outputVars)

    def SetOptions(self,
                   _nIterMax: int = 15,
                   _relaxFact: float = 0.9,
                   _relTol: float = 0.0001) -> None:
        self.nIterMax = _nIterMax
        self.relaxFact = _relaxFact
        self.relTol = _relTol

    def _Eval(self) -> None:
        raise NotImplementedError

    def Eval(self,
             _inputValues: Dict[str, ndarray] = None,
             _checkValues: bool = True,
             _cacheValues: bool = True) -> Dict[str, ndarray]:
        """ 

        Evaluate the MDA with the given inputs.

        All inputs (and outputs) not provided are set to zero.
        If they are not provided directly, but set in default values,
        those values are used. Finally, the default MDA values are overriden
        by default discipline values, if they are set.

        """

        for varList in [self.inputVars, self.outputVars]:
            for var in varList:
                if var.name not in self.defaultInputs:
                    self.defaultInputs[var.name] = zeros(var.size,
                                                            self._floatDataType)

        for disc in self.disciplines:
            self.defaultInputs.update(disc.defaultInputs)

        return super().Eval(_inputValues,
                            _checkValues,
                            _cacheValues)

    def _Differentiate(self) -> None:

        for disc in self.disciplines:

            disc.Differentiate(self.values)

        assembler = DerivativeAssembler(self.disciplines,
                                        self.outputVars,
                                        self.diffInputs,
                                        self.diffOutputs)

        self.jac = assembler.dFdX()
        
    def _ComputeResidual(self,
                         _curOutputValues: Dict[str, ndarray],
                         _prevOutputValues: Dict[str, ndarray]) -> ndarray:
        """
        
        Compute the residual namely the difference:
        
        _curOutputValues - _prevOutputValues

        for all coupling/output variables, and return it.

        The residual log is also updated, 
        but only a residual metric for each variable (and a total) is stored.

        The status is set to MDA_SUCCESS,
        if the total residual metric is below the specified tolerance.
        
        """

        residual: ndarray = zeros(self.sizeOutputs,
                                     self._floatDataType)
        
        residualMetric: Dict[str, float] = {}

        totalRes: float = 0.0

        r = 0

        for outVar in self.outputVars:

            residual[r: r + outVar.size] = _curOutputValues[outVar.name] - _prevOutputValues[outVar.name]

            residualMetric[outVar.name] = abs(mean(residual[r: r + outVar.size]) 
                                                 / mean(_curOutputValues[outVar.name]))

            totalRes += residualMetric[outVar.name]

            r += outVar.size

        residualMetric["total"] = totalRes

        self.residualLog.append(residualMetric)

        if totalRes <= self.relTol:
            self.status = self.MDA_SUCCESS

        return residual

    def PlotResidual(self,
                     _varNames: List[str]) -> None:
        """
        
        Plot the residual metric log for all provided variable names.

        Use the name "total", to plot the total MDA residual metric 

        """

        if not self.residualLog:
            raise MDANotEvaluatedError(self.name)

        for varName in _varNames:
            plt.plot([i for i in range(len(self.residualLog))],
                     [self.residualLog[i][varName]
                         for i in range(len(self.residualLog))],
                     label=varName)
            
        plt.title(f"{self.name} residual metric")
        plt.ylabel("Residual metric")
        plt.xlabel("Iterations")
        plt.legend()
        plt.show()

    def _TerminateCondition(self) -> bool:

        if self.status == self.MDA_SUCCESS:
            """ If converged, exit early """
            return True

        curIter: int = len(self.residualLog)
        """ Current iteration """

        curRes: float = 0.0 if not self.residualLog else self.residualLog[-1]["total"]
        """ Current (total) residual metric """


        if curIter == self.nIterMax:

            if self.status == self.MDA_FAIL:
                """ Iteration limit reached, and MDA has not converged """

                message = f"{self.name} has not converged in {self.nIterMax} iterations, (residual) {curRes} > (tolerance) {self.relTol}"
            
                warn(message)

            return True

        return False