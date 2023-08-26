import cvxpy as cp

def find_q_r(n):
    
    """
    Solves an equation: what is an equal for partition for 2**n:
    2**n = n*q + r
    What is n?
    Used in function(bgc).
    """

    q = cp.Variable(integer=True)
    r = cp.Variable(integer=True)

    constraints = [
        2**n == n*q + r,
        r >= 0,
        r <= n-1
    ]

    problem = cp.Problem(cp.Minimize(r), constraints)

    problem.solve()
    
    if problem.status == 'optimal':
        return int(q.value), int(r.value)