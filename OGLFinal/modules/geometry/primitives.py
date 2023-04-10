"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry
from ..utils.vector import vec

import numpy as np

class RectangleGeometry(AbstractGeometry):
    """A primitive rectangle."""
    
    def __init__(self, width=1, height=1):
        super().__init__()
        
        P0 = [-width/2, -height/2, 0]
        P1 = [ width/2, -height/2, 0]
        P2 = [-width/2, height/2, 0]
        P3 = [ width/2, height/2, 0]
        C0, C1, C2, C3 = vec(1,1,1), vec(1,0,0), vec(0,1,0), vec(0,0,1)
        positionData = [P0,P1,P3, P0,P3,P2]
        colorData    = [C0,C1,C3, C0,C3,C2]
        normalData = [vec(0, 0, 1) for x in range(6)]
        
        T0, T1, T2, T3 = [0,0], [1,0], [0,1], [1,1]
        uvData = [ T0,T1,T3, T0,T3,T2 ]
        self.addAttribute("vec2", "vertexUV", uvData)
        
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)        
        
        self.countVertices()

class BoxGeometry(AbstractGeometry):
    """A primitive box."""
    
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        
        P0 = [-width/2, -height/2, -depth/2]
        P1 = [ width/2, -height/2, -depth/2]
        P2 = [-width/2, height/2, -depth/2]
        P3 = [ width/2, height/2, -depth/2]
        P4 = [-width/2, -height/2, depth/2]
        P5 = [ width/2, -height/2, depth/2]
        P6 = [-width/2, height/2, depth/2]
        P7 = [ width/2, height/2, depth/2]
        
        # colors for faces in order: x+, x-, y+, y-, z+, z-
        C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
        C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
        C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]
        
        positionData = [ P5,P1,P3,P5,P3,P7, P0,P4,P6,P0,
                        P6,P2,P6,P7,P3,P6,P3,P2,
                        P0,P1,P5,P0,P5,P4,P4,P5,P7,
                        P4,P7,P6, P1,P0,P2,P1,P2,P3 ]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6
        
        # normal vectors for x+, x-, y+, y-, z+, z
        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [ 0, -1, 0]
        N5, N6 = [0, 0, 1], [ 0, 0, -1]
        normalData = [N1]*6 + [N2]*6 + [N3]*6 + [N4]*6 + [N5]*6 + [N6]*6
        
        # texture coordinates
        T0, T1, T2, T3 = [0,0], [1,0], [0,1], [1,1]
        uvData = [ T0,T1,T3, T0,T3,T2 ] * 6
        
        self.addAttribute("vec2", "vertexUV", uvData)        
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
                
        self.countVertices()


class DiceGeometry(AbstractGeometry):
    """A primitive box."""
    
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        
        P0 = [-width/2, -height/2, -depth/2]
        P1 = [ width/2, -height/2, -depth/2]
        P2 = [-width/2, height/2, -depth/2]
        P3 = [ width/2, height/2, -depth/2]
        P4 = [-width/2, -height/2, depth/2]
        P5 = [ width/2, -height/2, depth/2]
        P6 = [-width/2, height/2, depth/2]
        P7 = [ width/2, height/2, depth/2]
        
        # colors for faces in order: x+, x-, y+, y-, z+, z-
        C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
        C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
        C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]
        
        positionData = [ P5,P1,P3,P5,P3,P7, P0,P4,P6,P0,
                        P6,P2,P6,P7,P3,P6,P3,P2,
                        P0,P1,P5,P0,P5,P4,P4,P5,P7,
                        P4,P7,P6, P1,P0,P2,P1,P2,P3 ]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6
        
        # normal vectors for x+, x-, y+, y-, z+, z
        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [ 0, -1, 0]
        N5, N6 = [0, 0, 1], [ 0, 0, -1]
        normalData = [N1]*6 + [N2]*6 + [N3]*6 + [N4]*6 + [N5]*6 + [N6]*6
        
        uvData = []
        # texture coordinates
        for u in [0, 0.25, 0.5, 0.75]:
            T0, T1, T2, T3 = [u,0.34], [u+0.25,0.34], [u,0.66], [u+0.25,0.66]
            uvData += [ T0,T1,T3, T0,T3,T2 ]
            if np.isclose(u, 0.25):
                for v in [(0.0, 0.34), (0.66, 1.0)]:
                    T0, T1, T2, T3 = [u,v[0]], [u+0.25,v[0]], [u,v[1]], [u+0.25,v[1]]
                    uvData += [ T0,T1,T3, T0,T3,T2 ]
                    
        
        
        self.addAttribute("vec2", "vertexUV", uvData)        
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
                
        self.countVertices()
