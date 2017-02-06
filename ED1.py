
# coding: utf-8

# In[1]:

from pyomo.environ import *
import os
model = AbstractModel()
solverexe = "gurobi"
dirsolver = r"C:\Users\ch9fod\Documents\GitHub\ED\solvers"
datafile = "data1.dat"


# In[2]:

#set
model.G = Set()


# In[3]:

#parameters
model.a = Param(model.G)
model.b = Param(model.G)
model.Pmin = Param(model.G)
model.Pmax = Param(model.G)
#added just to calculate emissions
model.d = Param(model.G)
model.e = Param(model.G)
model.f = Param(model.G)
#lone parameter
model.D = Param()


# In[4]:

#variables
model.P = Var(model.G)


# In[5]:

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


# In[6]:

#objective
def cost_rule(model):
    return sum(model.a[i]*model.P[i] + 
               0.5*model.b[i]*model.P[i]**2 for i in model.G)
#default is to minimize        
model.OBJ = Objective(rule=cost_rule) 


# In[7]:

if solverexe == "gurobi":
    solver = SolverFactory(solverexe)
else:
    solver = SolverFactory(solverexe, 
                           executable=os.path.join(dirsolver, solverexe))
instance = model.create_instance(datafile)
instance.dual = Suffix(direction=Suffix.IMPORT)
results = solver.solve(instance)
#instance.solutions.load_from(results)
#print(results)


# In[8]:

instance.display()


# In[9]:

p = [0, 0, 0 ,0]
for i in range(3):
    p[i+1] = value(instance.P[i+1])


# In[10]:

print ("Total Emissions (tonCO2/MWh)")
x = y = 0
for i in range(3):
    y = (instance.d[i+1] + instance.e[i+1]*p[i+1] + 
        instance.f[i+1]*p[i+1]**2)
    x = x + y
    print(i+1, y)
print("Total",x)


# In[11]:

print ("Duals")
from pyomo.core import Constraint
for c in instance.component_objects(Constraint, active=True):
    print ("   Constraint",c)
    cobject = getattr(instance, str(c))
    for index in cobject:
        print ("      ", index, instance.dual[cobject[index]])

