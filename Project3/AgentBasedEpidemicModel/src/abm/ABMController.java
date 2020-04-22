package abm;

import abm.abmgui.ABMGui;
import abm.buildingmanager.BuildingManager;
import abm.peopleManager.PeopleManager;
import abm.utils.Communicator;
import abm.utils.messages.Message;
import abm.utils.messages.Shutdown;
import javafx.stage.Stage;

import java.util.concurrent.PriorityBlockingQueue;

/**
 * Main controller class, Agent Based Model (ABM) for simulating the
 * exploration of epidemic spread among the population in communities.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class ABMController extends Thread implements Communicator {

    private PriorityBlockingQueue<Message> messages;
    private boolean isRunning;
    private PeopleManager peopleManager;
    private BuildingManager buildingManager;
    private ABMGui gui;

    public ABMController(Stage primaryStage) {
        this.messages = new PriorityBlockingQueue<>();
        this.peopleManager = new PeopleManager(this);
        this.buildingManager = new BuildingManager(this);
        this.gui = new ABMGui(primaryStage, this);
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
            this.peopleManager.sendMessage(m);
            this.buildingManager.sendMessage(m);
            this.gui.sendMessage(m);
            this.isRunning = false;
            System.out.println("ABM Controller Shutting down.");
        }
    }
}
