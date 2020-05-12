This directory contains the final product for 
UNM CS 523's Project 3 for the Spring 2020 semester.
The class was tought by Dr. Melanie Moses.

The authors of the work found in this project are:
Anas Gauba and Siri Khalsa 

In this directory you will find three things:

1. COVID-19_Screening.pdf - this is the final paper that we wrote.
2. /Data - This is a directory that contains pictures and screenshots that we collected during our simulation experiment.
3. ABEM.jar - this is a runnable Java Jar file that contains the Agent Based Epidemic Model simulation that we wrote. This JAR file also includes a copy of ALL source files This will allow anyone that is curious to inspect the code and see how we may have implemented the simulation. to view the source extract the contents of the jar file.

To run the JAR file you must use the Java 10 runtime environment. It also uses JavaFX 10. Java 10 virtual machine contains JavaFX 10 built in and allows us to guarantee that someone will also have JavaFX installed if they use Java 10. So before running this program make sure Java version 10 is installed and currently activated as the current java  environment on your machine. Java 10 is set up very differently on MAC, Linux, and Windows. We leave it up to the reader to know how to configure that. The application must be launch from the terminal or command line. The instructions below assume that the terminal is currently inside of the directory where the JAR lives. Here are the help instructions bundled with our application:



Agent Based Epidemic Model Help - ABEM can be launched in three ways ways:

1. java -jar ABEM.jar 
2. java -jar ABEM.jar [Symptom_Scale_Threshold]
3. java -jar ABEM.jar [Symptom_Scale_Threshold] [ALPHA] [BETA]

Symptom_Scale_Threshold MUST be a number between 0.0 and 1.0

1 will run the application with the defaults SymptomScaleThreshold=0.4 ALPHA=2 BETA=3.5
2 will run the application with given command line SymptomScaleThreshold and ALPHA=2 BETA=3.5
3 will run the application with the given command line arguments

Example: 
	java -jar ABEM.jar 
	java -jar ABEM.jar 0.3 
	java -jar ABEM.jar 0.3 1.0 5.2





