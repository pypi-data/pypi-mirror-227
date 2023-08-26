import cvxpy as cp
import numpy as np

def computing_ab_i_odd(s_2, l, v):
    
    """
    Used in special case of n-bit BGC construction with flexible length.
    Used in function(m_length_BGC).
    """
    
    ## How many values we need to add before s_r
    E_v = int(np.floor((v-1)/3))
    E_v = s_2[:E_v]
        
    ## Computing b_i
    b_i = dict()
    for i in range(n):
        b_i[i] = 0
        if i in E_v:
            b_i[i] = E_v.count(i)
            
    inequalities = []
    TC = dict()

    ## How many a_i we need to compute:
    a_i = []
    for i in range(n):
        a_i.append(cp.Variable(integer=True))

    for i in range(n+2):
        if l%2 == 0:
            if i == n:
                TC_i = l - cp.floor(v/3) + cp.ceil(((v+4)%6)/6)
            elif i == n+1:
                TC_i = l - cp.floor(v/3) + cp.ceil(((v+1)%6)/6)
            elif i == s_2[-1]:
                TC_i = 3*(s_2.count(i)-1) - 2*a_i[i] + b_i[i]
            else:
                TC_i = 3*s_2.count(i) - 2*a_i[i] + b_i[i]
            TC[i] = TC_i
        else:
            if i == n:
                TC_i = l - cp.floor(v/3) + cp.ceil(((v+1)%6)/6)
            elif i == n+1:
                TC_i = l - cp.floor(v/3) + cp.ceil(((v+4)%6)/6)
            elif i == s_2[-1]:
                TC_i = 3*(s_2.count(i)-1) - 2*a_i[i] + b_i[i]
            else:
                TC_i = 3*s_2.count(i) - 2*a_i[i] + b_i[i]
            TC[i] = TC_i
                
    ## Solving the resulting inequalities for a_i
    inequalities = []
    for key1 in TC.keys():
        for key2 in TC.keys():
            if key1 != key2:
                inequalities.append(-2 <= TC[key1] - TC[key2])
                inequalities.append(TC[key1] - TC[key2] <= 2)
    inequalities.append(sum(a_i) == l)
    for i in range(len(a_i)):
        inequalities.append(a_i[i] >= 0)
        inequalities.append(a_i[i] <= l)

    a_values = dict()
    problem = cp.Problem(cp.Minimize(0), inequalities)
    problem.solve()

    if problem.status == 'optimal':
        for i in range(len(a_i)):
            a_values[i] = int(a_i[i].value)
    
    return [v, a_values, E_v]