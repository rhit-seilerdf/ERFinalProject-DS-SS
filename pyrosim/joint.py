from pyrosim.commonFunctions import Save_Whitespace

class JOINT: 

    def __init__(self,name,parent,child,type,position,axis,upper,lower):

        self.name = name

        self.parent = parent

        self.child  = child

        self.type   = type

        self.position = position

        self.axis = axis

        self.upper = upper

        self.lower = lower

        self.depth = 1

    def Save(self,f):

        Save_Whitespace(self.depth,f)
        f.write('<joint name="' + self.name + '" type="' + self.type + '">' + '\n')

        Save_Whitespace(self.depth,f)
        f.write('   <parent link="' + self.parent + '"/>' + '\n')

        Save_Whitespace(self.depth,f)
        f.write('   <child  link="' + self.child  + '"/>' + '\n')

        Save_Whitespace(self.depth,f)
        originString = str(self.position[0]) + " " + str(self.position[1]) + " " + str(self.position[2])
        f.write('   <origin rpy="0 0 0" xyz="' + originString + '" />\n')

        axisString = str(self.axis[0]) + " " + str(self.axis[1]) + " " + str(self.axis[2])
        Save_Whitespace(self.depth,f)
        f.write('   <axis xyz="' + axisString + '"/>\n')

        Save_Whitespace(self.depth,f)
        f.write('   <limit effort="0.0" lower="'+ str(self.lower) + '" upper="' + str(self.upper) + '" velocity="0.0"/>\n')

        Save_Whitespace(self.depth,f)
        f.write('</joint>' + '\n')

