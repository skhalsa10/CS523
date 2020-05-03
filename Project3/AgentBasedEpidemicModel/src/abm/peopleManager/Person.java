package abm.peopleManager;

import abm.utils.BuildingType;
import abm.utils.PersonLocationState;
import abm.utils.SIRQState;
import abm.utils.messages.Message;
import abm.utils.messages.PersonWaitingForDestination;
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
    private Point2D currentLocation;

    // current disease state based on SIR dynamics.
    private SIRQState currentSIRQState;

    // used these two countdowns to reduce the overhead of thread.
    private int atDestinationCountDown;
    private int atCommunityCountDown;
    private BuildingType buildingTypeToGo;
    private Point2D buildingDest;
    private int destID;

    // gives the locationState of a person currently in.
    private PersonLocationState currentLocationState;

    // how contgious the person is, how strong its symptoms are.
    private float sicknessScale;

    // random number generator for waiting random amount of time, whether at community or at destination.
    private Random randomTime;

    public Person(int ID, int homeCommunityID, Point2D currentLocation){
        this.ID = ID;
        this.homeCommunityID = homeCommunityID;
        this.currentLocation = currentLocation;

        // a person is in Susceptible state by default, other defaults.
        this.currentSIRQState = SIRQState.SUSCEPTIBLE;

        // atDestinationCountdown is 0 because by default we are atCommunity. No destination to goto by default.
        this.atDestinationCountDown = 0;
        this.buildingTypeToGo = null;
        this.buildingDest = null;
        this.destID = 0;

        // atCommunityCountDown is randomly set to 1-8 seconds. update() gets called 60fps so, we will multiply our
        // counter by 60. A person will wait randomly at the community before moving towards a destination.
        this.randomTime = new Random();
        this.atCommunityCountDown = 60 * (randomTime.nextInt(8) + 1);

        this.currentLocationState = PersonLocationState.AT_COMMUNITY;
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
                    if (this.atCommunityCountDown <= 0) {
                        this.atCommunityCountDown = 0;
                        // make the person go wait for a destination.
                        this.currentLocationState = PersonLocationState.WAITING_FOR_DESTINATION;
                        messagesQueue.put(new PersonWaitingForDestination(this.homeCommunityID,this.ID));
                    }
                }
                break;
            case WALKING:
                break;
            case WAITING_FOR_DESTINATION:
                // nothing updates, as the person is waiting for a destination to go to.
                break;
            case DESTINATION_GIVEN:
                // destination is given, so start moving in that direction.
                break;
            case AT_DESTINATION:

                break;


        }
    }

    private Point2D move() {
        return null;
    }
}
