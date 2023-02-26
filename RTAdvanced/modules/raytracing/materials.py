"""
Author: Liz Matthews, Geoff Matthews
"""
import pygame as pg
import pathlib

from ..utils.vector import vec

# Will only work if running rayTracer.py from source folder
IMAGE_FOLDER = pathlib.Path("resources/images/")
BROWN_STONE_IMAGE = pg.image.load(IMAGE_FOLDER / "brownStone.jpg")
GRAY_STONE_IMAGE = pg.image.load(IMAGE_FOLDER / "grayStone.jpg")


class Material(object):
    """A class to contain all properties of a material.
       Contains ambient, diffuse, specular colors.
       Contains shininess property.
       Contains specular coefficient."""
    def __init__(self, baseColor, ambient, diffuse, specular,
                 shine=100, specCoeff=1.0, reflective=False,
                 image=None):
        self.baseColor = vec(*baseColor)
        self.ambient = vec(*ambient)
        self.diffuse = vec(*diffuse)
        self.specular = vec(*specular)
        self.shine = shine
        self.specCoeff = specCoeff
        self.reflective = reflective
        self.image = image

    def getBaseColor(self):
        """Getter method for ambient color."""
        return self.baseColor

    def getAmbient(self):
        """Getter method for ambient color."""
        return self.ambient

    def getDiffuse(self):
        """Getter method for diffuse color."""
        return self.diffuse

    def getSpecular(self):
        """Getter method for specular color."""
        return self.specular

    def getShine(self):
        """Getter method for shininess factor."""
        return self.shine

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return self.specCoeff

    def isReflective(self):
        """Getter method for reflective."""
        return self.reflective

    def getImage(self):
        """Getter method for image"""
        return self.image
