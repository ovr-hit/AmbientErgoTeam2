class Posture:
    def __init__(self, average):
        """
        (average: tuple of tuples, current: tuple of tuples) -> Posture

        Initializes a Posture object with average and current posture data.
        """

        self.average = average # average (shoulderL, shoulderR, earL, earR)


    def get_posture(self, data):
        """
        () -> int

        Calculates the posture score based on the average and current posture data.
        """

        (shoulderL, shoulderR, earL, earR) = self.average
        (shoulderL_current, shoulderR_current, earL_current, earR_current) = (data['left_shoulder'], data['right_shoulder'], data['left_ear'], data['right_ear'])

        # Calculate the average tilt
        shoulder_tilt_avg = shoulderR[1] - shoulderL[1]
        ear_tilt_avg = earR[1] - earL[1]

        # Calculate the current tilt
        shoulder_tilt_current = shoulderR_current[1] - shoulderL_current[1]
        ear_tilt_current = earR_current[1] - earL_current[1]

        shoulder_dist_avg = (((shoulderR[0] - shoulderL[0])^2) + ((shoulderR[1] - shoulderL[1])^2))^(1/2)
        shoulder_dist_current = (((shoulderR_current[0] - shoulderL_current[0])^2) + ((shoulderR_current[1] - shoulderL_current[1])^2))^(1/2)

        shoulder_dist_diff = abs(shoulder_dist_current / shoulder_dist_avg)
        shoulder_tilt_diff = abs(shoulder_tilt_current / shoulder_tilt_avg)
        ear_tilt_diff = abs(ear_tilt_current / ear_tilt_avg)

        shoulder_tilt_score = min(25, (shoulder_tilt_current/shoulder_tilt_avg*2)*25)
        ear_score = min(25, ((ear_tilt_current/ear_tilt_avg*2)*25))
        shoulder_dist_score = min(50, (shoulder_dist_current/shoulder_dist_avg*0.3)*50)

        return (shoulder_tilt_score + ear_score + shoulder_dist_score)