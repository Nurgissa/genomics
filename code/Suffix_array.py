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
    #print R1
    B2 = xrange(2, len(T)+1, 3)
    R2 = [ smp.Sample(T, i, len(T)) for i in B2 ]
    #print R2
    R12 = R1 + R2
    #print "R12=", R12

    for i in xrange(0, len(R12)):
        R12[i].p = i
        #print R12[i], '-', i

    #for i, r_char in enumerate(R12):
    #    r_char.p = i
    #    print "r_char", r_char, "-", i
    s_R = built_in_sort(R12, 't')
    #print "sorted_suffixes R", s_R
    rank = 0
    for i in xrange(0, len(s_R)):
        if s_R[i].t != s_R[i-1].t:
            rank += 1
        s_R[i].r = rank
        #print s_R[i]

    T_new = [ i.r for i in R12 ]
    #print "T_new", T_new

    #print len(T_new),"-",rank

    if (rank < len(R12)):
        R_SA = suffix_array(T_new)
        #print "generated after rec", R_SA
    else:
        #print "asdasd", s_R
        R_SA = [len(R12)] + [i.p for i in s_R] 
        #print "when no recur:", R_SA

    r_Si = [None] * (len(T) + 3)
    r_Si[-2] = r_Si[-1] = 0
     

    
    #print R_SA
    s_R = [R12[i] for i in R_SA[1:]] 

    for i in xrange(len(s_R)):
        #if s_R[i] < len(R12):
        r_Si[s_R[i].i] = i
        #print "\t\t\t",s_R[i] 
    #print R12


    #print "s_R", s_R
    #print "r_Si:", r_Si

    #print R_SA
    #print T
    R0 = [ smp.Nonsample(T, i, r_Si[i+1]) for i in B0 ]
    #print R0
    ns_R = built_in_sort(R0,'pr')    
    #print ns_R
    #print "-------------------------"
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
            #print Sorted_R0
            if ns_R == []:
                SA.extend(i.i for i in s_R)
                if b != None: SA.append(b.i) 
                return SA
            else:
                a = ns_R.pop(0)
        #print b.i
        if b.i % 3 == 2:
            #print T[a.i], T[a.i+1], r_Si[a.i+2]
            #print b.i
            #print T[b.i+1]
            #print r_Si[b.i+2]

            ret = cmp_int(T[a.i], T[a.i+1], r_Si[a.i+2], T[b.i], T[b.i+1], r_Si[b.i+2])
        else:
            ##print T[a[1]], rank_Si[a[1]+1]
            ##print T[idx[1]], rank_Si[idx[1]+1]
            ret = cmp_int(T[a.i], r_Si[a.i+1], 0,
                          T[b.i], r_Si[b.i+1], 0)
        #print "RET=", ret
        if ret == 1: 
            SA.append(b.i)
            b = None
        else:
            SA.append(a.i)
            a = None
    #print SA
    return SA

def cmp_int(b0_0, b0_1, b0_2, b2_0, b2_1, b2_2):
    """
    The function returns 1 if B0 > B2 and -1 if B0 < B2
    """
    #print (b0_0, b0_1, b0_2), (b2_0, b2_1, b2_2)
    if b0_0 > b2_0:
        ##print b0_0,"-",b2_0
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
            #print y[x]%n
            bins[y[x]%n].append(y)        
        my_list=[]
        for section in bins:
            my_list.extend(section)
    return my_list


def main():
    #T = ['A' for i in xrange(1000)]
    #T = "yabbadabadoo"
    
    T = ut.read_fasta()
    print "Started processing...\n"
    start_time = time.time()
    suff_array = suffix_array(ut.convert_to_int(T))
    print time.time() - start_time, "seconds"
    print suff_array

    
if __name__ == '__main__':
    main()
