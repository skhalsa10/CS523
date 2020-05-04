package abm.abmgui;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.Communicator;
import abm.utils.SIRQState;
import abm.utils.messages.*;
import javafx.animation.AnimationTimer;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Point2D;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.layout.*;
import javafx.scene.text.*;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Collection;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.PriorityBlockingQueue;

import static abm.utils.ABMConstants.*;


/**
 * The GUI class to show the simulation of ABM epidemic spread.
 * @version 1.0.0
 * @author Siri Khalsa
 */
public class ABMGui extends AnimationTimer implements Runnable, Communicator {


    //JAVAFX Stuff
    private Stage stage;

    //main screen
    private Scene mainScene;
    private VBox mainRoot;
    private HBox bottomPaneMain;

    //graph screen
    private Scene graphScene;
    private VBox graphRoot;
    private HBox topPaneGraph;
    private Canvas graphCanvas;
    private StackPane graphCanvasContainer;
    private GraphicsContext gcGraph;
    private Text susceptibleText;
    private Text infectedText;
    private Text recoveredText;


    //animated map
    private Canvas canvas;
    private GraphicsContext gc;
    private StackPane canvasContainer;
    private int graphUpdateCounter;

    //buttons
    private Button viewGraph;
    private Button viewSim;

    //State related stuff
    private PriorityBlockingQueue<Message> messages;
    private ConcurrentHashMap<Integer,GUIPersonInfo> peopleMap;
    private boolean isRunning;
    private Screen currentScreen;
    private ArrayList<GraphTimeData> graphSlices;
    private Thread messageThread;
    private long lastUpdate = 0;//used to update 60 frames per second
    private int totalPeople;
    private int totalI;
    private int totalR;
    private int totalS;

