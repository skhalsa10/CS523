package abm.utils.messages;

import javafx.geometry.Point2D;

/**
 * This message is for updating person's location.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PersonChangedLocation extends Message {

    private int personId;
    private Point2D loc;


    public PersonChangedLocation(int personId, Point2D location) {
        this.personId = personId;

        this.loc = new Point2D(location.getX(), location.getY());
    }

    public int getPersonId() {
        return personId;
    }

    public Point2D getLoc() {
        return loc;
    }

}
