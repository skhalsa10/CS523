package abm.utils;

import abm.utils.messages.Message;

/**
 * Interface for providing ability to thread objects to receive messages and putting them in their
 * blocking queue and process that message as appropriate.
 * @version 1.0.0
 * @author Anas Gauba
 */
public interface Communicator {
    void sendMessage(Message m);
}
