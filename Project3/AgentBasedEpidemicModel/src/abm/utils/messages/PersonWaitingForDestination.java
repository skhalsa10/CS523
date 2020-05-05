package abm.utils.messages;

/**
 * This message triggers when a person from community x is waiting for a destination to go to.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PersonWaitingForDestination extends Message {

    private int personID;
    private int communityID;

    public PersonWaitingForDestination(int communityID, int personID) {
        this.communityID = communityID;
        this.personID = personID;
    }

    public int getCommunityID() {
        return communityID;
    }

    public int getPersonID() {
        return personID;
    }
}
