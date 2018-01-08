import org.gradle.api.tasks.Exec
import org.gradle.kotlin.dsl.*

repositories {
    jcenter()
}

plugins {
    base
}

tasks {

    val venv by creating {
        val envDir = project.file("v")
        outputs.dir(envDir)
        val pip = envDir.resolve("bin/pip")
        val python = envDir.resolve("bin/python")
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

    val testenv by creating {
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

    val pytest by creating {
        group = "Verification"
        description = "Runs all python tests using pytest"
        dependsOn(testenv)
        doLast {
            exec {
                commandLine("v/bin/pytest", "tests")
            }
        }
    }

}

task(name = "wrapper", type = Wrapper::class) {
    gradleVersion = "4.4.1"
}
