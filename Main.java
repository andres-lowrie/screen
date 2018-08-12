import java.io.BufferedWriter;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.StreamSupport;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;

public class Main {
    private static final String DATA_FILE_ROOT = "/root/data";
    private static final String WORD_FREQUENCIES_CSV = "word_frequencies.csv";

    public static void main(String[] args) throws Exception {
        Main m = new Main();

        System.out.println("Average field count across all files: " + m.getAverageFieldCount());
        System.out.println("Total rows across all files: " + m.getTotalRowCount());
        Map<String, Integer> frequencyMap = m.getWordCountMap();
        m.createCsvFile(frequencyMap);
    }


    private double getAverageFieldCount() throws Exception {
        double avg = Files.walk(Paths.get(DATA_FILE_ROOT))
                .filter(s -> s.toString().endsWith(".csv"))
                .mapToInt(this::getFieldCount)
                .average()
                .getAsDouble();
        return avg;
    }


    private int getFieldCount(Path file) {
        try (Reader reader = Files.newBufferedReader(file);
             CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader().withIgnoreHeaderCase())) {
            return csvParser.getHeaderMap().size();
        } catch (Exception e) {
            System.out.println("Encountered exception reading csv file: " + file.toString() + ".  Skipping field count for this file.");
        }
        return 0;
    }


    private long getTotalRowCount() throws Exception {
        long totalRows = Files.walk(Paths.get(DATA_FILE_ROOT))
                .filter(s -> s.toString().endsWith(".csv"))
                .mapToLong(this::getRowCountInCsv)
                .sum();
        return totalRows;
    }


    private long getRowCountInCsv(Path file) {
        try (Reader reader = Files.newBufferedReader(file);
             CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader().withIgnoreHeaderCase())) {
            return StreamSupport.stream(csvParser.spliterator(), false).count();
        } catch (Exception e) {
            System.out.println("Encountered exception reading csv file: " + file.toString() + "  skipping this file for row counting");
        }
        return 0;
    }


    private Map<String, Integer> getWordCountMap() throws IOException {
        Map<String, Integer> frequencyMap = Files.walk(Paths.get(DATA_FILE_ROOT))
                .filter(s -> s.toString().endsWith(".csv"))
                .map(this::wordCountMapInCsv)
                .reduce(new HashMap<>(), (map1, map2) -> {
                    for (Map.Entry<String, Integer> entry : map2.entrySet()) {
                        map1.put(entry.getKey(), map1.getOrDefault(entry.getKey(), 0) + entry.getValue());
                    }
                    return map1;
                });
        return frequencyMap;
    }


    private Map<String, Integer> wordCountMapInCsv(Path file) {
        Map<String, Integer> frequencyMap = new HashMap<>();

        try (Reader reader = Files.newBufferedReader(file);
             CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader().withIgnoreHeaderCase())) {
            for (CSVRecord record : csvParser) {
                // get a list of all the field values for this row
                List<String> valueList = new ArrayList<>(record.toMap().values());
                valueList.forEach(word ->
                        frequencyMap.merge(word.trim().toLowerCase(), 1, (v, newV) -> v + newV)
                );
            }
        } catch (Exception e) {
            System.out.println("Encountered exception reading csv file: " + file.toString() + ".  Skipping " +
                    "this file for word frequency counts.");
        }
        return frequencyMap;
    }


    private void createCsvFile(Map<String, Integer> frequencyMap) throws IOException {
        Path filePath = Paths.get(DATA_FILE_ROOT, WORD_FREQUENCIES_CSV);

        try (
                BufferedWriter writer = Files.newBufferedWriter(filePath);
                CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT
                        .withHeader("value", "count"))
        ) {
            frequencyMap.forEach((key, value) -> addRow(csvPrinter, key, value));
            csvPrinter.flush();
            System.out.println("File " + filePath.toString() + " written with " + frequencyMap.size() + " distinct words");
        }
    }


    private void addRow(CSVPrinter printer, Object key, Object value) {
        try {
            printer.printRecord(key, value);
        } catch (IOException exc) {
            System.out.println("Exception thrown while writing CSV record of word frequencies.");
        }
    }
}