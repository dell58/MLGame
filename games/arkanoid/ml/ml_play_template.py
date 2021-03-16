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
        self.ball_prev = None
        self.vector_prev = (0,0)

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
            self.ball_prev = scene_info['ball']
            command = 'SERVE_TO_RIGHT'
        else:
            ball_cur = scene_info['ball']
            platform_pos = scene_info['platform']
            bricks = scene_info['bricks']
            h_bricks = scene_info['hard_bricks']
            p_x = platform_pos[0] + 20 # platform middle
            vector = (ball_cur[0] - self.ball_prev[0],ball_cur[1] - self.ball_prev[1])
            if (vector[1] > 0): # ball fall
                offset = (vector[0] / vector[1]) * (400 - ball_cur[1])
                ballx_update = ball_cur[0] + offset
                if(ballx_update + 5 > 200):
                    ballx_update =  200 - (ballx_update + 5 - 200)
                elif (ballx_update < 0):
                    ballx_update *=-1
                pass
                if (ballx_update < platform_pos[0]):
                    command = 'MOVE_LEFT'
                elif (ballx_update > platform_pos[0] + 40):
                    command = 'MOVE_RIGHT'
                else:
                    command = 'NONE'
            else: # move platform to center
                if( p_x > 100):
                    command = 'MOVE_LEFT'
                elif ( p_x < 100):
                    command  = 'MOVE_RIGHT'
                else:
                    command ='NONE'
            self.ball_prev = ball_cur
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.ball_prev = None
        self.vector_prev = (0,0)
