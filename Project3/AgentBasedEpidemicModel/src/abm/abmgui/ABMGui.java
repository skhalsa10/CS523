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

    @Override
    public void handle(long now) {

    }

    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("Building Manager Shutting down.");
        }
    }
}
