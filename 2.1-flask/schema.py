from pydantic import BaseModel, field_validator


class AdvertisementBase(BaseModel):
    owner_id: int | None = None
    title: str | None = None
    description: str | None = None
       
    @field_validator('title')
    @classmethod
    def check_title(cls, value): 
        if len(value) > 100:
            raise ValueError('title is too large.')
        return value  
    
    @field_validator('description')
    @classmethod
    def check_description(cls, value): 
        if len(value) > 500:
            raise ValueError('description is too large.')
        return value 
    
    
class UpdateAdvertisement(AdvertisementBase):
    owner_id: int  | None = None
    title: str | None = None
    description: str | None = None       


class CreateAdvertisement(AdvertisementBase):
    owner_id: int 
    title: str
    description: str


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None       
    password: str | None = None 
       

    @field_validator('password')
    @classmethod
    def check_password(cls, value): 
        if len(value) < 8:
            raise ValueError('password is too short')
        return value 
    
    
class UpdateUser(UserBase):
    username: str | None = None
    email: str | None = None       
    password: str | None = None 
    
    
class CreateUser(UserBase):
    username: str
    email: str
    password: str 
    