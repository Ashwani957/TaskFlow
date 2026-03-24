from fastapi import Request, HTTPException , status,Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session 
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
from src.utils.db import get_db 
import jwt



def is_authenticated(request:Request,db:Session=Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            token = request.cookies.get("access_token")
        
        if not token: 
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is Missing")
        
        if token.startswith("Bearer "):
            token = token.split(" ")[-1]

    # Here we validate the token 
    
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        print(data)
        user_id=data.get("_id")
        exp_time=data.get("exp")
        user_name=data.get("username")
   
        if db is None:
            raise HTTPException(500, detail="Database session is None in is_authenticated helper")
        user =db.query(UserModel).filter(UserModel.id==user_id).first()
        # if the user does not exist then:
        if not user : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOu are unauthorized")


        return user ; 
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU are Unauthorized")

