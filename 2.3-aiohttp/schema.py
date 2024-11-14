from pydantic import BaseModel, field_validator

class AdvertisementBase(BaseModel):
    owner: str | None = None
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
    owner: str | None = None
    title: str | None = None
    description: str | None = None       

class CreateAdvertisement(AdvertisementBase):
    owner: str | None = None
    title: str
    description: str