package abm.utils.messages;

import javafx.geometry.Point2D;

public class UpdateLocation implements Message {

    private int personId;
    private Point2D loc;

    public UpdateLocation(int personId, Point2D location) {
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
