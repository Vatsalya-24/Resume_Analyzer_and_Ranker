package services;

import models.Candidate;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class ResumeProcessor {

    public List<Candidate> processResumes(List<File> resumeFiles) {
        List<Candidate> candidates = new ArrayList<>();

        for (File file : resumeFiles) {
            AbstractResumeParser parser = getParser(file);
            if (parser != null) {
                Candidate candidate = parser.parse(file);
                if (candidate != null) {
                    candidates.add(candidate);
                }
            } else {
                System.out.println("No parser found for: " + file.getName());
            }
        }
        return candidates;
    }

    private AbstractResumeParser getParser(File file) {
        String fileName = file.getName().toLowerCase();
        if (fileName.endsWith(".pdf")) {
            return new PdfResumeParser();
        } else if (fileName.endsWith(".docx")) {
            return new DocResumeParser();
        }
        return null;
    }
}
