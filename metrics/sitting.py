class sitting_detector:
    def is_person_sitting(self,data):

        if data is None:
            return False

        if data["nose"] is not None:
            x = data["nose"][0] # x,y,z = data["nose"]
            y = data["nose"][1]

            if 0 <= x <= 1 and 0 <= y <= 1: #Mediapipe uses normalized cooridnates of 0 <= x,y <= 1
                return True

        return False