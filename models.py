from typing import Any
from pydantic import BaseModel, model_validator


class Item(BaseModel):
    name: str
    item_id: str
    original_price: float
    price: float
    discount: str
    rating: float
    review: int
    location: str
    seller_name: str
    seller_id: str
    item_sold: str
    item_url: str
    image_url: str

    @model_validator(mode='before')
    @classmethod
    def prepare_data(cls, data: Any) -> Any:
        data['name'] = data.get('name', "")
        data['item_id'] = data.get('itemId', "")
        original_price = data.get('originalPrice') if data.get('originalPrice') else -1
        data['original_price'] = float(original_price)
        price = data.get('price') if data.get('price') else -1
        data['price'] = float(price)
        discount = data.get('discount') if data.get('discount') else " off"
        data['discount'] = discount[:-4]
        rating = data.get('ratingScore') if data.get('ratingScore') else 0
        data['rating'] = format(float(rating), ".2f")
        review = data.get('review') if data.get('review') else 0
        data['review'] = int(review)
        data['location'] = data.get('location', "")
        data['seller_name'] = data.get('sellerName', "")
        data['seller_id'] = data.get('sellerId', "")
        item_sold = data.get("itemSoldCntShow") if data.get("itemSoldCntShow") else "0 sold"
        data['item_sold'] = item_sold[:-5]
        data['item_url'] = data.get('itemUrl', "")
        data['image_url'] = data.get('image', "")
        return data