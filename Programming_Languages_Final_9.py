# -*- coding: utf-8 -*-

# Implementing RE
# Challenge Problem 
#
# Focus: All Units
#
#
# In this problem you will write a lexer, parser and interpreter for
# strings representing regular expressions. Your program will output 
# a non-deterministic finite state machine that accepts the same language
# as that regular expression. 
#
# For example, on input 
#
# ab*c
#
# Your program might output
# 
# edges = { (1,'a')  : [ 2 ] ,
#           (2,None) : [ 3 ] ,    # epsilon transition
#           (2,'b')  : [ 2 ] ,
#           (3,'c')  : [ 4 ] } 
# accepting = [4]
# start = 1
#
# We will consider the following regular expressions:
#
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you. 
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need. 
# 
import ply.lex as lex
import ply.yacc as yacc

# Fill in your code here. 
tokens = (
    'STAR', #'*'
    'OR',   #'|'
    'CHAR', #A-Z,a-z,0-9
    'LPAREN', #'('
    'RPAREN', #')'
    )
    
def t_STAR(token):
    r'\*' 
    return token

def t_OR(token):
    r'\|'
    return token

def t_CHAR(token):
    r'[0-9A-Za-z]'
    return token

def t_LPAREN(token):
    r'\('
    return token

def t_RPAREN(token):
    r'\)'
    return token

start = 'exp'

def p_start(p):
    'exp : regexp'
    p[0] = p[1]

def p_orcharpar(p):
    'regexp : CHAR OR LPAREN regexp RPAREN regexp'
    p[0] = [('or', [('char', p[1])], p[4])] + p[6]
    
def p_orcharchar(p):
    'regexp : CHAR OR CHAR regexp'
    p[0] = [('or', [('char', p[1])], [('char', p[3])])] + p[4]
    
def p_orparchar(p):
    'regexp : LPAREN regexp RPAREN OR CHAR regexp'
    p[0] = [('or', p[2], [('char', p[5])])] + p[6]
    
def p_orparpar(p):
    'regexp : LPAREN regexp RPAREN OR LPAREN regexp RPAREN regexp'
    p[0] = [('or', p[2], p[6])] + p[8]
    
def p_group(p):
    'regexp : CHAR regexp'
    p[0] = [('char', p[1])] + p[2]

def p_two(p):
    'regexp : CHAR CHAR'
    p[0] = [('char', p[1]), ('char', p[2])]
    
def p_star(p):
    'regexp : CHAR STAR regexp'
    p[0] = [('star', [('char', p[1])])] + p[3]
    
def p_parenstar(p):
    'regexp : LPAREN regexp RPAREN STAR regexp'
    p[0] = [('star', p[2])] + p[5]

def p_paren(p):
    'regexp : LPAREN regexp RPAREN regexp'
    p[0] = p[2]+p[4]
        
def p_empty(p):
    'regexp : '
    p[0] = []

def p_error(p):
    print p
    
    
lexer = lex.lex() 
parser = yacc.yacc()         

def test_lexer(input_string):
  #input_string = re.sub(r"//.*", "", input_string)
  lexer.input(input_string)
  result = [ ] 
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [tok.type]
  return result

def test_parser(input_string):
        lexer.input(input_string) 
        parse_tree = parser.parse(input_string,lexer=lexer)
        
        return parse_tree

