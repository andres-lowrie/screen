import java.io.File

class FileUtil {
    fun getCsvFiles(root: String): List<File> {
        return File(root)
                .walk()
                .filter { s -> s.isFile && s.path.endsWith(".csv") }
                .toList()
    }

    fun writeValueCountCsv(path: String, data: Map<String, Int>): Unit {
        File(path).printWriter().use { out ->
            out.println("value,count")
            data.entries.forEach { it -> out.println("${it.key},${it.value}") }
        }
    }
}
