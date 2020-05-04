package abm.buildingmanager;

import abm.utils.BuildingType;
import abm.utils.SIRQState;
import abm.utils.messages.BuildingContagionLevel;
import abm.utils.messages.ExitBuilding;

import java.util.HashMap;

public class Building {

    private HashMap<Integer, Double> infectedPeople;
    private int capacity;
    private int totalPeopleInside;
    private BuildingType buildingType;
    private int ID;
    private double infectionProbability;


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
            double contagionLevel = 0;
            for (Double prob : infectedPeople.values()) {
                contagionLevel += prob;
            }
            contagionLevel = contagionLevel/infectedPeople.size();
            BuildingContagionLevel messageToSend = new BuildingContagionLevel(m.getPersonId(),contagionLevel);
            return messageToSend;
        }else if(m.getPersonState() == SIRQState.RECOVERED){
            //here we do nothing more just return null
            return null;

        }else if(m.getPersonState() == SIRQState.QUARANTINED){
            System.out.println("Quarantined people should not be entering or exiting buildings");
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
