package abm.utils.messages;

import abm.utils.SIRQState;

/**
 * This message triggers when a person is asked to tell its current state.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PersonChangedState extends Message {

    private SIRQState SIRQState;
    private int personId;
    private int personCommunityId;

    public PersonChangedState(SIRQState newSIRQState, int personId, int personCommunityId) {
        this.SIRQState = newSIRQState;
        this.personId = personId;
        this.personCommunityId = personCommunityId;
    }

    public SIRQState getNewState() {
        return SIRQState;
    }

    public int getPersonId() {
        return personId;
    }

    public int getPersonCommunityId() {
        return personCommunityId;
    }
}
