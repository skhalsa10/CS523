package abm;

import abm.utils.ABMConstants;
import abm.utils.messages.Shutdown;
import javafx.application.Application;
import javafx.stage.Stage;

import java.util.List;


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
        List<String> args = parameters.getUnnamed();
        int argsSize = args.size();
        if(argsSize == 0){
            ABMConstants.setCommandLineArgs(.4,2.0,3.5);
        }else if(argsSize==1){
            ABMConstants.setCommandLineArgs(Double.parseDouble(args.get(0)),2.0,3.5);
        }else if(argsSize == 3){
            ABMConstants.setCommandLineArgs(Double.parseDouble(args.get(0)),
                    Double.parseDouble(args.get(1)),
                    Double.parseDouble(args.get(2)));
        }else{
            printInstructions();
            System.exit(1);
        }
        System.out.println(ABMConstants.SYMPTOM_SCALE_THRESHOLD);
        System.out.println(ABMConstants.ALPHA);
        System.out.println(ABMConstants.BETA);
        this.abm = new ABMController(primaryStage);


    }

    private void printInstructions() {
        System.out.println("Agent Based Epidemic Model Help - " +
                "ABEM can be launched in three ways ways:\n\n" +
                "1. java -jar ABEM \n" +
                "2. java -jar mobileAgents [Symptom_Scale_Threshold]\n" +
                "3. java -jar mobileAgents [Symptom_Scale_Threshold] [ALPHA] [BETA]\n\n" +
                "Symptom_Scale_Threshold MUST be a number between 0.0 and 1.0\n\n" +
                "1 will run the application with the defaults SymptomScaleThreshold=0.4 ALPHA=2 BETA=3.5\n" +
                "2 will run the application with given command line SymptomScaleThreshold and ALPHA=2 BETA=3.5\n" +
                "3 will run the application with the given command line arguments\n\n"+
                "Example: \n\tjava -jar ABEM \n\tjava -jar ABEM 0.3 \n\tjava -jar ABEM 0.3 1.0 5.2");
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
