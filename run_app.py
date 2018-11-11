from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-466588393845-465783418289-466220402164-0bcbf0b83683877e7450def9eda1fe17', #app verification token
							'xoxb-466588393845-465785530625-48RaJi7603iguafYmuUXNpSI', # bot verification token
							'eI5t9ThjVaM6k7xpahaf8PVZ', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))