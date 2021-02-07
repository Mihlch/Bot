import sys

def Hod(prev, result):
    if prev == "00":
        return "-0"
    else:
        if result == 'a' or result == 'e':
            return prev
        else:
            return "+0"

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
    Out.write(hod + n6 + n7)
    In.close()
    Out.close()