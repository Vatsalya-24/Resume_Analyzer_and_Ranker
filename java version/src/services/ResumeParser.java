package services;
import models.Candidate;
import java.io.File;

public interface ResumeParser {
    Candidate parse(File file);
}
