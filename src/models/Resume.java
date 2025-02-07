package models;
import java.io.File;

public class Resume {
    private File file;
    private String format;

    public Resume(File file, String format) {
        this.file = file;
        this.format = format;
    }

    public File getFile() { return file; }
    public String getFormat() { return format; }
}
