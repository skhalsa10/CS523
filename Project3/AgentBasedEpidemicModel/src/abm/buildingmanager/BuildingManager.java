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
 * @version 1.0.0
 * @author Anas Gauba
 */
public class BuildingManager extends Thread implements Communicator {

    private PriorityBlockingQueue<Message> messages;
    private ABMController abmController;
    private boolean isRunning;
    private HashMap<Integer, Building> communities;
    private HashMap<Integer, Building> hotels;
    private HashMap<Integer, Building> restaurants;
    private HashMap<Integer, Building> groceryStores;
    private HashMap<Integer, Building> hospitals;
    private Building airport;
    private Random random;

    public BuildingManager(ABMController abmController) {
        this.abmController = abmController;
        this.messages = new PriorityBlockingQueue<>();
        random = new Random();
        //TODO: Instantiate child classes here, other relevant stuff.
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
        this.airport = new Building(100, BuildingType.AIRPORT,1);

        this.isRunning = true;
        start();
    }

    private void initHospitals() {
        hospitals.put(1,new Building(50, BuildingType.HOSPITAL,1));
        hospitals.put(2,new Building(50, BuildingType.HOSPITAL,2));
    }

    private void initGroceryStores() {
        groceryStores.put(1,new Building(50, BuildingType.GROCERY_STORE,1));
        groceryStores.put(2,new Building(50, BuildingType.GROCERY_STORE,2));
    }

    private void initRestaurants() {
        int size = RESTAURANT_UPPERLEFT_CORNERS.size();
        for(int i = 1; i<=size;i++){
            //TODO capacity should be a constant
            restaurants.put(i,new Building(50, BuildingType.RESTURANT,i));
        }
    }

    private void initHotels() {
        hotels.put(1,new Building(50, BuildingType.HOTEL,1));
    }

    private void initCommunities() {
        int size = COMMUNITIES_UPPERLEFT_CORNERS.size();
        for(int i = 1; i<=size;i++){
            //TODO capacity should be a constant
            communities.put(i,new Building(50, BuildingType.COMMUNITY,i));
        }
    }

    @Override
    public void sendMessage(Message m) {
        this.messages.put(m);
    }

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

    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("Building Manager Shutting down.");
        }
        else if(m instanceof PersonWaitingForDestination){
            PersonWaitingForDestination m2 = (PersonWaitingForDestination)m;

            DestinationForPerson messageToSend = getRandomDestination(m2);
            abmController.sendMessage(m2);
        }
        else if(m instanceof EnterBuilding){

        }
        else if(m instanceof ExitBuilding){

        }
        else {
            System.out.println("error BuildingManager processMessage");
        }
    }

    private DestinationForPerson getRandomDestination(PersonWaitingForDestination m) {
        BuildingType[] buildingTypes = BuildingType.values();
        BuildingType type = buildingTypes[random.nextInt(5)];
        int id;
        Point2D location;
        Point2D coordinate;
        double xMinBound;
        double xMaxBound;
        double yMinBound;
        double yMaxBound;
        if(type == BuildingType.AIRPORT||type == BuildingType.HOTEL){
            id = 1;
            coordinate = AIRPORT_UPPERLEFT_CORNER;
            xMinBound = coordinate.getX() + 5;
            xMaxBound = coordinate.getX() + ABMConstants.COMMUNITY_WIDTH - 5;
            yMinBound = coordinate.getY() + 5;
            yMaxBound = coordinate.getY() + ABMConstants.COMMUNITY_HEIGHT - 5;
        } else if(type == BuildingType.RESTURANT){
            id = random.nextInt(restaurants.size())+1;
            coordinate = RESTAURANT_UPPERLEFT_CORNERS.get(id);
            xMinBound = coordinate.getX() + 5;
            xMaxBound = coordinate.getX() + ABMConstants.COMMUNITY_WIDTH - 5;
            yMinBound = coordinate.getY() + 5;
            yMaxBound = coordinate.getY() + ABMConstants.COMMUNITY_HEIGHT - 5;
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

        DestinationForPerson m2 = new DestinationForPerson(m.getCommunityID(),m.getPersonID(),id,type,location);
        return m2;
    }
}
