# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        r = requests.get("http://ee1bfaf2.ngrok.io/checkClothing")
        if r.status_code != 200:
            speak_output = "I can't connect to the device. "
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(True)
                    .response
            )
        
        r=r.json()
        #logger.log(r)
        if r['success']:
            temp = r['temp']
            
            if temp < 60 and not r['wearing_coat']:
                speak_output = f"It is currently {temp:.0f} degrees outside. "
                speak_output += f"The low today is {r['min_temp']:.0f} degrees, and the high is {r['max_temp']:.0f}. "
                speak_output += "You are wearing clothing for warm temperatures, put on a jacket or something "
            
            elif temp >= 60 and r['wearing_coat']:
                speak_output = f"It is currently {temp} degrees outside. "
                speak_output += f"The low today is {r['min_temp']:.0f} degrees, and the high is {r['max_temp']:.0f}. "
                speak_output += "You are wearing clothing for cold temperatures, take that off "
            else:
                speak_output = "Your clothing is appropriate for today's weather. "
            
            if r['is_raining']:
                speak_output += "It is currently raining. Wear a jacket or grab an umbrella on your way out! "
            
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(True)
                    .response
            )
        else:    
            speak_output = "I can't detect a person. "
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(True)
                    .response
            )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
