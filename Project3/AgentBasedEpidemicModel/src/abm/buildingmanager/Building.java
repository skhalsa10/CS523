package abm.buildingmanager;

import abm.utils.BuildingType;

import java.util.HashMap;

public class Building {

    private HashMap<Integer, Double> infectedPeople;
    private int capacity;
    private int totalPeopleInside;
    private BuildingType buildingType;
    private int ID;
    private double infectionProbability;


    public Building(int capacity, BuildingType buildingType, int ID) {
        this.infectedPeople = new HashMap<>();
        this.capacity = capacity;
        this.totalPeopleInside = 0;
        this.buildingType = buildingType;
        this.ID = ID;
        this.infectionProbability = 0;
    }
}
