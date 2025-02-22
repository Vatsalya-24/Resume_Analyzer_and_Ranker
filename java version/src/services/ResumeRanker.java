package services;

import models.Candidate;
import java.util.*;

public class ResumeRanker {
    private List<String> requiredSkills;

    public ResumeRanker(List<String> requiredSkills) {
        this.requiredSkills = requiredSkills;
    }

    public int calculateScore(Candidate candidate) {
        int score = 0;
        for (String skill : candidate.getSkills()) {
            if (requiredSkills.contains(skill.trim().toLowerCase())) {
                score += 10;
            }
        }
        score += candidate.getExperience() * 5;
        return score;
    }

    public List<Candidate> rankCandidates(List<Candidate> candidates) {
        candidates.sort(Comparator.comparingInt(this::calculateScore).reversed());
        return candidates;
    }
}
