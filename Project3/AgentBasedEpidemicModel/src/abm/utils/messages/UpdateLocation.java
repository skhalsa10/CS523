package abm.utils.messages;

import abm.utils.State;
import javafx.geometry.Point2D;

/**
 * This message is for updating person's location.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class UpdateLocation implements Message {

    private int personId;
    private Point2D loc;
    private State personState;

    public UpdateLocation(State personState, int personId, Point2D location) {
        this.personId = personId;
        this.personState = personState;
        this.loc = new Point2D(location.getX(), location.getY());
    }

    public int getPersonId() {
        return personId;
    }

    public Point2D getLoc() {
        return loc;
    }

    public State getPersonState() {
        return personState;
    }
}
