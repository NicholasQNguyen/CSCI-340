"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *
from .objects import Mesh, Light

class Renderer(object):
    """Handles the rendering of all meshes in the scene."""
    
    def __init__(self, clearColor=[0,0,0]):
        
        glEnable( GL_DEPTH_TEST )
        
        # Required for antialiasing
        glEnable( GL_MULTISAMPLE )
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)
    
    def render(self, scene, camera, renderTarget=None):
        
        # Extract list of all Mesh objects in scene
        descendantList = scene.getDescendantList()        
        meshList = [x for x in descendantList if isinstance(x, Mesh)]
        lightList = [x for x in descendantList if isinstance(x, Light)]
        # Pad out lights because there needs to be 4
        while len(lightList) < 4:
            lightList.append(Light())
        
        # Clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update camera view
        camera.updateViewMatrix()
            
        for mesh in meshList:
            
            # Only try to render if the mesh is visible.
            if mesh.visible:            
                glUseProgram(mesh.material.programRef)
                
                # Bind VAO
                glBindVertexArray(mesh.vaoRef)
                
                # Update uniform values stored outside of material
                mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
                mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
                mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix
                
                # if material uses light data, add lights from list
                if "light0" in mesh.material.uniforms.keys():
                    for lightNumber in range(4):
                        lightName = "light" + str(lightNumber)
                        lightObject = lightList[lightNumber]
                        mesh.material.uniforms[lightName].data = \
                                      lightObject
                # add camera position if needed (specular lighting)                        
                if "viewPosition" in mesh.material.uniforms.keys():
                    mesh.material.uniforms["viewPosition"].data = camera.getPosition()
                
                # Update uniforms stored in material
                for variableName, uniformObject in mesh.material.uniforms.items():
                    uniformObject.uploadData()
                    
                # Update render settings
                mesh.material.updateRenderSettings()
                glDrawArrays(mesh.material.settings["drawStyle"],
                             0, mesh.geometry.vertexCount)