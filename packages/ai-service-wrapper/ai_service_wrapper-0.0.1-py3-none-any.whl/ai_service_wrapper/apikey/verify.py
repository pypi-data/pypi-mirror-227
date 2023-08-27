import time
import requests
from ..utils.logger import setup_logger

logger = setup_logger("APIKEY")

def verify_apikey_by_file(apikey, apikeys_file):
    with open(apikeys_file, "r") as file:
        apikeys = [ key.strip("\n") for key in file ]
        if apikey in apikeys:
            return True
    
    return False

def verify_apikey(apikey, apikey_service_host, retry=3):
    print(apikey_service_host)
    for _ in range(retry):
        try:
            response = requests.post(f"{apikey_service_host}/api-keys/auth-http",
                                     data={ 
                                        "key": apikey,
                                        "requestAt": 0 
                                        })
            if response.status_code == 200:
                logger.info("Success verify apikey from apikey service")
                return True
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            logger.error(str(e))
    
    return False