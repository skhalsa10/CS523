package abm.abmgui;

import abm.ABMController;
import abm.utils.Communicator;
import abm.utils.messages.*;
import javafx.animation.AnimationTimer;
import javafx.stage.Stage;

import java.util.concurrent.PriorityBlockingQueue;

/**
 * The GUI class to show the simulation of ABM epidemic spread.
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class ABMGui extends AnimationTimer implements Runnable, Communicator {

    private Stage stage;
    private PriorityBlockingQueue<Message> messages;
    private boolean isRunning;
    private Screen currentScreen;

    private long lastUpdate = 0;//used to update 60 frames per second

    public ABMGui(Stage primaryStage, ABMController abmController) {
        this.stage = primaryStage;
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

    /**
     * This function comes from overriding the animation timer.
     * We want this to be called 60 frames a second. it will update the
     * drawing on the canvas.
     * @param now
     */
    @Override
    public void handle(long now) {
        //there are 1000 miliseconds in a second. if we divide this by 60 there
        // are 16.666667 ms between frame draws
        if (now - lastUpdate >= 16_667_000) {

            if(currentScreen == Screen.GRAPH){
                renderGraphScreen();

            } else {
                renderMainScreen();
            }
            // helped to stabalize the rendor time
            lastUpdate = now;
        }
    }

    private void renderGraphScreen() {
        //TODO - render the graph screen here. this will display the curve
    }

    private void renderMainScreen() {
        //TODO - render the main screen here
    }

    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("Building Manager Shutting down.");
        }
    }
}
