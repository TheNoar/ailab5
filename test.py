import math

'''
states = ('Healthy', 'Fever')
 
observations = ('normal', 'cold', 'dizzy')
 
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
 
transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
   }
 
emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
   }
'''   
   
def robotparse(fd):
    states = set()
    observ = set()
    start_prob = {}
    trans_prob = {}
    emiss_prob = {}
    
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
        #print(info)
        observ.add(info[1])
        '''
        try:
            start_prob[info[0]] += 1
        except KeyError:
            start_prob[info[0]] = 2
        '''
        start_prob[info[0]] = 1.0/12.0
        
        try:
            emiss_count[info[0]] += 1.0
            emiss_prob[info[0]][info[1]] += 1.0
        except KeyError:
            emiss_count[info[0]] = 3.0
            try:
                emiss_prob[info[0]][info[1]] = 2.0
            except KeyError:
                emiss_prob[info[0]] = {info[1]: 2.0}
        
        if last != None:
            try:
                trans_count[last] += 1.0
                trans_prob[last][info[0]] += 1.0
            except KeyError:
                trans_count[last] = 3.0
                try:
                    trans_prob[last][info[0]] = 2.0
                except KeyError:
                    trans_prob[last] = {info[0]: 2.0}
            last = info[0]
        else:
            last = info[0]
            
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
    ob = []
    for line in fd:
        line = line.rstrip('\n').split()
        if line[0] == '.':
            break
        ob.append(line[1])    
    return states, ob, start_prob, trans_prob, emiss_prob   
   
   
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        #V[0][y] = start_p[y] * emit_p[y][obs[0]]
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((2**(math.log(V[t-1][y0]) + math.log(trans_p[y0][y]) + math.log(emit_p[y][obs[t]])), y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])
 
# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)
    
def example():
    fd = open("robot_no_momemtum.data", 'r')
    states, observ, start_prob, trans_prob, emiss_prob = robotparse(fd)
    
    #print(states)
    #print(observ)
    #print(start_prob)
    #print(trans_prob)
    #print(emiss_prob)
    
    return viterbi(tuple(observ),
                   tuple(states),
                   start_prob,
                   trans_prob,
                   emiss_prob)

    
    #return viterbi(robotparse(fd))
print(example())
