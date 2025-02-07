package services;

import models.Candidate;
import java.util.*;
import java.util.regex.*;

public abstract class AbstractResumeParser implements ResumeParser {

    protected Candidate extractCandidate(String text) {
        String name = extractName(text);
        String email = extractEmail(text);
        List<String> skills = extractSkills(text);
        int experience = extractExperience(text);
        return new Candidate(name, email, skills, experience);
    }

    private String extractName(String text) {
        // Assumes name is at the start of the document (first line)
        return text.split("\n")[0].trim();
    }

    private String extractEmail(String text) {
        Matcher matcher = Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}").matcher(text);
        return matcher.find() ? matcher.group() : "Unknown";
    }

    private List<String> extractSkills(String text) {
        // Define a list of known skills (can be extended)
        List<String> knownSkills = Arrays.asList("Java", "Python", "C++", "Machine Learning", "Deep Learning",
                "SQL", "Spring Boot", "TensorFlow", "React", "JavaScript");

        List<String> detectedSkills = new ArrayList<>();
        for (String skill : knownSkills) {
            if (text.toLowerCase().contains(skill.toLowerCase())) {
                detectedSkills.add(skill);
            }
        }
        return detectedSkills.isEmpty() ? Arrays.asList("Unknown") : detectedSkills;
    }

    private int extractExperience(String text) {
        Matcher matcher = Pattern.compile("(\\d+)\\s+(?:years|year)\\s+of\\s+experience").matcher(text);
        return matcher.find() ? Integer.parseInt(matcher.group(1)) : 0;
    }
}
