import openai
import json

#Clase para utilizar cualquier LLM para procesar un texto
#Y regresar una funcion a llamar con sus parametros
#Uso el modelo 0613, pero puedes usar un poco de
#prompt engineering si quieres usar otro modelo
class LLM():
    def __init__(self):
        pass
    
    def process_functions(self, text):
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    #role define el "tipo de personalidad"
                    {"role": "system", "content": "Eres un asistente, tus funciones son: responder preguntas especificas, conversar sobre diversos temas y realizar funciones solicitadas"},
                    {"role": "user", "content": text},
            ], functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            },
                            "temperatura": {
                                "type": "string",
                                "description": "La temperatura, debes leerla como si fuera texto",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "hola",
                    "description": "Responder un saludo, debes saludar cordialmente en lenguaje natural con una formalidad intermedia cuando te digan 'hola' o un '¿como estas?' o '¿que tal hoy?'. ten en cuenta que eres un asistente virtual llamada SARA.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "saludo": {
                                "type": "string",
                                "description": "El saludo recibido, puede ser 'hola', '¿como estas?' o '¿que tal hoy?'",
                            },
                        },
                        "required": ["saludo"],
                    }
                },
                {
                    "name": "explicar_algo",
                    "description": "Explica un tema solicitado de manera comprensible.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tema": {
                                "type": "string",
                                "description": "El tema sobre el que se solicita la explicación. Si no se proporciona, se solicitará al usuario.",
                            },
                            "nivel": {
                                "type": "string",
                                "description": "El nivel de profundidad deseado para la explicación, puede ser 'básico', 'intermedio' o 'avanzado'.",
                            },
                            "ejemplos": {
                                "type": "boolean",
                                "description": "Indica si se deben incluir ejemplos en la explicación.",
                            }
                        },
                        "required": ["tema"]
                    }
                },                {
                    "name": "abrir_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            },
                            "nombre_pagina": {
                                "type": "string",
                                "description": "el nombre del sitio al que se desea entrar"
                            },
                            "buscador": {
                                "type": "string",
                                "description": "sitio especifico para buscar informacion en internet, la pagina es www.google.com"
                            }
                        }
                    }
                },
                {
                    "name": "responder",
                    "description": "responde cordial y brevemente lo solicitado",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "contenido": {
                                "type": "string",
                                "description": "contenido o tema que compone la conversacion",
                            },
                        }
                    }
                }

            ],
            function_call="auto",
        )
        
        message = response["choices"][0]["message"]
        
        #Nuestro amigo GPT quiere llamar a alguna funcion?
        if message.get("function_call"):
            #Sip
            function_name = message["function_call"]["name"] #Que funcion?
            args = message.to_dict()['function_call']['arguments'] #Con que datos?
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    #Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    #Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    #respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    #respuesta haya sido JSON por ejemplo
    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                #Aqui tambien puedes cambiar como se comporta
                {"role": "system", "content": "Eres un asistente, tus funciones son: responder preguntas especificas, conversar sobre diversos temas y realizar funciones solicitadas"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]