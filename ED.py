
# coding: utf-8

# In[1]:

from pyomo.environ import *
model = AbstractModel()


# In[2]:

#set
model.G = Set()


# In[3]:

#parameters
model.a = Param(model.G)
model.b = Param(model.G)
model.Pmin = Param(model.G)
model.Pmax = Param(model.G)
#lone parameter
model.D = Param()


# In[ ]:

#variables
model.P = Var(model.G)


# In[6]:

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
    return sum(model.a[i]*model.P[i] + 0.5*model.b[i]*model.P[i]**2 for i in model.G)
#default is to minimize        
model.OBJ = Objective(rule=cost_rule) 


# 
