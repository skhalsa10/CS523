# The code is borrowed from JIDT tool. It handles the case of discrete data to calculate mutual information.
# Credits to JIDT for the implementation, some modifications to the code to match our need was done by Anas Gauba.
import jpype as jp
import numpy
# Code for reading in file from JIDT demos example. I am not gonna pass a file here, instead
# I will pass the arrays from the .py file.
# # Our python data file readers are a bit of a hack, python users will do better on this:
# sys.path.append("C:\\Users\\anasf\\Downloads\\infodynamics-dist-1.5\\demos\\python")
# import readIntsFile

# Add JIDT jar library to the path
jarLoc = input("Provide the jar location of where your jidt infodynamics is:\n")

# example jar loc path for my pc: "C:\\Users\\anasf\\Downloads\\infodynamics-dist-1.5\\infodynamics.jar"
jarLocation = jarLoc
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# # 0. Load/prepare the data:
# dataRaw = readIntsFile.readIntsFile("C:\\Users\\anasf\\OneDrive\\CS523\\Project1\\r11-r12-r21-r22-afterN.txt")
# # As numpy array:
# data = numpy.array(dataRaw)
# source = JArray(JInt, 1)(data[:,2].tolist())
# destination = JArray(JInt, 1)(data[:,3].tolist())

def calculateMutualInfo(sourceCol, destCol):
    # changing the python's numpy.array type to java array type.
    sourceCol = jp.JArray(jp.JInt, 1)(sourceCol)
    destCol = jp.JArray(jp.JInt, 1)(destCol)

    # 1. Construct the calculator:
    calcClass = jp.JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete

    calc = calcClass(101, 101, 0)

    # 2. No other properties to set for discrete calculators.
    # 3. Initialise the calculator for (re-)use:
    calc.initialise()

    # 4. Supply the sample data:
    calc.addObservations(sourceCol, destCol)

    # 5. Compute the estimate:
    result = calc.computeAverageLocalOfObservations()

    print("MI_Discrete Value = %.4f bits" %
        (result))

    return result
