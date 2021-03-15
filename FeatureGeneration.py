import pickle
from os import path
import numpy as np
import glob
import pandas as pd

def transformCommand(command):
    if command == 'MOVE_RIGHT':
        return 2
    elif command == 'MOVE_LEFT':
        return 1
    else: # None
        return 0


def get_ArkanoidData(filename):
    Frames = []
    Balls = []
    Commands = []
    PlatformPos = []
    log = pickle.load((open(filename, 'rb')))
    log_ml = log['ml']
    logInfos = log_ml['scene_info']
    logCommands = log_ml['command']
    for sceneInfo in logInfos:
        Frames.append(sceneInfo['frame'])
        Balls.append(sceneInfo['ball'])
        PlatformPos.append(sceneInfo['platform'])
    for com in logCommands:
        Commands.append(transformCommand(com))

    commands_ary = np.array(Commands)
    commands_ary = commands_ary.reshape((len(Commands), 1))
    frame_ary = np.array(Frames)
    frame_ary = frame_ary.reshape((len(Frames), 1))
    ballpos_next = np.array(Balls[1:])
    ballpos_cur = np.array(Balls[:-1])
    vectors = ballpos_next - ballpos_cur
    data = np.hstack((frame_ary[1:],Balls[1:], PlatformPos[1:],vectors,commands_ary[1:]))
    return data

if __name__ == '__main__':
    
    filenames = glob.glob('games\\arkanoid\\log\\*.pickle')
    data = []
    for filename in filenames:
       tmp = get_ArkanoidData(filename)
       if len(data) == 0:
           data = tmp
       else:
           data = np.vstack((data,tmp))
    with open ('tmp.pickle','wb') as file:
        pickle.dump(data,file)
    with open ('tmp.pickle','rb') as file:
        ff = pickle.load(file)
        coms = ff[:,-1]
        none = 0
        right = 0
        left = 0
        for i in coms:
            if i == 0 :
                none += 1
            elif i == 1:
                right += 1
            else :
                left += 1 
        print('None:{}\nRight:{}\nLeft:{}'.format(none,right,left))
