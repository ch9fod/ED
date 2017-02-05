
# coding: utf-8

# In[ ]:

from pyomo.environ import *
model = AbstractModel()


# In[ ]:

#set
model.G = Set()


# In[ ]:

#parameters
model.a = Param(model.G)
model.b = Param(model.G)
model.Pmin = Param(model.G)
model.Pmax = Param(model.G)
model.d = Param(model.G)
model.e = Param(model.G)
model.f = Param(model.G)
#lone parameter
model.D = Param()


# In[ ]:

#variables
model.P = Var(model.G)


# In[ ]:

#constraints
def maxp(model,i):
    return model.P[i] <= model.Pmax[i]
model.maxprod = Constraint(model.G, rule = maxp)

def minp(model,i):
    return model.P[i] >= model.Pmin[i]
model.minprod = Constraint(model.G, rule = minp)

def demand_r(model,i):
    return model.D == sum(model.P[i] for i in model.G)
model.demand = Constraint(model.G, rule = demand_r)


# In[ ]:

#objective
def cost_rule(model):
    return sum(model.a[i]*model.P[i] + 0.5*model.b[i]*model.P[i]**2 + 10*model.d[i] + 10*model.e[i]*model.P[i] + 10*model.f[i]*model.P[i]**2 for i in model.G)
#default is to minimize        
model.OBJ = Objective(rule=cost_rule) 


# In[ ]:

#solver = SolverFactory('baron')
#instance = model.create_instance('data.dat')
#results = solver.solve(instance)
#instance.display()

