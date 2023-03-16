import sys
import traceback

from src.intrastructure import mail_service, questionnaire_store


def before_scenario(context, scenario):
    # This is a nasty global memory storage system, so we'll tidy up before each test
    questionnaire_store.clear()
    mail_service.clear()
    context.uac_for = {}


def after_step(context, step):
    if step.status == "failed":
        traceback.print_tb(step.exc_traceback, file=sys.stderr)
