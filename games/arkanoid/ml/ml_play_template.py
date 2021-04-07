"""
The template of the main script of the machine learning process
"""
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
            print('ball:',scene_info['ball'])
            print('platform',scene_info['platform'][0]+20)
            print('predict pos:',self.tmp)
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            self.ball_prev = scene_info['ball']
            command = 'SERVE_TO_LEFT'
        else:
            ball_cur = scene_info['ball']
            p_x = scene_info['platform'][0] + 20
            ret = self.cal_height(scene_info)
            vector = (ball_cur[0] - self.ball_prev[0],ball_cur[1] - self.ball_prev[1])
            if (vector[1] > 0): # ball fall
                if(ball_cur[1] >= 250):
                    offset = (400 - ball_cur[1])
                    if(vector[0] * vector[1] < 0):
                        offset *= -1
                    ballx_update = ball_cur[0] + offset
                    if((ballx_update + 5) > 200):
                        ballx_update =  200 - (ballx_update - 200)
                    elif (ballx_update < 0):
                        ballx_update *= -1
                    pass
                    self.vector_prev = vector
                    self.tmp = ballx_update
                    if (ballx_update < p_x and abs(p_x - ballx_update) > 15):
                        command = 'MOVE_LEFT'
                    elif (ballx_update > p_x and abs(p_x - ballx_update) > 15):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
                else:
                    command = 'NONE'
            else: # ball climbing
                if(ball_cur[1] >=300 and ball_cur[1]<=394): # move platform to the same direction of ball
                    if( vector[0] > 0 and p_x < 155):
                        command = 'MOVE_RIGHT'
                    elif ( vector[0] < 0 and p_x > 45):
                        command  = 'MOVE_LEFT'
                    else:
                        command = 'NONE'
                else: #return to middle
                    if(p_x > 100):
                        command = 'MOVE_LEFT'
                    elif(p_x < 100):
                        command = 'MOVE_RIGHT'
                    else:
                        command = 'NONE'
            self.ball_prev = ball_cur
        return command
    
    def cal_height(self,scene_info):
        bricks_lowest = 0
        h_bricks_lowest = 0
        if(len(scene_info['bricks']) != 0):
            bricks = sorted(scene_info['bricks'],key = lambda x : -x[1])
            bricks_lowest = bricks[0][1]
        if(len(scene_info['hard_bricks'])!=0):
            h_bricks = sorted(scene_info['hard_bricks'],key = lambda x:-x[1])
            h_bricks_lowest = h_bricks[0][1]
        return max(h_bricks_lowest,bricks_lowest)



    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.vector_prev = (0,0)