    public ABMGui(Stage primaryStage, ABMController abmController) {

        messages = new PriorityBlockingQueue<>();
        peopleMap = new ConcurrentHashMap<>();
        messageThread = new Thread(this);
        totalPeople = 0;
        totalI = 0;
        totalR = 0;
        totalS = 0;

        //time to initialize GUI stuff
        this.stage = primaryStage;
        this.stage.setTitle("Agent Based Epidemic Model");

        //buttons
        this.viewGraph = new Button("View Graph");
        viewGraph.setMinWidth(200);
        viewGraph.getStyleClass().add("viewGraph-button");
        viewGraph.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                currentScreen = Screen.GRAPH;
            }
        });
        this.viewSim = new Button("<");
        viewSim.getStyleClass().add("viewSim-button");
        viewSim.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                currentScreen = Screen.MAIN;
            }
        });


        //main stuff
        mainRoot = new VBox();
        mainRoot.setAlignment(Pos.CENTER);
        canvasContainer = new StackPane();
        canvas = new Canvas(MAP_WIDTH,MAP_HEIGHT);
        canvas.minWidth(MAP_WIDTH);
        canvas.minHeight(MAP_HEIGHT);
        canvas.maxWidth(MAP_WIDTH);
        canvas.maxHeight(MAP_HEIGHT);
        gc = canvas.getGraphicsContext2D();

        bottomPaneMain = new HBox();

        //graph screen
        recoveredText = new Text("Recovered");
        recoveredText.setFill(RECOVERED_COLOR);
        recoveredText.setFont(Font.font("verdana", FontWeight.BOLD, FontPosture.REGULAR, 20));
        recoveredText.setTextAlignment(TextAlignment.CENTER);
        susceptibleText = new Text("Susceptible");
        susceptibleText.setFill(SUSCEPTIBLE_COLOR);
        susceptibleText.setFont(Font.font("verdana", FontWeight.BOLD, FontPosture.REGULAR, 20));
        susceptibleText.setTextAlignment(TextAlignment.CENTER);
        infectedText = new Text("Infected");
        infectedText.setFill(INFECTED_COLOR);
        infectedText.setFont(Font.font("verdana", FontWeight.BOLD, FontPosture.REGULAR, 20));
        infectedText.setTextAlignment(TextAlignment.CENTER);
        graphRoot = new VBox();
        graphRoot.setAlignment(Pos.CENTER);
        graphCanvasContainer = new StackPane();
        graphCanvas = new Canvas(MAP_WIDTH,MAP_HEIGHT);
        graphCanvas.minWidth(MAP_WIDTH);
        graphCanvas.minHeight(MAP_HEIGHT);
        graphCanvas.maxWidth(MAP_WIDTH);
        graphCanvas.maxHeight(MAP_HEIGHT);
        gcGraph = graphCanvas.getGraphicsContext2D();
        topPaneGraph = new HBox();



        // initialize non javafx stuff
        currentScreen = Screen.MAIN;
        graphSlices = new ArrayList<>();
        graphUpdateCounter = 0;

        //once stuff is initialized lets place the pieces where they belong
        canvasContainer.getChildren().addAll(canvas);
        Pane spacer1 = new Pane();
        Pane spacer2 = new Pane();
        bottomPaneMain.getChildren().addAll(spacer1,viewGraph,spacer2);
        bottomPaneMain.setHgrow(spacer1, Priority.ALWAYS);
        bottomPaneMain.setHgrow(spacer2, Priority.ALWAYS);
        bottomPaneMain.setPadding(new Insets(5));

        mainRoot.getChildren().addAll(canvasContainer,bottomPaneMain);
        mainRoot.setVgrow(canvasContainer,Priority.ALWAYS);

        //graph screen
        graphCanvasContainer.getChildren().addAll(graphCanvas);
        Pane spacer3 = new Pane();
        topPaneGraph.getChildren().addAll(viewSim,spacer3,recoveredText,susceptibleText,infectedText);
        topPaneGraph.setHgrow(spacer3,Priority.ALWAYS);
        topPaneGraph.setSpacing(10);
        topPaneGraph.setPadding(new Insets(5));
        topPaneGraph.setAlignment(Pos.BASELINE_CENTER);

        graphRoot.getChildren().addAll(topPaneGraph,graphCanvasContainer);
        graphRoot.setVgrow(graphCanvasContainer,Priority.ALWAYS);



        //set the scenes to display
        graphScene = new Scene(graphRoot);
        mainScene = new Scene(mainRoot, mainRoot.getMaxWidth(), mainRoot.getMaxHeight());
        mainScene.getStylesheets().add("abm/abmgui/GUI.css");
        graphScene.getStylesheets().add("abm/abmgui/GUI.css");


        stage.setMinWidth(ABMConstants.WINDOW_WIDTH);
        stage.setMinHeight(ABMConstants.WINDOW_HEIGHT);


        //display the stage
        stage.setScene(mainScene);
        stage.show();
        stage.setResizable(false);

        isRunning = true;
        System.out.println("Starting message Thread before");
        messageThread.start();
        System.out.println("Starting message Thread after");
        this.start();

        //DEBUG DATA TODO DELETE
        graphSlices.add(new GraphTimeData(0,0,0));

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
            //first update any data points used for graph 60 will update every sec
            if(graphUpdateCounter == 60){
                graphUpdateCounter = 0;
                graphSlices.add(new GraphTimeData(totalI,totalS, totalR));
                //TODO may possibly need to send message to the system if socialdistancing is activated.
            }

            if(currentScreen == Screen.GRAPH){
                renderGraphScreen();

            } else {
                renderMainScreen();
            }
            // helped to stabalize the rendor time
            lastUpdate = now;
            graphUpdateCounter++;
        }
    }

    private void renderGraphScreen() {
        stage.setScene(graphScene);
        //clear the screen
        gcGraph.setFill(CANVAS_BACKGROUND_COLOR);
        gcGraph.fillRect(0,0,ABMConstants.MAP_WIDTH,ABMConstants.MAP_HEIGHT);


        int timeSlices = graphSlices.size();
        //now loop through graph slices and render them
        for(int i = 0;i<timeSlices;i++){

            //get heights
            double rHeight = getRHeight(graphSlices.get(i));
            double sHeight = getSHeight(graphSlices.get(i));
            double iHeight = getIHeight(graphSlices.get(i));
            //get the current x
            double x = i*TIME_SLICE_WIDTH;

            //lets start drawing top down
            //draw the rect for the R
            gcGraph.setFill(RECOVERED_COLOR);
            gcGraph.fillRect(x,0,TIME_SLICE_WIDTH,rHeight);


            //draw the rect for S
            gcGraph.setFill(SUSCEPTIBLE_COLOR);
            gcGraph.fillRect(x,rHeight,TIME_SLICE_WIDTH,sHeight);

            //draw the rect for I
            gcGraph.setFill(INFECTED_COLOR);
            gcGraph.fillRect(x,rHeight+sHeight,TIME_SLICE_WIDTH,iHeight);


        }
    }

    /**
     * This returns the height for
     */
    private double getRHeight(GraphTimeData slice) {
        double percentSI = slice.getR()/(double)totalPeople;
        return percentSI*graphCanvas.getHeight();
    }
    /**
     * This returns the height for
     */
    private double getSHeight(GraphTimeData slice) {
        double percentSI = slice.getS()/(double)totalPeople;
        return percentSI*graphCanvas.getHeight();
    }

    /**
     * This function returns the hight for I
     */
    private double getIHeight(GraphTimeData slice) {
        double percentInfected = slice.getI()/(double)totalPeople;
        return percentInfected*graphCanvas.getHeight();
    }

    private void renderMainScreen() {
        stage.setScene(mainScene);
        gc.setFill(CANVAS_BACKGROUND_COLOR);
        gc.fillRect(0,0,MAP_WIDTH,MAP_HEIGHT);

        //now lets draw the communities
        gc.setFill(COMMUNITY_COLOR);
        for (Point2D corner:COMMUNITIES_UPPERLEFT_CORNERS) {
            gc.fillRect(corner.getX(),corner.getY(),COMMUNITY_WIDTH,COMMUNITY_HEIGHT);
        }

        //now lets draw the airport
        gc.setFill(AIRPORT_COLOR);
        gc.fillRect(AIRPORT_UPPERLEFT_CORNER.getX(),
                    AIRPORT_UPPERLEFT_CORNER.getY(),
                    AIRPORT_WIDTH,AIRPORT_HEIGHT);

        //now lets draw the two Grocery stores
        gc.setFill(BUILDING_COLOR);
        gc.fillRect(GROCERY1_UPPERLEFT.getX(),GROCERY1_UPPERLEFT.getY(),BUILDING_WIDTH,BUILDING_HEIGHT);
        gc.fillRect(GROCERY2_UPPERLEFT.getX(),GROCERY2_UPPERLEFT.getY(),BUILDING_WIDTH,BUILDING_HEIGHT);

        //now lets draw the hospitals
        gc.fillRect(HOSPITAL1_UPPERLEFT.getX(),HOSPITAL1_UPPERLEFT.getY(),BUILDING_WIDTH,BUILDING_HEIGHT);
        gc.fillRect(HOSPITAL2_UPPERLEFT.getX(),HOSPITAL2_UPPERLEFT.getY(),BUILDING_WIDTH,BUILDING_HEIGHT);

        //now lets draw the hotel
        gc.fillRect(HOTEL_UPPERLEFT.getX(),HOTEL_UPPERLEFT.getY(),BUILDING_WIDTH,BUILDING_HEIGHT);

        //now lets draw all the restaurants
        gc.setFill(RESTAURANT_COLOR);
        for (Point2D corners: RESTAURANT_UPPERLEFT_CORNERS) {
            gc.fillRect(corners.getX(),corners.getY(),RESTAURANT_WIDTH,RESTAURANT_HEIGHT);
        }

        //now lastly lets render those dang people!
        for (GUIPersonInfo p : peopleMap.values()) {
            switch (p.getPersonSIRQState()){
                case INFECTED:
                    gc.setFill(INFECTED_COLOR);
                    break;
                case RECOVERED:
                    gc.setFill(RECOVERED_COLOR);
                    break;
                case QUARANTINED:
                    //TODO need to add color
                    break;
                case SUSCEPTIBLE:
                    gc.setFill(SUSCEPTIBLE_COLOR);
                    break;
            }
            //TODO change the width and height to constants
            gc.fillOval(p.getLocation().getX(),p.getLocation().getY(),5,5);
        }
    }

    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            System.out.println("GUI is Shutting down");
            isRunning = false;
            this.stop();
        }
        else if (m instanceof NewPerson){
            NewPerson m2 = (NewPerson)m;
            totalPeople++;
            peopleMap.put(m2.getPersonId(),new GUIPersonInfo(m2.getPersonSIRQState(),m2.getLoc()));
            if(m2.getPersonSIRQState() == SIRQState.SUSCEPTIBLE){
                totalS++;
            }
            else if(m2.getPersonSIRQState() == SIRQState.RECOVERED){
                totalR++;
            }
            //TODO I am assuming the QUARANTINE ARE INFECTED. May need to change.
            else if(m2.getPersonSIRQState() == SIRQState.INFECTED||m2.getPersonSIRQState() == SIRQState.QUARANTINED){
                totalI++;
            }
            else {
                System.out.println("CHECK NEW PERSON MESSAGE IN GUI");
            }
        }
    }
}
