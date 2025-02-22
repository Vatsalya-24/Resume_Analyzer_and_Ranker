package services;

import models.Candidate;
import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class DocResumeParser extends AbstractResumeParser {

    @Override
    public Candidate parse(File file) {
        StringBuilder text = new StringBuilder();

        try (FileInputStream fis = new FileInputStream(file);
             ZipInputStream zis = new ZipInputStream(fis)) {

            ZipEntry entry;
            while ((entry = zis.getNextEntry()) != null) {
                if (entry.getName().equals("word/document.xml")) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(zis));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        text.append(line.replaceAll("<[^>]+>", " ")).append(" "); // Remove XML tags
                    }
                    break;
                }
            }
        } catch (Exception e) {
            System.err.println("Error parsing DOCX: " + e.getMessage());
        }

        return extractCandidate(text.toString());
    }
}
