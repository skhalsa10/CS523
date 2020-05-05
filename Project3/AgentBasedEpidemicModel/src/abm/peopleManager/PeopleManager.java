package abm.peopleManager;

import abm.ABMController;
import abm.utils.ABMConstants;
import abm.utils.Communicator;
import abm.utils.PersonLocationState;
import abm.utils.SIRQState;
import abm.utils.messages.Shutdown;
import abm.utils.messages.*;
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

        // we will have a random person in the community who's infected with Covid-19. Random person between 1-X
        //where X = # of communities * # of people in each community.
        int randomPersonId = randomBounds.nextInt(ABMConstants.COMMUNITIES*ABMConstants.PEOPLE_IN_COMMUNITY) + 1;


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

                if (personId == randomPersonId) {
                    person.setCurrentSIRQState(SIRQState.INFECTED);
                    person.setSicknessScale(randomBounds.nextDouble());
                }

                // give this new person's info to the controller so the gui can render.
                this.abmController.sendMessage(new NewPerson(person.getCurrentSIRQState(), personId, personLocation));
                
                personId++;
            }
            communities.put(communityId, peopleInCommunity);
        }
    }

    private ArrayList<Person> addNeighbors(Person currentPerson, ArrayList<Person> peopleInThisCommunity) {
        ArrayList<Person> neighbors = new ArrayList<>();
        for (Person p : peopleInThisCommunity) {
            if (p != currentPerson) {
                neighbors.add(p);
            }
        }
        return neighbors;
    }

    private synchronized void processMessage(Message m) {
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("People Manager Shutting down.");
        }
        // update people's location state.
        if (m instanceof UpdatePeopleState) {
            // go thru every community and every person in it to update their location state.
            for (Integer communityID : communities.keySet()) {
                ArrayList<Person> people = communities.get(communityID);
                for (Person person : people) {
                    ArrayList<Person> neighbors = addNeighbors(person, people);
                    person.update(this.messages, neighbors);
                }
            }
        }
        if (m instanceof PersonWaitingForDestination) {
            this.abmController.sendMessage(m);
        }
        if (m instanceof DestinationForPerson) {
            DestinationForPerson dest = (DestinationForPerson) m;
            ArrayList<Person> people = communities.get(dest.getPersonCommunityID());
            Person person;
            for (Person p : people) {
                if (p.getID() == dest.getPersonID()) {
                    person = p;
                    person.setDestBuildingID(dest.getBuildingID());
                    person.setBuildingTypeToGo(dest.getBuildingTypeToGo());
                    person.setBuildingDest(dest.getBuildingDestToGo());
                    person.setLocationState(PersonLocationState.DESTINATION_GIVEN);
                    break;
                }
            }
        }
        if (m instanceof PersonChangedLocation) {
            this.abmController.sendMessage(m);
        }
        if (m instanceof PersonChangedState) {
            this.abmController.sendMessage(m);
        }
    }
}
