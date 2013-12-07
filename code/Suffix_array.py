from operator import itemgetter, attrgetter
import sys
import time
import Sample as smp


def suffix_array(T):
    
    B0 = xrange(0, len(T)+1, 3)
    
    B1 = xrange(1, len(T)+1, 3) 
    R1 = [ smp.Sample(T, i, len(T)) for i in B1 ]
    print R1
    B2 = xrange(2, len(T)+1, 3)
    R2 = [ smp.Sample(T, i, len(T)) for i in B2 ]
    print R2
    R12 = R1 + R2
    print "R12=", R12

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
    print "T_new", T_new

    print len(T_new),"-",rank

    if (rank < len(R12)):
        R_SA = suffix_array(T_new)
        print "generated after rec", R_SA
    else:
        print "asdasd", s_R
        R_SA = [len(R12)] + [i.p for i in s_R] 
        print "when no recur:", R_SA

    r_Si = [None] * (len(T) + 3)
    r_Si[-2] = r_Si[-1] = 0
     

    
    print R_SA
    s_R = [R12[i] for i in R_SA[1:]] 

    for i in xrange(len(s_R)):
        #if s_R[i] < len(R12):
        r_Si[s_R[i].i] = i
        print "\t\t\t",s_R[i] 
    print R12


    print "s_R", s_R
    print "r_Si:", r_Si

    print R_SA
    print T
    R0 = [ smp.Nonsample(T, i, r_Si[i+1]) for i in B0 ]
    print R0
    ns_R = built_in_sort(R0,'pr')    
    print ns_R
    print "-------------------------"
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
        print b.i
        if b.i % 3 == 2:
            print T[a.i], T[a.i+1], r_Si[a.i+2]
            print b.i
            print T[b.i+1]
            print r_Si[b.i+2]

            ret = cmp_int(T[a.i], T[a.i+1], r_Si[a.i+2], T[b.i], T[b.i+1], r_Si[b.i+2])
        else:
            ##print T[a[1]], rank_Si[a[1]+1]
            ##print T[idx[1]], rank_Si[idx[1]+1]
            ret = cmp_int(T[a.i], r_Si[a.i+1], 0,
                          T[b.i], r_Si[b.i+1], 0)
        print "RET=", ret
        if ret == 1: 
            SA.append(b.i)
            b = None
        else:
            SA.append(a.i)
            a = None
    print SA
    return SA

