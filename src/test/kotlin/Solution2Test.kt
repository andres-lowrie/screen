import org.junit.Test

class Solution2Test {

    @Test
    fun testWordCountOfAllCsvs() {
        val expectedResult =
                mapOf(
                        "adc" to 1,
                        "dasf" to 1,
                        "hgr" to 1,
                        "3" to 1,
                        "hdf" to 1,
                        "666" to 1,
                        "2" to 3,
                        "1" to 6,
                        "aqw" to 2,
                        "xcvv" to 3
                )

        val csvFiles = FileUtil().getCsvFiles("src/test/data")
        val wordCounts = Solution2().wordCountOfAllCsvs(csvFiles)

        assert(expectedResult.keys
                .map { k -> wordCounts[k] == expectedResult[k] }
                .all { b -> b }
        )
    }
}
