package abm.utils.messages;

/**
 * This message is triggered when a ExitBuilding message is received. this is the response with a
 * a contagion probability that can be used by peoplemanager to check if the person is now infected.
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class BuildingContagionLevel extends Message {

    private int personId;
    private double probOfInfection;
    private int personCommunityId;

    /**
     *
     * @param personId the ID of the person  to run the infection probability on
     * @param  probOfInfection this is a probability of infection
     */
    public BuildingContagionLevel(int personId, double probOfInfection, int personCommunityId){
        this.personId = personId;
        this.probOfInfection = probOfInfection;
        this.personCommunityId = personCommunityId;
    }

    public int getPersonId() {
        return personId;
    }

    public int getPersonCommunityId() {
        return personCommunityId;
    }

    public double getProbOfInfection() {
        return probOfInfection;
    }
    

}
