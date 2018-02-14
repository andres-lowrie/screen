package com.screen;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class Application {

	private static Map<String, Integer> wordsMap;

	public static void main(String[] args) {
		String inputDirectory = args[0];
		wordsMap = new HashMap<>();

		System.out.println("input directory: " + inputDirectory);
		List<File> csvFiles = new ArrayList<File>();
		getCsvFiles(new File(inputDirectory), csvFiles);

		long totalfields = 0l;
		long totalCount = 0l;
		for (File f : csvFiles) {
			final Result result = readFile(f);
			totalfields += result.getFieldsCount();
			totalCount += result.getTotalRowsCount();
		}
		writeOuput((totalfields / csvFiles.size()), totalCount);

		final String outputFile = writeWordCountToCsv();
		System.out.println("word count file path = " + outputFile);
	}

	private static void writeOuput(long avgTotalfields, long totalCount) {
		System.out.println("average number of fields across all the .csv files = " + avgTotalfields);
		System.out.println("total number or rows for the all the .csv files = " + totalCount);

		final File file = new File("output");
		try (BufferedWriter out = new BufferedWriter(new FileWriter(file))) {
			out.write("average number of fields across all the .csv files = " + avgTotalfields);
			out.write(System.lineSeparator());
			out.write("total number or rows for the all the .csv files = " + totalCount);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static String writeWordCountToCsv() {
		final File file = new File("word_count.csv");
		try (BufferedWriter out = new BufferedWriter(new FileWriter(file))) {
			out.write("value,count");
			out.write(System.lineSeparator());
			for (Entry<String, Integer> entry : wordsMap.entrySet()) {
				out.write(entry.getKey() + "," + entry.getValue() + System.lineSeparator());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		return file.getAbsolutePath();
	}

	private static Result readFile(File f) {
		Result result = null;
		try (BufferedReader br = new BufferedReader(new FileReader(f))) {
			int fieldsCount = 0;
			int totalRowsCount = 0;
			String line = "";
			boolean isHeader = true;
			while ((line = br.readLine()) != null) {
				final String[] words = line.split(",");
				if (isHeader) {
					fieldsCount = words.length;
				} else {
					for (String word : words) {
						wordsMap.put(word.trim(),
								wordsMap.get(word.trim()) == null ? 1 : wordsMap.get(word.trim()) + 1);
					}
					totalRowsCount++;
				}
				isHeader = false;
			}
			result = new Result(fieldsCount, totalRowsCount);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return result;
	}

	private static void getCsvFiles(File input, List<File> output) {

		if (input.isDirectory()) {
			for (File f : input.listFiles()) {
				getCsvFiles(f, output);
			}
		} else if (input.getAbsolutePath().endsWith(".csv")) {
			output.add(input);
		}
	}

}
