'''Farmer_Fox.py
by Dan Wang
UWNetID: daw1230
Student number: 1978194

Assignment 2, in CSE 415, Autumn 2019.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''
#<METADATA>
PROBLEM_NAME = "Farmer Fox Chicken and Grain"
PROBLEM_AUTHORS = ['D. Wang']
PROBLEM_CREATION_DATE = "12-OCT-2019"
#<METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
Far=0 # array index to access farmer counts
Fox=1 # array index to access fox counts
C=2 # array index to access chicken counts 
G=3 # array index to access grain counts 
LEFT=0 # array index to access left side of river
RIGHT=1 # array index to access right side of river

class State():

    def __init__(self, d=None):
        if d==None:
            d = {'all':[[0,0],[0,0],[0,0],[0,0]],
                 'boat':LEFT}
        self.d = d
        
    def __eq__(self,s2):
        for prop in ['all', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        p = self.d['all']
##        txt = "\n Farmer on left:"+str(p[Far][LEFT])+"\n"
##        txt += " Fox on left:"+str(p[Fox][LEFT])+"\n"
##        txt += " Chicken on left:"+str(p[C][LEFT])+"\n"
##        txt += " Grain on left:"+str(p[G][LEFT])+"\n"
##        txt += "   Farmer on right:"+str(p[Far][RIGHT])+"\n"
##        txt += "   Fox on right:"+str(p[Fox][RIGHT])+"\n"
##        txt += "   Chicken on right:"+str(p[C][RIGHT])+"\n"
##        txt += "   Grain on right:"+str(p[G][RIGHT])+"\n"
##        side='left'
##        if self.d['boat']==1: side='right'
##        txt += " boat is on the "+side+".\n"
        txt=str(p)
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.d['all']=[self.d['all'][F_f_C_or_G][:] for F_f_C_or_G in [Far, Fox, C, G]]
        news.d['boat'] = self.d['boat']
        return news

    def can_move(self,far,fox,c,g):
        '''Tests whether it's legal to move the boat and take
        far Farmer, fox Fox, c Chicken, and g Grain.'''
        side = self.d['boat'] # Where the boat is.
        p = self.d['all']
        if far<1: return False # Need farmer to steer boat.
        far_available = p[Far][side]
        if far_available < far: return False # Can't take more far's than available
        fox_available = p[Fox][side]
        if fox_available < fox: return False # Can't take more fox's than available
        c_available = p[C][side]
        if c_available < c: return False # Can't take more c's than available
        g_available = p[G][side]
        if g_available < g: return False # Can't take more g's than available
        far_remaining = far_available - far
        fox_remaining = fox_available - fox
        c_remaining = c_available - c
        g_remaining = g_available - g
        # fox and chicken, as well as chicken and grain, cannot be left together:
        if far_remaining==0 and g_remaining==0 and fox_remaining>0 and c_remaining>0: return False
        if far_remaining==0 and fox_remaining==0 and c_remaining>0 and g_remaining>0: return False
        far_at_arrival = p[Far][1-side]+far
        fox_at_arrival = p[Fox][1-side]+fox
        c_at_arrival = p[C][1-side]+c
        g_at_arrival = p[G][1-side]+g
        if far_at_arrival==0 and g_at_arrival==0 and fox_at_arrival>0 and c_at_arrival>0: return False
        if far_at_arrival==0 and fox_at_arrival==0 and c_at_arrival>0 and g_at_arrival>0: return False
        return True

    def move(self,far,fox,c,g):
        '''Assuming it's legal to make the move, this computes
        the new state resulting from moving the boat carrying
        far Farmer, fox Fox, c Chicken, and g Grain.'''
        news = self.copy()      # start with a deep copy.
        side = self.d['boat']         # where is the boat?
        p = news.d['all']          # get the array of arrays of people.
        p[Far][side] = p[Far][side]-far     # Remove Ffcg from the current side.
        p[Fox][side] = p[Fox][side]-fox
        p[C][side] = p[C][side]-c
        p[G][side] = p[G][side]-g
        p[Far][1-side] = p[Far][1-side]+far # Add them at the other side.
        p[Fox][1-side] = p[Fox][1-side]+fox
        p[C][1-side] = p[C][1-side]+c
        p[G][1-side] = p[G][1-side]+g
        news.d['boat'] = 1-side       # Move the boat itself.
        return news
    
def goal_test(s):
    '''If all Ffcg are on the right, then s is a goal state.'''
    p = s.d['all']
    return (p[Far][RIGHT]==1 and p[Fox][RIGHT]==1 and p[C][RIGHT]==1 and p[G][RIGHT]==1)

def goal_message(s):
    return "Congratulations on successfully guiding the farmer, fox, chicken, and grain across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)
    
    def apply(self, s):
        return self.state_transf(s)
#<COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'all':[[1, 0], [1, 0], [1, 0], [1, 0]], 'boat':LEFT})
#</INITIAL_STATE>

#<OPERATORS>
Ffcg_combinations = [(1,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1)]

OPERATORS = [Operator(
  "Cross the river with "+str(far)+" farmer, "+str(fox)+" fox, "+str(c)+" chicken, and "+str(g)+" grain",
  lambda s, far1=far, fox1=fox, c1=c, g1=g: s.can_move(far1,fox1,c1,g1),
  lambda s, far1=far, fox1=fox, c1=c, g1=g: s.move(far1,fox1,c1,g1)) 
  for (far,fox,c,g) in Ffcg_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
