package abm.utils;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;

import java.util.ArrayList;

/**
 * This constant class for putting tunable parameters, colors, dimensions for buildings, gui map width,height,etc.
 * It also supports modifying some command line args based on user input.
 * @version 1.0.0
 * @author Anas Gauba & Siri Khalsa
 */
public class ABMConstants {
    public final static double MAP_WIDTH = 0.625*javafx.stage.Screen.getPrimary().getBounds().getMaxX();
    public final static double MAP_HEIGHT = 0.741*javafx.stage.Screen.getPrimary().getBounds().getMaxY();


    public final static double WINDOW_WIDTH = 0.625*javafx.stage.Screen.getPrimary().getBounds().getMaxX();
    public final static double WINDOW_HEIGHT = 0.8333*javafx.stage.Screen.getPrimary().getBounds().getMaxY();

    // circle representing a person.
    public final static double PERSON_RENDER_WIDTH = 0.004166667*MAP_WIDTH;
    public final static double PERSON_RENDER_HEIGHT = PERSON_RENDER_WIDTH;

    // radius, R of a person for disease spread. Representing as a BOX so we don't have to do trig math for circles.
    public final static double INFECTION_RADIUS_BOX = 2*PERSON_RENDER_WIDTH;//tunable by multiplying.

    // how long a person stays in community or other destination. How long it stays in quarantine?
    // default here is person stays at community for 10-25 seconds
    // (USE this formula for calculating min and max values: min = max-min, max = max+min-1).
    public final static int AT_COMMUNITY_MIN = 10;//TUNABLE
    public final static int AT_COMMUNITY_MAX = 16;//TUNABLE

    // default here is person stays at destination for 10-20 seconds.
    public final static int AT_DESTINATION_MIN = 10;//TUNABLE
    public final static int AT_DESTINATION_MAX = 11;//TUNABLE

    // default here is person stays in quarantine for 30-60 seconds.
    public final static int AT_QUARANTINE_MIN = 30;//TUNABLE
    public final static int AT_QUARANTINE_MAX = 31;//TUNABLE

    //default here is person recovers on its own no matter they get quarantined or not. 45-70 seconds.
    // NOTE: people who are above SYMPTOM_SCALE_THRESHOLD WILL get quarantined, the rest can recover on their own.
    public final static int TILL_RECOVERY_MIN = 45;
    public final static int TILL_RECOVERY_MAX = 26;

    // countDown to quarantine check that peopleManager uses. Then it initiates a message to put people to quarantine.
    public final static int COUNTDOWN_TO_QUARANTINE_CHECK = 40;//TUNABLE

    // amount of time to wait until epidemic spreads. By default, 60 seconds.
    public final static int COUNTDOWN_TILL_EPIDEMIC_SPREAD = 60;//TUNABLE

    //this flag will turn on average contagion level in BuildingContagionLevel
    // or turn on max contagion level
    public final static boolean BUILDING_CONTAGION_IS_MAX = false;

    // symptomScale threshold, means we test this percent of people
    public static double SYMPTOM_SCALE_THRESHOLD = 0.1;

    //the variables for the beta distributions
    public static double ALPHA = 2.0;
    public static double BETA = 3.5;

    //Colors
    public final static Color CANVAS_BACKGROUND_COLOR= Color.web("#333333");
    public final static Color COMMUNITY_COLOR= Color.web("#999999");
    public final static Color SUSCEPTIBLE_COLOR = Color.web("#5EF884");
    public final static Color INFECTED_COLOR = Color.web("#954B4A");
    public final static Color RECOVERED_COLOR = Color.web("#406CA3");
    public final static Color QUARANTINED_COLOR = Color.WHITE;
    public final static Color AIRPORT_COLOR = Color.web("#ffdba9");
    public final static Color BUILDING_COLOR = Color.web("#ffdbb9");
    public final static Color RESTAURANT_COLOR = Color.web("#83bbe5");

    //GUI GRAPH CONSTANTS
    public final static int TIME_SLICE_WIDTH = 1;

