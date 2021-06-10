'''YourUWNetID_VI.py
(rename this file using your own UWNetID.)

Value Iteration for Markov Decision Processes.
'''
from TOH_MDP import *

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
   return "Wang, Dan" # For an autograder.

Vkplus1 = {}
Q_Values_Dict = {}

def one_step_of_VI(S, A, T, R, gamma, Vk):
   '''S is list of all the states defined for this MDP.
   A is a list of all the possible actions.
   T is a function representing the MDP's transition model.
   R is a function representing the MDP's reward function.
   gamma is the discount factor.
   The current value of each state s is accessible as Vk[s].
   '''

   '''Your code should fill the dictionaries Vkplus1 and Q_Values_dict
   with a new value for each state, and each q-state, and assign them
   to the state's and q-state's entries in the dictionaries, as in
       Vkplus1[s] = new_value
       Q_Values_Dict[(s, a)] = new_q_value

   Also determine delta_max, which we define to be the maximum
   amount that the absolute value of any state's value is changed
   during this iteration.
   '''
   global Q_Values_Dict
   for s in S:
      for a in A:
         Q_Values_Dict[(s, a)] = 0
         for sp in S:
           Q_Values_Dict[(s, a)] += T(s,a,sp)*(R(s,a,sp)+gamma*Vk[sp])
      Vkplus1[s] = max(Q_Values_Dict[(s, a)] for a in A)
   delta_max = max(abs(Vkplus1[s]-Vk[s]) for s in S)
   
   return (Vkplus1, delta_max) # placeholder

def return_Q_values(S, A):
   '''Return the dictionary whose keys are (state, action) tuples,
   and whose values are floats representing the Q values from the
   most recent call to one_step_of_VI. This is the normal case, and
   the values of S and A passed in here can be ignored.
   However, if no such call has been made yet, use S and A to
   create the answer dictionary, and use 0.0 for all the values.
   '''
   global Q_Values_Dict
   if not Q_Values_Dict:
      for s in S:
         for a in A:
            Q_Values_Dict[(s, a)] = 0  
   return Q_Values_Dict # placeholder

Policy = {}
def extract_policy(S, A):
   '''Return a dictionary mapping states to actions. Obtain the policy
   using the q-values most recently computed.  If none have yet been
   computed, call return_Q_values to initialize q-values, and then
   extract a policy.  Ties between actions having the same (s, a) value
   can be broken arbitrarily.
   '''
   global Policy
   Policy = {}
   if not Q_Values_Dict:
      return_Q_values(S, A)

   for s in S:
      maxQ = max(Q_Values_Dict[(s, a)] for a in A)
      for a in A:
         if Q_Values_Dict[(s, a)] == maxQ:
            Policy[s] = a
            break
   return Policy

def apply_policy(s):
   '''Return the action that your current best policy implies for state s.'''
   global Policy
   return Policy[s] # placeholder


