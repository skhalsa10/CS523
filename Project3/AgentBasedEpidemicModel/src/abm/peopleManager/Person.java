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
 * The goal of this class is to encapsulate the behavior of a person.
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
    private int buildingDestID;

    // gives the locationState of a person currently in.
    private PersonLocationState currentLocationState;

    // how contagious the person is, how strong its symptoms are.
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
        this.buildingDestID = 0;

        // by default, we are not quarantined and a person is not sick.
        this.quarantineCountDown = 0;
        this.sicknessScale = 0;

        // atCommunityCountDown is randomly set to 10-25 seconds. update() gets called 60fps so, we will multiply our
        // counter by 60. A person will wait randomly at the community before moving towards a destination.
        this.rand = new Random();
        this.atCommunityCountDown = 60 * (rand.nextInt(16) + 10);

        // pick a destination inside community so a person can move in their community while they are inside.
        this.currentLocationState = PersonLocationState.AT_COMMUNITY;
        setWalkInsideCommunity();
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

    public void setSicknessScale(double sicknessLevel) {
        this.sicknessScale = sicknessLevel;
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
        return buildingDestID;
    }

    public void setDestBuildingID(int newDestBuildingID) {
        this.buildingDestID = newDestBuildingID;
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
                    // check whether a person has reached close to destination building.
                    if (isCloseToDestination(buildingDest)) {
                        // at the destination, add a random destinationCountDown. The person will randomly be
                        // at the destination for 10-20 seconds.
                        this.currentLocationState = PersonLocationState.AT_DESTINATION;
                        this.atDestinationCountDown = 60 * (rand.nextInt(11) + 10);

                        // now that we have reached the destination, check to see which building we are inside? so we can
                        // keep walking inside the building while we are there.
                        checkBuildingToWalkInsideTo();

                        messagesQueue.put(new EnterBuilding(
                                this.buildingDestID, this.buildingTypeToGo, this.ID, this.currentSIRQState, this.sicknessScale));
                    } else {
                        moveTowardsDestination(buildingDest);
                        messagesQueue.put(new PersonChangedLocation(this.ID, this.currentLocation));
                    }
                }
                else {
                    // walking towards the home community.
                    if (isCloseToDestination(homeLocation)) {
                        // at the community. start atCommunityCountDown randomly.
                        // TODO: Check whether the person has been infected? if it has been infected we quarantine them
                        //  inside their community for a little longer.
                        this.currentLocationState = PersonLocationState.AT_COMMUNITY;
                        this.atCommunityCountDown = 60 * (rand.nextInt(16) + 10);

                        // now we walk inside the community while we are there.
                        setWalkInsideCommunity();
                    }
                    else {
                        moveTowardsDestination(homeLocation);
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
                moveTowardsDestination(buildingDest);
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

                        messagesQueue.put(new ExitBuilding(this.buildingDestID,this.buildingTypeToGo,this.ID,this.currentSIRQState));
                    }
                }
                break;
        }
    }

    /**
     * This method is for walking between destination a to b, either from community -> dest, vice versa.
     * It changes its movement speed based on the total distance between the destinations.
     * @param walkDest either buildingDest or homeLocation.
     */
    private void moveTowardsDestination(Point2D walkDest) {
        currentLocation = currentLocation.add(
                (walkDest.getX() - currentLocation.getX()) / distance*2,
                (walkDest.getY() - currentLocation.getY())/ distance*2);

    }
    
    /**
     * This method is for moving inside the community and inside destination. It moves
     * slowly and gradually.
     */
    private void moveInsideBuilding() {
        double xInc;
        double yInc;

        if(walkInside.getX()-currentLocation.getX()>=0) {
            xInc = .1;
        }
        else {
            xInc = -.1;
        }
        if(walkInside.getY()-currentLocation.getY()>=0) {
            yInc = .1;
        }
        else {
            yInc = -.1;
        }

        currentLocation = currentLocation.add(xInc, yInc);
    }

    /**
     * This method checks for whether a person is close to reaching their dest?
     * @param dest home or other building.
     * @return T/F whether person is close to reaching destination.
     */
    private boolean isCloseToDestination(Point2D dest) {
        return currentLocation.getX() < dest.getX() + 1 && currentLocation.getX() > dest.getX() - 1 &&
                currentLocation.getY() > dest.getY() - 1 && currentLocation.getY() < dest.getY() + 1;
    }

    private void setWalkInsideCommunity() {
        Point2D communityLocation = ABMConstants.COMMUNITIES_UPPERLEFT_CORNERS.get(this.homeCommunityID-1);
        double x = rand.nextDouble() * ABMConstants.COMMUNITY_WIDTH + communityLocation.getX();
        double y = rand.nextDouble() * ABMConstants.COMMUNITY_HEIGHT + communityLocation.getY();
        this.walkInside = new Point2D(x, y);
    }

    private void checkBuildingToWalkInsideTo() {
        double x;
        double y;

        switch (this.buildingTypeToGo) {
            case AIRPORT:
                // there is only one airport.
                x = rand.nextDouble() * ABMConstants.AIRPORT_WIDTH + ABMConstants.AIRPORT_UPPERLEFT_CORNER.getX();
                y = rand.nextDouble() * ABMConstants.AIRPORT_HEIGHT + ABMConstants.AIRPORT_UPPERLEFT_CORNER.getY();
                this.walkInside = new Point2D(x, y);
                break;
            case GROCERY_STORE:
                // there are only two grocery stores.
                if (buildingDestID == 1) {
                    x = rand.nextDouble() * ABMConstants.BUILDING_WIDTH + ABMConstants.GROCERY1_UPPERLEFT.getX();
                    y = rand.nextDouble() * ABMConstants.BUILDING_HEIGHT + ABMConstants.GROCERY1_UPPERLEFT.getY();
                    this.walkInside = new Point2D(x, y);
                }
                else {
                    x = rand.nextDouble() * ABMConstants.BUILDING_WIDTH + ABMConstants.GROCERY2_UPPERLEFT.getX();
                    y = rand.nextDouble() * ABMConstants.BUILDING_HEIGHT + ABMConstants.GROCERY2_UPPERLEFT.getY();
                    this.walkInside = new Point2D(x, y);
                }
                break;
            case HOSPITAL:
                // there are only two hospitals.
                if (buildingDestID == 1) {
                    x = rand.nextDouble() * ABMConstants.BUILDING_WIDTH + ABMConstants.HOSPITAL1_UPPERLEFT.getX();
                    y = rand.nextDouble() * ABMConstants.BUILDING_HEIGHT + ABMConstants.HOSPITAL1_UPPERLEFT.getY();
                    this.walkInside = new Point2D(x, y);
                }
                else {
                    x = rand.nextDouble() * ABMConstants.BUILDING_WIDTH + ABMConstants.HOSPITAL2_UPPERLEFT.getX();
                    y = rand.nextDouble() * ABMConstants.BUILDING_HEIGHT + ABMConstants.HOSPITAL2_UPPERLEFT.getY();
                    this.walkInside = new Point2D(x, y);
                }
                break;
            case HOTEL:
                // there is only one hotel.
                x = rand.nextDouble() * ABMConstants.BUILDING_WIDTH + ABMConstants.HOTEL_UPPERLEFT.getX();
                y = rand.nextDouble() * ABMConstants.BUILDING_HEIGHT + ABMConstants.HOTEL_UPPERLEFT.getY();
                this.walkInside = new Point2D(x, y);
                break;
            case RESTURANT:
                // look for which restaurant the person is going.
                Point2D restaurantLocation = ABMConstants.RESTAURANT_UPPERLEFT_CORNERS.get(this.buildingDestID-1);
                x = rand.nextDouble() * ABMConstants.RESTAURANT_WIDTH + restaurantLocation.getX();
                y = rand.nextDouble() * ABMConstants.RESTAURANT_HEIGHT + restaurantLocation.getY();
                this.walkInside = new Point2D(x, y);
                break;
        }
    }
}
