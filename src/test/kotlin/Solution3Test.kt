import org.junit.Test

class Solution3Test {

    @Test
    fun testTotalNumberOfRowsInCsvs() {
        val csvFiles = FileUtil().getCsvFiles("src/test/data")
        val numRows = Solution3().totalNumberOfRowsInCsvs(csvFiles)
        assert(numRows == 13)
    }
}