    // number of communities, and how many people in each community, list of each
    // communities UPPER_LEFT corner.
    public final static int COMMUNITIES = 18;
    public final static int PEOPLE_IN_COMMUNITY = 60;//TUNABLE

    // padding between communities in the gui.
    private final static double PADDING_WIDTH = 10;
    private final static double PADDING_HEIGHT = 15;

    // determines the number of paddings there are among communities (in x and y direction).
    private final static int X_PADDINGS = 7;
    private final static int Y_PADDINGS = 6;

    // number of communities in x and y direction.
    private final static int X_COMMUNITIES = 6;
    private final static int Y_COMMUNITIES = 5;

    public final static double COMMUNITY_WIDTH = (MAP_WIDTH-PADDING_WIDTH*X_PADDINGS)/X_COMMUNITIES;
    public final static double COMMUNITY_HEIGHT = (MAP_HEIGHT-PADDING_HEIGHT*Y_PADDINGS)/Y_COMMUNITIES;

    //lets calculate the center space
    private final static double CENTER_WIDTH =  4*COMMUNITY_WIDTH+3*PADDING_WIDTH;
    private final static double CENTER_HEIGHT =  3*COMMUNITY_HEIGHT+2*PADDING_HEIGHT;

    //airport dimensions and upper left corner
    public final static double AIRPORT_WIDTH = 2*(COMMUNITY_WIDTH/3);
    public final static double AIRPORT_HEIGHT = COMMUNITY_HEIGHT/2+ COMMUNITY_HEIGHT+2*PADDING_HEIGHT;
    public final static Point2D AIRPORT_UPPERLEFT_CORNER = new Point2D(MAP_WIDTH-(2*PADDING_WIDTH)-2*(COMMUNITY_WIDTH/3)-COMMUNITY_WIDTH,COMMUNITY_HEIGHT+2*PADDING_HEIGHT+3*(COMMUNITY_HEIGHT/4));

    //lets calculate the center width without Airport
    private final static double CENTER_WIDTH_NO_AIRPORT = CENTER_WIDTH-PADDING_WIDTH-AIRPORT_WIDTH;

    //lets calculate the BUILDING sizes
    public final static double BUILDING_WIDTH = (CENTER_WIDTH_NO_AIRPORT/3) - 2*PADDING_WIDTH;
    public final static double BUILDING_HEIGHT = COMMUNITY_HEIGHT;
    public final static int BUILDING_CAPACITY = 50;

    public final static Point2D GROCERY1_UPPERLEFT = new Point2D(3*PADDING_WIDTH+COMMUNITY_WIDTH,2*PADDING_HEIGHT+COMMUNITY_HEIGHT);
    public final static Point2D GROCERY2_UPPERLEFT = new Point2D(GROCERY1_UPPERLEFT.getX()+2*BUILDING_WIDTH+2*PADDING_WIDTH,GROCERY1_UPPERLEFT.getY()+2*PADDING_HEIGHT+2*COMMUNITY_HEIGHT);
    public final static Point2D HOSPITAL1_UPPERLEFT = new Point2D(GROCERY1_UPPERLEFT.getX()+2*BUILDING_WIDTH+2*PADDING_WIDTH,GROCERY1_UPPERLEFT.getY());
    public final static Point2D HOSPITAL2_UPPERLEFT = new Point2D(GROCERY1_UPPERLEFT.getX()+BUILDING_WIDTH+PADDING_WIDTH, GROCERY1_UPPERLEFT.getY()+COMMUNITY_HEIGHT+PADDING_HEIGHT) ;
    public final static Point2D HOTEL_UPPERLEFT = new Point2D(GROCERY1_UPPERLEFT.getX(),GROCERY1_UPPERLEFT.getY()+2*PADDING_HEIGHT+2*COMMUNITY_HEIGHT);

    //RESTAURANT buildings
    public final static double RESTAURANT_WIDTH = BUILDING_WIDTH/3;
    public final static double RESTAURANT_HEIGHT = BUILDING_HEIGHT/3;

