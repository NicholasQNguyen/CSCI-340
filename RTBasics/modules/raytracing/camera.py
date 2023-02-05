"""
Author: Liz Matthews, Geoff Matthews
"""
from ..utils.vector import vec, lerp
import numpy as np

class Camera(object):
    """Camera object for raytracing.
    Initialization camera pointing
    at an arbitrary plane focus. Can get position
    and obtain a ray based on a percentage along
    the x and y of the focus plane."""

    def set(self,
            focus = vec(0,0,0),
            fwd = vec(0,0,-1),
            up = vec(0,1,0),
            fov = 90.0,
            distance = 2.5,
            aspect = 4/3):
        """Sets up the camera given the parameters.
           Calculates position, ul, ur, ll, and lr."""
        
        right = np.cross(up, fwd)
        # From SOHCAHTOA
        self.width = 2 * np.tan(fov/2) * distance
        self.height = np.reciprocal(aspect) * self.width
        self.position = -fwd * distance
        self.ul = (fwd * distance + self.position) + \
                  (up * (self.height / 2)) - \
                  (right * (self.width / 2))
        self.ur = (fwd * distance + self.position) + \
                  (up * (self.height / 2)) + \
                  (right * (self.width / 2))
        self.ll = (fwd * distance + self.position) - \
                  (up * (self.height / 2)) - \
                  (right * (self.width / 2))
        self.lr = (fwd * distance + self.position) - \
                  (up * (self.height / 2)) + \
                  (right * (self.width / 2))

    def __init__(self,
                 focus = vec(0,0,0),
                 fwd = vec(0,0,-1),
                 up = vec(0,1,0),
                 fov = 45.0,
                 distance = 2.5,
                 aspect = 4/3):
        self.set(focus, fwd, up, fov, distance, aspect)

    def getRay(self, xPercent, yPercent):
        """Returns a ray based on a percentage for the x and y coordinate."""
        p0 = lerp(self.ul, self.ur, xPercent)
        p1 = lerp(self.ll, self.lr, xPercent)
        worldPos = lerp(p0, p1, yPercent)
        return worldPos - self.position

    def getPosition(self):
        """Getter method for position."""
        return self.position
    
    def getDistanceToFocus(self, point):
        """Getter method for distance from the given point to the center of focus."""
        focus = (self.ul + self.ur + self.ll + self.lr) / 4
        return np.linalg.norm(point - focus)
