import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class FileReaderExample {
    public static void main(String[] args) {
        String filePath = "path/to/your/file.txt";
        File file = new File(filePath);

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line = reader.readLine();
            while (line != null) {
                System.out.println(line);
                line = reader.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String detectLineSeparator(String text) {
        if (text.contains("\r\n")) {
            return "\r\n"; // Windows line separator
        } else if (text.contains("\r")) {
            return "\r"; // MacOS line separator
        } else {
            return "\n"; // Linux line separator
        }
    }
}