    public final static ArrayList<Point2D> COMMUNITIES_UPPERLEFT_CORNERS = getCommunitiesUpperleftCorners();
    public final static ArrayList<Point2D> RESTAURANT_UPPERLEFT_CORNERS = getRestaurantUpperleftCorners();

    /**
     * helper class that builds a list of restaurant upper left corners.
     * @return
     */
    private static ArrayList<Point2D> getRestaurantUpperleftCorners() {
        ArrayList<Point2D> upperLeftCorners = new ArrayList<>();

        //top
        double x = GROCERY1_UPPERLEFT.getX()+BUILDING_WIDTH+PADDING_WIDTH;
        double y = GROCERY1_UPPERLEFT.getY();
        addUpperLeftRestaurantPoints(x,y,upperLeftCorners);

        //right
        x = HOSPITAL1_UPPERLEFT.getX();
        y = HOSPITAL1_UPPERLEFT.getY()+BUILDING_HEIGHT+PADDING_HEIGHT;
        addUpperLeftRestaurantPoints(x,y,upperLeftCorners);

        //bottom
        x = HOSPITAL2_UPPERLEFT.getX();
        y = HOSPITAL2_UPPERLEFT.getY()+BUILDING_HEIGHT+PADDING_HEIGHT;
        addUpperLeftRestaurantPoints(x,y,upperLeftCorners);

        //left
        x = GROCERY1_UPPERLEFT.getX();
        y = GROCERY1_UPPERLEFT.getY()+BUILDING_HEIGHT+PADDING_HEIGHT;
        addUpperLeftRestaurantPoints(x,y,upperLeftCorners);

        return upperLeftCorners;
    }

    /**
     * helper for the helper function above to build a list of upper left courners used for the restaurants
     * @param x
     * @param y
     * @param upperLeftCorners
     */
    private static void addUpperLeftRestaurantPoints(double x, double y, ArrayList<Point2D> upperLeftCorners) {
        upperLeftCorners.add(new Point2D(x, y));
        upperLeftCorners.add(new Point2D(x+2*RESTAURANT_WIDTH, y));
        upperLeftCorners.add(new Point2D(x+2*RESTAURANT_WIDTH, y+2*RESTAURANT_HEIGHT));
        upperLeftCorners.add(new Point2D(x, y+2*RESTAURANT_HEIGHT));
    }

    /**
     * this private helper starts at the upperleft community when compared to the prototype
     * and it moves counter clockwise around the edge of the graph update the lcoations to the list
     * @return array list of upper left corners for the communities
     */
    private static ArrayList<Point2D> getCommunitiesUpperleftCorners() {
        ArrayList<Point2D> upperLeftCorners = new ArrayList<>();
        // initial first left community.
        double upperLeftX = PADDING_WIDTH;
        double upperLeftY = PADDING_HEIGHT;

        // go topLeft -> topRight first.
        for (int i = 1; i< X_COMMUNITIES;i++) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftX += COMMUNITY_WIDTH+PADDING_WIDTH;
        }

        // go topRight ->  bottomRight.
        for (int i = 1; i< Y_COMMUNITIES;i++) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftY += COMMUNITY_HEIGHT+PADDING_HEIGHT;
        }


        // go bottomRight -> bottomLeft.
        for (int i = 1; i< X_COMMUNITIES;i++) {
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftX -= COMMUNITY_WIDTH+PADDING_WIDTH;
        }


        // go bottomLeft -> topLeft.
        for (int i = 1; i< Y_COMMUNITIES;i++){
            upperLeftCorners.add(new Point2D(upperLeftX, upperLeftY));
            upperLeftY -= COMMUNITY_HEIGHT+PADDING_HEIGHT;
        }

        return upperLeftCorners;
    }


    /**
     * this will initialize the command line arguments for use in the ABM
     * @param threshold symptom threshold number between 0 and 1
     * @param alpha used for beta distribution in person class
     * @param beta used for beta distribution in Person Class
     */
    public static void setCommandLineArgs(double threshold, double alpha, double beta){
        SYMPTOM_SCALE_THRESHOLD = threshold;
        ALPHA = alpha;
        BETA = beta;

    }
}
