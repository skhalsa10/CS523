package abm.peopleManager;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.Communicator;
import abm.utils.messages.Message;
import abm.utils.messages.Shutdown;
import abm.utils.messages.UpdateLocation;
import abm.utils.messages.UpdatePeopleState;
import javafx.geometry.Point2D;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.PriorityBlockingQueue;

/**
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PeopleManager extends Thread implements Communicator {

    private PriorityBlockingQueue<Message> messages;
    private ABMController abmController;
    private HashMap<Integer, ArrayList<Person>> communities;
    private boolean isRunning;

    public PeopleManager(ABMController abmController) {
        this.abmController = abmController;
        this.messages = new PriorityBlockingQueue<>();
        this.communities = new HashMap<>();

        this.isRunning = true;
        initializeCommunities();
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
     * There are x communities in our prototype in which there will be y
     * people.
     */
    private void initializeCommunities() {
        int personId = 1;
        Random randomBounds = new Random();

        for (int communityId = 1; communityId <= ABMConstants.COMMUNITIES; communityId++) {
            ArrayList<Person> peopleInCommunity = new ArrayList<>();
            // bounds for each person based on the communityId number.
            Point2D communityCoordinate = ABMConstants.COMMUNITIES_UPPERLEFT_CORNERS.get(communityId-1);
            double xMinBound = communityCoordinate.getX() + 5;
            double xMaxBound = communityCoordinate.getX() + ABMConstants.COMMUNITY_WIDTH - 5;
            double yMinBound = communityCoordinate.getY() + 5;
            double yMaxBound = communityCoordinate.getY() + ABMConstants.COMMUNITY_HEIGHT - 5;

            for (int peopleCounter = 1; peopleCounter <= ABMConstants.PEOPLE_IN_COMMUNITY; peopleCounter++) {
                // generate random location of a person inside specific communityId.
                Point2D personLocation = new Point2D(xMinBound + (xMaxBound - xMinBound) * randomBounds.nextDouble(),
                        yMinBound + (yMaxBound - yMinBound) * randomBounds.nextDouble());

                Person person = new Person(personId, communityId, personLocation);
                peopleInCommunity.add(person);
                personId++;

                // give this person's info to the controller so the gui can render.
                this.abmController.sendMessage(new UpdateLocation(person.getCurrentState(), personId, personLocation));
            }
            communities.put(communityId, peopleInCommunity);
        }
    }

    private synchronized void processMessage(Message m) {
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("People Manager Shutting down.");
        }
        if (m instanceof UpdatePeopleState) {

        }
    }
}
