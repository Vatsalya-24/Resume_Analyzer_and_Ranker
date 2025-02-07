package models;
import java.util.List;

public class Candidate {
    private String name;
    private String email;
    private List<String> skills;
    private int experience;

    public Candidate(String name, String email, List<String> skills, int experience) {
        this.name = name;
        this.email = email;
        this.skills = skills;
        this.experience = experience;
    }

    public String getName() { return name; }
    public String getEmail() { return email; }
    public List<String> getSkills() { return skills; }
    public int getExperience() { return experience; }

    @Override
    public String toString() {
        return name + " | Email: " + email + " | Skills: " + skills + " | Experience: " + experience + " years";
    }
}
