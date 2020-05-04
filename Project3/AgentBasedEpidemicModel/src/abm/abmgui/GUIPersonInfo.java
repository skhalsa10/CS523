package abm.abmgui;

import abm.utils.SIRQState;
import javafx.geometry.Point2D;

public class GUIPersonInfo {

    private SIRQState personSIRQState;
    private Point2D location;

    public GUIPersonInfo(SIRQState personSIRQState, Point2D location){
        this.personSIRQState = personSIRQState;
        this.location = location;
    }

    public SIRQState getPersonSIRQState() {
        return personSIRQState;
    }

    public Point2D getLocation() {
        return location;
    }

    public void setPersonSIRQState(SIRQState personSIRQState) {
        this.personSIRQState = personSIRQState;
    }

    public void setLocation(Point2D location) {
        this.location = location;
    }
}
