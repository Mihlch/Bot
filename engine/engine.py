#!/usr/bin/env python

import sys
import os
import subprocess

wall = 99
apple = 1
frobots = 10

workDir = os.path.join(os.getcwd(), "output", "")

def arenaToPic(A, picName, step):
  if (sys.version_info >= (3,0)):
    print ("Save arena into " + picName + ".txt")
    with open(picName + ".txt", "w") as arenaFile:
      arenaFile.write('Step: ' + str(step) + "\n")
      arenaFile.write(arenaToStr(A))
      arenaFile.close
    return #Saveing of images is not supported for Python3

  import bmp
  import bmpfont_arial_12
  print ("Save arena into " + picName + ".bmp")

  side = 20
  sz = len(A) - 2
  img = bmp.BitMap(side * (sz + 2), side * (sz + 2), bmp.Color.WHITE.lighten() )
  img.setFont(bmpfont_arial_12.font_data)
  img.setPenColor(bmp.Color.BLACK)
  img.drawText('Step: ' + str(step), 10, 0)

  for x in range(sz):
    for y in range(sz):
      img.setPenColor(bmp.Color.BLACK)
      img.drawRect(side + x * side, side + y * side, side, side)
      if A[y + 1][x + 1] == 0:
        continue
      if A[y + 1][x + 1] == wall:
        img.setPenColor(bmp.Color.BLACK)
        img.drawRect(side + x * side, side + y * side, side, side, True)
      elif A[y + 1][x + 1] == apple:
        img.setPenColor(bmp.Color.RED)
        img.drawCircle(side + x * side + side / 2, side + y * side + side / 2, side / 2 - 3, True)
      elif A[y + 1][x + 1] >= frobots: #all robots
        rIdx = A[y + 1][x + 1] - frobots
        if rIdx == 0:
          img.setPenColor(bmp.Color.DKGREEN)
        elif rIdx == 1:
          img.setPenColor(bmp.Color.CYAN)
        elif rIdx == 2:
          img.setPenColor(bmp.Color.GREEN)
        elif rIdx == 3:
          img.setPenColor(bmp.Color.MAGENTA)
        elif rIdx == 4:
          img.setPenColor(bmp.Color.PURPLE)
        elif rIdx == 5:
          img.setPenColor(bmp.Color.BROWN)
        elif rIdx == 6:
          img.setPenColor(bmp.Color.DKRED)
        img.drawCircle(side + x * side + side / 2, side + y * side + side / 2, side / 2 - 3, True)
        img.setPenColor(bmp.Color.WHITE)
        img.drawText(str(rIdx), side + x * side + 8, side + y * side + 2)
  
  img.saveFile(picName + ".bmp")
  return 0

def runRobot(rName, rIn, rOut):
  print ("Run robot " + rName)
  prevdir = os.getcwd()
  os.chdir(rName)
  try:
    with open("run") as runFile:
      runLines = runFile.readlines()
      runFile.close()
      runLine = runLines[0].strip()
      retCode = subprocess.check_call(runLine + " " + rIn + " " + rOut, shell=True)
  finally:
    os.chdir(prevdir)

def getCoordFromArena(A, v):
  i = 0
  for row in A:
    j = 0
    for col in row:
      if col == v:
        return i, j
      j = j + 1
    i = i + 1
  return -1, -1

def nbElementsOnArena(A, v):
  nb = 0
  for row in A:
    for col in row:
      if col == v:
        nb += 1
  return nb

