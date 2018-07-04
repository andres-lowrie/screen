package com.test.filerun;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class FileUtil {

	private static Map<String, Long> wordMap = new HashMap<String, Long>();

	private static long countOfFields = 0;

	private static long countOfTotalRows = 0;

	public static void readOpenCSVFile(String fileNamWithPath) {
		Reader reader = null;
		CSVReader csvParser = null;
		long fileFieldsCount = 0;

		try {
			reader = Files.newBufferedReader(Paths.get(fileNamWithPath));
	        csvParser = new CSVReader(reader);
			String[] nextRecord;
			while ((nextRecord = csvParser.readNext()) != null) {
				if (fileFieldsCount == 0) {
					fileFieldsCount =nextRecord.length;
					countOfFields += fileFieldsCount;
				}
				for (String word : nextRecord) {
					if(word!=null && !word.trim().isEmpty()) {
						Long currentCount = wordMap.get(word.toLowerCase());
						if (currentCount != null) {
							currentCount++;
							wordMap.put(word.toLowerCase(), currentCount);
						} else {
							wordMap.put(word.toLowerCase(), new Long(1));
						}
					}
				}
				countOfTotalRows++;
			}

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println(fileNamWithPath);
			e.printStackTrace();
		} finally {
			if (csvParser  != null) {
				try {
					csvParser.close();
					if (reader != null) {
						try {
							reader.close();
						} catch (IOException e) {
							e.printStackTrace();
						}
					}
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}

	}
	public static void writecsvFile(String filePath, String filename) {
		BufferedWriter writer = null;
		CSVWriter csvWriter = null;
		try {
			Files.deleteIfExists(Paths.get(filePath + "/" + filename));
			writer = Files.newBufferedWriter(Paths.get(filePath + "/" + filename));
			csvWriter = new CSVWriter(writer,
                    CSVWriter.DEFAULT_SEPARATOR,
                    CSVWriter.NO_QUOTE_CHARACTER,
                    CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                    CSVWriter.DEFAULT_LINE_END);
            String[] header = {"value", "count"};
            csvWriter.writeNext(header);
			for (String word : wordMap.keySet()) {
				csvWriter.writeNext(new String[] {word,wordMap.get(word).toString()}) ;
			}
			csvWriter.flush();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (csvWriter != null)
					csvWriter.close();
				if (writer != null)
					writer.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
	}

	public static void main(String[] args) {

		String filePath = "/root/data";
		//Scanner input = new Scanner(System.in);
		//String filePath = input.next();
		List<String> fileLocations = new ArrayList<String>();
		long noOfFiles = 0;
		try {
			Files.walk(Paths.get(filePath)).filter(Files::isRegularFile).forEach(x -> {
				if (x.getFileName().toFile().getName().endsWith(".csv"))
					fileLocations.add(x.toAbsolutePath().toString());
			});
			System.out.println(fileLocations.toString());
			noOfFiles = fileLocations.size();

			fileLocations.stream().forEach(fileLocation -> {
				readOpenCSVFile(fileLocation);
			});
			System.out.println("Avg Number of Fields per file " + (countOfFields / noOfFiles));
			// write to csv file
			writecsvFile(filePath, "output_sumanth.csv");
			
			System.out.println("what's the total number or rows for the all the .csv files ->" + (countOfTotalRows));

			System.out.println("Total Distinct Word Count ->" + (wordMap.size()));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
