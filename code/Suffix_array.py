from operator import itemgetter, attrgetter
import sys
import time
import Sample as smp
import Utils as ut


def suffix_array(T):
    """
    TO-DO:
    """
    B0 = xrange(0, len(T)+1, 3)
    
    B1 = xrange(1, len(T)+1, 3) 
    R1 = [ smp.Sample(T, i, len(T)) for i in B1 ]
    
    B2 = xrange(2, len(T)+1, 3)
    R2 = [ smp.Sample(T, i, len(T)) for i in B2 ]
    
    R12 = R1 + R2
    

    for i, ch in enumerate(R12):
        ch.p = i
        
    s_R = built_in_sort(R12, 't')
    
    def rank_suffixes(suffixes, rank=1):
        for i, suffix in enumerate(suffixes):
            if i > 0 and suffix.t != suffixes[i-1].t: 
                rank += 1
            suffix.r = rank
        return rank
    rank = rank_suffixes(s_R)
    
    R_prime = [suffix.r for suffix in R12]

    T_new = [ i.r for i in R12 ]
    
    if (rank < len(R12)):
        R_SA = suffix_array(T_new)
    else:
        R_SA = [len(R12)] + [i.p for i in s_R] 

    r_Si = [None] * (len(T) + 3)
    r_Si[-2] = r_Si[-1] = 0
     
    s_R = [R12[i] for i in R_SA[1:]] 

    for i, SAi in enumerate(R_SA):
        if SAi < len(R12): 
            r_Si[R12[SAi].i] = i

    R0 = [ smp.Nonsample(T, i, r_Si[i+1]) for i in B0 ]
    ns_R = built_in_sort(R0,'pr')    
    
    T.append(0)
    T.append(0)
    T.append(0)
    
    b, a = None, None
    SA = []

    while(1):
        if b == None:
            if s_R == []:
                SA.extend([i.i for i in ns_R])
                if a != None: SA.append(a.i) 
                return SA
            else:
                b = s_R.pop(0)
        if a == None:
            
            if ns_R == []:
                SA.extend(i.i for i in s_R)
                if b != None: SA.append(b.i) 
                return SA
            else:
                a = ns_R.pop(0)
        if b.i % 3 == 2:
            ret = cmp_int(T[a.i], T[a.i+1], r_Si[a.i+2], T[b.i], T[b.i+1], r_Si[b.i+2])
        else:
            ret = cmp_int(T[a.i], r_Si[a.i+1], 0,
                          T[b.i], r_Si[b.i+1], 0)
        if ret == 1: 
            SA.append(b.i)
            b = None
        else:
            SA.append(a.i)
            a = None
    return SA

def cmp_int(b0_0, b0_1, b0_2, b2_0, b2_1, b2_2):
    """
    The function returns 1 if B0 > B2 and -1 if B0 < B2
    """
    if b0_0 > b2_0:
        return 1
    elif b0_0 < b2_0:
        return -1
    else:
        if b0_1 > b2_1:
            return 1
        elif b0_1 < b2_1:
            return -1
        else:
            if b0_2 > b2_2:
                return 1
            elif b0_2 < b2_2:
                return -1

def built_in_sort(my_list, my_attr): 
    """
    TO-DO:
    """   
    return sorted(my_list, key=attrgetter(my_attr))

def radix_sort(my_list, n, max_len): 
    """
    TO-DO:
    """
    for x in xrange(max_len-1, -1, -1):
        bins = [[] for i in xrange(n)]
        for y in my_list:
            bins[y[x]%n].append(y)        
        my_list=[]
        for section in bins:
            my_list.extend(section)
    return my_list


def main():
    
    #T = "yabbadabadoo"

    T = ut.read_fasta()

    #print "Started processing...\n"
    start_time = time.time()
    suffix_arr = suffix_array(ut.convert_to_int(T))
    print time.time() - start_time, "seconds"
    print suffix_arr

    
if __name__ == '__main__':
    main()