def cmp_int(b0_0, b0_1, b0_2, b2_0, b2_1, b2_2):
    """
    The function return 1 if B0 > B2 and -1 if B0 < B2
    """
    print (b0_0, b0_1, b0_2), (b2_0, b2_1, b2_2)
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

    """

    #Enables 0 as unique terminating character by starting ranks at 1
    rank_dict = {}
    
    
    

    for triplet in sorted_suffixes_R:
        rank_dict[triplet.index] = triplet.rank
    
    
    #print "rank dict", rank_dict

    #recursive call
    resolved_ranks = 0
    recovered_ranks_list = []
    #new_rank_list = 
    #R_prime_suffix_array = []
    
       

        
    if (rank < len(R)):  #we had repeats of characters of R, make a recursive call to sort
        #print "fuck"
        precompute_rank(sorted_suffixes_R, rank_dict)

        
    




        R_prime_suffix_array = ksa(R_prime, rn)
        
    else:
        ##print "yahoo"
        #directly form suffix array
        R_prime_suffix_array = [len(R)] + [suffix.rpos for suffix in sorted_suffixes_R] 
        print "R_prime_suffix_array:", R_prime_suffix_array
    

    rank_Si = [None] * (length + 3) #why plus 3? -> additiionally define rank(S_(n+1) = rank(S_(n+2)) = 0
    rank_Si[-2] = rank_Si[-1] = 0
    #print "rank_Si:", rank_Si 

    #build rank(S_i) lookup array
    for i, SAi in enumerate(R_prime_suffix_array):
        ##print i, "--", SAi
        if SAi < len(R): #ignore the index pointing to the terminating character of R_prime
            rank_Si[R[SAi].index] = i
    #print "rank_Si", rank_Si
    sorted_suffixes_R = [R[i] for i in R_prime_suffix_array[1:]] 

    ##print "after sort R", R
    print "sorted_suffixes_R", sorted_suffixes_R

    #karkkainen-sanders step 2: sort nonsample suffixes
    nonsample_suffix_pairs = [NonsamplePair(T, idx, rank_Si) for idx in B_0]
    ##print "nonsample_suffix_pairs", nonsample_suffix_pairs
    sorted_nonsample_suffix_pairs = sorted(nonsample_suffix_pairs, key=lambda p: p.pair)    
    print sorted_nonsample_suffix_pairs
    #karkkainen-sanders step 3: merge
    cur_Sc, cur_Sb0 = 0, 0
    objs_SA = []
    
    def getT(idx):
        if idx < len(T):
            return T[idx]
        return 0
    while cur_Sc < len(sorted_suffixes_R) and cur_Sb0 < len(sorted_nonsample_suffix_pairs):
        i = sorted_suffixes_R[cur_Sc].index
        j = sorted_nonsample_suffix_pairs[cur_Sb0].index
        if i % 3 == 1: #i in B_1
            #S_i =< S_j iff (T[i], rank(S_t+1) =< (t_j, rank(s_j+1))
            if (getT(i), rank_Si[i+1]) < (getT(j), rank_Si[j+1]):
                objs_SA.append(sorted_suffixes_R[cur_Sc])
                cur_Sc += 1
            else:
                objs_SA.append(sorted_nonsample_suffix_pairs[cur_Sb0])
                cur_Sb0 += 1
        else: #i in B_2
            if (getT(i), getT(i+1),  rank_Si[i+2]) < (getT(j), getT(j+1), rank_Si[j+2]):
                objs_SA.append(sorted_suffixes_R[cur_Sc])
                cur_Sc += 1
            else:
                objs_SA.append(sorted_nonsample_suffix_pairs[cur_Sb0])
                cur_Sb0 += 1
    
    objs_SA += sorted_suffixes_R[cur_Sc:]
    objs_SA += sorted_nonsample_suffix_pairs[cur_Sb0:]
    SA = [suffix_object.index for suffix_object in objs_SA]
    print "------back from recursion---------"
    print SA
    return SA
        
    



def simulate_sequence(length):
    dna = ['A', 'C', 'G', 'T']
    sequence = ''
    for i in range(length):
        sequence += random.choice(dna)
    return sequence

def read_fasta():
    snippet = ""
    for line in fileinput.input():
        snippet += line.strip()
    return snippet


rec_num = []
"""

def built_in_sort(my_list, my_attr):    
    return sorted(my_list, key=attrgetter(my_attr))

def radix_sort(my_list, n, max_len): 
    
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
    
    #if len(sys.argv) != 2:
    #    inputerr()
    #T = sys.argv[1].strip()
    #T = "yabbadabbado"
    #T = "mississippi"
    #T = "ababababababab"
    T = ['A' for i in xrange(10000)] 
    #print T
    #if not T.isalnum():
    #    inputerr()
    #T = ""
    #T = read_fasta()
    #T = simulate_sequence(500)
    myT = []
    for chr in T:
        myT.append(ord(chr))
    ##print myT
    #myT = [5,1,2,2,1,3,1,2,2,1,3,4]
    print "File was loaded.\n Started processing...\n"
    start_time = time.time()
    sa = suffix_array(myT)
    ##print T
    ##print ["{0:^2}".format(chr) for chr in T]
    ##print ["{0:^2}".format(i) for i, chr in enumerate(T)]
    print time.time() - start_time, "seconds"
    

    print sa
