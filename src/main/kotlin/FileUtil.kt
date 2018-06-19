import java.io.File

class FileUtil {
    fun getCsvFiles(root: String): List<File> {
        return File(root)
                .walk()
                .filter { s -> s.isFile && s.path.endsWith(".csv") }
                .toList()
    }
}
