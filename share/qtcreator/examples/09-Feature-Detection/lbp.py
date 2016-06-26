# Local Binary Patterns (LBP) Example
#
# This example shows off how to use the local binary pattern feature descriptor
# on your OpenMV Cam. LBP descriptors work like Freak feature descriptors.
#
# WARNING: LBP supports needs to be reworked! As of right now this feature needs
# a lot of work to be made into somethin useful. This script will reamin to show
# that the functionality exists, but, in its current state is inadequate.

import sensor, time, image
sensor.reset()

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# Skip a few frames to allow the sensor settle down
# Note: This takes more time when exec from the IDE.
for i in range(0, 30):
    img = sensor.snapshot()
    img.draw_string(0, 0, "Please wait...")

d0 = None
#d0 = image.load_descriptor(image.LBP, "/desc.lbp")
clock = time.clock()

while (True):
    clock.tick()
    img = sensor.snapshot()

    objects = img.find_features(face_cascade, threshold=0.5, scale=1.25)
    if objects:
        face = objects[0]
        d1 = img.find_lbp(face)
        if (d0 == None):
            d0 = d1
        else:
            dist = image.match_descriptor(image.LBP, d0, d1)
            img.draw_string(0, 10, "Match %d%%"%(dist))

        img.draw_rectangle(face)
    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))
