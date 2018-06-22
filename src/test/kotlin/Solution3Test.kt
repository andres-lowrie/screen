import com.rlperez.FileUtil
import com.rlperez.Solution3
import org.junit.Test

class Solution3Test {

    @Test
    fun testTotalNumberOfRowsInCsvs() {
        val csvFiles = FileUtil().getCsvFiles("src/test/data")
        val numRows = Solution3().totalNumberOfRowsInCsvs(csvFiles)
        assert(numRows == 16L)
    }
}
