def rencer(scene, camera):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera.updateViewMatrix()
    descendantList = scene.getDescendantList()
    meshList = [x for x in descendantList if type(x) is Mesh]
    for mesh in meshList:
        if mesh.visible:
            glUseProgram(mesh.material.programRef)
            glBindVertexArray.mesh.vaoRef
            mesh.material.uniforms["modelMatrix"].data
