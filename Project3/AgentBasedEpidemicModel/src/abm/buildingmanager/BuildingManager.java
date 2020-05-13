package abm.buildingmanager;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.BuildingType;
import abm.utils.Communicator;
import abm.utils.messages.*;
import javafx.geometry.Point2D;

import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.PriorityBlockingQueue;

import static abm.utils.ABMConstants.*;

/**
 * This class manages the creation of buildings, responding to messages from the Message Passing Protocal.
 * It manages the entering and exiting of buildings and routing the behavior accordingly to the correct buildings
 *
 * This Class ONLY sends messages to the ABMController and as for as it is concerned is unaware of People Behavior.
 *
 *
 * @version 1.0.0
 * @author Siri Khalsa
 *
 * class skeleton by
 * @author Anas Gauba
 */
public class BuildingManager extends Thread implements Communicator {

    private PriorityBlockingQueue<Message> messages;//blocking queue to store messages
    private ABMController abmController;//reference to parent object
    private boolean isRunning; //used to loop in thread run
    private HashMap<Integer, Building> communities;//keeo track of community buildings
    private HashMap<Integer, Building> hotels; //keep track of hotels
    private HashMap<Integer, Building> restaurants; //keep track og restaurants
    private HashMap<Integer, Building> groceryStores; //keep track of grocery stores
    private HashMap<Integer, Building> hospitals; //keep track of hospitals
    private Building airport; //keep track of airport
    private Random random;

    /**
     * lets construct the simple building manager
     *
     * @param abmController The Building Manager requires a
     *                      reference to its parent object to pass messages to
     */
    public BuildingManager(ABMController abmController) {
        //initialize everything!
        this.abmController = abmController;
        this.messages = new PriorityBlockingQueue<>();
        random = new Random();
        this.communities = new HashMap<>();
        initCommunities();
        this.hotels = new HashMap<>();
        initHotels();
        this.restaurants = new HashMap<>();
        initRestaurants();
        this.groceryStores = new HashMap<>();
        initGroceryStores();
        this.hospitals = new HashMap<>();
        initHospitals();
        this.airport = new Building(BUILDING_CAPACITY, BuildingType.AIRPORT,1);

        //start the thread
        this.isRunning = true;
        start();
    }

    /**
     * helper class to initialize hospital buildings
     */
    private void initHospitals() {
        hospitals.put(1,new Building(BUILDING_CAPACITY, BuildingType.HOSPITAL,1));
        hospitals.put(2,new Building(BUILDING_CAPACITY, BuildingType.HOSPITAL,2));
    }
    /**
     * helper class to initialize Grocery Store buildings
     */
    private void initGroceryStores() {
        groceryStores.put(1,new Building(BUILDING_CAPACITY, BuildingType.GROCERY_STORE,1));
        groceryStores.put(2,new Building(BUILDING_CAPACITY, BuildingType.GROCERY_STORE,2));
    }
    /**
     * helper class to initialize Restaurants buildings
     */
    private void initRestaurants() {
        int size = RESTAURANT_UPPERLEFT_CORNERS.size();
        for(int i = 1; i<=size;i++){
            restaurants.put(i,new Building(BUILDING_CAPACITY, BuildingType.RESTURANT,i));
        }
    }
    /**
     * helper class to initialize Hotels buildings
     */
    private void initHotels() {
        hotels.put(1,new Building(BUILDING_CAPACITY, BuildingType.HOTEL,1));
    }
    /**
     * helper class to initialize Communities buildings
     */
    private void initCommunities() {
        int size = COMMUNITIES_UPPERLEFT_CORNERS.size();
        for(int i = 1; i<=size;i++){
            communities.put(i,new Building(PEOPLE_IN_COMMUNITY, BuildingType.COMMUNITY,i));
        }
    }

    /**
     * Puts a message into the priority blocking queue sent by other objects.
     * @param m message to put in queue.
     */
    @Override
    public void sendMessage(Message m) {
        this.messages.put(m);
    }

