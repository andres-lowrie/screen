class ScreenApplication

fun main(args: Array<String>) {
    val fileUtil = FileUtil()
    val files = fileUtil.getCsvFiles(args[0])

    println("Executing solution for question 1...")
    val solution1 = Solution1()
    println(solution1.averageNumberOfFieldsPerCsv(files))

    println("Executing solution for question 2...")
    val solution2 = Solution2()
    val wordCounts = solution2.wordCountOfAllCsvs(files)
    println("Writing output to ./solution2.csv")
    fileUtil.writeValueCountCsv("./solution2.csv", wordCounts)

    println("Executing solution for question 3...")
    val solution3 = Solution3()
    println(solution3.totalNumberOfRowsInCsvs(files))
}
