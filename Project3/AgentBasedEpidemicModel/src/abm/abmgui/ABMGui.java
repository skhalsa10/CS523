package abm.abmgui;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.Communicator;
import abm.utils.SIRQState;
import abm.utils.messages.Shutdown;
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
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.PriorityBlockingQueue;

import static abm.utils.ABMConstants.*;


/**
 * The GUI class to show the simulation of ABM epidemic spread.
 * This is a JavaFX GUI. you will notice most of the layout of the GUI
 * is performed in the constructor. State is updated using a Message
 * Passing Protocol with the ABMController
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

    /**
     * Contruct GUI layout nodes and state to animate on canvases.
     *
     * @param primaryStage this is the stage to display the scenes on
     * @param abmController the only object the GUI communicates with through a Message Passing Protocol
     */
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
        //define the view graph button
        this.viewGraph = new Button("View Graph");
        viewGraph.setMinWidth(200);
        viewGraph.getStyleClass().add("viewGraph-button");
        viewGraph.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                currentScreen = Screen.GRAPH;
            }
        });

        //define the back button and give it a stylesheet
        this.viewSim = new Button("<");
        viewSim.getStyleClass().add("viewSim-button");
        viewSim.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                currentScreen = Screen.MAIN;
            }
        });


        //main stuff
        //the root node always determines the fundamental layout .
        // the main screen should be dedicated to an animated canvas.
        //i want the button at the bottom of the screen so a vbox will
        // give layout of panes stacked on top of eachother
        mainRoot = new VBox();
        mainRoot.setAlignment(Pos.CENTER);
        canvasContainer = new StackPane();
        canvas = new Canvas(MAP_WIDTH,MAP_HEIGHT);
        canvas.minWidth(MAP_WIDTH);
        canvas.minHeight(MAP_HEIGHT);
        canvas.maxWidth(MAP_WIDTH);
        canvas.maxHeight(MAP_HEIGHT);
        //this is used to draw to main canvas
        gc = canvas.getGraphicsContext2D();

        bottomPaneMain = new HBox();

        //graph screen
        //init the text nodes and set their style and color
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
        //every sceen needs a root node this is the fundamental layout structure that we want
        // in this case virticle structure buttons and key on top and graph below
        graphRoot = new VBox();
        graphRoot.setAlignment(Pos.CENTER);
        graphCanvasContainer = new StackPane();
        graphCanvas = new Canvas(MAP_WIDTH,MAP_HEIGHT);
        graphCanvas.minWidth(MAP_WIDTH);
        graphCanvas.minHeight(MAP_HEIGHT);
        graphCanvas.maxWidth(MAP_WIDTH);
        graphCanvas.maxHeight(MAP_HEIGHT);
        //used to draw to
        gcGraph = graphCanvas.getGraphicsContext2D();
        topPaneGraph = new HBox();



        // initialize non javafx stuff
        currentScreen = Screen.MAIN;
        graphSlices = new ArrayList<>();
        graphUpdateCounter = 0;

        //once stuff is initialized lets place the pieces where they belong

        //place canvas in a stack pane as it renders good here
        canvasContainer.getChildren().addAll(canvas);
        //see below for why i make these
        Pane spacer1 = new Pane();
        Pane spacer2 = new Pane();
        //the bottom pane is used to display button. surround button with spacers
        bottomPaneMain.getChildren().addAll(spacer1,viewGraph,spacer2);
        //these two spacers will expand and take up as much room that they can equally
        //this has an effect of centering the button in the bottom panel
        bottomPaneMain.setHgrow(spacer1, Priority.ALWAYS);
        bottomPaneMain.setHgrow(spacer2, Priority.ALWAYS);
        bottomPaneMain.setPadding(new Insets(5));

        //add from top to bottom canvas and the buttonpannel
        mainRoot.getChildren().addAll(canvasContainer,bottomPaneMain);
        mainRoot.setVgrow(canvasContainer,Priority.ALWAYS);

        //graph screen
        //place the canvas inside of a Stack pane this would allow us to stack other nodes above the canvas
        // but I also find the canvas does not render well is most panes and it is best to stick it in a stackpane.
        // the stack pane can then be placed in other panes
        graphCanvasContainer.getChildren().addAll(graphCanvas);
        //the spacer is used to control the layout of text nodes
        Pane spacer3 = new Pane();
        //lets add the back button and colored text as a key
        topPaneGraph.getChildren().addAll(viewSim,spacer3,recoveredText,susceptibleText,infectedText);
        //this will push the the back button to the upper left corner and all text to the upper right corner
        topPaneGraph.setHgrow(spacer3,Priority.ALWAYS);
        //spacing between nodes... this spaces the text further apart and
        // makes it more aesthetically pleasing
        topPaneGraph.setSpacing(10);
        //this spaces the nodes from the edges
        topPaneGraph.setPadding(new Insets(5));
        //i think this pulls the text nodes to the bottom
        // otherwise they hover towards the top edge and it looks horrible
        topPaneGraph.setAlignment(Pos.BASELINE_CENTER);

        //add nodes to list of childred added in order. since this is a vbox it adds them top to bottom
        graphRoot.getChildren().addAll(topPaneGraph,graphCanvasContainer);
        //this forces the canvs to expand and take of as much room is possible in the virticle direction
        graphRoot.setVgrow(graphCanvasContainer,Priority.ALWAYS);



        //set the scenes to display on stage and give them the root Node
        graphScene = new Scene(graphRoot);
        mainScene = new Scene(mainRoot);
        //attach scenes to css file
        mainScene.getStylesheets().add("abm/abmgui/GUI.css");
        graphScene.getStylesheets().add("abm/abmgui/GUI.css");

        //if window was resizable this would force it to never resize below this
        stage.setMinWidth(ABMConstants.WINDOW_WIDTH);
        stage.setMinHeight(ABMConstants.WINDOW_HEIGHT);


        //display the stage
        stage.setScene(mainScene);
        stage.show();
        stage.setResizable(false);

        //start thread for the message queu
        isRunning = true;
        messageThread.start();
        //start animationtimer thread
        this.start();



    }

    /**
     * allows this object to perform Message Passing Comunication
     * @param m this message is received and placed in a queue for processing later.
     */
    @Override
    public void sendMessage(Message m) {
        this.messages.put(m);
    }

    /**
     * this is implemented from the thread dedicated to processing messages
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
            if(graphUpdateCounter == 30){
                graphUpdateCounter = 0;
                //this will had a data slice to the graph to be rendered. graph slices are
                // rendered as rectangles in the graph
                graphSlices.add(new GraphTimeData(totalI,totalS, totalR));
                //TODO may possibly need to send message to the system if socialdistancing is activated.
            }

            //this is set by the button just render what the button tells us
            if(currentScreen == Screen.GRAPH){
                renderGraphScreen();

            } else {
                renderMainScreen();
            }
            // helped to stabalize the rendor time to 60 frames a sec
            lastUpdate = now;
            graphUpdateCounter++;
        }
    }

    /**
     * this method will draw the current state of the graph
     */
    private void renderGraphScreen() {
        //make sure the scene is what is displayed on stage
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
            //rHeight is where R line ends and the S line begins in y coordinate space
            gcGraph.fillRect(x,rHeight,TIME_SLICE_WIDTH,sHeight);

            //draw the rect for I
            gcGraph.setFill(INFECTED_COLOR);
            //rHeight+sHeight is where to start drawing the I rectangle in y space
            gcGraph.fillRect(x,rHeight+sHeight,TIME_SLICE_WIDTH,iHeight);


        }
    }

    /**
     * This returns the height for R
     */
    private double getRHeight(GraphTimeData slice) {
        //for the total people find a percentage that is recovered
        double percentSI = slice.getR()/(double)totalPeople;
        //now convert that percentage into the verticle height of drawable canvas area
        return percentSI*graphCanvas.getHeight();
    }
    /**
     * This returns the height for S
     */
    private double getSHeight(GraphTimeData slice) {
        //for the total people find a percentage that is susceptable
        double percentSI = slice.getS()/(double)totalPeople;
        //now convert that percentage into the verticle height of drawable canvas area
        return percentSI*graphCanvas.getHeight();
    }

    /**
     * This function returns the height for I
     */
    private double getIHeight(GraphTimeData slice) {
        //for the total people find a percentage that is infected
        double percentInfected = slice.getI()/(double)totalPeople;
        //now convert that percentage into the verticle height of drawable canvas area
        return percentInfected*graphCanvas.getHeight();
    }

    /**
     * this function renders the main screen. this is the map that has the people walking
     * the people state can be seen by the colors of the circles. this gets called 60 times a second
     */
    private void renderMainScreen() {
        //if this method is called force the Main scene to be displayed on the stage
        stage.setScene(mainScene);
        //this draws the background and clears the screen
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
        //based on their state set the fill to use
        for (GUIPersonInfo p : peopleMap.values()) {
            switch (p.getPersonSIRQState()){
                case INFECTED:
                    gc.setFill(INFECTED_COLOR);
                    break;
                case RECOVERED:
                    gc.setFill(RECOVERED_COLOR);
                    break;
                case QUARANTINED:
                    gc.setFill(QUARANTINED_COLOR);
                    break;
                case SUSCEPTIBLE:
                    gc.setFill(SUSCEPTIBLE_COLOR);
                    break;
            }
            //draw a fill circle
            gc.fillOval(p.getLocation().getX(),p.getLocation().getY(),PERSON_RENDER_WIDTH,PERSON_RENDER_HEIGHT);
        }
    }

    /**
     * Here we just process message m
     * @param m
     */
    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            System.out.println("GUI is Shutting down");
            isRunning = false;
            this.stop();
        }
        else if (m instanceof NewPerson){
            NewPerson m2 = (NewPerson)m;
            //keep track of total people
            totalPeople++;
            //keep track of all people and their state and location
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
        else if (m instanceof PersonChangedLocation){
            //update the location
            PersonChangedLocation m2 = (PersonChangedLocation)m;
            peopleMap.get(m2.getPersonId()).setLocation(m2.getLoc());
        }
        else if (m instanceof PersonChangedState){
            PersonChangedState m2 = (PersonChangedState)m;
            //update the graph data
            updateGraphData(peopleMap.get(m2.getPersonId()).getPersonSIRQState(),m2.getNewState());
            peopleMap.get(m2.getPersonId()).setPersonSIRQState(m2.getNewState());

        }
        else {
            System.out.println("error processing message " +m+" inside of GUI");
        }
    }

    /**
     * this will update the totals for the total infected, total Recovered, and total susceptible.
     * every second these totals get graphed on the graph.
     *
     * @param oldState the old state of person
     * @param newState the new state of person
     */
    private void updateGraphData(SIRQState oldState, SIRQState newState) {
        if(oldState == newState){
            System.out.println("this should not happen Check updateGraphData");
        }
        else if(oldState==SIRQState.INFECTED && newState == SIRQState.QUARANTINED){
            //Quarantines is still infected as far as the graph is concerned so data doesnt change
        }
        else if(oldState==SIRQState.INFECTED && newState == SIRQState.RECOVERED){
            totalI--;
            totalR++;
        }
        else if(oldState==SIRQState.SUSCEPTIBLE && newState == SIRQState.INFECTED){
            totalS--;
            totalI++;
        }
        else if (oldState==SIRQState.QUARANTINED && newState == SIRQState.RECOVERED) {
            totalI--;
            totalR++;
        }
        else{
            System.out.println("something ait right check GUI updateGraphData method");
        }
    }
}
