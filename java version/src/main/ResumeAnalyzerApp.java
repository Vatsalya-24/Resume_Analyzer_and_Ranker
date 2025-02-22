package main;
import models.Candidate;
import services.ResumeProcessor;
import services.ResumeRanker;
import java.io.File;
import java.util.*;

public class ResumeAnalyzerApp {
    private static final String RESUME_FOLDER = "D:\\project\\Smart_Resume_Analyzer_and_Ranker\\Resume";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Step 1: Get required skills from user
        System.out.println("Enter required skills (comma-separated): ");
        String[] skillArray = scanner.nextLine().split(",");
        List<String> requiredSkills = Arrays.asList(skillArray);

        // Step 2: Load resumes
        File folder = new File(RESUME_FOLDER);
        File[] files = folder.listFiles();

        if (files == null || files.length == 0) {
            System.out.println("No resumes found in the folder.");
            return;
        }

        List<File> resumeFiles = Arrays.asList(files);

        // Step 3: Process resumes
        ResumeProcessor processor = new ResumeProcessor();
        List<Candidate> candidates = processor.processResumes(resumeFiles);

        // Step 4: Rank resumes
        ResumeRanker ranker = new ResumeRanker(requiredSkills);
        List<Candidate> rankedCandidates = ranker.rankCandidates(candidates);

        // Step 5: Display ranked results
        System.out.println("\nRanked Resumes:");
        for (Candidate c : rankedCandidates) {
            System.out.println(c);
        }
    }
}
