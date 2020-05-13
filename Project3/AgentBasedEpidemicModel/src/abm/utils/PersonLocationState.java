package abm.utils;

/**
 * This enum class is for identifying the destination state of a person at a given time in the simulation.
 * By default initially, every person will be in their communities.
 * @version 1.0.0
 * @author Anas Gauba
 */
public enum PersonLocationState {
    AT_COMMUNITY, WALKING, WAITING_FOR_DESTINATION, DESTINATION_GIVEN, AT_DESTINATION
}
