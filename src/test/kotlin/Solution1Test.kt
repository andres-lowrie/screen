import com.rlperez.FileUtil
import com.rlperez.Solution1
import org.junit.Test

class Solution1Test {

    @Test
    fun testAverageNumberOfFieldsPerCsv() {
        val csvFiles = FileUtil().getCsvFiles("src/test/data")
        val average = Solution1().averageNumberOfFieldsPerCsv(csvFiles)
        assert(Math.floor(average * 1000).toInt() == 3666)
    }
}
