"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

import numpy as np


class Matrix(object):
    @staticmethod
    def makeIdentity():
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]).astype(float)
    @staticmethod
    def makeTranslation(x, y, z):    
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationX(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ 1, 0, 0, 0],
                         [ 0, c,-s, 0],
                         [ 0, s, c, 0],
                         [ 0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationY(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationZ(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ c, -s, 0, 0],
                         [ s,  c, 0, 0],
                         [ 0,  0, 1, 0],
                         [ 0,  0, 0, 1]]).astype(float)

    @staticmethod
    def makeScale(s):
        return np.array([[ s, 0, 0, 0],
                         [ 0, s, 0, 0],
                         [ 0, 0, s, 0],
                         [ 0, 0, 0, 1]]).astype(float)
       
    @staticmethod
    def makePerspective(angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        a = angleOfView * np.pi / 180.0
        d = 1.0 / np.tan(a/2)
        r = aspectRatio
        b = (far + near) / (near - far)
        c =   2*far*near / (near - far)
        return np.array([[d/r, 0, 0, 0],
                         [  0, d, 0, 0],
                         [  0, 0, b, c],
                         [  0, 0,-1, 0]]).astype(float)
                 
    @staticmethod
    def inverse(matrix):
        return np.linalg.inv(matrix)

    @staticmethod
    def makeScaleAsymmetric(a, b, c):
        return np.array([[a, 0, 0, 0],
                         [0, b, 0, 0],
                         [0, 0, c, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makeRotate(a, b, c):
        return(makeRotationZ(c) @ makeRotationY(b) @ makeRotationX(a))

    @staticmethod
    def applyMatrix(baseMatrix, appliedMatrix, local=True):
        if local:
            return baseMatrix @ appliedMatrix
        else:
            return appliedMatrix @ baseMatrix

    @staticmethod
    def translate(matrix, x, y, z):
        return Matrix.applyMatrix(matrix, Matrix.makeTranslation(x, y, z))

    @staticmethod
    def rotateX(matrix, angle):
        return Matrix.applyMatrix(matrix, Matrix.makeRotationX(angle))

    @staticmethod
    def rotateY(matrix, angle):
        return Matrix.applyMatrix(matrix, Matrix.makeRotationY(angle))

    @staticmethod
    def rotateZ(matrix, angle):
        return Matrix.applyMatrix(matrix, Matrix.makeRotationZ(angle))

    @staticmethod
    def rotate(matrix, a, b, c):
        matrix = Matrix.rotateZ(matrix, c)
        matrix = Matrix.rotateY(matrix, b)
        matrix = Matrix.rotateX(matrix, a)
        return matrix

    @staticmethod
    def scale(s):
        return Matrix.applyMatrix(matrix, Matrix.makeScale(s))

    @staticmethod
    def scaleAsymmetric(matrix, a, b, c):
        return Matrix.applyMatrix(matrix, Matrix.makeScaleAsymmetrix(a, b, c))
