import cProfile
import Utils as ut

class Sample():
    def __init__(self, T, idx, length):
        t_i = lambda i: T[i] if i < length else 0
        self._triple = (t_i(idx), t_i(idx + 1), t_i(idx + 2))
        self._index = idx
        self._rank = None
        self._rpos = None

    
    @property
    def triple(self):
        return self._triple

    @property
    def index(self):
        return self._index

    @property
    def rpos(self):
        return self._rpos

    @rpos.setter
    def rpos(self, pos):
        self._rpos = pos
        
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, pos):
        self._rank = pos
    
class Nonsample():
    def __init__(self, T, idx, S_i_ranks):
        self.index = idx
        self.pair = None
        max_index = len(T)
        if idx < max_index:
            self.pair = (T[self.index], S_i_ranks[self.index + 1])
        else:
            self.pair = (0, S_i_ranks[self.index + 1])

def suffix_array(T, rn):
    rn.append(len(rn))
    length = len(T)
    B_0, B_1, B_2 = xrange(0, length+1, 3), xrange(1, length+1, 3), xrange(2, length+1, 3)
    
    R_0 = [ Sample(T, idx, length) for idx in B_0 ]
    R_1 = [ Sample(T, idx, length) for idx in B_1 ]
    R_2 = [ Sample(T, idx, length) for idx in B_2 ]

    R = R_1 + R_2
    
    for i, r_char in enumerate(R):
        r_char.rpos = i
    sorted_suffixes_R = sorted(R, key=lambda suffix_char: suffix_char.triple)
    
    rank_dict = {}
    def rank_suffixes(suffixes, rank=1):
        for i, suffix in enumerate(suffixes):
            if i > 0 and suffix.triple != suffixes[i-1].triple: 
                rank += 1
                rank_dict[suffix.index] = rank
            suffix.rank = rank
        return rank
    rank = rank_suffixes(sorted_suffixes_R)
    
    R_prime = [suffix.rank for suffix in R]
    
    

    for triplet in sorted_suffixes_R:
        rank_dict[triplet.index] = triplet.rank
    
    print len(R_prime),"-",rank
    

    
    resolved_ranks = 0
    recovered_ranks_list = []
          
    if (rank < len(R)): 
        precompute_rank(sorted_suffixes_R, rank_dict)
        R_prime_suffix_array = suffix_array(R_prime, rn)
        
    else:
        R_prime_suffix_array = [len(R)] + [suffix.rpos for suffix in sorted_suffixes_R] 
        
    

    rank_Si = [None] * (length + 3)
    rank_Si[-2] = rank_Si[-1] = 0
    

    
    for i, SAi in enumerate(R_prime_suffix_array):    
        if SAi < len(R):
            rank_Si[R[SAi].index] = i
    
    sorted_suffixes_R = [R[i] for i in R_prime_suffix_array[1:]] 

    nonsample_suffix_pairs = [Nonsample(T, idx, rank_Si) for idx in B_0]
    
    sorted_nonsample_suffix_pairs = sorted(nonsample_suffix_pairs, key=lambda p: p.pair)    
    
    cur_Sc, cur_Sb0 = 0, 0
    objs_SA = []
    
    def getT(idx):
        if idx < len(T):
            return T[idx]
        return 0
    while cur_Sc < len(sorted_suffixes_R) and cur_Sb0 < len(sorted_nonsample_suffix_pairs):
        i = sorted_suffixes_R[cur_Sc].index
        j = sorted_nonsample_suffix_pairs[cur_Sb0].index
        if i % 3 == 1: 

            if (getT(i), rank_Si[i+1]) < (getT(j), rank_Si[j+1]):
                objs_SA.append(sorted_suffixes_R[cur_Sc])
                cur_Sc += 1
            else:
                objs_SA.append(sorted_nonsample_suffix_pairs[cur_Sb0])
                cur_Sb0 += 1
        else:
            if (getT(i), getT(i+1),  rank_Si[i+2]) < (getT(j), getT(j+1), rank_Si[j+2]):
                objs_SA.append(sorted_suffixes_R[cur_Sc])
                cur_Sc += 1
            else:
                objs_SA.append(sorted_nonsample_suffix_pairs[cur_Sb0])
                cur_Sb0 += 1
    
    objs_SA += sorted_suffixes_R[cur_Sc:]
    objs_SA += sorted_nonsample_suffix_pairs[cur_Sb0:]
    SA = [suffix_object.index for suffix_object in objs_SA]
    return SA
        
    

import sys
import time
import fileinput



def read_fasta():
    snippet = ""
    for line in fileinput.input():
        snippet += line.strip()
    return snippet


rec_num = []
def main():
    
    T = ""

    T = read_fasta()
    print "File loaded..."
    start_time = time.time()
    sa = suffix_array(ut.convert_to_int(T), rec_num)
    print time.time() - start_time, "seconds"
    print len(rec_num)
    

def precompute_rank(sorted_suffixes_R, rank_dict):
    count = 1
    recovered_ranks_list = []
    same_set = 0
    diff_set = 0
    next_to = 0
    for i in xrange(len(sorted_suffixes_R)-1, 0, -1):
        if sorted_suffixes_R[i-1].triple == sorted_suffixes_R[i].triple:
            if sorted_suffixes_R[i-1].index + 3 == sorted_suffixes_R[i].index:
                next_to += 1
            if sorted_suffixes_R[i-1].index % 3 == 1 and sorted_suffixes_R[i].index % 3 == 1:
                same_set += 1
            elif sorted_suffixes_R[i-1].index % 3 == 2 and sorted_suffixes_R[i].index % 3 == 2:
                same_set += 1
            else:
                diff_set += 1
    print "same_set collision", same_set
    print "next_to", next_to
    print "diff_set collision", diff_set
    if next_to == 0:
        pass
        

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
