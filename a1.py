def arc(p,i,l): 
    # determines the allowed row and columns(hence named arc) for a specified variable in a kmap specified by ith term in list term(here l)
    # Arguments:
    # p: number of row or columns to choose the allowed ones to choose from.
    # i: used to specify which variable from list l by specifying it's index i is specifying the allowed rows and columns.
    # l: the list which contains the variables of kmap, like term argument in is_legal_region.
    # Return:
    # list : list which contains the allowed rows and columns for a particular variable
    list =[]
    if p==2:
        if l[i] ==None:
            list.append(0)
            list.append(1)
        elif l[i]:
            list.append(1)
        else:
            list.append(0)
    elif p ==4:
        if l[i] ==None:
            list.extend([0,1,2,3])
        elif i%2 : # used to specify the allowed row and columns for second variables which are stored at odd positions, oddno.%2 ==1 which is interpreted as True by python.
            if l[i]:
                list.extend([1,2])
            else:
                list.extend([0,3])
        else :
            if l[i]:
                list.extend([2,3])
            else:
                list.extend([0,1])
    return list

def arcintersection(i1,i2,l):
    # returns the allowed rows and columns in case 2 variables are needed to determine it.
    # Arguments:
    # i1: index for the first variable
    # i2: index for the second variable
    # l: the list which stores the variables used to determine allowed or columns
    # Return:
    # lst3: list which is intersection of lst1 and lst2 containing allowed rows and columns for variable indexed i1 and i2 respectively.
    lst1 = arc(4,i1,l)
    lst2 = arc(4,i2,l)
    lst3 = [value for value in lst1 if value in lst2] # list comprehension for intersection
    return lst3

def tlbr(dict,term):
    # finds and returns the top left and bottom right corner which specify a region when region and variables o it are specified
    # Arguments:
    # dict: dictionary which specifies the needed region
    # term: list defining a region for the kmap
    # Return:
    # tuple with tl(coordinate of top left corner) and br(coordinate for bottom right corner) and legality as it's elements.
    l = list(dict.keys())
    tl = l[0] # works only when keys are listed in an arranged manner
    br = l[-1] # works only when keys are listed in an arranged manner
    tr = ([i for i in l if (i[0]==tl[0])])[-1] # tr(top right coordinate) using list comprehension to get the top row and consecutively it's last member.
    bl = ([i for i in l if (i[0]==br[0])])[0] # br(bottom right coordinate) using list comprehension to get the bottom row and consecutively it's first member.
    n = len(term)
    if n==3:
        if term[0]== None and term[1] ==0: #statement to check left right wrapping
            tl,br = tr,bl 
    elif n==4:
        s1 = term[0]== None and term[1] ==0 # statement to check left right wrapping
        s2 = term[2]== None and term[3] ==0 # statement to check top bottom wrapping
        if s1 and s2: 
            tl,br = br,tl
        elif s1:
            tl,br = tr,bl
        elif s2:
            tl,br = bl,tr
    return (tl,br,legality(dict))
    
def legality(region):
    # function to find legality of given region that is given as a dictionary by returning a boolean answer specifying the same.
    return 0 not in region.values()

def is_legal_region(kmap_function,term):
    # determines whether the specified region is LEGAL for the K-map function
    # Arguments:
    # kmap_function: n * m list containing the kmap function
    # for 2-input kmap this will 2*2
    # 3-input kmap this will 2*4
    # 4-input kmap this will 4*4
    #term: a list of size k, where k is the number of inputs in function (2,3 or 4)
    # (term[i] = 0 or 1 or None, corresponding to the i-th variable)
    # Return:
    # three-tuple: (top-left coordinate, bottom right coordinate, boolean value)
    # each coordinate is represented as a 2-tuple
    n = len(term)  # used for finding the type of kmap
    reg = {} # dictionary for specifying the region
    r = [] # list specifying allowed rows
    c = [] # list specifying allowed columns
    if n ==2:
        c.extend(arc(2,0,term))
        r.extend(arc(2,1,term))
        i = 0
        while i<2:
            if i in r:
                j= 0
                while j<2:
                    if j in c:
                        reg[(i,j)] = kmap_function[i][j]
                    j+=1
            i+=1
    elif n==3:
        c.extend(arcintersection(0,1,term))
        r.extend(arc(2,2,term))
        i = 0
        while i<2:
            if i in r:
                j= 0
                while j<4:
                    if j in c:
                        reg[(i,j)] = kmap_function[i][j]
                    j+=1
            i+=1
    else:
        c.extend(arcintersection(0,1,term))
        r.extend(arcintersection(2,3,term))
        i = 0
        while i<4:
            if i in r:
                j= 0
                while j<4:
                    if j in c:
                        reg[(i,j)] = kmap_function[i][j]
                    j+=1
            i+=1
    return tlbr(reg,term)


