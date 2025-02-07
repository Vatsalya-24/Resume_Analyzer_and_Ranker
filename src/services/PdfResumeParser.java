package services;

import models.Candidate;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;

public class PdfResumeParser extends AbstractResumeParser {

    @Override
    public Candidate parse(File file) {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            StringBuilder text = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                text.append(line).append("\n");
            }
            return extractCandidate(text.toString());
        } catch (Exception e) {
            System.err.println("Error parsing PDF: " + e.getMessage());
        }
        return null;
    }
}
