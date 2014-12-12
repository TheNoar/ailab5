## Assignment 5

import getopt, math, time, sys
   
def robotparse(fd):
    states = set()
    observ = set()
    start_prob = {}
    trans_prob = {}
    emiss_prob = {}
    start_count = 12.0
    trans_count = {}
    emiss_count = {}
    info = []
    last = None
    
    for line in fd:
        line = line.rstrip('\n')
        info = line.split(' ')
        if info[0] == '.':
            last = None
            continue
        elif info[0] == '..':
            break
        states.add(info[0])
        observ.add(info[1])
        try:
            start_count += 1.0
            start_prob[info[0]] += 1.0
        except KeyError:
            start_prob[info[0]] = 2.0
        
        try:
            emiss_count[info[0]] += 1.0
            emiss_prob[info[0]][info[1]] += 1.0
        except KeyError:
            try:
                emiss_prob[info[0]][info[1]] = 2.0
            except KeyError:
                emiss_count[info[0]] = 5.0
                emiss_prob[info[0]] = {info[1]: 2.0}
        
        if last != None:
            try:
                trans_count[last] += 1.0
                trans_prob[last][info[0]] += 1.0
            except KeyError:
                try:
                    trans_prob[last][info[0]] = 2.0
                except KeyError:
                    trans_count[last] = 13.0
                    trans_prob[last] = {info[0]: 2.0}
            last = info[0]
        else:
            last = info[0]

    for key in start_prob:
        start_prob[key] = start_prob[key]/start_count

    for key in emiss_prob:
        for ob in observ:
            try:
                emiss_prob[key][ob] = emiss_prob[key][ob]/emiss_count[key]
            except KeyError:
                emiss_prob[key][ob] = 1.0/emiss_count[key]
    
    for key in trans_prob:
        for state in states:
            try:
                trans_prob[key][state] = trans_prob[key][state]/trans_count[key]
            except KeyError:
                trans_prob[key][state] = 1.0/trans_count[key] 
    obs = []
    paths = []
    temp1 = []
    temp2 = []
    for line in fd:
        line = line.rstrip('\n').split()
        if line[0] == '.':
            obs.append(list(temp1))
            paths.append(list(temp2))
            temp1 = []
            temp2 = []
            continue
        temp1.append(line[1])
        temp2.append(line[0])

    return states, obs, start_prob, trans_prob, emiss_prob, paths  

def typoparse(fd):
    states = set()
    observ = set()
    start_prob = {}
    trans_prob = {}
    emiss_prob = {}
    
    start_count = 26.0
    trans_count = {}
    emiss_count = {}
    
    info = []
    last = None
    
    for line in fd:
        line = line.rstrip('\n')
        info = line.split(' ')

        if info[0] == '..':
            break
        states.add(info[0])
        observ.add(info[1])
        
        try:
            start_count += 1.0
            start_prob[info[0]] += 1.0
        except KeyError:
            start_prob[info[0]] = 2.0
        
        try:
            emiss_count[info[0]] += 1.0
            emiss_prob[info[0]][info[1]] += 1.0
        except KeyError:
            try:
                emiss_prob[info[0]][info[1]] = 2.0
            except KeyError:
                emiss_count[info[0]] = 27.0
                emiss_prob[info[0]] = {info[1]: 2.0}
        
        if last != None:
            try:
                trans_count[last] += 1.0
                trans_prob[last][info[0]] += 1.0
            except KeyError:
                try:
                    trans_prob[last][info[0]] = 2.0
                except KeyError:
                    trans_count[last] = 27.0
                    trans_prob[last] = {info[0]: 2.0}
            last = info[0]
        else:
            last = info[0]

    for key in start_prob:
        start_prob[key] = start_prob[key]/start_count
            
    for key in emiss_prob:
        for ob in observ:
            try:
                emiss_prob[key][ob] = emiss_prob[key][ob]/emiss_count[key]
            except KeyError:
                emiss_prob[key][ob] = 1.0/emiss_count[key]
    
    for key in trans_prob:
        for state in states:
            try:
                trans_prob[key][state] = trans_prob[key][state]/trans_count[key]
            except KeyError:
                trans_prob[key][state] = 1.0/trans_count[key]        
    obs = []
    paths = []
    temp1 = []
    temp2 = []
    for line in fd:
        line = line.rstrip('\n').split()
        if line[0] == '_':
            obs.append(list(temp1))
            paths.append(list(temp2))
            temp1 = []
            temp2 = []
            continue
        temp1.append(line[1])
        temp2.append(line[0])

    return states, obs, start_prob, trans_prob, emiss_prob, paths  
      
