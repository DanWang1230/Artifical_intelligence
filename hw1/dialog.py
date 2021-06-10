# dialog.py

# This program runs a dialog between two agents, which must be defined

# elsewhere as separate modules.



import fany23_agent as agentA

import daw1230_agent as agentB



N_TURNS = 12



turn = 0

print(str(turn)+"A: "+agentA.agentName() + ': ' + agentA.introduce()+"\n")

print(str(turn)+"B: "+agentB.agentName() + ': ' + agentB.introduce()+"\n")

remark = ""

for i in range(N_TURNS):

    turn += 1

    remark = agentA.respond(remark)

    print(str(turn)+"A: "+agentA.agentName() + ': ' + remark+"\n")

    remark = agentB.respond(remark)

    print(str(turn)+"B: "+agentB.agentName() + ': ' + remark+"\n")

