package com.rlperez

import java.io.File

class Solution2 {
    // Was unclear if I should count the header or not so I decided to count the headers.
    // Assuming that we will be dealing with a lot of large files so I'll process them
    // with parallel stream.
    // Not sure if sorting was required but this could be changed to do that.
    fun wordCountOfAllCsvs(files: List<File>): Map<String, Int> {
        val result: MutableMap<String, Int> = LinkedHashMap()
        files.parallelStream().map { it -> wordCountOfCsv(it) }
                .sequential()
                .forEach { it ->
                    it.forEach { it ->
                        result[it.key] = result.getOrDefault(it.key, 0) + it.value
                    }
                }

        return result
    }

    private fun wordCountOfCsv(file: File): Map<String, Int> {
        val result: MutableMap<String, Int> = LinkedHashMap()
        file.bufferedReader()
                .lines()
                .forEach { l ->
                    l.split(",")
                            .groupBy { it }
                            .map { Pair(it.key, it.value.size) }
                            .forEach { it -> result[it.first] = result.getOrDefault(it.first, 0) + it.second }
                }

        return result
    }
}
