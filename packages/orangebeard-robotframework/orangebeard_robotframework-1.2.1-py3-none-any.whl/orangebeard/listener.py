import asyncio
import os
import platform
import re
import hashlib
import json

from datetime import datetime
from pytz import reference

from orangebeard.async_client import AsyncOrangebeardClient
from orangebeard.entity.TestType import TestType
from orangebeard.entity.TestStatus import TestStatus
from orangebeard.entity.LogLevel import LogLevel
from orangebeard.entity.LogFormat import LogFormat
from orangebeard.entity.Attachment import AttachmentFile, AttachmentMetaData
from orangebeard.entity.Attribute import Attribute
from robot.libraries.BuiltIn import BuiltIn
from robot.api.interfaces import ListenerV2

tz = reference.LocalTimezone()


def get_variable(name, defaultValue=None):
    return BuiltIn().get_variable_value("${" + name + "}", defaultValue)


def get_status(statusStr) -> TestStatus:
    if statusStr == "FAIL":
        return TestStatus.FAILED
    if statusStr == "PASS":
        return TestStatus.PASSED
    if statusStr in ("NOT RUN", "SKIP"):
        return TestStatus.SKIPPED
    else:
        raise ValueError("Unknown status: {0}".format(statusStr))


def get_level(levelStr) -> LogLevel:
    if levelStr == "INFO":
        return LogLevel.INFO
    if levelStr == "WARN":
        return LogLevel.WARN
    if levelStr in ("ERROR", "FATAL", "FAIL"):
        return LogLevel.ERROR
    if levelStr in ("DEBUG", "TRACE"):
        return LogLevel.DEBUG
    else:
        raise ValueError("Unknown level: {0}".format(levelStr))


