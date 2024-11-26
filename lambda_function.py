from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.services import ServiceException
from typing import Union, List, Optional, Tuple
import logging

from coordinates_finder import search_coordinates
from caja_vecina_finder import search_cajas_vecinas, search_ATM, search_cajas_vecinas_and_ATM, CajaVecina, ATM

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sb = CustomSkillBuilder(api_client=DefaultApiClient())

def get_device_location(handler_input) -> Optional[Tuple[float, float]]:
    try:
        service_client_fact = handler_input.service_client_factory
        if not service_client_fact:
            return None

        try:
            geo_supported = handler_input.request_envelope.context.system.device.supported_interfaces.geolocation
            device_geolocation = handler_input.request_envelope.context.geolocation
            if geo_supported and device_geolocation.coordinate:
                return (device_geolocation.coordinate.latitude_in_degrees,
                       device_geolocation.coordinate.longitude_in_degrees)
        except ServiceException as e:
            logger.info(f"Geolocation not available: {str(e)}")
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting device location: {str(e)}")
        return None

def format_entities_response(entities: List[Union[CajaVecina, ATM]], count: int = 3) -> str:
    if not entities:
        return "No encontré ninguna ubicación cercana."
    
    speech_text = "He encontrado estas ubicaciones cercanas: "
    for i, entity in enumerate(entities[:count], 1):
        speech_text += f"Número {i}: {entity.get_speech_text()} "
    return speech_text

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = ("Puedes buscar servicios de BancoEstado diciendo: "
                      "'busca Cajas Vecinas cerca' para Cajas Vecinas, "
                      "'busca Cajeros cerca' para Cajeros Automáticos, o "
                      "'busca Cajas Vecinas o Cajeros cerca' para ambos. "
                      "También puedes especificar una dirección diciendo "
                      "'cerca de' seguido de tu dirección.")
        
        handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Bienvenido", speech_text))\
            .set_should_end_session(False)
        return handler_input.response_builder.response

class FindBancoEstadoEntitiesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("FindCajasVecinasIntent")(handler_input) or
                is_intent_name("FindATMIntent")(handler_input) or
                is_intent_name("FindBothIntent")(handler_input))

    def handle(self, handler_input):
        try:
            intent_name = handler_input.request_envelope.request.intent.name
            slots = handler_input.request_envelope.request.intent.slots
            address = slots.get("address", None)
            address_value = address.value if address else None
            
            if address_value:
                lat, lng = search_coordinates(address_value)
                if lat is None or lng is None:
                    speech_text = ("No pude encontrar esa dirección. "
                                 "Por favor, intenta nuevamente con una dirección diferente.")
                    return handler_input.response_builder.speak(speech_text)\
                        .set_should_end_session(False).response
            else:
                location = get_device_location(handler_input)
                
                if location:
                    lat, lng = location
                else:
                    speech_text = ("No pude obtener tu ubicación actual. "
                                 "Por favor, especifica una dirección diciendo "
                                 "'busca cerca de' seguido de tu dirección.")
                    return handler_input.response_builder.speak(speech_text)\
                        .set_should_end_session(False).response
            
            entities = []
            try:
                if intent_name == "FindCajasVecinasIntent":
                    data = search_cajas_vecinas(lat, lng)
                    if data:
                        entities = [CajaVecina(item) for item in data]
                elif intent_name == "FindATMIntent":
                    data = search_ATM(lat, lng)
                    if data:
                        entities = [ATM(item) for item in data]
                else:
                    entities = search_cajas_vecinas_and_ATM(lat, lng)
            except Exception as e:
                logger.error(f"Error searching for entities: {str(e)}")
                speech_text = ("Lo siento, hubo un problema buscando servicios. "
                             "Por favor, intenta nuevamente.")
                return handler_input.response_builder.speak(speech_text)\
                    .set_should_end_session(False).response
            
            if not entities:
                speech_text = "No encontré servicios cercanos a esa ubicación."
                return handler_input.response_builder.speak(speech_text)\
                    .set_should_end_session(False).response
            
            speech_text = format_entities_response(entities)
            title = "Ubicaciones Cercanas"
            
            return handler_input.response_builder.speak(speech_text)\
                .set_card(SimpleCard(title, speech_text))\
                .set_should_end_session(False).response
                
        except Exception as e:
            logger.error(f"Error in FindBancoEstadoEntitiesIntentHandler: {str(e)}", exc_info=True)
            speech_text = ("Lo siento, ocurrió un error inesperado. "
                         "Por favor, intenta nuevamente.")
            return handler_input.response_builder.speak(speech_text)\
                .set_should_end_session(False).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = ("Puedes buscar servicios de BancoEstado diciendo: "
                      "'busca Cajas Vecinas cerca' para Cajas Vecinas, "
                      "'busca Cajeros cerca' para Cajeros Automáticos, o "
                      "'busca Cajas Vecinas o Cajeros cerca' para ambos. "
                      "También puedes especificar una dirección diciendo "
                      "'cerca de' seguido de tu dirección.")
        
        return handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Ayuda", speech_text))\
            .set_should_end_session(False).response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speech_text = "¡Nos vemos!"
        return handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Adiós", speech_text))\
            .set_should_end_session(True).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speech_text = ("Lo siento, tuve problemas procesando tu solicitud. "
                      "Por favor, intenta nuevamente.")
        
        return handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Error", speech_text))\
            .set_should_end_session(False).response

class PermissionsGrantedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("Connections.Response")(handler_input) and \
               handler_input.request_envelope.request.name == "AskFor"

    def handle(self, handler_input):
        if handler_input.request_envelope.request.status.code == "200":
            speech_text = ("Gracias por otorgar los permisos. "
                         "Ahora puedo ayudarte a encontrar servicios cerca de tu ubicación. "
                         "¿Qué deseas buscar?")
        else:
            speech_text = ("Sin acceso a tu ubicación, necesitarás especificar "
                         "una dirección. Por ejemplo, puedes decir 'busca cajeros cerca de' "
                         "seguido de tu dirección.")

        return handler_input.response_builder.speak(speech_text)\
            .set_should_end_session(False).response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FindBancoEstadoEntitiesIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(PermissionsGrantedRequestHandler())

def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)