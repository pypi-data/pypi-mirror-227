def bgc(n, s = None):
    
    """
    Balanced Gray codes construction.
    Takes a transition sequence for a balanced Gray code with n-2 bits,
    returns a transition sequence of n-bit BGC.
    Is dependent on function(find_q_r).
    Used in function(n_bgc)
    """

    ### Calculation of q, r
    q, r = find_q_r(n=n)

    ### Partition p_i
    p_i = []

    if q%2 == 0:
        q_def = int(r/2)
        if q_def != 0:
            Q = list(range(1, n-1))[-q_def:]
        else:
            Q = []
    
        for i in range(n):
            if i in Q:
                p_i.append(q+2)
            else:
                p_i.append(q)
    elif q%2 != 0:
        q_def = int((n+r)/2)
        if q_def != 0:
            Q = list(range(1, n-1))[-q_def:]
        else:
            Q = []
    
        for i in range(n):
            if i in Q:
                p_i.append(q+1)
            else:
                p_i.append(q-1)
            
    p_i = sorted(p_i)

    ### Calculation b_i
    if s is None:
        if n == 4:
            s = [1, 2, 1, 2]
        elif n == 5:
            s = [1, 2, 3, 2, 1, 2, 3, 2]
    b_i = []

    for i in range(1, len(set(s))+1):
        if i != s[len(s)-1]:
            b = (4*s.count(i) - p_i[i-1])/2
            b_i.append(int(b))
        else:
            b = (4*(s.count(i) - 1) - p_i[i-1])/2
            b_i.append(int(b))
    l = sum(b_i)

    counts = dict()
    for i in range(len(b_i)):
        counts[i+1] = b_i[i]
    
    s = s[:-1]
    u = []
    t = []
    new_counts = dict()
    for i in range(1, n-1):
        new_counts[i] = 0
    for i in s:
        if new_counts[i] >= counts[i]:
            u[-1].append(i)
        else:
            t.append([i])
            u.append([])
        new_counts[i] += 1
    n = n-2

    s_2 = []

    for t_i, u_i in zip(t, u):
        s_2 = s_2 + t_i + u_i
    s_2 = s_2 + [n+1]

    row_count = 0
    for i in range(len(u)-1, -1, -1):
        if row_count == 0:
            s_2 = s_2 + list(reversed(u[i])) + [n+2] + u[i] + [n+1] + list(reversed(u[i])) + t[i]
            row_count = 1
        else:
            s_2 = s_2 + list(reversed(u[i])) + [n+1] + u[i] + [n+2] + list(reversed(u[i])) + t[i]
            row_count = 0
    if row_count == 0:
        s_2 = s_2 + [n+2] + [n+1] + [n+2]
    elif row_count == 1:
        s_2 = s_2 + [n+1] + [n+2] + [n+1]

    return s_2