import time

class wrist:
    def __init__(self):
        self.start_time_of_streak = None
        self.time_of_last_action = None
        self.seconds_active = 0
        self.times_of_action = []

    def update(self, data):
        if data == None:
            return
        if "timestamp" in data:
            current_time = float(data["timestamp"])
        else:
            current_time = float(time.time())
            
        action_done = False
        
        if "clicked" in data:
            if data["clicked"] == True:
                action_done = True
        if "key_pressed" in data:
            if data["key_pressed"] == True:
                action_done = True
        
        if action_done == True:
            if self.start_time_of_streak == None:
                self.start_time_of_streak = current_time
            elif self.time_of_last_action != None:
                if (current_time - self.time_of_last_action) > 30.0:
                    self.start_time_of_streak = current_time
                    
            self.time_of_last_action = current_time
            self.seconds_active = current_time - self.start_time_of_streak
            self.times_of_action.append(current_time)
        
        kept_times_of_action = []
        for one_action_time in self.times_of_action:
            if (current_time - one_action_time) <= 60.0:
                kept_times_of_action.append(one_action_time)
        self.times_of_action = kept_times_of_action
                
    def get_points(self):
        streak_score = (self.seconds_active / 3600.0) * 60.0
        
        if streak_score > 60.0:
            streak_score = 60.0
            
        actions_count = float(len(self.times_of_action))
        rate_score = (actions_count / 150.0) * 40.0
        if rate_score > 40.0:
            rate_score = 40.0
        
        total_score = streak_score + rate_score
        if total_score > 100.0:
            total_score = 100.0

        return float(total_score)