package abm.utils;

/**
 * This enum class is for identifying the disease state of a person at a given time in the simulation.
 * By default initially, every person will be in Susceptible state.
 * @version 1.0.0
 * @author Anas Gauba
 */
public enum SIRQState {
    SUSCEPTIBLE, INFECTED, RECOVERED, QUARANTINED
}
