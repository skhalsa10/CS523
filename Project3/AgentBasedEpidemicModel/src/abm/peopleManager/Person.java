package abm.peopleManager;

import abm.utils.Location;
import abm.utils.State;

/**
 * This Class encapsulates a Person inside of the Agent Based Epidemic Model.
 *
 * The goal of this class is to encapsulate the bahavior of a person.
 * The person is a member of a community that exists in the world. It starts
 *
 * @author Siri
 * @author Anas
 */
public class Person {
    //declare all Person related variables below
    private int ID;
    private int homeCommunityID;
    private Location location;
    private State state;
    private int destCountdown;


    public Person(int ID, int homeCommunityID, Location location){
        //initialize parameters
        this.ID = ID;
        this.homeCommunityID = homeCommunityID;
        this.location = location;

        //default values below
        this.state = State.SUSCEPTIBLE;
        this.destCountdown = 0;
    }

    public Location getLocation() {
        return location;
    }
}
