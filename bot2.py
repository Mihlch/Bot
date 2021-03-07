import sys

def Hod(prev, result, raz, nhod, pam):
    if prev == "00":
        return "+0"
    else:
        if (result == 'w' or result == 'r') and (prev == '+0' and int(nhod) < int(raz)):
            return "0-"
        elif (result == 'w' or result == 'r') and prev == '0-':
            return "-0"
        elif (result == 'w' or result == 'r') and (prev == '-0' or prev == '+0'):
            return '0+'
        elif prev == '0+' and pam[nhod-2] == '+0':
                return '-0'
        elif prev == '0+':
            return '+0'
        else:
            return prev

def List_to_streing(l):
    s = ''
    for i in l:
        s = s + i + ' '
    return s


if __name__ == '__main__':
    In = open(sys.argv[1], 'r')
    Out = open(sys.argv[2], 'w')
    fin = [s.strip() for s in In]
    n1 = int(fin[0])
    n2 = int(fin[1])
    n3 = fin[2]
    n4 = fin[3]
    n5 = fin[4]
    n6 = 2**(n1**2)*16
    if len(fin) > 6:
        n7 = fin[6].split()
    else:
        n7 = []
    hod = Hod(n4, n5, n1, n2, n7)
    hod = str(hod)
    n7.append(hod)
    Out.write(hod + '\n')
    Out.write(str(n6)+'\n')
    Out.write(List_to_streing(n7))
    In.close()
    Out.close()