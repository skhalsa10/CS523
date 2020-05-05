package abm.utils.messages;

import abm.utils.SIRQState;
import javafx.geometry.Point2D;

/**
 * This message is for updating person's location.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class NewPerson extends Message {

    private int personId;
    private Point2D loc;
    private SIRQState personSIRQState;


    public NewPerson(SIRQState personSIRQState, int personId, Point2D location) {
        this.personId = personId;
        this.personSIRQState = personSIRQState;
        this.loc = new Point2D(location.getX(), location.getY());
    }

    public int getPersonId() {
        return personId;
    }

    public Point2D getLoc() {
        return loc;
    }

    public SIRQState getPersonSIRQState() {
        return personSIRQState;
    }

}