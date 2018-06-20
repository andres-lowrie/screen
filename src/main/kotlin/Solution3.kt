import java.io.File

class Solution3 {
    // Assumed the header counts as a row.
    fun totalNumberOfRowsInCsvs(files: List<File>): Long {
        return files.parallelStream()
                .map { it ->
                    it.bufferedReader()
                            .lines()
                            .count()
                }
                .mapToLong(Long::toLong)
                .sum()
    }
}
