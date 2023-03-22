import java.io.FileInputStream;
import java.io.IOException;
import java.nio.charset.Charset;

public class UnicodeFileDetector {
    public static void main(String[] args) {
        String filePath = "path/to/your/file.txt";

        try (FileInputStream fis = new FileInputStream(filePath)) {
            byte[] bom = new byte[4];
            int bytesRead = fis.read(bom, 0, bom.length);

            if (bytesRead >= 2) {
                // Check for BOM for UTF-16 and UTF-32
                if (bom[0] == (byte)0xFE && bom[1] == (byte)0xFF) {
                    System.out.println("The file is a UTF-16 Unicode file (big-endian).");
                } else if (bom[0] == (byte)0xFF && bom[1] == (byte)0xFE) {
                    System.out.println("The file is a UTF-16 Unicode file (little-endian).");
                } else if (bytesRead >= 3 && bom[0] == (byte)0xEF && bom[1] == (byte)0xBB && bom[2] == (byte)0xBF) {
                    System.out.println("The file is a UTF-8 Unicode file.");
                } else if (bytesRead >= 4 && bom[0] == (byte)0x00 && bom[1] == (byte)0x00 && bom[2] == (byte)0xFE && bom[3] == (byte)0xFF) {
                    System.out.println("The file is a UTF-32 Unicode file (big-endian).");
                } else if (bytesRead >= 4 && bom[0] == (byte)0xFF && bom[1] == (byte)0xFE && bom[2] == (byte)0x00 && bom[3] == (byte)0x00) {
                    System.out.println("The file is a UTF-32 Unicode file (little-endian).");
                } else {
                    System.out.println("The file is not a Unicode file.");
                }
            } else {
                System.out.println("The file is not a Unicode file.");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
