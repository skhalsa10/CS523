package abm.utils.messages;

import abm.utils.State;

/**
 * This message triggers when a person is asked to tell its current state.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PersonChangedState implements Message {

    private State state;
    private int personId;

    public PersonChangedState(State newState, int personId) {
        this.state = newState;
        this.personId = personId;
    }

    public State getNewState() {
        return state;
    }

    public int getPersonId() {
        return personId;
    }
}
