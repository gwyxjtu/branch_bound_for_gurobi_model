import gurobipy as gp
from gurobipy import GRB

"""branch and bound code
输入gurobi的MIP模型 目前仅仅支持binary variable
"""


class Node:
    def __init__(self, model, upper_bound, lower_bound, candidate_vars):
        """初始化节点

        Args:
            model (_type_): gurobi model object
            upper_bound (_type_): _description_
            lower_bound (_type_): _description_
            candidate_vars (_type_): list,NumVars
        """
        self.upper_bound, self.lower_bound = upper_bound, lower_bound
        self.model = model
        # print(candidate_vars,upper_bound,lower_bound)
        self.candidate_vars = candidate_vars.copy()
        assert(upper_bound >= lower_bound), "upper bound is less than lower bound"

    def optimize(self, heuristic_solve):
        """求解Node

        Args:
            heuristic_solve (anotherFuc): 传入函数参数,求解节点的方法

        Returns:
            _type_: _description_
        """
        self.obj_values, self.solution = heuristic_solve(self.model)
        if self.obj_values == None:
            return "infeasible"
        return "feasible"
    
    def update_upper_bound(self):
        """更新upbound,最小化问题的话,上界无条件更新
        """
        # if self.upper_bound > self.obj_values:
        self.upper_bound = self.obj_values
        assert(self.lower_bound <= self.obj_values)
        assert(self.lower_bound <= self.upper_bound), "upper bound is less than lower bound"

    def update_lower_bound(self):
        """更新lowerbound,最小化问题下界条件更新
        """
        if self.lower_bound < self.obj_values:
            self.lower_bound = self.obj_values
            assert(self.lower_bound <= self.obj_values)
            assert(self.lower_bound <= self.upper_bound), "upper bound is less than lower bound"
        
    def is_integer(self):
        """判断解的质量

        Returns:
            _type_: True则表示解OK
        """
        for var in self.solution:
            if 0 < var.x and var.x < 1:
                return False
        return True
    
    def is_child_problem(self):
        # print(self.candidate_vars)
        # print(len(self.candidate_vars))
        if len(self.candidate_vars) > 0:
            return True
    
    def get_child_problem(self):
        """_summary_得替换成GRBgetvarbyname,因为不是所有变量都是binary

        Returns:
            _type_: _description_
        """
        self.child_left, self.child_right = self.model.copy(), self.model.copy()
        branch_index, self.condidate_child_vars = self.choice_branch(self.candidate_vars)
        # 分枝left bound 和 right bound。
        # print(branch_index)
        # print(self.child_left.getVarByName('x0'))
        # for v in self.child_left.getVars():
        #     print('%s' % (v.VarName,))
        self.child_left.addConstr(self.child_left.getVarByName(branch_index) == 0,"left")
        self.child_right.addConstr(self.child_right.getVarByName(branch_index) == 1,"right")
        self.child_left.write("left.lp")
        self.child_right.write("right.lp")
        node_left = Node(self.child_left, self.upper_bound, self.lower_bound, self.condidate_child_vars)
        node_right = Node(self.child_right, self.upper_bound, self.lower_bound, self.condidate_child_vars)

        return node_left, node_right
    
    def choice_branch(self, candidate_vars):
        """选择分枝的变量,这里可以加一些优化,但是似乎不太好加   现在是从等待分枝的变量中直接pop0

        Args:
            candidate_vars (_type_): 维护一个栈,剩余的需要分枝的binary variables

        Returns:
            _type_: _description_
        """
        self.condidate_child_vars = self.candidate_vars.copy()
        branch_index = self.condidate_child_vars.pop(0)  # 改为name后应该弹出的是str：varName
        return branch_index, self.condidate_child_vars
    
    def write(self):
        self.model.write("model.lp")
    

def heuristic_solve(problem):
    problem.Params.OutputFlag = 0
    problem.optimize()
    if problem.status == GRB.INFEASIBLE:
        return None, None
    # for v in problem.getVars():
    #     print('%s %g' % (v.VarName, v.X))
    # print('Obj: %g' % problem.ObjVal)
    return problem.ObjVal, problem.getVars()

def choice_node(condidate_node):
    """选择下一个计算的节点 现在也是pop0

    Args:
        condidate_node (_type_): 维护的还没计算的节点

    Returns:
        _type_: _description_
    """
    node = condidate_node.pop(0)
    return node, condidate_node


def solve(model,candidate_vars):
    model.update()
    upper_bound, lower_bound = float('inf'), float('-inf')
    model_relax = model.relax()
    root_node = Node(model = model_relax, upper_bound = upper_bound, lower_bound = lower_bound, candidate_vars = candidate_vars)
    candidate_node = [root_node]
    current_optimum = None
    while candidate_node:
        # print(candidate_node)
        node, candidate_node = choice_node(candidate_node)
        if node.upper_bound <= lower_bound:
            print("prune by bound")
            continue
        model_status = node.optimize(heuristic_solve)
        if model_status == 'infeasible':
            print("prune by infeasiblity")
            continue
        node.update_lower_bound()
        if node.lower_bound >= upper_bound:
            print("prune by bound")
            continue
        if node.is_integer():
            # print('yes')
            # exit(0)
            node.update_upper_bound()
            # lower bound 
            if node.upper_bound < upper_bound:
                upper_bound = node.upper_bound
                current_optimum = node.solution
            continue

        if node.is_child_problem():
            child_node1, child_node2 = node.get_child_problem()
            candidate_node.append(child_node1)
            candidate_node.append(child_node2)
    print('lower_bound: ',lower_bound)
    print("upper_bound: ", upper_bound)
    print("optimum:", current_optimum)

    


    

