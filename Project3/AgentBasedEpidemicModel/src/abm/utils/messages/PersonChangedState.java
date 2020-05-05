package abm.utils.messages;

import abm.utils.SIRQState;

/**
 * This message triggers when a person is asked to tell its current state.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PersonChangedState extends TimeMarker implements Message{

    private SIRQState SIRQState;
    private int personId;

    public PersonChangedState(SIRQState newSIRQState, int personId) {
        this.SIRQState = newSIRQState;
        this.personId = personId;
    }

    public SIRQState getNewState() {
        return SIRQState;
    }

    public int getPersonId() {
        return personId;
    }
}
