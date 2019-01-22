plugins {
    base
    id("com.lovelysystems.gradle") version ("1.2.0")
}

lovely {
    gitProject()
}

val envDir = project.file("v")
val pip = envDir.resolve("bin/pip")
val python = envDir.resolve("bin/python")

val writeVersion by tasks.creating {
    val out = file("VERSION.txt")
    outputs.file(out)
    out.writeText(project.version.toString())
}

val venv by tasks.creating {
    outputs.dir(envDir)
    doLast {
        exec {
            commandLine("python3", "-m", "venv", "--clear", envDir)
        }
        exec {
            commandLine(pip, "install", "--upgrade", "pip==9.0.1")
        }
        exec {
            commandLine(pip, "install", "pip-tools==1.10.1")
        }
    }
}

val testenv by tasks.creating {
    dependsOn(venv)
    doLast {
        exec {
            commandLine("v/bin/pip-sync", "requirements.txt")
        }
        exec {
            commandLine("v/bin/pip", "install", "-e", projectDir)
        }
    }
}

val pytest by tasks.creating {
    group = "Verification"
    description = "Runs all python tests using pytest"
    dependsOn(testenv)
    doLast {
        exec {
            commandLine("v/bin/pytest", "tests")
        }
    }
}

val sdist by tasks.creating {
    dependsOn(venv, writeVersion)
    inputs.files(fileTree("src"))
    val out = buildDir.resolve("sdist")
    outputs.dir(out)
    out.deleteRecursively()
    doLast {
        exec {
            commandLine(python, "setup.py", "sdist", "--dist-dir", out)
        }
    }
}

