package abm;

import abm.utils.ABMConstants;
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
        Parameters parameters = getParameters();
        System.out.println(parameters.getUnnamed().get(0));
        this.abm = new ABMController(primaryStage);
        System.out.println(ABMConstants.test);
        ABMConstants.init(Integer.parseInt(parameters.getUnnamed().get(0)));
        System.out.println(ABMConstants.test);
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
