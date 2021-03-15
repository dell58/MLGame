import pickle
import numpy as np
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.ball_prev = (75,400)
        with open('knnmodel.pickle','rb') as file:
            self.knn = pickle.load(file)

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
        else:
            if(scene_info['frame'] == 1):#skip first one frame
                self.ball_prev = scene_info['ball']
                command = 'NONE'
            else:
                ball_cur  = scene_info['ball']
                ball_vector = (ball_cur[0] - self.ball_prev[0],ball_cur[1] - self.ball_prev[1])
                self.ball_prev = ball_cur
                info_line = np.hstack((scene_info['frame'],scene_info['ball'],scene_info['platform'],ball_vector))
                com = self.knn.predict([info_line])
                if(com == 1):
                    command = 'MOVE_LEFT'
                elif (com == 2):
                    command = 'MOVE_RIGHT'
                else:
                    command = 'NONE'
            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.ball_prev = (75,400)
