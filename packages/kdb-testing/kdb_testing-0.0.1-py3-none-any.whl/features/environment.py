# https://behave.readthedocs.io/en/stable/tutorial.html#environmental-controls
# https://behave.readthedocs.io/en/stable/api.html#behave.runner.Context
from behave import fixture, use_fixture
import _thread
import logging
import os
import webbrowser
from pathlib import Path

import kdb
from conftest import check_and_create_build_lock_file
from kdb import LOG_DIR, XML_REPORT_DIR, HTML_REPORT_DIR, DATA_REPORT_DIR
from kdb.common.mobile_manager import MobileManager
from kdb.common.profiles import Profiles
from kdb.common.utils import FileUtil
from kdb.report.report_manager import ReportManager
from kdb.report.test_case_log import TestCaseLog
from kdb.webdriver import kdb_driver
from behave import use_step_matcher

# -- SELECT DEFAULT STEP MATCHER: Use "re" matcher as default.
# use_step_matcher("cfparse")
# use_step_matcher("re")
use_step_matcher("parse")


def before_step(context, step):
    """These run before every step."""
    pass


def after_step(context, step):
    """These run after every step."""
    pass


def before_scenario(context, scenario):
    """These run before each scenario is run."""
    TestCaseLog.reset()
    # context.config.userdata[scenario.name + '_start_time'] = int(round(time.time() * 1000))


def after_scenario(context, scenario):
    """These run after each scenario is run."""
    # create testcase report
    # test_duration = int(round(time.time() * 1000)) - context.config.userdata.get(scenario.name + '_start_time')
    if not context.config.userdata.get("no-report"):
        # add trace log record if failed/assert fail
        if context.failed:
            TestCaseLog.add_test_step('', {}, 0, 'trace', context.stderr_capture.getvalue())
        # generate html file
        _thread.start_new_thread(ReportManager.create_test_case_report, (
            scenario.name, not context.failed, int(scenario.duration * 1000), scenario.filename))
    # print duration and status
    logging.info(f'=======Result===={scenario.name}===')
    logging.info("Testing duration: %s ms" % str(int(scenario.duration * 1000)))
    if not context.failed:
        logging.info("Testing result: %s" % 'PASSED')
    else:
        logging.info("Testing result: %s" % 'FAILURES')


def before_feature(context, feature):
    """These run before each feature file is exercised."""
    context.profile = Profiles(kdb.PROFILE_NAME)


def after_feature(context, feature):
    """These run bafter each feature file is exercised."""
    context.config.junit_directory = XML_REPORT_DIR
    # set xml_report_name in userdata that using in after_all hook
    # feature_name = os.path.splitext(os.path.basename(feature.filename))[0]
    feature_name = os.path.splitext(feature.filename)[0]
    feature_name = feature_name.replace('/', '.').replace('features.', '')
    xml_fname = 'TESTS-' + feature_name + '.xml'
    context.config.userdata.xml_report_name = xml_fname


def before_all(context):
    """These run before the whole shooting match."""
    logging.info("Setting up...")
    userdata = context.config.userdata

    # remove old output folder
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively, (Path(HTML_REPORT_DIR).parent, 3))
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively, (Path(XML_REPORT_DIR).parent, 3))
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively, (Path(DATA_REPORT_DIR).parent, 3))

    # update env variable
    # kdb.ENV = session.config.getoption("--env")
    kdb.ENV = userdata.get("env", "dev")
    # browser name is inputted in cmd
    # kdb.BROWSER = session.config.getoption("--browser")
    kdb.BROWSER = userdata.get("browser", "chrome")
    # the param values is inputted in cmd
    # parameters = session.config.getoption("--params")
    parameters = userdata.get("params")
    if parameters:
        kdb.PARAMS = str(parameters).split(",")
    # The CI workspace
    # kdb.WORKSPACE = session.config.getoption("--workspace")
    kdb.WORKSPACE = userdata.get("workspace")
    # create build lock file
    if kdb.WORKSPACE:
        check_and_create_build_lock_file()
    #
    kdb.PROFILE_NAME = userdata.get("profile")
    kdb.APP_PATH = userdata.get("app-path")

    # create logs folder if not exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    # create html folder if not exists
    if not userdata.get("no-report") and not os.path.exists(HTML_REPORT_DIR):
        os.makedirs(HTML_REPORT_DIR, exist_ok=True)
    logging.info("Set up successfully")


def after_all(context):
    """These run after the whole shooting match."""
    logging.info(context.config.userdata.xml_report_name)
    logging.info('start after_all(context)')
    userdata = context.config.userdata

    # pytest_sessionfinish
    # close all browser and terminal web driver
    kdb_driver.quit()
    # close appium server port if opened
    MobileManager.close_mobile_port()

    # pytest_terminal_summary
    # copy the data/resources to CI workspace
    if kdb.WORKSPACE:
        _thread.start_new_thread(FileUtil.copytree, (DATA_REPORT_DIR, kdb.WORKSPACE))
    # generate and open html report file in browser
    if not userdata.get("no-report"):
        # feature_name = os.path.splitext(os.path.basename(context.feature.filename))[0]
        # xml_fname = 'TESTS-' + feature_name + '.xml'
        xml_fname = context.config.userdata.xml_report_name
        # generate report
        html_file_path = ReportManager.create_index_report(xml_fname)
        # open report file in browser when run test on local (that means, the kdb.WORKSPACE is None)
        if html_file_path is not None:
            logging.info('The HTML report are generated!')
            if not kdb.WORKSPACE:
                webbrowser.open_new(html_file_path)
            else:
                # copy the html report to CI workspace
                logging.info(
                    '>>> Copying the HTML report to CI workspace from %s to %s.' % (HTML_REPORT_DIR, kdb.WORKSPACE))
                FileUtil.copytree(HTML_REPORT_DIR, kdb.WORKSPACE)
