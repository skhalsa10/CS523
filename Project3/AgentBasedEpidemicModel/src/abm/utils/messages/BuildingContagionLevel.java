package abm.utils.messages;

import abm.utils.BuildingType;
import abm.utils.SIRQState;

/**
 * This message is triggered when a ExitBuilding message is received. this is the response with a
 * a contagion probability that can be used by peoplemanager to check if the person is now infected.
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class BuildingContagionLevel extends TimeMarker implements Message{

    private int personId;
    private double probOfInfection;

    /**
     *
     * @param personId the ID of the person  to run the infection probability on
     * @param  probOfInfection this is a probability of infection
     */
    public BuildingContagionLevel(int personId, double probOfInfection){
        this.personId = personId;
        this.probOfInfection = probOfInfection;
    }

    public int getPersonId() {
        return personId;
    }

    public double getProbOfInfection() {
        return probOfInfection;
    }
}
