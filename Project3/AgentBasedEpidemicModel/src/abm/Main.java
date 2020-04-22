package abm;

import abm.utils.messages.Shutdown;
import javafx.application.Application;
import javafx.stage.Stage;

/**
 * This class is entry point for javafx, initializes the controller class as well.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class Main extends Application {

    private ABMController abm;

    @Override
    public void start(Stage primaryStage) throws Exception {
        this.abm = new ABMController(primaryStage);
    }

    @Override
    public void stop() throws Exception {
        System.out.println("Main shutting down");
        this.abm.sendMessage(new Shutdown());
    }

    public static void main(String[] args) {
        launch(args);
    }
}