def arenaToStr(A):
  return (('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in A])) + "\n").replace(' 0 ', '   ')

def getNewPos(rCoordX, rCoordY, curMove):
  rNewPosX = rCoordX
  rNewPosY = rCoordY
  if curMove[0] == "-":
    rNewPosX = rCoordX - 1
  elif curMove[0] == "+":
    rNewPosX = rCoordX + 1
  if curMove[1] == "-":
    rNewPosY = rCoordY - 1
  elif curMove[1] == "+":
    rNewPosY = rCoordY + 1
  return rNewPosX, rNewPosY

def simulate(taskType, arena, robots, out):
  print ("Simulation")
  print (arenaToStr(arena))
  print (robots)
  step = 0
  apples = []
  prevSteps = []
  prevStepsRess = []
  prevMemory = []
  nbRobots = len(robots)
  curMove = []
  curMem = []
  for r in range(nbRobots):
    apples.append(1)
    prevSteps.append("00")
    prevStepsRess.append("a")
    prevMemory.append("")
    curMove.append("")
    curMem.append("")

  log = "Simulate, taskType = " + taskType + ", robots " + str(robots) + ".\n"

  pairOfTheSameStepsDetected = False
  arenaWithoutApples = False
  for it in range(2 * len(arena) * len(arena)):
    log += "\nStep " + str(step)
    if taskType == 'A' or taskType == 'B':
      log += ", apples: " + str(apples[0])
    else:
      log += ", apples: " + str(apples)
    log += ".\n" + arenaToStr(arena)

    arenaToPic(arena, workDir + "a" + str(step).zfill(3), step)

    if ((taskType == 'A' or taskType == 'B') and pairOfTheSameStepsDetected) or arenaWithoutApples:
      log += "Stop.\n"
      print ("Stop.")
      break

    for r in range(nbRobots):
      rName = robots[r]
      if taskType == 'A' or taskType == 'B':
        rIn  = workDir + "ri" + str(step).zfill(3) + ".txt"
        rOut = workDir + "ro" + str(step).zfill(3) + ".txt"
      elif taskType == 'C':
        rIn  = workDir + "r" + str(r) + "_" + rName + "i" + str(step).zfill(3) + ".txt"
        rOut = workDir + "r" + str(r) + "_" + rName + "o" + str(step).zfill(3) + ".txt"
      rCoordX, rCoordY = getCoordFromArena(arena, frobots + r)
      rInText = str(len(arena)-2) + "\n" + str(step) + "\n"
      if taskType == 'A':
        rInText += str(rCoordX) + " " + str(rCoordY) + "\n"
      else:
        rInText += "-1 -1\n"
      rInText += prevSteps[r] + "\n" + prevStepsRess[r] + "\n"
      if prevMemory[r]:
        rInText += prevMemory[r] + "\n"
      else:
        rInText += "0\n"
      with open(rIn, "w") as fi:
        fi.write(rInText)
        fi.close
      runRobot(rName, rIn, rOut)
      with open(rOut) as fo:
        res = fo.readlines()
        fo.close
      curMove[r] = res[0].rstrip()

      curMem[r] = ""
      if int(res[1].rstrip()) > 0:
        curMem[r] += res[1].rstrip() + "\n"
        i = 2
        while len(res) > i and res[i].strip():
          curMem[r] += res[i].strip() + "\n"
          i += 1

      if taskType == 'A' or taskType == 'B':
        rNewPosX, rNewPosY = getNewPos(rCoordX, rCoordY, curMove[r])
        log += " Decision of the robot \"" + robots[r] + "\": " + curMove[r] + ". "
        
        stepRes = "e" #empty
        if arena[rNewPosX][rNewPosY] == wall:
          stepRes = "w" #wall
        elif arena[rNewPosX][rNewPosY] == apple:
          stepRes = "a" #apple
          apples[r] += 1
        elif arena[rNewPosX][rNewPosY] >= frobots and (rNewPosX != rCoordX or rNewPosY != rCoordY):
          stepRes = "r" #other robot

        if stepRes == "a" or stepRes == "e":
          if rNewPosX != rCoordX or rNewPosY != rCoordY:
            arena[rCoordX][rCoordY] = 0
          arena[rNewPosX][rNewPosY] = frobots + r

        log += " Result: " + stepRes + ".\n" 

        if rNewPosX == rCoordX and rNewPosY == rCoordY and curMove[r] == prevSteps[r] and curMem[r] == prevMemory[r]:
          log += "The same step with the same result detected."
          pairOfTheSameStepsDetected = True

        prevStepsRess[r] = stepRes
  
      prevSteps[r] = curMove[r]
      prevMemory[r] = curMem[r]

      if prevMemory[r]:
        log += " Memory of " + str(r) + "-th robot \"" + rName + "\": " + prevMemory[r] + "\n"

    if taskType == 'C':
      decisionMade = []
      rNewPosX = []
      rNewPosY = []
      rCoordX = []
      rCoordY = []
      for r in range(nbRobots):
        decisionMade.append(False)
        rCoordXr, rCoordYr = getCoordFromArena(arena, frobots + r)
        rNewPosXr, rNewPosYr = getNewPos(rCoordXr, rCoordYr, curMove[r])
        rNewPosX.append(rNewPosXr)
        rNewPosY.append(rNewPosYr)
        rCoordX.append(rCoordXr)
        rCoordY.append(rCoordYr)
      
      for r in range(nbRobots):
        s = "curMove[" + str(r) + "] == " + str(curMove[r]) + ", newPos = (" + str(rNewPosX[r]) + ", " + str(rNewPosY[r]) + ")"
        log += s + "\n"
        print (s)

      for r in range(nbRobots):
        if curMove[r] == "00":
          prevStepsRess[r] = "e"
          decisionMade[r] = True

      doneSmth = True
      while doneSmth:
        doneSmth = False
        for r in range(nbRobots):
          if decisionMade[r]:
            continue
          if arena[rNewPosX[r]][rNewPosY[r]] == wall:
            prevStepsRess[r] = "w"
            decisionMade[r] = True
            doneSmth = True
          elif arena[rNewPosX[r]][rNewPosY[r]] != 0 and arena[rNewPosX[r]][rNewPosY[r]] >= frobots and decisionMade[arena[rNewPosX[r]][rNewPosY[r]] - frobots]:
            prevStepsRess[r] = "r"
            decisionMade[r] = True
            doneSmth = True

      doneSmth = True
      while doneSmth:
        doneSmth = False
        for r in range(nbRobots):
          if decisionMade[r]:
            continue
          conflictExists = False
          for r2 in range(nbRobots):            
            if r != r2:
              if rNewPosX[r] == rNewPosX[r2] and rNewPosY[r] == rNewPosY[r2]:
                conflictExists = True
              if rNewPosX[r] == rCoordX[r2] and rNewPosY[r] == rCoordY[r2]:
                if rNewPosX[r2] == rCoordX[r] and rNewPosY[r2] == rCoordY[r]:
                  conflictExists = True
                if decisionMade[r2]:
                  conflictExists = True
          if not conflictExists:
            if arena[rNewPosX[r]][rNewPosY[r]] != apple and arena[rNewPosX[r]][rNewPosY[r]] != 0:
              continue
            prevStepsRess[r] = "e"
            if arena[rNewPosX[r]][rNewPosY[r]] == apple:
              prevStepsRess[r] = "a"
              apples[r] += 1
            arena[rCoordX[r]][rCoordY[r]] = 0
            arena[rNewPosX[r]][rNewPosY[r]] = frobots + r
            decisionMade[r] = True
            doneSmth = True
          else:
            prevStepsRess[r] = "r"
            decisionMade[r] = True
            doneSmth = True

      for r in range(nbRobots):
        if not decisionMade[r]:
          prevStepsRess[r] = "r"
#          log += "Error: wrong decision for robot " + str(r) + "(" + robots[r] + ").\n"

    if nbElementsOnArena(arena, apple) == 0:
      log += "There are no apples on the arena."
      arenaWithoutApples = True

    step = step + 1

  with open(out, "w") as logFile:
    logFile.write(log)
    logFile.close

def main(argv=None):
  if len(sys.argv) < 3:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' replayin.txt replayout.txt')
    sys.exit(1)

  if not os.path.exists(sys.argv[1]):
    sys.stderr.write('ERROR: File ' + sys.argv[1] + ' not found!')
    sys.exit(1)

  if not os.path.exists(workDir):
    os.makedirs(workDir)

  with open(sys.argv[1]) as fi:
    content = fi.readlines()
    fi.close

  sizex = int(content[0])
  sizey = sizex
  arena = [[apple for x in range(sizex + 2)] for x in range(sizey + 2)]
  for x in range(0, sizex + 2):
    arena[0][x] = wall
  for x in range(0, sizex + 2):
    arena[sizey + 1][x] = wall
  for y in range(0, sizey + 2):
    arena[y][0] = wall
  for y in range(0, sizey + 2):
    arena[y][sizex + 1] = wall

  taskTypeLst = content[1].split(" ")
  taskType = taskTypeLst[0]
  print ("TaskType: " + taskType)

  robots = []

  if taskType == 'A':
    rCoordX = int(taskTypeLst[1])
    rCoordY = int(taskTypeLst[2])
    print ("Robot coord: " + str(rCoordX) + ", " + str(rCoordY))
    arena[rCoordX][rCoordY] = frobots
    robotName = content[2].rstrip()
    print ("robotName = " + robotName)
    robots.append(robotName)
  elif taskType == 'B':
    rCoordX = int(taskTypeLst[1])
    rCoordY = int(taskTypeLst[2])
    print ("Robot coord: " + str(rCoordX) + ", " + str(rCoordY))
    arena[rCoordX][rCoordY] = frobots
    wCoordX = int(taskTypeLst[3])
    wCoordY = int(taskTypeLst[4])
    print ("Wall coord: " + str(wCoordX) + ", " + str(wCoordY))
    arena[wCoordX][wCoordY] = wall
    robotName = content[2].rstrip()
    print ("robotName = " + robotName)
    robots.append(robotName)
  elif taskType == 'C':
    nbRobots = int(taskTypeLst[1])
    print ("nbRobots = " + str(nbRobots))
    for x in range(0, nbRobots):
      robotInfo = content[2 + x].split(' ')
      robots.append(robotInfo[0])
      if arena[int(robotInfo[1])][int(robotInfo[2])] != apple:
        sys.stderr.write('ERROR: Wrong coordinates of robot ' + str(x))
        sys.exit(1)
      arena[int(robotInfo[1])][int(robotInfo[2])] = frobots + x
    print (robots)
  else:
    sys.stderr.write('ERROR: Unknown task type ' + taskType)
    sys.exit(1)

  simulate(taskType, arena, robots, sys.argv[2])

if __name__ == '__main__':
  main()
