import sys
import json
import collections

from pprint import pprint as pp

global classmap
global n1


def wall_in_map(prev):
    global classmap
    global n1
    x = classmap.x
    y = classmap.y
    if prev == "+0":
        classmap.arr[x - 1][y] = 4
        classmap.arr[x + n1][y] = 4 # зделать проверку на  выход из массива через if
    elif prev == "-0":
        classmap.arr[x + 1][y] = 4
        classmap.arr[x - n1][y] = 4
    elif prev == "0+":
        classmap.arr[x][y + 1] = 4
        classmap.arr[x][y - n1] = 4
    elif prev == "0-":
        classmap.arr[x][y - 1] = 4
        classmap.arr[x][y + n1] = 4


def prov_sosed(x, y):
    if classmap.arr[x][y + 1] == 0:
        return "0+"
    elif classmap.arr[x][y - 1] == 0:
        return "0-"
    elif classmap.arr[x + 1][y] == 0:
        return "-0"
    elif classmap.arr[x - 1][y] == 0:
        return "+0"
    else:
        return "00"


def hod_v_kord(prev, x, y):
    if prev == "+0":
        x -= 1
    elif prev == "-0":
        x += 1
    elif prev == "0-":
        y -= 1
    elif prev == "0+":
        y += 1
    return x, y


class Cell:

    def __init__(self, x, y, path) -> None:
        super().__init__()
        self.path = path
        self.y = y
        self.x = x

    def neighbours(self):
        x, y = self.x, self.y
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def bfs():
    global classmap
    visited, queue = set(), collections.deque(
        [Cell(*classmap.coords(), [])]
    )
    visited.add(classmap.coords())
    while queue:
        cell = queue.popleft()
        for n in cell.neighbours():
            if classmap.arr[n[0]][n[1]] == 0:
                return cell.path[0]
            if n not in visited and classmap.arr[n[0]][n[1]] != 4:
                visited.add(n)
                queue.append(Cell(*n, cell.path + [n]))


def Hod(prev, result, raz, nhod, pam):
    global classmap
    if result == "w":
        wall_in_map(prev)
    else:
        k = hod_v_kord(prev, classmap.x, classmap.y)
        classmap.x = k[0]
        classmap.y = k[1]
    pr = prov_sosed(classmap.x, classmap.y)
    if pr != "00":
        return pr
    else:
        BFS = bfs()
        return classmap.path_to(BFS[0], BFS[1])



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

    def coords(self):
        return self.x, self.y

    def path_to(self,x, y):
        if x>self.x:
            return "-0"
        elif x<self.x:
            return "+0"
        elif y>self.y:
            return "0+"
        else:
            return "0-"


if __name__ == '__main__':
    global classmap
    global n1
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
        for i in range((n1 + 1) * 2):
            classmap.arr.append([])
            for j in range((n1 + 1) * 2):
                classmap.arr[i].append(0)
    else:
        n7 = fin[6]
        classmap_dict = json.loads(n7)
        classmap = Map(**classmap_dict)
    classmap.arr[classmap.x][classmap.y] = 1
    hod = Hod(n4, n5, n1, n2, n7)
    hod = str(hod)
    strmap = json.dumps(classmap.__dict__)
    lenmap = len(strmap)
    Out.write(hod + '\n')
    Out.write(str(lenmap * 4) + '\n')
    Out.write(strmap)
    In.close()
    Out.close()
    # print(classmap.x)
    # print(classmap.y)
    # pp(classmap.arr)