    /**
     * This buildingManager thread takes a messages from its priority blocking queue and processes them when it gets
     * a chance. If waiting is necessary for the message to become available, it waits, then processes the message.
     */
    @Override
    public void run() {
        while (isRunning) {
            try {
                Message m = this.messages.take();
                processMessage(m);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Processes different messages that are passed from the ABMController or Building.
     * @param m message to process.
     */
    private synchronized void processMessage(Message m) {
        //shutdown this thread
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("Building Manager Shutting down.");
        }
        else if(m instanceof PersonWaitingForDestination){
            PersonWaitingForDestination m2 = (PersonWaitingForDestination)m;

            DestinationForPerson messageToSend = getRandomDestination(m2);
            abmController.sendMessage(messageToSend);
        }
        else if(m instanceof EnterBuilding){
            EnterBuilding m2 = (EnterBuilding)m;
            processEnterBuildingMessage(m2);
        }
        else if(m instanceof ExitBuilding){
            ExitBuilding m2 = (ExitBuilding)m;
            BuildingContagionLevel mToSend =  processExitBuildingMessage(m2);
            if(mToSend!= null) {
                abmController.sendMessage(mToSend);
            }
        }
        else {
            System.out.println("error BuildingManager processMessage");
        }
    }

    /**
     * Here we process the ExitBuilding Message. We parse the message so we
     * can call the correct Building.exitMessage()
     * @param m
     * @return
     */
    private BuildingContagionLevel processExitBuildingMessage(ExitBuilding m) {
        switch (m.getBuildingType()){
            case GROCERY_STORE:
                return groceryStores.get(m.getBuildingId()).exitBuilding(m);
            case HOTEL:
                return hotels.get(m.getBuildingId()).exitBuilding(m);
            case AIRPORT:
                return airport.exitBuilding(m);
            case HOSPITAL:
                return hospitals.get(m.getBuildingId()).exitBuilding(m);
            case RESTURANT:
                return restaurants.get(m.getBuildingId()).exitBuilding(m);
            case COMMUNITY:
                System.out.println("error in processExitBuildingMessage in buildingManager");
                break;
        }
        System.out.println("Returning NUll here should be an error");
        return null;
    }

    /**
     * this will process the EnterBuilding message to do this we
     * parse the message and find the Building being entered and call the enterbuilding function on it.
     * @param m
     */
    private void processEnterBuildingMessage(EnterBuilding m) {
        switch (m.getBuildingType()){
            case GROCERY_STORE:
                groceryStores.get(m.getBuildingId()).enterBuilding(m.getPersonId(),m.getPersonState(),m.getSymptomScale());
                break;
            case HOTEL:
                hotels.get(m.getBuildingId()).enterBuilding(m.getPersonId(),m.getPersonState(),m.getSymptomScale());
                break;
            case AIRPORT:
                airport.enterBuilding(m.getPersonId(),m.getPersonState(),m.getSymptomScale());
                break;
            case HOSPITAL:
                hospitals.get(m.getBuildingId()).enterBuilding(m.getPersonId(),m.getPersonState(),m.getSymptomScale());
                break;
            case RESTURANT:
                restaurants.get(m.getBuildingId()).enterBuilding(m.getPersonId(),m.getPersonState(),m.getSymptomScale());
                break;
            case COMMUNITY:
                System.out.println("error in processEnterBuildingMessage in buildingManager");
                break;
        }
    }

    /**
     * this will find a random destination for a person requesting it.
     * @param m
     * @return DestionationForPerson Message
     */
    private DestinationForPerson getRandomDestination(PersonWaitingForDestination m) {
        //get the building type:
        BuildingType[] buildingTypes = BuildingType.values();
        BuildingType type = buildingTypes[random.nextInt(5)];
        //get the id and random coordinate inside of building
        int id;
        Point2D location;
        Point2D coordinate;
        double xMinBound;
        double xMaxBound;
        double yMinBound;
        double yMaxBound;
        if(type == BuildingType.AIRPORT||type == BuildingType.HOTEL){
            id = 1;
            if(type == BuildingType.AIRPORT) {
                coordinate = AIRPORT_UPPERLEFT_CORNER;
            }else{
                coordinate = HOTEL_UPPERLEFT;
            }
            xMinBound = coordinate.getX() + 5;
            yMinBound = coordinate.getY() + 5;
            if(type == BuildingType.AIRPORT){
                xMaxBound = coordinate.getX() + AIRPORT_WIDTH- 5;
                yMaxBound = coordinate.getY() + AIRPORT_HEIGHT - 5;
            }else{
                xMaxBound = coordinate.getX() + COMMUNITY_WIDTH - 5;
                yMaxBound = coordinate.getY() + COMMUNITY_HEIGHT - 5;
            }



        } else if(type == BuildingType.RESTURANT){
            id = random.nextInt(restaurants.size())+1;
            coordinate = RESTAURANT_UPPERLEFT_CORNERS.get(id-1);
            xMinBound = coordinate.getX() + 5;
            xMaxBound = coordinate.getX() + COMMUNITY_WIDTH - 5;
            yMinBound = coordinate.getY() + 5;
            yMaxBound = coordinate.getY() + COMMUNITY_HEIGHT - 5;
        }else{
            id = random.nextInt(2)+1;
            if(id ==1){
                if(type == BuildingType.GROCERY_STORE){
                    coordinate = GROCERY1_UPPERLEFT;
                }else{
                    coordinate = HOSPITAL1_UPPERLEFT;
                }
            }else{
                if(type == BuildingType.GROCERY_STORE){
                    coordinate = GROCERY2_UPPERLEFT;
                }else{
                    coordinate = HOSPITAL2_UPPERLEFT;
                }
            }

            xMinBound = coordinate.getX() + 5;
            xMaxBound = coordinate.getX() + ABMConstants.COMMUNITY_WIDTH - 5;
            yMinBound = coordinate.getY() + 5;
            yMaxBound = coordinate.getY() + ABMConstants.COMMUNITY_HEIGHT - 5;
        }

        location = new Point2D(xMinBound + (xMaxBound - xMinBound) * random.nextDouble(),
                yMinBound + (yMaxBound - yMinBound) * random.nextDouble());
        //now create the message from collected data above
        DestinationForPerson m2 = new DestinationForPerson(m.getCommunityID(),m.getPersonID(),id,type,location);
        return m2;
    }
}
