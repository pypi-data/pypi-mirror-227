def n_bgc(n):
    
    """
    Takes n and returns n-bit BGC.
    Is dependent on function(bgc).
    Used in function(m_length_BGC).
    """
    
    if n == 2:
        s_2 = [1, 2, 1, 2]
        counter = 2
    elif n == 3:
        s_2 = [1, 2, 3, 2, 1, 2, 3, 2]
        counter = 3
    elif n >3 and n%2 == 0:
        counter = 4
        s_2 = bgc(n=counter)
    elif n > 3 and n%2 != 0:
        counter = 5
        s_2 = bgc(n=counter)
    while counter != n:
        counter = counter + 2
        s_2 = bgc(n=counter, s = s_2)
        
    balance = []
    for item in set(s_2):
        balance.append(s_2.count(item))
        
    #print(balance)
    return s_2