from typing import Callable, Dict, List, Tuple

from numpy import ndarray, zeros, eye
from scipy.optimize import minimize

from pymdo.core.variable import Variable, FLOAT_DATA_TYPE
from pymdo.core.variable import ArrayToDict, DictToArray, DictToArray2d
from pymdo.core.variable import NormalizeDesignVector, deNormalizeDesignVector
from pymdo.core.variable import NormalizeGradient
from pymdo.core.discipline import Discipline
from pymdo.mda.mda import SeperateInputsAndOutputs
from pymdo.mda.smart_mda import SmartMDA
from .mdo import MDOptProblem

from pprint import pprint


class IDF(MDOptProblem):

    def __init__(self,
                 _disciplines: List[Discipline],
                 _designVariables: List[Variable],
                 _objective: Variable,
                 _maximizeObjective: bool = False,
                 _useNormalization: bool = True,
                 _saveDesignVector: bool = False) -> None:
        
        super().__init__(_disciplines,
                         _designVariables,
                         _objective,
                         _maximizeObjective,
                         _useNormalization,
                         _saveDesignVector)

        _, self.couplings = SeperateInputsAndOutputs(self.disciplines)

        self.targetVariables = [Variable(var.name + "_t",
                                          var.size,
                                          var.lb,
                                          var.ub)
                                 for var in self.couplings]

        self.designVariables += self.targetVariables

        self.constraints = [Variable(var.name + "_con",
                                     var.size,
                                     0,
                                     0)
                            for var in self.couplings]

        self.values: Dict[str, ndarray] = {}

        self.jac: Dict[str, Dict[str, ndarray]] = {}
    
    def _CreateConsistencyConstraints(self):
         """
         
         """
         pass
        
    def _SetValues(self) -> Dict[str, ndarray]:

        for disc in self.disciplines:

                disc.Eval(self.values)

                self.values.update(disc.GetOutputValues())
        
        return self.values
    
    def _SetGrad(self) -> Dict[str, Dict[str, ndarray]]:
        
        for disc in self.disciplines:

            disc.Differentiate()

            #self.jac
        

    def Execute(self,
                _initialDesignVector: Dict[str, ndarray],
                _algoName: str = "SLSQP",
                **_options) -> Tuple[Dict[str, ndarray], float]:

        mda = SmartMDA(self.disciplines)

        self.values = mda.Eval(_initialDesignVector)

        return super().Execute(_initialDesignVector,
                               _algoName,
                               **_options)

