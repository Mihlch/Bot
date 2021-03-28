import sys
import json

global classmap
global n1
global w

def wall_in_map(prev):
    global classmap
    global w
    x = classmap.x
    y = classmap.y
    if prev == "+0":
        classmap.arr[x][y - 1] = 99
    elif prev == "-0":
        classmap.arr[x][y + 1] = 99
    elif prev == "0+":
        classmap.arr[x + 1][y] = 99
    elif prev == "0-":
        classmap.arr[x - 1][y] = 99
    w += 1

def Hod(prev, result, raz, nhod, pam):
    global classmap
    global w
    if prev == "00":
        return "+0"
    if w < raz*4 + 2:
        if result == "w":
            wall_in_map(prev)
        elif prev == "+0" and result != "w" and result != "r":
            classmap.y -= 1
            return prev

def List_to_streing(l):
    s = ''
    for i in l:
        s = s + i + ' '
    return s

class Map:
    x = None
    y = None
    arr = None

    def __init__(self, x, y, arr=None) -> None:
        super().__init__()
        self.y = y
        self.arr = arr
        self.x = x
        if arr is None:
            self.arr = []


if __name__ == '__main__':
    global classmap
    global n1
    global w
    In = open(sys.argv[1], 'r')
    Out = open(sys.argv[2], 'w')
    fin = [s.strip() for s in In]
    n1 = int(fin[0])
    n2 = int(fin[1])
    n3 = fin[2]
    n4 = fin[3]
    n5 = fin[4]
    n7 = None
    if n2 == 0:
        classmap = Map(n1, n1)
        w = 0
        for i in range(n1*2-1):
            classmap.arr.append([])
            for j in range(n1 * 2 - 1):
                classmap.arr[i].append(0)
    else:
        n7 = fin[6]
        classmap_dict = json.loads(n7)
        classmap = Map(**classmap_dict)
    classmap.arr[classmap.x][classmap.y] = 10
    hod = Hod(n4, n5, n1, n2, n7)
    hod = str(hod)
    strmap = json.dumps(classmap.__dict__)
    lenmap = len(strmap)
    print(strmap)
    Out.write(hod + '\n')
    Out.write(str(lenmap*4) + '\n')
    Out.write(strmap)
    In.close()
    Out.close()