import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CSVFileReader {
    public static void main(String[] args) {
        String filePath = "path/to/your/file.csv";

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String[] headers = reader.readLine().split(","); // Read the header row
            String line;
            while ((line = reader.readLine()) != null) {
                String[] values = line.split(",");
                // Process each row of data
                for (int i = 0; i < values.length; i++) {
                    System.out.println(headers[i] + ": " + values[i]);
                }
                System.out.println(); // Add a blank line between rows
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