class DiceGeometry(AbstractGeometry):
    """A primitive box."""
    
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        
        P0 = [-width/2, -height/2, -depth/2]
        P1 = [ width/2, -height/2, -depth/2]
        P2 = [-width/2, height/2, -depth/2]
        P3 = [ width/2, height/2, -depth/2]
        P4 = [-width/2, -height/2, depth/2]
        P5 = [ width/2, -height/2, depth/2]
        P6 = [-width/2, height/2, depth/2]
        P7 = [ width/2, height/2, depth/2]
        
        # colors for faces in order: x+, x-, y+, y-, z+, z-
        C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
        C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
        C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]
        
        positionData = [ P5,P1,P3,P5,P3,P7, P0,P4,P6,P0,
                        P6,P2,P6,P7,P3,P6,P3,P2,
                        P0,P1,P5,P0,P5,P4,P4,P5,P7,
                        P4,P7,P6, P1,P0,P2,P1,P2,P3 ]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6
        
        # normal vectors for x+, x-, y+, y-, z+, z
        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [ 0, -1, 0]
        N5, N6 = [0, 0, 1], [ 0, 0, -1]
        normalData = [N1]*6 + [N2]*6 + [N3]*6 + [N4]*6 + [N5]*6 + [N6]*6
        
        uvData = []
        # texture coordinates
        for u in [0, 0.25, 0.5, 0.75]:
            T0, T1, T2, T3 = [u,0.34], [u+0.25,0.34], [u,0.66], [u+0.25,0.66]
            uvData += [ T0,T1,T3, T0,T3,T2 ]
            if np.isclose(u, 0.25):
                for v in [(0.0, 0.34), (0.66, 1.0)]:
                    T0, T1, T2, T3 = [u,v[0]], [u+0.25,v[0]], [u,v[1]], [u+0.25,v[1]]
                    uvData += [ T0,T1,T3, T0,T3,T2 ]
                    
        
        
        self.addAttribute("vec2", "vertexUV", uvData)        
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
                
        self.countVertices()

class PolygonGeometry(AbstractGeometry):
    """A primitive polygon."""
    
    def __init__(self, sides=3, radius=1):
        super().__init__()
        
        A = 2 * np.pi / sides
        positionData = []
        colorData = []
        normalData = []
        normal = vec(0,0,1)
        uvData = []
        uvCenter = [0.5, 0.5]
        
        for n in range(sides):
            positionData.append([0, 0, 0])
            positionData.append([radius*np.cos(n*A),
                                  radius*np.sin(n*A),
                                  0])
            positionData.append([radius*np.cos((n+1)*A),
                                  radius*np.sin((n+1)*A),
                                  0])
            colorData.append([1, 1, 1])
            colorData.append([1, 0, 0])
            colorData.append([0, 0, 1])
            for i in range(3):
                normalData.append(vec(*normal))
                
            uvData.append(uvCenter)
            uvData.append([np.cos(n*A)*0.5 + 0.5,np.sin(n*A)*0.5 + 0.5 ])
            uvData.append([np.cos((n+1)*A)*0.5 + 0.5,np.sin((n+1)*A)*0.5 + 0.5 ])
                
        self.addAttribute("vec2", "vertexUV", uvData)
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)    
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
                
        self.countVertices()
