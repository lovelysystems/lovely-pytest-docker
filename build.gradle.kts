plugins {
    base
    id("com.lovelysystems.gradle") version ("1.14.2")
}

lovely {
    gitProject()
    pythonProject("python3.11")
}
