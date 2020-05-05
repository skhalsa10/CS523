package abm.utils.messages;

public abstract class TimeMarker implements Comparable<TimeMarker> {
    protected long timeStamp;

    public TimeMarker(){
        timeStamp = System.nanoTime();
    }



    /**
     * Will be used to sort messages in priority blocking queue. The earlier message should be processed first.
     * If we do not want to use a timestamp(which should work) we will need to identify a priority protocol that
     * we can all follow.
     *
     * @return timestamp in nanoseconds
     */
    protected long getTimeStamp(){
        return this.timeStamp;
    }



    @Override
    public int compareTo(TimeMarker o) {
        long result = this.getTimeStamp() - o.getTimeStamp();
        if (result > 0 ) { return 1; }
        else if (result == 0) { return 0; }
        else { return -1; }
    }

//    @Override
//    protected int compareTo(TimeMarker o) {
//        long result = this.getTimeStamp() - o.getTimeStamp();
//        if (result > 0 ) { return 1; }
//        else if (result == 0) { return 0; }
//        else { return -1; }
//    }
}