def topicparse(fd):
    states = set()
    observ = set()
    start_prob = {}
    trans_prob = {}
    emiss_prob = {}
    
    trans_count = {}
    emiss_count = {}
    
    info = []
    last = None

    testset = True
    temp1 = []
    temp2 = []

    for line in fd:
        line = line.rstrip('\n')
        info = line.split(' ')
        if info[0] == '..':
            testset = False
            continue
        states.add(info[0])
        start_prob[info[0]] = 1.0

        if last != None:
            try:
                trans_count[last] += 1.0
                trans_prob[last][info[0]] += 1.0
            except KeyError:
                try:
                    trans_prob[last][info[0]] = 2.0
                except KeyError:
                    trans_count[last] = 7.0
                    trans_prob[last] = {info[0]: 2.0}
            last = info[0]
        else:
            last = info[0]

        if testset:
            for j in range(1,int(len(info)/4)):
                temp1.append(info[j])
                temp2.append(info[0])

        for i in range(1,int(len(info))):
            observ.add(info[i])
            try:
                emiss_count[info[0]] += 1.0
                emiss_prob[info[0]][info[i]] += 1.0
            except KeyError:
                try:
                    emiss_prob[info[0]][info[i]] = 2.0
                except KeyError:
                    emiss_count[info[0]] = 6.0
                    emiss_prob[info[0]] = {info[i]: 2.0}
            
    for key in start_prob:
        start_prob[key] = 1.0/len(states)

    for key in emiss_prob:
        for ob in observ:
            try:
                emiss_prob[key][ob] = emiss_prob[key][ob]/emiss_count[key]
            except KeyError:
                emiss_prob[key][ob] = 1.0/emiss_count[key]
    
    for key in trans_prob:
        for state in states:
            try:
                trans_prob[key][state] = trans_prob[key][state]/trans_count[key]
            except KeyError:
                trans_prob[key][state] = 1.0/trans_count[key]        
    obs = []
    paths = []
    obs.append(list(temp1))
    paths.append(list(temp2))

    return states, obs, start_prob, trans_prob, emiss_prob, paths 

   
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    for y in states:
        V[0][y] = (math.log10(start_p[y]) + math.log10(emit_p[y][obs[0]]))
        path[y] = [y]
    thing = len(obs)
    err =0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            temp = []
            for y0 in states:
                try:
                    temp.append(((V[t-1][y0] + math.log10(trans_p[y0][y]) + math.log10(emit_p[y][obs[t]])), y0))
                except KeyError:

                    temp.append((-sys.maxsize-1,y0))
            (prob, state) = max(temp)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
         path = newpath
        pers = int((t*100)/(thing-1)) 
        print("["+"="*int(pers/5)+" "*(20-int(pers/5))+"]: "+str(pers)+"%", end=chr(13))
    n = 0 
    if len(obs) != 1:
        n = t
    (prob, state) = max((V[n][y], y) for y in states)
    return (10**prob, path[state])

def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

def print_pretty(table):
    labs = sorted(max(table.values(), key=len))
    s = "\t" + "\t".join(labs) +"\n"
    for j in table:
        s +=  j + "\t" + "\t".join("%.7s" %(table[j][q]) for q in labs) + "\n" 
    return s

def compare(a, b):
    if len(a)!=len(b) or len(a)==0:
        print("length error")
        return 0
    count = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            count += 1
    return (count*100)/len(a)

def main():
    try:
        optlist, remainder = getopt.getopt(sys.argv[1:], 'p:o:h')
        if len(optlist) == 0:
            print( "***Options required***" )
            usage()
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in optlist:
        if o == "-h":
          usage()
        elif o == "-p":
            if a == "1":
                fd = open("robot_no_momemtum.data", 'r')
                func = robotparse
            elif a == "2":
                fd = open("typos10.data", 'r')
                func = typoparse
            elif a == "3":
                fd = open("topics.data", 'r')
                func = topicparse
        elif o == "-o":
            if a == "1":
                states, all_observ, start_prob, trans_prob, emiss_prob, paths = func(fd)
            elif a == "2":
                print("Funtionality not implemented kill all humanz.")
                sys.exit(0)

    fdout = open("output.txt", 'w')
    fdout.write(print_pretty(trans_prob))
    fdout.write(print_pretty(emiss_prob))
 
    t1 = time.time()
    totalsame = 0
    for i in range(len(paths)):
        prob, path = viterbi(tuple(all_observ[i]),
                   tuple(states),
                   start_prob,
                   trans_prob,
                   emiss_prob)
        same = compare(path, paths[i])
        totalsame += same
        fdout.write(str(path) + "\n" + str(paths[i]) + "\n" + "Sameness: " + str(same) + "\n")
    t2 = time.time()

    print("The output is in the output.txt file")
    print("Accuracy: " +str(totalsame/len(paths)))

    timeness = t2 - t1
    ret = str(int((timeness/60)/60))+":"+str(int((timeness/60)%60))+":"+str(int(timeness%60))
    return ret
    
def usage():
  print( """
  Usage:
  ---------
    Flags
    -p: Choose the file to Run (1 for robot, 2 for typo correct, and 3 for topic change)
    -o: Specify the HMM order (1 or 2)

    Example Usage: 
    "python assignment5.py -p 1 -o 1" will run the toy robot with a first order HMM
  ---------
  """ )
  sys.exit(2)

if __name__ == "__main__":
    print(main())