"""
def precompute_rank(sorted_suffixes_R, rank_dict):
    #print sorted_suffixes_R
    count = 1
    recovered_ranks_list = []
    same_set = 0
    diff_set = 0
    next_to = 0
    for i in xrange(len(sorted_suffixes_R)-1, 0, -1):
        #print sorted_suffixes_R[i]
        if sorted_suffixes_R[i-1].triple == sorted_suffixes_R[i].triple:
            #resolved_ranks += 2
            #print "Collision detected on ", sorted_suffixes_R[i-1]," and ", sorted_suffixes_R[i] 

            if sorted_suffixes_R[i-1].index + 3 == sorted_suffixes_R[i].index:
                next_to += 1
                #print sorted_suffixes_R[i-1],"-",sorted_suffixes_R[i]
                #print sorted_suffixes_R[i],'-',rank_dict[sorted_suffixes_R[i].index+3],"-",sorted_suffixes_R[i+1]
                print "--"
                #print sorted_suffixes_R[i-1],'-',rank_dict[sorted_suffixes_R[i-1].index+3],"-",sorted_suffixes_R[i]
                print "=="
            if sorted_suffixes_R[i-1].index % 3 == 1 and sorted_suffixes_R[i].index % 3 == 1:
                same_set += 1
            elif sorted_suffixes_R[i-1].index % 3 == 2 and sorted_suffixes_R[i].index % 3 == 2:
                same_set += 1
            else:
                diff_set += 1
    print "same_set collision", same_set
    print "next_to", next_to
    print "diff_set collision", diff_set
    """
