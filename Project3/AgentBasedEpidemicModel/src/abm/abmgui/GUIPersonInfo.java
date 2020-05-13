package abm.abmgui;

import abm.utils.SIRQState;
import javafx.geometry.Point2D;

/**
 * keeps track of the SIRQState and location of a person so the gui can represent it on the graph
 */
public class GUIPersonInfo {

    private SIRQState personSIRQState;
    private Point2D location;

    public GUIPersonInfo(SIRQState personSIRQState, Point2D location){
        this.personSIRQState = personSIRQState;
        this.location = location;
    }

    /**
     *
     * @return the SIRQState
     */
    public SIRQState getPersonSIRQState() {
        return personSIRQState;
    }

    /**
     *
     * @return the location
     */
    public Point2D getLocation() {
        return location;
    }

    /**
     * set the SIRQState
     * @param personSIRQState
     */
    public void setPersonSIRQState(SIRQState personSIRQState) {
        this.personSIRQState = personSIRQState;
    }

    /**
     * set the location
     * @param location
     */
    public void setLocation(Point2D location) {
        this.location = location;
    }
}
