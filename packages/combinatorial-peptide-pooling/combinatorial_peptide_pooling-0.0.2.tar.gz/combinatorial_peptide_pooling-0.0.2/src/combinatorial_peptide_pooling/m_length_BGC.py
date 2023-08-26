import cvxpy as cp
import numpy as np

def m_length_BGC(m, n):
    
    """
    Construction of n-bit BGC with flexible length from n-2 bit BGC.
    Is dependent on function(computing_ab_i_odd) and function(n_bgc).
    """
    
    n = n-2
    s_2 = n_bgc(n = n)
    s_2 = [x - 1 for x in s_2]
    
    ### if 3*2**n < m < 2**(n+2) (Case I)
    if 3*2**n < m < 2**(n+2):
        intervals = [np.floor(m/(n+2)) -3, np.floor(m/(n+2))]
    
        ## l is chosen from intervals
        l_options = dict()
        for l in list(range(int(intervals[0]), int(intervals[1]) + 1)):
            ## How many values we need to add before s_r
            u = m - 3*2**n
            if l%2 == 0:
                E_u = s_2[-l:][:-1]
            elif l%2 != 0:
                E_u = s_2[-l-1:][:-1]
        
            ## Computing b_i
            b_i = dict()
            for i in range(n):
                b_i[i] = 0
                if i in E_u:
                    b_i[i] = E_u.count(i)

            inequalities = []
            TC = dict()

            ## How many a_i we need to compute:
            a_i = []
            for i in range(n):
                a_i.append(cp.Variable(integer=True))

            for i in range(n+2):
                if l%2 == 0:
                    if i == n:
                        TC_i = l + 2
                    elif i == n+1:
                        TC_i = l + 2
                    elif i == s_2[-1]:
                        TC_i = 3*(s_2.count(i)-1) - 2*a_i[i] + b_i[i]
                    else:
                        TC_i = 3*s_2.count(i) - 2*a_i[i] + b_i[i]
                    TC[i] = TC_i
                else:
                    if i == n:
                        TC_i = l + 2
                    elif i == n+1:
                        TC_i = l + 1
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
            for i in range(len(a_i)):
                inequalities.append(a_i[i] >= 0)
                inequalities.append(a_i[i] <= l)
            inequalities.append(sum(a_i) == l)

            a_values = dict()
            problem = cp.Problem(cp.Minimize(0), inequalities)
            problem.solve()

            if problem.status == 'optimal':
                for i in range(len(a_i)):
                    a_values[i] = int(a_i[i].value)
                break
            l_options[l] = [u, a_values]
                    
        s_2 = s_2[:-1]
        u = []
        t = []
        new_counts = dict()
        for i in range(0, n):
            new_counts[i] = 0
        for i in s_2:
            if new_counts[i] >= a_values[i]:
                u[-1].append(i)
            else:
                t.append([i])
                u.append([])
            new_counts[i] += 1
    
        flex_s = []
        if l%2 == 0:
            flex_s = flex_s + E_u + [n]
            row_count = 0
            for i in range(l-1, -1, -1):
                if row_count == 0:
                    flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                    row_count = 1
                elif row_count == 1:
                    flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                    row_count = 0
            flex_s = flex_s + [n+1] + [n] + [n+1]
    
        elif l%2 != 0:
            flex_s = flex_s + E_u + [n]
            row_count = 0
            for i in range(l-1, -1, -1):
                if row_count == 0:
                    flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                    row_count = 1
                elif row_count == 1:
                    flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                    row_count = 0
            flex_s = flex_s + [n] + [n+1] + [n]
    
            
        balance = []
        for item in set(flex_s):
            balance.append(flex_s.count(item))
        #print(balance)
    
        return flex_s
    
    ### if 2**(n+1) < m <= 3*(2**n) (Case II)
    if 2**(n+1) < m <= 3*(2**n):
        v = 3*(2**n)-m
        intervals = [np.floor(m/(n+2)) + np.floor(v/3) -2, np.floor(m/(n+2)) + np.floor(v/3) +2]
    
        ## Possible l's and v's:
        l_options = dict()
    
        ## l is chosen from intervals
        for l in list(range(int(intervals[0]), int(intervals[1]) + 1)):
            l_options[l] = computing_ab_i_odd(s_2 = s_2, l = l, v = v)
            
            if l_options[l][1] != {}:
                v = l_options[l][0]
                if v > 1:
                    el = int(np.floor((v+1)/3))
                    t = s_2[:el]
                    a_i = l_options[l][1]
                    verdict = []
                    for item in a_i.keys():
                        if a_i[item] != t.count(item):
                            verdict.append('No')
                        else:
                            verdict.append('True')
                    if a_i == {}:
                        verdict.append('No')
                        
                    if 'No' not in verdict:
                        u = []
                        t = []
                        new_counts = dict()
                        for i in range(0, n):
                            new_counts[i] = 0
                        for i in s_2:
                            if new_counts[i] >= a_values[i]:
                                u[-1].append(i)
                            else:
                                t.append([i])
                                u.append([])
                            new_counts[i] += 1
                        
                        flex_s = []
                        if l%2 == 0:
                            row_count = 0
                            for i in range(l-1, -1, -1):
                                if row_count == 0:
                                    flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                                    row_count = 1
                                elif row_count == 1:
                                    flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                                    row_count = 0
                                    flex_s = flex_s + [n+1] + [n] + [n+1]
    
                        elif l%2 != 0:
                            row_count = 0
                            for i in range(l-1, -1, -1):
                                if row_count == 0:
                                    flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                                    row_count = 1
                                elif row_count == 1:
                                    flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                                    row_count = 0
                                    flex_s = flex_s + [n] + [n+1] + [n]
                        flex_s = flex_s[:-v] 
                        balance = []
                        for item in set(flex_s):
                            balance.append(flex_s.count(item))
                        #print(balance)
                        return flex_s
                    
                    elif 'No' in verdict:
                        new_options = dict()
                        new_s = s_2[1:] + [s_2[0]]
                        new_options[l] = computing_ab_i_odd(s_2 = new_s, l = l, v = v)
                        v = new_options[l][0]
                        if v > 1:
                            el = int(np.floor((v+1)/3))
                            t = new_s[:el]
                            a_i = new_options[l][1]
                            verdict = []
                            for item in a_i.keys():
                                if a_i[item] != t.count(item):
                                    verdict.append('No')
                                else:
                                    verdict.append('True')
                            if a_i == {}:
                                verdict.append('No')
                        
                            if 'No' not in verdict:
                                
                                u = []
                                t = []
                                new_counts = dict()
                                for i in range(0, n):
                                    new_counts[i] = 0
                                for i in s_2:
                                    if new_counts[i] >= a_values[i]:
                                        u[-1].append(i)
                                    else:
                                        t.append([i])
                                        u.append([])
                                    new_counts[i] += 1
                                
                                flex_s = []
                                if l%2 == 0:
                                    row_count = 0
                                    for i in range(l-1, -1, -1):
                                        if row_count == 0:
                                            flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                                            row_count = 1
                                        elif row_count == 1:
                                            flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                                            row_count = 0
                                            flex_s = flex_s + [n+1] + [n] + [n+1]
    
                                elif l%2 != 0:
                                    row_count = 0
                                    for i in range(l-1, -1, -1):
                                        if row_count == 0:
                                            flex_s = flex_s + list(reversed(u[i])) + [n+1] + u[i] + [n] + list(reversed(u[i])) + t[i]
                                            row_count = 1
                                        elif row_count == 1:
                                            flex_s = flex_s + list(reversed(u[i])) + [n] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
                                            row_count = 0
                                            flex_s = flex_s + [n] + [n+1] + [n]
                                flex_s = flex_s[:-v]
                                balance = []
                                for item in set(flex_s):
                                    balance.append(flex_s.count(item))
                                #print(balance)
                                return flex_s