# Until the user enters an exit sequence


from camera import Camera
from metrics.posture import Posture
from metrics.sitting import Sitting
from metrics.wrist import Wrist

# Create camera 
# Create metric classes
camera = Camera()
posture = Posture()
wrist = Wrist()

ashL = (0,0,0)
ashR = (0,0,0)
aeL = (0,0,0)
aeR = (0,0,0)

for i in range (0,1800):
    data = camera.get_data()

    shoulderL = data["left_shoulder"]
    shoulderR = data["right_shoulder"]
    earL = data["left_ear"]
    earR = data["right_ear"]

    for j in range (0,2):
        ashL[j] = ashL[j]+shoulderL[j]
        ashR[j] = ashR[j]+shoulderR[j]
        aeL[j] = aeL[j]+earL[j]
        aeR[j] = aeR[j]+earR[j]

for i in range (0,2):
    ashL[j] = ashL[j]/1800
    ashR[j] = ashR[j]/1800
    aeL[j] = aeL[j]/1800
    aeR[j] = aeR[j]/1800

avg = (ashL,ashR,aeL,aeR)




    





