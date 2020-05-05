package abm.utils.messages;

import abm.utils.BuildingType;
import javafx.geometry.Point2D;

/**
 * This message triggers when a buildingManager gives a destination building
 * that a person from a specific community should go to.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class DestinationForPerson extends Message {

    private int personCommunityID;
    private int personID;
    private int buildingID;
    private BuildingType buildingTypeToGo;
    private Point2D buildingDestToGo;

    public DestinationForPerson(int personCommunityID, int personID, int buildingID, BuildingType destBuilding, Point2D destBuildingToGo) {
        this.personCommunityID = personCommunityID;
        this.personID = personID;
        this.buildingID = buildingID;
        this.buildingTypeToGo = destBuilding;
        this.buildingDestToGo = destBuildingToGo;
    }

    public int getPersonCommunityID() {
        return personCommunityID;
    }

    public int getPersonID() {
        return personID;
    }

    public int getBuildingID() {
        return buildingID;
    }

    public BuildingType getBuildingTypeToGo() {
        return buildingTypeToGo;
    }

    public Point2D getBuildingDestToGo() {
        return buildingDestToGo;
    }
}
