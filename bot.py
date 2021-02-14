import sys

def Hod(prev, result):
    if prev == "00":
        return "+0"
    else:
        if result == 'w' or result == 'r':
            return "0+"
        else:
            return prev

if __name__ == '__main__':
    In = open(sys.argv[1], 'r')
    Out = open(sys.argv[2], 'w')
    n1 = In.readline()
    n2 = In.readline()
    n3 = In.readline()
    n4 = In.readline()
    n5 = In.readline()
    n6 = In.readline()
    n7 = In.readline().split()
    hod = Hod(n4, n5)
    n7 = str(n7)
    hod = str(hod)
    Out.write(hod)
    Out.write(n6)
    Out.write(n7)
    In.close()
    Out.close()