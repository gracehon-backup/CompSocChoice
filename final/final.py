from finalAux import *
from finalSCFs import *

if __name__ == "__main__":

    data = [[[1,0.34],[2,0.08],[3,0.27],[0,-0.57]],
            [[1,0.65],[2,-0.26],[3,0.38],[0,0.96]],
            [[1,0.25],[2,-0.61],[3,0.14],[0,-0.09]],
            [[1,-0.97],[2,1],[3,0.4],[0,-0.58]]]

    names = [0,1,2,3]

    print(filter(data))
    print(f"STV: {STV(filter(data),names)}")
    print(f"Plurality: {plurality(filter(data),names,[])[0]}")
    print(f"Approval: {approval(filter(data),names)}")
    print(f"Condorcet: {condorcet(filter(data),names)}")
    print(f"Borda: {borda(filter(data),names)}")
    print(f"Copeland: {copeland(filter(data),names)}")