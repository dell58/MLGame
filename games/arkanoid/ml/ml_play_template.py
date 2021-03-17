"""
The template of the main script of the machine learning process
"""
import pickle
import numpy as np
class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.vector_prev = (0,0)
        self.tmp = 0

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            print(scene_info['ball'])
            print(scene_info['platform'])
            print(self.tmp)
            print(self.vector_prev)
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            self.ball_prev = scene_info['ball']
            command = 'SERVE_TO_LEFT'
        else:
            ball_cur = scene_info['ball']
            p_x = scene_info['platform'][0] + 20
            vector = (ball_cur[0] - self.ball_prev[0],ball_cur[1] - self.ball_prev[1])
            if (vector[1] > 0): # ball fall
                offset = (vector[0] / vector[1]) * (400 - ball_cur[1])
                ballx_update = ball_cur[0] + offset
                if(ballx_update + 5 > 200):
                    ballx_update =  200 - (ballx_update + 5 - 200)
                elif (ballx_update < 0):
                    ballx_update *= -1
                pass
                self.vector_prev = vector
                self.tmp = ballx_update
                if (ballx_update < p_x and abs(p_x-ballx_update) > 15):
                    command = 'MOVE_LEFT'
                elif (ballx_update > p_x and abs(p_x-ballx_update) > 15):
                    command = 'MOVE_RIGHT'
                else:
                    command = 'NONE'
            else: # ball climbing
                if(ball_cur[1] >=300): # move platform to the same direction of ball
                    if( vector[0] > 0 and p_x < 155):
                        command = 'MOVE_RIGHT'
                    elif ( vector[0] < 0 and p_x > 45):
                        command  = 'MOVE_LEFT'
                    else:
                        command = 'NONE'
                else:
                    if(p_x > 100):
                        command = 'MOVE_LEFT'
                    elif(p_x < 100):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
            self.ball_prev = ball_cur
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.vector_prev = (0,0)
