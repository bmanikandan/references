

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CSVFileReaderDouble {
    public static void main(String[] args) {
        String filePath = "path/to/your/file.csv";
        String delimiter = ",";
        String quote = "\"";

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String[] headers = reader.readLine().split(delimiter); // Read the header row
            String line;
            while ((line = reader.readLine()) != null) {
                String[] values = parseCSVLine(line, delimiter, quote);
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

    private static String[] parseCSVLine(String line, String delimiter, String quote) {
        String[] values = line.split(delimiter);
        for (int i = 0; i < values.length; i++) {
            if (values[i].startsWith(quote) && values[i].endsWith(quote)) {
                values[i] = values[i].substring(1, values[i].length() - 1);
            }
        }
        return values;
    }
}
