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
import java.util.Iterator;
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
    private Random randomBounds;
    // this is initiated when we find a person becoming infected. When this hits 0, we make people quarantine who are above
    // some symptomScale threshold.
    private int countDownToQuarantine;
    // this initially runs for x seconds, when it hits 0, then we make a person infected and start disease spread.
    private int countDownTillEpidemicSpread;
    // map for person's symptomScale for their disease.
    private HashMap<Person,Double> symptomScaleThresholds;

    public PeopleManager(ABMController abmController) {
        this.abmController = abmController;
        this.messages = new PriorityBlockingQueue<>();
        this.communities = new HashMap<>();
        this.randomBounds = new Random();

        this.isRunning = true;
        // Initiate countDownToQuarantine counter to half a minute.
        // When it hits 0 in UpdatePeopleState message (called 60fps), we reset it.
        this.countDownToQuarantine = 60*ABMConstants.COUNTDOWN_TO_QUARANTINE_CHECK;

        this.symptomScaleThresholds = new HashMap<>();

        // wait this much time before spreading disease.
        this.countDownTillEpidemicSpread = 60 * ABMConstants.COUNTDOWN_TILL_EPIDEMIC_SPREAD;

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

    /**
     * Helper lookup method for quickly looking up the person in the map.
     * @param destPersonId to look for.
     * @param peopleInCommunity list of people in some i community.
     * @return a person with the intended id.
     */
    private Person lookupPerson(int destPersonId, ArrayList<Person> peopleInCommunity) {
        // get the first person then offset to lookup the intended person.
        int firstPersonInCommunityId = peopleInCommunity.get(0).getID();
        int offset = destPersonId - firstPersonInCommunityId;
        return peopleInCommunity.get(offset);
    }

    private void setRandomPersonToInfect() {
        // we will have a random person in the community who's infected with Covid-19. Random person between 1-X
        //where X = # of communities * # of people in each community.
        //int randomPersonId = randomBounds.nextInt(ABMConstants.COMMUNITIES*ABMConstants.PEOPLE_IN_COMMUNITY) + 1;
        int randomCommunityId = randomBounds.nextInt(ABMConstants.COMMUNITIES) + 1;
        Person randomPerson = communities.get(randomCommunityId).get(randomBounds.nextInt(ABMConstants.PEOPLE_IN_COMMUNITY));

        randomPerson.setCurrentSIRQState(SIRQState.INFECTED);
        randomPerson.setSymptomScale(randomBounds.nextDouble());

        // put this guy in symptomScaleThresholds map.
        this.symptomScaleThresholds.put(randomPerson,randomPerson.getSymptomLevel());

        abmController.sendMessage(new PersonChangedState(SIRQState.INFECTED,randomPerson.getID(),randomCommunityId));
    }

    private synchronized void processMessage(Message m) {
        if (m instanceof Shutdown) {
            this.isRunning = false;
            System.out.println("People Manager Shutting down.");
        }
        // update people's location state.
        if (m instanceof UpdatePeopleState) {
            // initially we wait until countDownTillEpidemicSpread hits 0 before we make a random person infected and start disease spread.
            if (this.countDownTillEpidemicSpread > 0) {
                this.countDownTillEpidemicSpread--;

                if (this.countDownTillEpidemicSpread <= 0) {
                    setRandomPersonToInfect();
                }
            }
            // go thru every community and every person in it to update their location state.
            for (Integer communityID : communities.keySet()) {
                ArrayList<Person> people = communities.get(communityID);
                for (Person person : people) {
                    ArrayList<Person> neighbors = addNeighbors(person, people);
                    person.update(this.messages, neighbors);
                }
            }
            // when countDownToQuarantine hits 0, put a PutPeopleToQuarantine message in peopleManager's message queue.
            if (this.countDownToQuarantine > 0) {
                this.countDownToQuarantine--;
                if (this.countDownToQuarantine <= 0) {
                    // reset the countDown back.
                    this.countDownToQuarantine = 60*ABMConstants.COUNTDOWN_TO_QUARANTINE_CHECK;

                    System.out.println("In updateState, QUArantine threshold map: " + symptomScaleThresholds.keySet().size());
                    this.sendMessage(new PutPeopleInQuarantine());
                }
            }
        }
        if (m instanceof PersonWaitingForDestination) {
            this.abmController.sendMessage(m);
        }
        if (m instanceof DestinationForPerson) {
            DestinationForPerson dest = (DestinationForPerson) m;

            Person person = lookupPerson(dest.getPersonID(),communities.get(dest.getPersonCommunityID()));
            person.setDestBuildingID(dest.getBuildingID());
            person.setBuildingTypeToGo(dest.getBuildingTypeToGo());
            person.setBuildingDest(dest.getBuildingDestToGo());
            person.setLocationState(PersonLocationState.DESTINATION_GIVEN);
        }
        if (m instanceof PersonChangedLocation) {
            this.abmController.sendMessage(m);
        }
        if (m instanceof PersonChangedState) {
            // when person sends this message, check if person infected, then put to symptomScalethresholds map.
            PersonChangedState changedState = (PersonChangedState) m;
            if (changedState.getNewState() == SIRQState.INFECTED) {
                Person person = lookupPerson(changedState.getPersonId(),communities.get(changedState.getPersonCommunityId()));
                //System.out.println(person.getID() == changedState.getPersonId());

                // put this infected person in the threshold map so when its time to put people in quarantine, this person's
                // symptom/sickness threshold will be checked.
                this.symptomScaleThresholds.put(person,person.getSymptomLevel());
                System.out.println("In personChangeState PERSON BECOME INFECTEDDDDDDD,  quarantine map size: " + symptomScaleThresholds.keySet().size());
            }
            this.abmController.sendMessage(m);
        }
        if (m instanceof EnterBuilding) {
            this.abmController.sendMessage(m);
        }
        if (m instanceof ExitBuilding) {
            this.abmController.sendMessage(m);
        }
        // when a person exits building, buildingManager sends this so peopleManager can
        // check whether the person (who isn't sick yet) has caught the virus?
        if (m instanceof BuildingContagionLevel) {
            BuildingContagionLevel m2 = (BuildingContagionLevel) m;

            //System.out.println("From BuildingContagion Message-> CommuntiyId: " + m2.getPersonCommunityId() + " personId: " + m2.getPersonId());
            Person person = lookupPerson(m2.getPersonId(),communities.get(m2.getPersonCommunityId()));
            if (person.getCurrentSIRQState() == SIRQState.SUSCEPTIBLE) {
                // check the likelihood of getting this person infected when they were at some x building?
                //System.out.println("Contaigon level: " + m2.getProbOfInfection());
                if (person.amIInfected(m2.getProbOfInfection())) {
                    //System.out.println("INFECTEDDDDDD");
                    // this person caught the virus while being in some building.
                    person.setCurrentSIRQState(SIRQState.INFECTED);
                    person.setSymptomScale(randomBounds.nextDouble());

                    // start recovery process of this person on its own no matter they get quarantined or not!
                    person.setTillRecoveryCountDown();

                    this.abmController.sendMessage(new PersonChangedState(person.getCurrentSIRQState(), person.getID(), person.getHomeCommunityID()));
                }
            }
        }
        // putting people in quarantine who are above symptomScale threshold, means we have tested these people.
        if (m instanceof PutPeopleInQuarantine) {
            System.out.println("In putPeopleQuarantine msg");

            // symptomScaleThresholds has all infected people. All of them go to quarantine.
            Iterator<Person> iterator = symptomScaleThresholds.keySet().iterator();
            while (iterator.hasNext()) {
                Person person = iterator.next();
                if (symptomScaleThresholds.get(person) >= ABMConstants.SYMPTOM_SCALE_THRESHOLD) {
                    person.setCurrentSIRQState(SIRQState.QUARANTINED);
                    this.abmController.sendMessage(new PersonChangedState(person.getCurrentSIRQState(), person.getID(), person.getHomeCommunityID()));
                    // remove this person from the map, iterator will remove it.
                    iterator.remove();
                }
            }
        }
    }
}
