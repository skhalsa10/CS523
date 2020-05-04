package abm.peopleManager;

import abm.utils.ABMConstants;
import abm.utils.BuildingType;
import abm.utils.PersonLocationState;
import abm.utils.SIRQState;
import abm.utils.messages.*;
import javafx.geometry.Point2D;

import java.util.Random;
import java.util.concurrent.PriorityBlockingQueue;

/**
 * This Class encapsulates a Person inside of the Agent Based Epidemic Model.
 *
 * The goal of this class is to encapsulate the bahavior of a person.
 * The person owns a
 */
public class Person {
    private int ID;
    private int homeCommunityID;
    // homeLocation is saved so the person can go back to their home. walkInside is used to walk inside a building.
    private Point2D currentLocation;
    private Point2D homeLocation;
    private Point2D walkInside;

    // determined when destination is given or when the person is walking back to homeLocation.
    private double distance;

    // current disease state based on SIR dynamics.
    private SIRQState currentSIRQState;

    // used these two countdowns to reduce the overhead of thread.
    private int atDestinationCountDown;
    private int atCommunityCountDown;
    // quarantine countdown will be helpful when a person is infected, its placed into quarantine, when this
    // countdown hits 0, they recover.
    private int quarantineCountDown;
    private BuildingType buildingTypeToGo;
    private Point2D buildingDest;
    private int destID;

    // gives the locationState of a person currently in.
    private PersonLocationState currentLocationState;

    // how contgious the person is, how strong its symptoms are.
    private double sicknessScale;

    // random number generator for waiting random amount of time, whether at community or at destination and generating
    // random destination for a person to walk inside a building.
    private Random rand;

    public Person(int ID, int homeCommunityID, Point2D currentLocation){
        this.ID = ID;
        this.homeCommunityID = homeCommunityID;
        this.currentLocation = currentLocation;
        // save the home location so the person can walk back to home after exiting from the building.
        this.homeLocation = currentLocation;

        // a person is in Susceptible state by default, other defaults.
        this.currentSIRQState = SIRQState.SUSCEPTIBLE;

        // atDestinationCountdown is 0 because by default we are atCommunity. No destination to goto by default.
        this.atDestinationCountDown = 0;
        this.buildingTypeToGo = null;
        this.buildingDest = null;
        this.destID = 0;

        // by default, we are not quarantined.
        this.quarantineCountDown = 0;

        // atCommunityCountDown is randomly set to 1-8 seconds. update() gets called 60fps so, we will multiply our
        // counter by 60. A person will wait randomly at the community before moving towards a destination.
        this.rand = new Random();
        this.atCommunityCountDown = 60 * (rand.nextInt(8) + 1);

        // pick a destination inside community so a person can move in their community while they are inside.
        this.currentLocationState = PersonLocationState.AT_COMMUNITY;
        setWalkInsideBuildingDest();
    }

    public int getID() {
        return ID;
    }

    public int getHomeCommunityID() {
        return homeCommunityID;
    }

    public SIRQState getCurrentSIRQState() {
        return currentSIRQState;
    }

    public void setCurrentSIRQState(SIRQState newSIRQState) {
        this.currentSIRQState = newSIRQState;
    }

    public BuildingType getDestBuildingToGo() {
        return buildingTypeToGo;
    }

    public void setBuildingTypeToGo(BuildingType newDestToGo) {
        this.buildingTypeToGo = newDestToGo;
    }

    public void setBuildingDest(Point2D buildingDestination) {
        this.buildingDest = buildingDestination;
    }

    public int getDestBuildingID() {
        return destID;
    }

    public void setDestBuildingID(int newDestBuildingID) {
        this.destID = newDestBuildingID;
    }

    public PersonLocationState getCurrentLocationState() {
        return currentLocationState;
    }

    public void setLocationState(PersonLocationState newLocationState) {
        this.currentLocationState = newLocationState;
    }

