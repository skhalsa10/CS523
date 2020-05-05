package abm.utils.messages;

import abm.utils.BuildingType;
import abm.utils.SIRQState;

/**
 * This message gets triggered when a person arrives at a building
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class EnterBuilding extends Message {
    private int buildingId;
    private BuildingType buildingType;
    private int personId;
    private SIRQState personState;
    private double contagionLevel;

    public EnterBuilding(int buildingId, BuildingType buildingType, int personId, SIRQState personState, double contagionLevel) {
        this.buildingId = buildingId;
        this.buildingType = buildingType;
        this.personId = personId;
        this.personState = personState;
        this.contagionLevel = contagionLevel;
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

    public double getContagionLevel() {
        return contagionLevel;
    }
}
