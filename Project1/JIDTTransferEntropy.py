# The code is borrowed from JIDT tool. It handles the case of discrete data to calculate transfer entropy.
# This code is implemented by JIDT and modified by Anas Gauba.
import sys
import numpy as np
import jpype as jp


# JIDT Generated Code for Transfer Entropy.
pythonDemos = input("Please provide the path to the python demos for your jidt installation. For example: '\..\infodynamics-dist-1.5\demos\python'\n")
# example path for my pc: "C:\\Users\\anasf\\Downloads\\infodynamics-dist-1.5\\demos\\python"
sys.path.append(pythonDemos)
import readIntsFile

jarLoc = input("Now provide the jar location of where your jidt infodynamics is:\n")

# example jar loc path for my pc: "C:\\Users\\anasf\\Downloads\\infodynamics-dist-1.5\\infodynamics.jar"
jarLocation = jarLoc

# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def calculateTransferEntropy(sourceCol, destCol):
    # changing the python's numpy.array type to java array type.
    sourceCol = jp.JArray(jp.JInt, 1)(sourceCol)
    destCol = jp.JArray(jp.JInt, 1)(destCol)

    calcClass = jp.JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete

    # For our data, the numbers range from 0 to 100. That's why we want the base to be 101.
    calc = calcClass(101, 1, 1, 1, 1, 1)

    calc.initialise()

    calc.addObservations(sourceCol, destCol)

    result = calc.computeAverageLocalOfObservations()

    print("TE_Discrete Value = %.4f bits" %
        (result))

    return result