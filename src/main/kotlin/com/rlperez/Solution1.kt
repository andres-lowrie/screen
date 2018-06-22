package com.rlperez

import java.io.File

class Solution1 {
    // Counting the headers of the CSVs. Assuming headers have no commas in the fields themselves.
    // Using parallel stream because I assume the intent is to do this over a lot of files.
    // Not using a big data framework but this algorithm should work if translated to hadoop.
    fun averageNumberOfFieldsPerCsv(files: List<File>): Double {
        val sumOfFields = files.parallelStream()
                .map { f ->
                    f.bufferedReader()
                            .lines()
                            .findFirst().map { l -> l.split(",").count() }
                            .orElse(0)
                }
                .reduce { sum, it -> sum + it }
                .orElse(0)
        return (sumOfFields + 0.0) / files.size
    }
}
