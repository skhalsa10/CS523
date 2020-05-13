package abm.abmgui;

/**
 * This class is a simple encapsulation of time related data on the graph.
 * it encapsulates the amount of people in their states at a give time slice
 */
public class GraphTimeData {

    private int I;
    private int S;
    private int R;

    public GraphTimeData(int I, int S, int R){
        this.I = I;
        this.S = S;
        this.R = R;
    }

    /**
     *
     * @return infected count
     */
    public int getI() { return I; }

    /**
     *
     * @return susceptible count
     */
    public int getS() {
        return S;
    }

    /**
     *
     * @return recovered count
     */
    public int getR() { return R; }
}
