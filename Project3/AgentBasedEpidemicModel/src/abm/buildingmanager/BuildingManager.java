package abm.buildingmanager;

import abm.ABMController;
import abm.utils.Communicator;
import abm.utils.messages.Message;
import abm.utils.messages.Shutdown;

import java.util.HashMap;
import java.util.concurrent.PriorityBlockingQueue;

/**
 * @version 1.0.0
 * @author Anas Gauba
 */
public class BuildingManager extends Thread implements Communicator {

    private PriorityBlockingQueue<Message> messages;
    private ABMController abmController;
    private boolean isRunning;
    private HashMap<Integer, Community> communities;
    private HashMap<Integer, Hotel> hotels;
    private HashMap<Integer, Resturant> restaurants;
    private HashMap<Integer, GroceryStore> groceryStores;
    private HashMap<Integer, Hospital> hospitals;

    public BuildingManager(ABMController abmController) {
        this.abmController = abmController;
        this.messages = new PriorityBlockingQueue<>();
        //TODO: Instantiate child classes here, other relevant stuff.
        this.communities = new HashMap<>();
        this.hotels = new HashMap<>();
        this.restaurants = new HashMap<>();
        this.groceryStores = new HashMap<>();
        this.hospitals = new HashMap<>();

        this.isRunning = true;
        start();
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
    }
}