"""
            if sorted_suffixes_R[i].index in rank_dict:
                print sorted_suffixes_R[i],'-',rank_dict[sorted_suffixes_R[i].index+3]
                print sorted_suffixes_R[i-1],'-',rank_dict[sorted_suffixes_R[i-1].index+3]
                if rank_dict[sorted_suffixes_R[i].index+3] > rank_dict[sorted_suffixes_R[i-1].index+3]:


                    recovered_ranks_list.append(sorted_suffixes_R[i-1].index)
                    #recovered_ranks_list.append(sorted_suffixes_R[i].index)
                    
                    rank_dict[sorted_suffixes_R[i-1].index] = count
                    count += 1

                    #if sorted_suffixes_R[i+1] in sorted_suffixes_R:
                    ##print sorted_suffixes_R[i-1],",",sorted_suffixes_R[i]
                    continue
                elif rank_dict[sorted_suffixes_R[i].index+3] < rank_dict[sorted_suffixes_R[i-1].index+3]:

                    #recovered_ranks_list.append(sorted_suffixes_R[i-1].index)
                    recovered_ranks_list.append(sorted_suffixes_R[i].index)
                    ##print sorted_suffixes_R[i],",",sorted_suffixes_R[i-1]
                    rank_dict[sorted_suffixes_R[i].index] = count
                    count += 1
                    #continue
                else:
                    #print "equality: can't resolve ranking"
                    resolved_ranks -= 2
            else:
                pass
                #print "no rank for ", sorted_suffixes_R[i+3].index
        #print 'Index[',sorted_suffixes_R[i].index,'] - ',sorted_suffixes_R[i].triple
        print recovered_ranks_list[::-1]
        
        if sorted_suffixes_R[i].index not in recovered_ranks_list:
            recovered_ranks_list.append(sorted_suffixes_R[i].index)
    recovered_ranks_list.append(sorted_suffixes_R[0].index)
    #if len(recovered_ranks_list) == len(R): 
    #print "resolved ranks for ",resolved_ranks," triplets"
    print recovered_ranks_list[::-1]
    #print "****************************"
    if len(recovered_ranks_list) == len(R):
        pass
        print "it is possible to avoid 1 level of recursion"
    #print len(R) - len(recovered_ranks_list)
    #print rank_dict
    #print "****************************"
"""        
"""
    

    #pass
def precompute_set(sorted_suffixes_R, rank_dict):
    count = 1
    resolved_ranks = 0
    recovered_ranks_list = []
    #print "***try to restore results***"
    ptr_a = None
    #print rank_dict
    #print R
    while True:
        #print sorted_suffixes_R
        if ptr_a is None:
            ptr_a = sorted_suffixes_R.pop() 
        try:
            #print "ptr_a",ptr_a
            #print "last idx",sorted_suffixes_R[-1]
            #print "count =",count
            if ptr_a.triple == sorted_suffixes_R[-1].triple:
                print "rule 2: Comparing",ptr_a, " and ", sorted_suffixes_R[-1]

                print "ptr_a index", rank_dict[ptr_a.index+3]
                print "sorted_suffixes_R[-1] index", rank_dict[sorted_suffixes_R[-1].index+3]

                if rank_dict[ptr_a.index+3] > rank_dict[sorted_suffixes_R[-1].index+3]:
                    recovered_ranks_list.append(sorted_suffixes_R.pop())

                elif rank_dict[ptr_a.index+3] < rank_dict[sorted_suffixes_R[-1].index+3]:
                    recovered_ranks_list.append(ptr_a)
                    ptr_a = None
                else:
                    print "tie" 
                    break               
            else:
                print "rule 1: Comparing",ptr_a, " and ", sorted_suffixes_R[-1]
                recovered_ranks_list.append(ptr_a)
                ptr_a = None
        except:
            recovered_ranks_list.append(ptr_a)
            break
    print recovered_ranks_list



        


    
        if sorted_suffixes_R[i-1].triple == sorted_suffixes_R[i].triple:
            #resolved_ranks += 2
            print "Collision detected on ", sorted_suffixes_R[i-1]," and ", sorted_suffixes_R[i] 
            if sorted_suffixes_R[i].index in rank_dict:
                ##print sorted_suffixes_R[i].triple,'-',rank_dict[sorted_suffixes_R[i].index+3]
                ##print sorted_suffixes_R[i-1].triple,'-',rank_dict[sorted_suffixes_R[i-1].index+3]
                if rank_dict[sorted_suffixes_R[i].index+3] > rank_dict[sorted_suffixes_R[i-1].index+3]:
                    recovered_ranks_list.append(sorted_suffixes_R[i-1].index)
                    #recovered_ranks_list.append(sorted_suffixes_R[i].index)
                    
                    rank_dict[sorted_suffixes_R[i-1].index] = count
                    count += 1

                    #if sorted_suffixes_R[i+1] in sorted_suffixes_R:
                    ##print sorted_suffixes_R[i-1],",",sorted_suffixes_R[i]
                    continue
                elif rank_dict[sorted_suffixes_R[i].index+3] < rank_dict[sorted_suffixes_R[i-1].index+3]:
                    #recovered_ranks_list.append(sorted_suffixes_R[i-1].index)
                    recovered_ranks_list.append(sorted_suffixes_R[i].index)
                    ##print sorted_suffixes_R[i],",",sorted_suffixes_R[i-1]
                    rank_dict[sorted_suffixes_R[i].index] = count
                    count += 1
                    #continue
                else:
                    #print "equality: can't resolve ranking"
                    resolved_ranks -= 2
            else:
                pass
                #print "no rank for ", sorted_suffixes_R[i+3].index
        #print 'Index[',sorted_suffixes_R[i].index,'] - ',sorted_suffixes_R[i].triple
        print recovered_ranks_list[::-1]
        
        if sorted_suffixes_R[i].index not in recovered_ranks_list:
            recovered_ranks_list.append(sorted_suffixes_R[i].index)
    recovered_ranks_list.append(sorted_suffixes_R[0].index)
    #if len(recovered_ranks_list) == len(R): 
    #print "resolved ranks for ",resolved_ranks," triplets"
    print recovered_ranks_list[::-1]
    #print "****************************"
    if len(recovered_ranks_list) == len(R):
        pass
        #print "it is possible to avoid 1 level of recursion"
    #print len(R) - len(recovered_ranks_list)
    #print rank_dict
    #print "****************************"
"""
    


    
if __name__ == '__main__':
    main()
