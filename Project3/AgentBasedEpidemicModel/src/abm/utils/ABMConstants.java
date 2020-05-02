package abm.utils;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;

import java.util.ArrayList;

public class ABMConstants {
    public final static int MAP_WIDTH = 1200;
    public final static int MAP_HEIGHT = 800;

    public final static int WINDOW_WIDTH = 1200;
    public final static int WINDOW_HEIGHT = 900;

    //Colors
    public final static Color CANVAS_BACKGROUND= Color.web("#333333");
    public final static Color SUSCEPTIBLE = Color.web("#5EF884");
    public final static Color INFECTED = Color.web("#954B4A");
    public final static Color RECOVERED = Color.web("#406CA3");

    //GUI GRAPH CONSTANTS
    public final static int TIME_SLICE_WIDTH = 2;

    // number of communities, and how many people in each community, list of each
    // communities UPPER_LEFT corner.
    public final static int COMMUNITIES = 18;
    public final static int PEOPLE_IN_COMMUNITY = 20;
    public final static int TOTAL_NUMBER_OF_PEOPLE = COMMUNITIES*PEOPLE_IN_COMMUNITY;

    // padding between communities in the gui.
    private final static double PADDING_WIDTH = 10;
    private final static double PADDING_HEIGHT = 10;

    // determines the number of paddings there are among communities (in x and y direction).
    private final static int X_PADDINGS = 7;
    private final static int Y_PADDINGS = 6;

    // number of communities in x and y direction.
    private final static int X_COMMUNITIES = 6;
    private final static int Y_COMMUNITIES = 5;

    public final static double COMMUNITY_WIDTH = (MAP_WIDTH-PADDING_WIDTH*X_PADDINGS)/X_COMMUNITIES;
    public final static double COMMUNITY_HEIGHT = (MAP_HEIGHT-PADDING_HEIGHT*Y_PADDINGS)/Y_COMMUNITIES;

    public final static ArrayList<Point2D> COMMUNITIES_UPPERLEFT_CORNERS = getCommunitiesUpperleftCorners();

    private static ArrayList<Point2D> getCommunitiesUpperleftCorners() {
        ArrayList<Point2D> upperLeftCorners = new ArrayList<>();
        // initial first left community.
        double upperLeftX = PADDING_WIDTH;
        double upperLeftY = PADDING_HEIGHT;

        // go topLeft -> topRight first.
        while (upperLeftX != MAP_WIDTH-(COMMUNITY_WIDTH+PADDING_WIDTH)) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftX += COMMUNITY_WIDTH+PADDING_WIDTH;
        }
        // go topRight ->  bottomRight.
        while (upperLeftY != MAP_HEIGHT-(COMMUNITY_HEIGHT+PADDING_HEIGHT)) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftY += COMMUNITY_HEIGHT+PADDING_HEIGHT;
        }
        // go bottomRight -> bottomLeft.
        while (upperLeftX != PADDING_WIDTH) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftX -= COMMUNITY_WIDTH+PADDING_WIDTH;
        }
        // go bottomLeft -> topLeft.
        while (upperLeftY != PADDING_HEIGHT) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftY -= COMMUNITY_HEIGHT+PADDING_HEIGHT;
        }
        return upperLeftCorners;
    };
}