    public void update(PriorityBlockingQueue<Message> messagesQueue) {
        switch (this.currentLocationState) {
            case AT_COMMUNITY:
                // begin decrementing the counter.
                if (this.atCommunityCountDown > 0) {
                    this.atCommunityCountDown--;
                    moveInsideBuilding();
                    messagesQueue.put(new PersonChangedLocation(this.ID, currentLocation));
                    if (this.atCommunityCountDown <= 0) {
                        this.atCommunityCountDown = 0;
                        // make the person go wait for a destination.
                        this.currentLocationState = PersonLocationState.WAITING_FOR_DESTINATION;
                        messagesQueue.put(new PersonWaitingForDestination(this.homeCommunityID,this.ID));
                    }
                }
                break;
            case WALKING:
                // check whether walking towards a building or towards community?
                if (this.buildingDest != null) {
                    // check whether a person has reached closed to dest.
                    if (isCloseToDestination()) {
                        // at the destination, add a random destinationCountDown. The person will randomly be
                        // at the destination for 1-5 seconds.
                        this.currentLocationState = PersonLocationState.AT_DESTINATION;
                        this.atDestinationCountDown = 60 * (rand.nextInt(5) + 1);

                        messagesQueue.put(new EnterBuilding(
                                this.destID, this.buildingTypeToGo, this.ID, this.currentSIRQState, this.sicknessScale));
                    } else {
                        moveTowardsDestination();
                        messagesQueue.put(new PersonChangedLocation(this.ID, this.currentLocation));
                    }
                }
                else {
                    // walking towards the home community.
                    if (isCloseToDestination()) {
                        // at the community. start atCommunityCountDown randomly.
                        // TODO: Check whether the person has been infected? if it has been infected we quarantine them
                        //  inside their community for a little longer.
                        this.currentLocationState = PersonLocationState.AT_COMMUNITY;
                        this.atCommunityCountDown = 60 * (rand.nextInt(8) + 1);
                    }
                    else {
                        moveTowardsDestination();
                        messagesQueue.put(new PersonChangedLocation(this.ID, this.currentLocation));
                    }
                }
                break;
            case WAITING_FOR_DESTINATION:
                // nothing updates, as the person is waiting for a destination to go to.
                break;
            case DESTINATION_GIVEN:
                // destination is given, so start moving/walking in that direction.
                this.currentLocationState = PersonLocationState.WALKING;
                this.distance = buildingDest.distance(currentLocation);
                moveTowardsDestination();
                messagesQueue.put(new PersonChangedLocation(this.ID, this.currentLocation));
                break;
            case AT_DESTINATION:
                // begin decrementing the atDestinationCountDown counter.
                if (this.atDestinationCountDown > 0) {
                    this.atDestinationCountDown--;
                    moveInsideBuilding();
                    messagesQueue.put(new PersonChangedLocation(this.ID, currentLocation));
                    if (this.atDestinationCountDown <= 0) {
                        this.atDestinationCountDown = 0;
                        // we need to exit the building now and start walking back to our home community, change the distance
                        // value now since we are going back home.
                        this.buildingDest = null;
                        this.distance = currentLocation.distance(homeLocation);
                        this.currentLocationState = PersonLocationState.WALKING;

                        messagesQueue.put(new ExitBuilding(this.destID,this.buildingTypeToGo,this.ID,this.currentSIRQState));
                    }
                }
                break;
        }
    }

    /**
     * This method is for walking between destination a to b. It changes its movement speed based
     * on the total distance between the destinations.
     */
    private void moveTowardsDestination() {
        currentLocation = currentLocation.add(
                (buildingDest.getX() - currentLocation.getX()) / distance*2,
                (buildingDest.getY() - currentLocation.getY())/ distance*2);

    }

    /**
     * This method is for moving inside the community and inside destination. It moves
     * slowly and gradually.
     */
    private void moveInsideBuilding() {
        double xInc;
        double yInc;

        if(walkInside.getX()-currentLocation.getX()>=0) {
            xInc = .2;
        }
        else {
            xInc = -.2;
        }
        if(walkInside.getY()-currentLocation.getY()>=0) {
            yInc = .2;
        }
        else {
            yInc = -.2;
        }

        currentLocation = currentLocation.add(xInc, yInc);
    }

    private boolean isCloseToDestination() {
        return currentLocation.getX() < buildingDest.getX() + 1 && currentLocation.getX() > buildingDest.getX() - 1 &&
                currentLocation.getY() > buildingDest.getY() - 1 && currentLocation.getY() < buildingDest.getY() + 1;
    }

    private void setWalkInsideBuildingDest() {
        // check whether walking inside their community or at some other destination?
        switch (this.currentLocationState) {

        }
        if (this.currentLocationState == PersonLocationState.AT_COMMUNITY) {
            Point2D communityCoord = ABMConstants.COMMUNITIES_UPPERLEFT_CORNERS.get(this.homeCommunityID-1);
            double x = rand.nextDouble() * ABMConstants.COMMUNITY_WIDTH + communityCoord.getX();
            double y = rand.nextDouble() * ABMConstants.COMMUNITY_HEIGHT + communityCoord.getY();
            this.walkInside = new Point2D(x, y);
        }
        else {

        }
    }
}
