from shell		import shellhelper		as sh
from shell		import assertshell		as ash
from logger     import Logger

def Run(image):
    return sh.AsyncCall(["docker", "run", image])

def StopContainers(containerHashesArray):
    return sh.AsyncCall(["docker", "stop", "-f"] + containerHashesArray)

def ClearContainers(containerHashesArray):
    return sh.AsyncCall(["docker", "rm", "-f"] + containerHashesArray)

def ClearImages(imageHashesArray):
    return sh.AsyncCall(["docker", "rmi", "-f"] + imageHashesArray)

def ClearDocker(additionalArgs):
    if not ash.AssertDockerInstalled():
        return

    Logger.Info("Checking docker containers..")
    dockerPS = sh.AsyncCall(["docker", "ps", "-a", "-q"], printOutput = False)

    Logger.Info("Checking docker images..")
    dockerIMAGES = sh.AsyncCall(["docker", "images", "-q"], printOutput=False)

    psOutput = (dockerPS.communicate()[0]).split('\n')
    imagesOutput = (dockerIMAGES.communicate()[0]).split('\n')

    if len(psOutput) == 0 and len(imagesOutput) == 0:
        return True

    if len(additionalArgs) == 2:
        if additionalArgs[1] == '--all':
            Logger.Info("Clearing docker containers and images..")

            StopContainers(psOutput)
            ClearContainers(psOutput)

            ClearImages(imagesOutput)
            dockerIMAGES.stdout.close()
    else:
        Logger.Info("Clearing docker containers..")
        StopContainers(psOutput)
        ClearContainers(psOutput)

    dockerPS.stdout.close()

    return True
