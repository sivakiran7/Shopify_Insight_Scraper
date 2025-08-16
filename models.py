from typing import List, Optional
from pydantic import BaseModel
"""
Pydantic is a Python library used with FastAPI (and other frameworks) for data validation and data parsing.
It makes sure the data you send/receive in your API has the right types and structure.
"""

#faq format
class FAQ(BaseModel):
    question: str
    answer: str

# prduct deatils 
class Product(BaseModel):
    title: str
    handle: Optional[str]
    price: Optional[str]
    image: Optional[str]
    url: Optional[str]

# brand context details
class BrandContext(BaseModel):
    brand_name: Optional[str]
    products: List[Product]
    hero_products: List[Product]
    privacy_policy: Optional[str]
    return_refund_policy: Optional[str]
    faqs: List[FAQ]
    social_handles: List[str]
    contact_details: List[str]
    about: Optional[str]
    important_links: List[str]
