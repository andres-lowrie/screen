import org.junit.Test


class FileUtilTest {

    @Test
    fun contextLoads() {
    }

    @Test
    fun findCsvFilesWithMixedPaths() {
        val csvPaths = FileUtil().getCsvFiles("src/test/data")
        assert(csvPaths.isNotEmpty())
        assert(csvPaths.size == 3)
        assert(csvPaths.all { f -> f.isFile })
        assert(csvPaths.all { f -> f.absolutePath.endsWith(".csv") })
    }
}
