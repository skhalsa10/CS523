package abm.utils.messages;

import abm.utils.BuildingType;
import abm.utils.SIRQState;

/**
 * This message is triggered when a person exits a building. it gets sent from the
 * peopleManager class to the building manager. If the person is susceptible they should expect
 * a message eventually from the building manager with a contagion level probability fro 0 to 1
 * the people manager will then use this probability to check if the person becoems infected.
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class ExitBuilding extends Message {

    private int buildingId;
    private int personCommunityId;
    private BuildingType buildingType;
    private int personId;
    private SIRQState personState;

    /**
     *
     * @param buildingId the id of the building that is being exited
     * @param buildingType the type of the building being exited
     * @param personCommunityId the community this person being exited from building belong to.
     * @param personId the ID of the person
     * @param personState the SIRQ State of the person.
     */
    public ExitBuilding(int buildingId,int personCommunityId, BuildingType buildingType,int personId, SIRQState personState){
        this.buildingId = buildingId;
        this.buildingType = buildingType;
        this.personId = personId;
        this.personState = personState;
        this.personCommunityId = personCommunityId;
    }

    public int getPersonCommunityId() {
        return personCommunityId;
    }

    public int getBuildingId() {
        return buildingId;
    }

    public BuildingType getBuildingType() {
        return buildingType;
    }

    public int getPersonId() {
        return personId;
    }

    public SIRQState getPersonState() {
        return personState;
    }
}