class listener(ListenerV2):
    def __init__(self):
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self.eventloop = asyncio.get_event_loop()

        self.suites = {}
        self.tests = {}
        self.steps = []

    def start_suite(self, name, attributes):
        self.startTestRunIfNeeded()
        suiteKey = attributes.get("longname")
        suiteNames = list(map(self.pad_suiteName, suiteKey.split(".")))

        if not self.suites.get(suiteKey):
            startedSuites = self.eventloop.run_until_complete(
                self.client.startSuite(
                    self.testRunUUID, suiteNames, description=attributes.get("doc")
                )
            )
            for suite in startedSuites:
                self.suites[".".join(suiteNames)] = suite
                suiteNames.pop()

    def pad_suiteName(self, suiteName):
        if len(suiteName) < 3:
            return suiteName + "  "
        return suiteName

    def start_test(self, name, attributes):
        suiteNames = attributes.get("longname").split(".")
        suiteNames.pop()
        suiteKey = ".".join(suiteNames)

        suiteUUID = self.suites.get(suiteKey)

        template = attributes.get("template")
        tags = attributes.get("tags")

        orangebeardAttrs = []

        if len(template) > 0 or len(tags) > 0:
            if len(template) > 0:
                orangebeardAttrs.append(Attribute("template", template))
            if len(tags) > 0:
                for tag in tags:
                    orangebeardAttrs.append(Attribute(value=tag))

        testUUID = self.eventloop.run_until_complete(
            self.client.startTest(
                self.testRunUUID,
                suiteUUID,
                name,
                TestType.TEST,
                attributes=orangebeardAttrs if len(orangebeardAttrs) > 0 else None,
                description=attributes.get("doc"),
                startTime=datetime.now(tz),
            )
        )
        self.tests[attributes.get("id")] = testUUID

    def end_test(self, name, attributes):
        testUUID = self.tests.get(attributes.get("id"))
        status = get_status(attributes.get("status"))
        message = attributes.get("message")
        if len(message) > 0:
            level = LogLevel.INFO if status == TestStatus.PASSED else LogLevel.ERROR
            self.eventloop.run_until_complete(
                self.client.log(self.testRunUUID, testUUID, level, message)
            )
        self.eventloop.run_until_complete(
            self.client.finishTest(
                testUUID, self.testRunUUID, status, endTime=datetime.now(tz)
            )
        )
        self.tests.pop(attributes.get("id"))

    def start_keyword(self, name, attributes):
        testUUID = list(self.tests.values())[-1] if len(self.tests) else None
        parentStepUUID = self.steps[-1] if len(self.steps) > 0 else None

        if testUUID is None:
            # start suite keyword (setup) as a virtual test (BEFORE_TEST)
            kwHash = hashlib.md5(
                (
                    name
                    + json.dumps(attributes.get("args"), sort_keys=True)
                ).encode("utf-8")
            ).hexdigest()
            
            stepTypePrefix = attributes.get("type")
            beforeStepName = "{0}: {1}".format(stepTypePrefix.capitalize(), attributes.get("kwname"))

            suiteUUID = list(self.suites.values())[-1]
            testUUID = self.eventloop.run_until_complete(
                self.client.startTest(
                    self.testRunUUID,
                    suiteUUID,
                    beforeStepName,
                    TestType.BEFORE,
                    attributes=None,
                    description=attributes.get("doc"),
                    startTime=datetime.now(tz),
                )
            )
            self.tests[kwHash] = testUUID

        else:
            stepName = (
                attributes.get("kwname")
                if len(attributes.get("kwname")) > 0
                else attributes.get("type")
            )
            stepTypePrefix = attributes.get("type")
            stepArgs = attributes.get("args")

            stepDisplayName = (
                "{0}: {1} ({2})".format(
                    stepTypePrefix.capitalize(), stepName, ", ".join(stepArgs)
                )
                if len(stepArgs) > 0
                else "{0}: {1}".format(stepTypePrefix.capitalize(), stepName)
            )

            # omit args if too long (TODO: log them separately)
            if len(stepDisplayName) > 128:
                stepDisplayName = "{0}: {1}".format(
                    stepTypePrefix.capitalize(), stepName
                )

            stepUUID = self.eventloop.run_until_complete(
                self.client.startStep(
                    self.testRunUUID,
                    testUUID,
                    stepDisplayName,
                    parentStepUUID,
                    description=attributes.get("doc"),
                    startTime=datetime.now(tz),
                )
            )
            self.steps.append(stepUUID)

    def end_keyword(self, name, attributes):
        stepUUID = self.steps[-1] if len(self.steps) > 0 else None

        if stepUUID is None:
            # Was a suite setup step wrapped in test item
            kwHash = hashlib.md5(
                (
                    name
                    + json.dumps(attributes.get("args"), sort_keys=True)
                ).encode("utf-8")
            ).hexdigest()

            testUUID = self.tests.get(kwHash)
            status = get_status(attributes.get("status"))

            self.eventloop.run_until_complete(
                self.client.finishTest(
                    testUUID, self.testRunUUID, status, endTime=datetime.now(tz)
                )
            )
            self.tests.pop(kwHash)

        else:
            status = get_status(attributes.get("status"))

            self.eventloop.run_until_complete(
                self.client.finishStep(
                    stepUUID, self.testRunUUID, status, endTime=datetime.now(tz)
                )
            )
            self.steps.pop()

    def log_message(self, message):
        stepUUID = self.steps[-1] if len(self.steps) > 0 else None

        testUUID = testUUID = list(self.tests.values())[-1]

        level = get_level(message["level"])
        logMsg = message["message"]

        if message["html"] == "yes":
            images = re.findall('src="(.+?)"', logMsg)
            if len(images) > 0:
                logUUID = self.eventloop.run_until_complete(
                    self.client.log(
                        self.testRunUUID,
                        testUUID,
                        level,
                        images[0],
                        stepUUID,
                        logTime=datetime.now(tz),
                    )
                )

                attachmentFile = AttachmentFile(
                    images[0],
                    open(
                        "{0}{1}{2}".format(self.outDir, os.path.sep, images[0]), "rb"
                    ).read(),
                )
                attachmentMeta = AttachmentMetaData(
                    self.testRunUUID,
                    testUUID,
                    logUUID,
                    stepUUID,
                    attachmentTime=datetime.now(tz),
                )
                self.eventloop.run_until_complete(
                    self.client.logAttachment(attachmentFile, attachmentMeta)
                )
            else:
                self.eventloop.run_until_complete(
                    self.client.log(
                        self.testRunUUID,
                        testUUID,
                        level,
                        logMsg,
                        stepUUID,
                        logFormat=LogFormat.HTML,
                    )
                )
        else:
            self.eventloop.run_until_complete(
                self.client.log(self.testRunUUID, testUUID, level, logMsg, stepUUID)
            )

    def close(self):
        self.eventloop.run_until_complete(self.client.finishTestRun(self.testRunUUID))

    def startTestRunIfNeeded(self):
        if not hasattr(self, "testRunUUID"):
            self.endpoint = get_variable("orangebeard_endpoint")
            self.accessToken = get_variable("orangebeard_accesstoken")
            self.project = get_variable("orangebeard_project")
            self.testset = get_variable("orangebeard_testset")
            self.description = get_variable("orangebeard_description")
            self.outDir = get_variable("OUTPUT_DIR")

            ##create client and initialize context
            self.client = AsyncOrangebeardClient(
                self.endpoint, self.accessToken, self.project
            )

            ##start test run
            self.testRunUUID = self.eventloop.run_until_complete(
                self.client.startTestrun(
                    self.testset,
                    startTime=datetime.now(tz),
                    description=self.description,
                )
            )
