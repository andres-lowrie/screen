import com.rlperez.FileUtil
import org.junit.Test


class FileUtilTest {

    @Test
    fun contextLoads() {
    }

    @Test
    fun findCsvFilesWithMixedPaths() {
        val csvFiles = FileUtil().getCsvFiles("src/test/data")
        assert(csvFiles.isNotEmpty())
        assert(csvFiles.size == 3)
        assert(csvFiles.all { f -> f.isFile })
        assert(csvFiles.all { f -> f.absolutePath.endsWith(".csv") })
    }
}
