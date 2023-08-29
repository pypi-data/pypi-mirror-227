from typing import Dict, List

from numpy import ndarray

from pymdo.core.variable import Variable, FLOAT_DATA_TYPE
from pymdo.core.discipline import Discipline
from pymdo.mda.mda import MDA
from pymdo.mda.smart_mda import SmartMDA
from .mdo import MDOptProblem


class MDF(MDOptProblem):

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

        self.mda: MDA = SmartMDA(self.disciplines)
        """ MDA used for converging the system to feasibility """

        # self.mda.AddDiffInput(self.designVariables)

        # self.mda.AddDiffOutput([self.objective])
    
    def _SetValues(self) -> Dict[str, ndarray]:
        return self.mda.Eval(self.designVector)
    
    def _SetGrad(self) -> Dict[str, Dict[str, ndarray]]:
        return self.mda.Differentiate()