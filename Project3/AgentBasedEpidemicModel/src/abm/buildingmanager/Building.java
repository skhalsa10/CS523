package abm.buildingmanager;

import abm.utils.BuildingType;
import abm.utils.SIRQState;
import abm.utils.messages.BuildingContagionLevel;
import abm.utils.messages.ExitBuilding;

import java.util.HashMap;

/**
 * The Building Class abstracts Building object and behavior. This is used for the
 * Buildings in the center of the map. these buildings have simple behavior they allow people
 * to enter and exit the building. They also keep track of the SymptomScale of the infected and
 * send the average symptom scale to the people manager when an exit building is requested.
 *
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class Building {

    private HashMap<Integer, Double> infectedPeople; //keep track of infected people ID and symptom level
    private int capacity;
    private int totalPeopleInside;
    private BuildingType buildingType;
    private int ID;
    private double infectionProbability;

    /**
     *
     * @param capacity the number of people that can enter this building at a time.
     * @param buildingType the type this building is
     * @param ID the Id of this building. this is NOT unique but the building type plus this ID IS unique.
     */
    public Building(int capacity, BuildingType buildingType, int ID) {
        this.infectedPeople = new HashMap<>();
        this.capacity = capacity;
        this.totalPeopleInside = 0;
        this.buildingType = buildingType;
        this.ID = ID;
        this.infectionProbability = 0; //is this needed?
    }

    /**
     * When a person enters a building if they are infected they get added to the infectedPeople map
     * @param personID
     * @param personState
     * @param symptomScale
     */
    public void enterBuilding(int personID, SIRQState personState, double symptomScale){
        totalPeopleInside++;
        if(personState == SIRQState.INFECTED){
            infectedPeople.put(personID,symptomScale);
        }
    }

    /**
     * this function gets called when a Person exits the building
     * @param m the ExitBuilding message already has all
     *          the information needed  by the building pass it to the method
     * @return BuildingContagionLevel Message  to be forwarded to the ABMController or
     *         null if no action needs to be taken
     */
    public BuildingContagionLevel exitBuilding(ExitBuilding m){
        totalPeopleInside--;
        if(m.getPersonState() == SIRQState.SUSCEPTIBLE){
            //lets collect the average contagion level of all people in the building
            double contagionLevel = 0;
            for (Double prob : infectedPeople.values()) {
                contagionLevel += prob;
            }
            int size = infectedPeople.size();
            if(size > 0) {
                contagionLevel = contagionLevel / size;
            }
            BuildingContagionLevel messageToSend = new BuildingContagionLevel(m.getPersonId(),contagionLevel,m.getPersonCommunityId());
            return messageToSend;
        }
        else if(m.getPersonState() == SIRQState.RECOVERED){
            //here we do nothing more just return null
            infectedPeople.remove(m.getPersonId());
            return null;

        }else if(m.getPersonState() == SIRQState.QUARANTINED){
            //if a quarantine person is leaving a building that means they were infected but became
            // Quarantined inside the building remove them from the list
            infectedPeople.remove(m.getPersonId());
            return null;

        }else if(m.getPersonState() == SIRQState.INFECTED){
            // lets remove them from the infectedpeople list
            infectedPeople.remove(m.getPersonId());
            return null;

        } else{
            System.out.println("Printing in error check the exitbuilding function in building class");
            return null;
        }

    }
}
