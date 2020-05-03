package abm.utils.messages;

/**
 * Messaging system for blocking queues.
 * @version 1.0.0
 * @author Anas Gauba
 */
public interface Message extends Comparable<Message> {
    long timeStamp = System.nanoTime();

    /**
     * Will be used to sort messages in priority blocking queue. The earlier message should be processed first.
     * If we do not want to use a timestamp(which should work) we will need to identify a priority protocol that
     * we can all follow.
     *
     * @return timestamp in nanoseconds
     */
    default long getTimeStamp(){
        return this.timeStamp;
    }


    @Override
    default int compareTo(Message o) {
        long result = this.getTimeStamp() - o.getTimeStamp();
        if (result > 0 ) { return 1; }
        else if (result == 0) { return 0; }
        else { return -1; }
    }}
