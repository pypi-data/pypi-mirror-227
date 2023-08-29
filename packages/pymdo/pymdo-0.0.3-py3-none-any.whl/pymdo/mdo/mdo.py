from typing import Dict, List, Tuple, Callable

from numpy import ndarray, zeros, ones, bool8, mean, isinf, isneginf
from scipy.optimize import Bounds, NonlinearConstraint, minimize
import matplotlib.pyplot as plt


from pymdo.core.variable import Variable, FLOAT_DATA_TYPE
from pymdo.core.variable import ArrayToDict, DictToArray, DictToArray2d
from pymdo.core.variable import NormalizeDesignVector, deNormalizeDesignVector
from pymdo.core.variable import NormalizeGradient
from pymdo.core.discipline import Discipline


class MDOptProblem:

    def __init__(self,
                 _disciplines: List[Discipline],
                 _designVariables: List[Variable],
                 _objective: Variable,
                 _maximizeObjective: bool = False,
                 _useNormalization: bool = True,
                 _saveDesignVector: bool = False) -> None:

        self.disciplines: List[Discipline] = _disciplines
        """ List of disciplines modelling the problem """

        self.designVariables: List(Variable) = _designVariables
        """ List of design variables """

        self.sizeDesignVars: int = sum([dv.size for dv in self.designVariables])

        self.objective: Variable = _objective
        """ Optimization objective """

        self.maximizeObjective: bool = _maximizeObjective
        """ Whether to maximize the objective """

        self.constraints: List[Variable] = []
        """ List of constraints """

        self.useNormalization: bool = _useNormalization
        """ Whether or not to normalize design variable and gradient values """

        self.values: Dict[str, ndarray] = {}
        """ Current values of discipline variables """

        self.grad: Dict[str, Dict[str, ndarray]] = {}
        """ Current gradient values """

        self.designVector: Dict[str, ndarray] = {}
        """ Current design variables values """

        self.optLog: List[Dict[str, ndarray]] = []
        """ Optimization Log.
            By default saves the objective and constraint values
            for each optimization cycle.

            Set saveDesignVector to True to also save the design vector.
        """

        self.saveDesignVector: bool = _saveDesignVector
        """ Whether to save the design vector for each optimization cycle """
    
    def _GetDesignVariableBounds(self) -> Bounds:

        lb = zeros(self.sizeDesignVars, FLOAT_DATA_TYPE)

        ub = zeros(self.sizeDesignVars, FLOAT_DATA_TYPE)

        keepFeasible = zeros(self.sizeDesignVars, bool8)

        r = 0

        for var in self.designVariables: 

            _lb = 0.0 if self.useNormalization else var.lb
            _ub = 1.0 if self.useNormalization else var.ub

            lb[r : r + var.size] = _lb * ones(var.size, FLOAT_DATA_TYPE)

            ub[r : r + var.size] = _ub * ones(var.size, FLOAT_DATA_TYPE)

            keepFeasible[r : r + var.size] = var.keepFeasible * ones(var.size, bool8)

            r += var.size

        return Bounds(lb, 
                      ub, 
                      keepFeasible) 

    def AddConstraint(self,
                       _constraint: Variable) -> None:
        """

        Add a constraint to the optimization problem.

        A constraint variable's behaviour is represented by its lower and upper bounds.

        If lb == ub, then it is treated as equality constraint (h(x) = 0).

        If lb = -inf and ub is finite, then the constraint is h(x) <= ub.

        Conversely, if ub = inf and lb is finite, then the constraint is h(x) >= lb

        """
        if _constraint not in self.constraints:

            self.constraints.append(_constraint)
    
    def _CreateConstraintFunc(self, 
                              _constraint: Variable) -> Tuple[Callable, Callable]:

        def h(_inputValues: ndarray) -> ndarray:

            if self.values:

                return self.values[_constraint.name]

            else:

                return zeros(_constraint.size,
                             dtype=FLOAT_DATA_TYPE)
            
        def dh(_inputValues: ndarray) -> ndarray:

            if self.grad:

                return DictToArray2d(self.designVariables,
                                     [_constraint],
                                     self.grad,
                                     True)
        
        return h, dh
    
    def _GetConstraints(self) -> List[NonlinearConstraint]:

        cons = []

        for con in self.constraints:

            h, dh = self._CreateConstraintFunc(con)

            _lb = con.lb

            _ub = con.ub
            
            cons.append(NonlinearConstraint(fun = h,
                                                   lb = ones(con.size, 
                                                             dtype = FLOAT_DATA_TYPE) * _lb,
                                                   ub = ones(con.size, 
                                                             dtype = FLOAT_DATA_TYPE) * _ub,
                                                   jac = dh,
                                                   keep_feasible = ones(con.size, bool8) * con.keepFeasible))

        return cons
    
    def _SetValues(self) -> Dict[str, ndarray]:
        raise NotImplementedError
    
    def _SetGrad(self) -> Dict[str, Dict[str, ndarray]]:
        raise NotImplementedError
    
    def _GetFunc(self) -> Tuple[Callable, Callable]:

        def F(_designPointArray: ndarray) -> float:

            self.designVector = ArrayToDict(self.designVariables,
                                            _designPointArray)

            if self.useNormalization:
                self.designVector = deNormalizeDesignVector(self.designVariables,
                                                            self.designVector)

            self.values = self._SetValues()

            return self._UpdateOptimizationLog()
        
        def dF(_designPointArray: ndarray) -> ndarray:

            self.grad = self._SetGrad()

            if self.useNormalization:

                self.grad = NormalizeGradient(self.designVariables,
                                              [self.objective] +
                                              self.constraints,
                                              self.grad)

            grad = DictToArray2d(self.designVariables,
                                 [self.objective],
                                 self.grad,
                                 True)

            if self.maximizeObjective:

                grad = - grad

            return grad
        
        return F, dF
    
    def Execute(self, _initialDesignVector: Dict[str, ndarray],
                _algoName: str = "SLSQP",
                _options=None) -> Tuple[Dict[str, ndarray], float]:
        
        if self.useNormalization:
            _initialDesignVector = NormalizeDesignVector(self.designVariables,
                                                         _initialDesignVector)

        _initialDesignVectorArray = DictToArray(self.designVariables,
                                                _initialDesignVector)

        bnds = self._GetDesignVariableBounds()

        cons = self._GetConstraints()

        F, dF = self._GetFunc()

        result = minimize(fun=F,
                          x0=_initialDesignVectorArray,
                          method=_algoName,
                          jac=dF,
                          bounds=bnds,
                          constraints=cons,
                          options=_options)

        return (self.designVector, result.fun)
    

    def _UpdateOptimizationLog(self) -> float:
        """
        Update the optimization log.

        Return the (signed) objecgive value.
        
        """
        
        self.optLog.append({self.objective.name: self.values[self.objective.name]})

        self.optLog[-1].update({con.name: self.values[con.name] for con in self.constraints})

        if self.saveDesignVector:
            self.optLog[-1].update(self.designVector)

        objValue = self.optLog[-1][self.objective.name]
        
        if self.maximizeObjective:

            objValue = - objValue
        
        return objValue
    
    def PlotOptimizationHistory(self):

        cycles = [i for i in range(len(self.optLog))]

        optLog = {var.name: [mean(self.optLog[i][var.name]) for i in cycles]
                  for var in self.constraints + [self.objective]}


        for var in self.constraints + [self.objective]:
            
            plt.plot(cycles,
                    optLog[var.name], 
                    label = "value",
                    color = "k")
            
            if not isneginf(var.lb):
                
                plt.plot(cycles,
                         [var.lb for _ in cycles],
                         color = "orange",
                         label = "lb")
            
            if not isinf(var.ub):
                
                plt.plot(cycles,
                         [var.ub for _ in cycles],
                         color = "red",
                         label = "ub")

            plt.xlabel(" Cycles ")
            
            plt.ylabel(var.name)

            plt.legend()
            
            plt.grid()

            plt.show()
    
    def SaveOptHistory(self, 
                       _directory: str, 
                       _fullHistory: bool = False):
        pass