def re_to_nfsm(re_string): 
        # Feel free to overwrite this with your own code. 
        lexer.input(re_string)
        parse_tree = parser.parse(re_string, lexer=lexer) 
        answer = interpret(parse_tree)
        return (answer[2], answer[1], answer[0]) 

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def interpret(trees):
    states = [1]
    edges = {}
    current_state = 1
    ending_states = []
    for tree in trees:
        node_type = tree[0]
        #each 'tree' represents all the ways to go from state x to state y
        next_state = max(states)+1
        if node_type == 'char':
            #there is only one way to go
            edges[(current_state, tree[1])] = [next_state]
            states.append(next_state)
            current_state = next_state
            if tree == trees[-1]:
                ending_states.append(next_state)
        elif node_type == 'star':
            #we can do stay put or epsilon transition
            inside = interpret(tree[1])
            dic = inside[2]
            #step through dic and add to edges after modifying as necessary
            new_states = [dic[i][0]+current_state-1 for i in dic if dic[i][0] not in inside[1]]
            print new_states
            states += new_states
            next_state = max(states)+1
            for k in dic:
                if dic[k][0] in inside[1]:
                    edges[(k[0]+current_state-1, k[1])] = [current_state] #ending where we began
                else:
                    edges[(k[0]+current_state-1, k[1])] = [dic[k][0]+current_state-1]
            
            #epsilon transition is also possible
            edges[(current_state, None)] = [next_state]
            
            current_state = next_state
            states.append(next_state)
            
            if tree == trees[-1]:
                ending_states.append(next_state)
                
        elif node_type == 'or':
            #this can go one of two ways...
            leftor = interpret(tree[1])
            rightor = interpret(tree[2])
            
            new_states = [leftor[2][i][0]+current_state-1 for i in leftor[2] if leftor[2][i][0] not in leftor[1]]
            states+=new_states
            new_states2 = [rightor[2][i][0]+current_state+len(new_states)-1 for i in rightor[2] if rightor[2][i][0] not in rightor[1]]
            states+=new_states2
            next_state = max(states)+1
            for k in leftor[2]:
                if leftor[2][k][0] in leftor[1]:
                    edges[(k[0]+current_state-1, k[1])] = [next_state]
                else:
                    edges[(k[0]+current_state-1, k[1])] = [leftor[2][k][0]+current_state-1]
            for k in rightor[2]:
                if rightor[2][k][0] in rightor[1]:
                    if tree == trees[-1]:
                        if k[0]==1:
                            edges[(current_state, k[1])] = [next_state+1]
                        else:
                            edges[(k[0]+current_state+len(new_states)-1, k[1])] = [next_state+1]
                        ending_states += [next_state, next_state+1]
                    else:
                        if k[0]==1:
                            edges[(current_state, k[1])] = [next_state]
                        else:
                            edges[(k[0]+current_state+len(new_states)-1, k[1])] = [next_state]
                else:
                    if k[0]==1:
                        edges[(current_state, k[1])] = [rightor[2][k][0]+current_state+len(new_states)-1]
                    else:
                        edges[(k[0]+current_state+len(new_states)-1, k[1])] = [rightor[2][k][0]+len(new_states)+current_state-1]
            
            
            current_state = next_state
            states.append(next_state)
            
    return (1, ending_states, edges)
            

def nfsmaccepts(edges, accepting, current, string, visited):
        # If we have visited this state before, return false. 
        if (current, string) in visited:
                return False
        visited.append((current, string))       

        # Check all outgoing epsilon transitions (letter == None) from this
        # state. 
        if (current, None) in edges:
                for dest in edges[(current, None)]:
                        if nfsmaccepts(edges, accepting, dest, string, visited):
                                return True

        # If we are out of input characters, check if this is an
        # accepting state. 
        if string == "":
                return current in accepting

        # If we are not out of input characters, try all possible
        # outgoing transitions labeled with the next character. 
        letter = string[0]
        rest = string[1:]
        if (current, letter) in edges:
                for dest in edges[(current, letter)]:
                        if nfsmaccepts(edges, accepting, dest, rest, visited):
                                return True
        return False

def test(re_string, e, ac_s, st_s, strings):
  my_e, my_ac_s, my_st_s = re_to_nfsm(re_string)
  for string in strings:
      print nfsmaccepts(e,ac_s,st_s,string,[]) == \
            nfsmaccepts(my_e,my_ac_s,my_st_s,string,[]) 


edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] } 
accepting_state = [4]
start_state = 1

test("a(b*)c", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,    
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] } 
accepting_state = [1]
start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 

