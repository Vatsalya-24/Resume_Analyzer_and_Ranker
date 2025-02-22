package services;
import java.io.File;

public class ResumeParserFactory {
    public static ResumeParser getParser(File file) {
        String fileName = file.getName().toLowerCase();
        if (fileName.endsWith(".pdf")) {
            return new PdfResumeParser();
        } else if (fileName.endsWith(".doc") || fileName.endsWith(".docx")) {
            return new DocResumeParser();
        } else {
            System.err.println("Unsupported file format: " + fileName);
            return null;
        }
    }
}
