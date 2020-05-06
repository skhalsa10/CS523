package abm.utils.messages;

/**
 * This message triggers when the countDown for quarantining people hit 0 in peopleManager.
 * It tells PeopleManager to quarantine people who are above certain symptomScale threshold.
 * @version 1.0.0
 * @author Anas Gauba
 */
public class PutPeopleInQuarantine extends Message {
    public PutPeopleInQuarantine() {

    }
}
