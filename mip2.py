import gurobipy as gp
from gurobipy import GRB


model = gp.Model("mip1")
x = model.addVars(10, name = 'x', vtype = GRB.BINARY)

# model.setObjective(x[0] + x[1] + 2*x[2] + 3*x[8] + 5*x[9], GRB.MINIMIZE)
# model.addConstr(x[0] + 2*x[1] + 3*x[2] + 5*x[3] + 3*x[4] >= 8, "c0")
# model.addConstr(2*x[3] + 2*x[4] + 3*x[5] + 5*x[6] + 3*x[7] >= 14, "c1")
# model.addConstr(x[7] + x[8] + 3*x[9] >= 4, "c2")
# model.addConstr(2*x[0] + x[2] + 3*x[7] + 3*x[8] + 2*x[9] >= 8, "c3")
# model.addConstr(x[7] + x[8] + 3*x[9] >= 1, "c4")
# model.addConstr(2*x[4] + 2*x[5] + x[6] + 5*x[7] + 3*x[8] >= 4, "c5")
# model.addConstr(2*x[2] + 3*x[9] >= 5)

model.setObjective(-x[0]  -x[1]  -2*x[2]  -2*x[8] - x[9], GRB.MINIMIZE)
model.addConstr(x[0] + 2*x[1] + 3*x[2] + 5*x[3] + 3*x[4] <= 8, "c0")
model.addConstr(2*x[3] + 2*x[4] + 3*x[5] + 5*x[6] + 3*x[7] <= 10, "c1")
model.addConstr(x[7] + x[8] + 3*x[9] <= 4, "c2")
model.addConstr(2*x[0] + x[2] + 3*x[7] + 3*x[8] + 2*x[9] <= 8, "c3")
model.addConstr(x[7] + x[8] + 3*x[9] >= 1, "c4")
model.addConstr(2*x[4] + 2*x[5] + x[6] + 5*x[7] + 3*x[8] >= 4, "c5")
model.optimize()

model.optimize()
model.write("model_integer.lp")
for v in model.getVars():
    print('%s %g' % (v.VarName, v.X))

print('Obj: %g' % model.ObjVal)

