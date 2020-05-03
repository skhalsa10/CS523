package abm.peopleManager;

import abm.utils.State;
import javafx.geometry.Point2D;


/**
 * This Class encapsulates a Person inside of the Agent Based Epidemic Model.
 *
 * The goal of this class is to encapsulate the bahavior of a person.
 * The person owns a
 */
public class Person {
    private int ID;
    private int homeCommunityID;
    private State currentState;
    private int destinationCountDown;
    private Point2D currentLocation;
    // how contgious the person is, how strong its symptoms are.
    private float sicknessScale;

    public Person(int ID, int homeCommunityID, Point2D currentLocation){
        this.ID = ID;
        this.homeCommunityID = homeCommunityID;
        this.currentLocation = currentLocation;

        // a person is in Susceptible state by default.
        this.currentState = State.SUSCEPTIBLE;
        this.destinationCountDown = 0;
    }

    public State getCurrentState() {
        return currentState;
    }
}
