package abm.utils;

/**
 * represents a location in 2d space
 * @version 1
 * @author Siri
 */
public class Location
{
    double x;
    double y;

    public Location(double x, double y){
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public Location getCopy(){
        return new Location(this.x, this.y);
    }
}
