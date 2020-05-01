package abm.abmgui;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.Communicator;
import abm.utils.messages.*;
import javafx.animation.AnimationTimer;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.text.*;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Collection;
import java.util.concurrent.PriorityBlockingQueue;

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


    //animated map
    private Canvas canvas;
    private GraphicsContext gc;
    private StackPane canvasContainer;

    //buttons
    private Button viewGraph;
    private Button viewSim;

    //State related stuff
    private PriorityBlockingQueue<Message> messages;
    private boolean isRunning;
    private Screen currentScreen;
    private ArrayList<GraphTimeData> graphSlices;

    private long lastUpdate = 0;//used to update 60 frames per second

    public ABMGui(Stage primaryStage, ABMController abmController) {
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
        canvas = new Canvas(ABMConstants.MAP_WIDTH,ABMConstants.MAP_HEIGHT);
        canvas.minWidth(ABMConstants.MAP_WIDTH);
        canvas.minHeight(ABMConstants.MAP_HEIGHT);
        canvas.maxWidth(ABMConstants.MAP_WIDTH);
        canvas.maxHeight(ABMConstants.MAP_HEIGHT);
        gc = canvas.getGraphicsContext2D();

        bottomPaneMain = new HBox();

        //graph screen
        susceptibleText = new Text("Susceptible");
        susceptibleText.setFill(ABMConstants.SUSCEPTIBLE);
        susceptibleText.setFont(Font.font("verdana", FontWeight.BOLD, FontPosture.REGULAR, 20));
        susceptibleText.setTextAlignment(TextAlignment.CENTER);
        infectedText = new Text("Infected");
        infectedText.setFill(ABMConstants.INFECTED);
        infectedText.setFont(Font.font("verdana", FontWeight.BOLD, FontPosture.REGULAR, 20));
        infectedText.setTextAlignment(TextAlignment.CENTER);
        graphRoot = new VBox();
        graphRoot.setAlignment(Pos.CENTER);
        graphCanvasContainer = new StackPane();
        graphCanvas = new Canvas(ABMConstants.MAP_WIDTH,ABMConstants.MAP_HEIGHT);
        graphCanvas.minWidth(ABMConstants.MAP_WIDTH);
        graphCanvas.minHeight(ABMConstants.MAP_HEIGHT);
        graphCanvas.maxWidth(ABMConstants.MAP_WIDTH);
        graphCanvas.maxHeight(ABMConstants.MAP_HEIGHT);
        gcGraph = graphCanvas.getGraphicsContext2D();
        topPaneGraph = new HBox();



        // initialize non javafx stuff
        currentScreen = Screen.MAIN;
        graphSlices = new ArrayList<>();

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
        topPaneGraph.getChildren().addAll(viewSim,spacer3,susceptibleText,infectedText);
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

        System.out.println(mainRoot.getWidth());

        //display the stage
        stage.setScene(mainScene);
        stage.show();
        stage.setResizable(false);

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
        stage.setScene(graphScene);
        gcGraph.setFill(ABMConstants.CANVAS_BACKGROUND);
        gcGraph.fillRect(0,0,ABMConstants.MAP_WIDTH,ABMConstants.MAP_HEIGHT);

    }

    private void renderMainScreen() {
        stage.setScene(mainScene);
        gc.setFill(ABMConstants.CANVAS_BACKGROUND);
        gc.fillRect(0,0,ABMConstants.MAP_WIDTH,ABMConstants.MAP_HEIGHT);
    }

    private synchronized void processMessage(Message m) {
        //TODO: Implement this as we add messages.
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("Building Manager Shutting down.");
        }
    }
}
