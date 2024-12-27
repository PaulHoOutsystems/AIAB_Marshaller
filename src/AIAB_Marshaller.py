import logging, socket
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request
from flask_restx import Api, Resource

logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler('AIAB_Marshaller.log',
                                    when="d",
                                    interval=1,
                                    backupCount=5)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)
app.config.from_prefixed_env()
api = Api(app, version='1.0', title='AIAB Marshaller',
          description='AIAB Marshaller',
          )
       
def setup():
    logger.debug("TO-DO: Do some setup activities here if needed")
        

@api.route('/hello/<name>')
@api.doc(params={'name': 'Your name'})
class HelloWorld(Resource):
    def get(self, name):
        return {'message': "hello, " + name + "@" + socket.gethostname()}

    @api.response(403, 'Not Authorized')
    def post(self, name):
        api.abort(403)    


@api.route('/v1/chat/completions')
class Chat(Resource):
    def post(self):
        aiab_request = request.json

        # Do note that during AI Agent builder setup of adding endpoint, there is a ping message being sent
        # we need to accomodate and also respond with a 200
        if (str(aiab_request['messages'][0]['content']).startswith("This is a test. Answer only with") and  str(aiab_request['messages'][0]['role']) == "system"):
            return  {}, 200
        
        
        logger.info(aiab_request)
        temp = aiab_request['temperature']
        max_tokens = aiab_request['maxTokens']
        
        for msg in aiab_request['messages']:
            msg_role = msg['role']
            msg_content = msg['content']
            logger.debug("This is a user_role ("+ str(msg_role) + ") sent content message :" + str(msg_content))
        
        logger.debug("Temperature = " + str(temp))
        logger.debug("Max Tokens = " + str(max_tokens))
        
        # Do some processing here which interacts with on-premise model and prepare for the response back to AI Agent builder
        # .... below are only examples, please replace with appropriate processed values from custom AI model response
        choices = [
            {
            'content' : 'Some content here',
            },
            {
            'content' : 'More content here',
            },        
        ] 
        completedTokens = 100
        promptTokens = 200
        totalTokens = 300
        # .... end of processing
        
 
        response_json = {}
        response_json['choices'] = choices
        response_json['usage'] = {
            'completionTokens' :  completedTokens,
            'promptTokens' :  promptTokens,
            'totalTokens' :  totalTokens,
        }           

        return  response_json, 200

@api.route('/v1/chat/generate')
class GenerateChat(Resource):
    def post(self):
        aiab_request = request.json
 
        # Do note that during AI Agent builder setup of adding endpoint, there is a ping message being sent
        # we need to accomodate and also respond with a 200
        if (str(aiab_request['messages'][0]['content']).startswith("This is a test. Answer only with") and  str(aiab_request['messages'][0]['role']) == "system"):
            return  {}, 200
        
        
        logger.info(aiab_request)
        temp = aiab_request['temperature']
        max_tokens = aiab_request['maxTokens']

        logger.debug("Temperature = " + str(temp))
        logger.debug("Max Tokens = " + str(max_tokens))
                
        for msg in aiab_request['messages']:
            msg_role = msg['role']
            msg_content = msg['content']
            logger.debug("This is a user_role ("+ str(msg_role) + ") sent content message :" + str(msg_content))
            
        
        # Do some processing here which interacts with on-premise model and prepare for the response back to AI Agent builder
        # .... below are only examples, please replace with appropriate processed values from custom AI model response
        choices = [
            {
            'content' : 'Some content here',
            },
            {
            'content' : 'More content here',
            },        
        ] 
        completedTokens = 100
        promptTokens = 200
        totalTokens = 300
        # .... end of processing
        
 
        response_json = {}
        response_json['choices'] = choices
        response_json['usage'] = {
            'completionTokens' :  completedTokens,
            'promptTokens' :  promptTokens,
            'totalTokens' :  totalTokens,
        }        
        
        return  response_json, 200      

setup()


