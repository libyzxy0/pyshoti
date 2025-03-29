from flask import Blueprint, Response
from controllers.api_controller import get_shoti, add_user, add_shoti, get_shoti_db

api_bp = Blueprint('api', __name__)


@api_bp.route("/", methods=["GET", "POST"])
def ascii_response():
    message = """          _--__              
         /  /  \             
        |    ,-.)            
/\_     ( ((` =(             
\ /      \)\  _/    _/\      
 \\    .-'   '--.   \ /      
  \\_.' ,  \  \  \  //       
   \_.-'\,_/ _/'\ \//        
         \   (   '_/         
         |  . '.             
         |      \            
    Shoti API is awesome!
         \  _|   \           
          \  |   |           
           '.|   |           
              \  '\__        
               `-._  '. _    
                  \`;-.` `._
                   \ \ `'-._|      
                     \ )     
                      \_\ """
    return Response(message, content_type="text/plain;")

api_bp.route("/get-db", methods=["GET", "POST"])(get_shoti_db)
api_bp.route("/get-shoti", methods=["GET", "POST"])(get_shoti)
api_bp.route("/new-user", methods=["POST"])(add_user)
api_bp.route("/new-shoti", methods=["POST"])(add_shoti)
