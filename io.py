from mola.core import Mesh as _Mesh
from mola.core import Vertex as _Vertex
from mola.core import Face as _Face

def importOBJMesh(filename):
    """Loads a Wavefront OBJ file. """
    mesh=_Mesh()
    group=""
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'g':
            group=values[1]
        elif values[0] == 'v':
            v = map(float, values[1:4])
            mesh.vertices.append(_Vertex(v[0],v[1],v[2]))
        elif values[0] == 'f':
            face = _Face([])
            face.group=group
            for v in values[1:]:
                w = v.split('/')
                vertex=mesh.vertices[int(w[0])-1]
                face.vertices.append(vertex)
            mesh.faces.append(face)
    return mesh

def importOBJFaces(filename):
    """Loads a Wavefront OBJ file. """
    return importOBJMesh(fileName).faces

def exportOBJMeshWithColors(mesh,fileNameOBJ,exportColors=True,exportGroups=True,weldVertices=True):
    exportOBJFacesWithColors(mesh.faces,fileNameOBJ,exportColors,exportGroups,weldVertices)

def exportOBJFacesWithColors(faces,fileNameOBJ,exportColors=True,exportGroups=True,weldVertices=True):

    """
    Exports the faces as an Alias wavefront obj file.

    Arguments:
    ----------
    faces : list of mola.core.Face
        The face to be measured
    fileNameOBJ : String
        The path and filename for the *.obj mesh file
    """

    file = open(fileNameOBJ, "w")

    if exportColors:
        fileNameMTL=fileNameOBJ+".mtl"
        file.write("mtllib ./"+fileNameMTL+"\n");
        fileMTL = open(fileNameMTL, "w")
        materials=set()

    if exportGroups:
        faces.sort(key=lambda x: x.group)

    vertexCount=0
    vertices={}
    currentGroup=None

    for face in faces:
        if exportGroups and face.group!=currentGroup:
            file.write("g "+str(face.group)+"\n")
            currentGroup=face.group
        if exportColors:
            materials.add(face.color)
            file.write("usemtl material"+str(face.color)+"\n")
        faceString="f"

        if weldVertices:
            for p in face.vertices:
                ptuple=(p.x,p.y,p.z)
                if ptuple in vertices:
                    faceString+=" "+str(vertices[ptuple])
                else:
                    vertexCount+=1
                    faceString+=" "+str(vertexCount)
                    vertices[ptuple]=vertexCount
                    file.write("v "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
        else:
            for p in face.vertices:
                vertexCount+=1
                faceString+=" "+str(vertexCount)
                file.write("v "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")

        faceString+="\n"
        file.write(faceString)
    file.close()

    if exportColors:
        for mat in materials:
            fileMTL.write("newmtl material"+str(mat)+"\n");
            fileMTL.write("Kd "+str(mat[0])+" "+" "+str(mat[1])+" "+str(mat[2])+"\n");
        fileMTL.close()
