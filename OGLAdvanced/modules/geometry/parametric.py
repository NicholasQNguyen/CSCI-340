"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry, PolygonGeometry
from ..utils.matrix import Matrix
from ..utils.vector import normalize, vec, calcNormal
from ..utils.definitions import EPSILON, safeMultiply

import numpy as np


class AbstractParametric(AbstractGeometry):
    """Abstract parametric class for parametric geometry.
       Expects a surface function which defines the surface
       of the shape. *Start, *End, and *Resolution define
       how much of the shape is created and at what level
       of detail."""
       
    def __init__(self, uStart, uEnd, uResolution,
                       vStart, vEnd, vResolution,
                       surfaceFunction):
        super().__init__()
        
        # Generate set of points based on the function
        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / vResolution
        
        positions     = []
        vertexNormals = []
        uvs = []
        
        for uIndex in range(uResolution+1):
            vArray = []
            nArray = []
            uvArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append(surfaceFunction(u,v))
                
                P0 = surfaceFunction(u,       v)
                P1 = surfaceFunction(u+0.001, v)
                P2 = surfaceFunction(u,       v+0.001)
                normal = calcNormal(P0, P1, P2)
                    
                nArray.append(normal)
                
                uCoord = uIndex/uResolution
                vCoord = vIndex/vResolution
                uvArray.append([uCoord, vCoord])
                
            positions.append(vArray)
            vertexNormals.append(nArray)
            uvs.append(uvArray)
            
            
        # Store vertex data
        positionData     = []
        colorData        = []
        vertexNormalData = []
        faceNormalData   = []
        uvData = []
        
        # Default vertex colors
        C1, C2, C3 = vec(1,0,0), vec(0,1,0), vec(0,0,1)
        C4, C5, C6 = vec(0,1,1), vec(1,0,1), vec(1,1,0)
        
        # Group vertex data into triangles
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):        
                # Position data
                pA = positions[xIndex+0][yIndex+0]
                pB = positions[xIndex+1][yIndex+0]
                pC = positions[xIndex+1][yIndex+1]
                pD = positions[xIndex+0][yIndex+1]
                positionData += [ pA.copy(), pB.copy(),
                                  pC.copy(), pA.copy(),
                                  pC.copy(), pD.copy()]
                # Color data
                
                c1, c2, c3 = [1,0,0], [0,1,0], [0,0,1]
                c4, c5, c6 = [0,1,1], [1,0,1], [1,1,0]
                colorData += [c1, c2, c3,
                              c4, c5, c6]
                
                    
                    
                # Vertex data
                nA = vertexNormals[xIndex+0][yIndex+0]
                nB = vertexNormals[xIndex+1][yIndex+0]
                nC = vertexNormals[xIndex+1][yIndex+1]
                nD = vertexNormals[xIndex+0][yIndex+1]
                vertexNormalData += [ nA.copy(), nB.copy(),
                                  nC.copy(), nA.copy(),
                                  nC.copy(), nD.copy() ]
                
                # face normal vectors
                   
                fn0 = calcNormal(pA, pB, pC)
                fn1 = calcNormal(pA, pC, pD)
                faceNormalData += [fn0,fn0,fn0, fn1,fn1,fn1]
                
                # uv coordinates
                uvA = uvs[xIndex+0][yIndex+0]
                uvB = uvs[xIndex+1][yIndex+0]
                uvD = uvs[xIndex+0][yIndex+1]
                uvC = uvs[xIndex+1][yIndex+1]
                uvData += [uvA,uvB,uvC, uvA,uvC,uvD]

        self.addAttribute("vec3", "vertexNormal", vertexNormalData)
        self.addAttribute("vec3", "faceNormal", faceNormalData)      
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()

## Some parametric shapes ##


class PlaneGeometry(AbstractParametric):
    def __init__(self, width=1, height=1,
                 widthSegments=8, heightSegments=8):
        
        def S(u,v):
            return [u, v, 0]
        
        super().__init__(-width/2, width/2,
                         widthSegments,
                         -height/2, height/2,
                         heightSegments, S)

class EllipsoidGeometry(AbstractParametric):
    def __init__(self, width=1, height=1, depth=1,
             radiusSegments=32, heightSegments=16,
             uStart=0,        uEnd=2*np.pi,
             vStart=-np.pi/2, vEnd=np.pi/2):
        def S(u,v):
            return [width/2 * np.sin(u) * np.cos(v),
                    height/2 * np.sin(v),
                    depth/2 * np.cos(u) * np.cos(v)]
        super().__init__(uStart, uEnd,
                         radiusSegments,
                         vStart, vEnd,
                         heightSegments, S)

class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1,
             radiusSegments=32,
             heightSegments=16,
             uStart=0,        uEnd=2*np.pi,
             vStart=-np.pi/2, vEnd=np.pi/2):
        super().__init__(2*radius,
                        2*radius,
                        2*radius,
                        radiusSegments,
                        heightSegments,
                        uStart, uEnd,
                        vStart, vEnd)
    
class CylindricalGeometry(AbstractParametric):
    def __init__(self, radiusTop=1, radiusBottom=1,
                 height=1, radialSegments=32,
                 heightSegments=4,
                 closedTop=True,
                 closedBottom=True):
        def S(u,v):
            return [ (v*radiusTop + (1-v)*radiusBottom) * np.sin(u),
                    height * (v - 0.5),
                    (v*radiusTop + (1-v)*radiusBottom) * np.cos(u) ]
        super().__init__(0, 2*np.pi,
                         radialSegments,
                         0, 1,
                         heightSegments,
                         S)
        
        if closedTop:
            topGeometry = PolygonGeometry(radialSegments,
                                          radiusTop)
            transform = Matrix.makeTranslation(0, height/2, 0) @ Matrix.makeRotationY(-np.pi/2) @ Matrix.makeRotationX(-np.pi/2)
            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)
            
        if closedBottom:
            bottomGeometry = PolygonGeometry(radialSegments,
                                             radiusBottom)
            transform = Matrix.makeTranslation(0, -height/2, 0) @ Matrix.makeRotationY(-np.pi/2) @ Matrix.makeRotationX(np.pi/2)
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)
    
class CylinderGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32,
                 heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, radialSegments,
                         heightSegments, closed, closed)
        
class PrismGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=6, heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, sides,
                         heightSegments, closed, closed)

class ConeGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32, heightSegments=4,
                 closed=True):
        super().__init__(0, radius, height,
                         radialSegments, heightSegments,
                         False, closed)

class PyramidGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=4, heightSegments=4,
                 closed=True):
        super().__init__(0, radius, height,
                         sides, heightSegments,
                         False, closed)
    