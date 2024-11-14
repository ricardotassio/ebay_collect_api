import logging

import pandas as pd
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding

from src.config.db import get_collection
from src.config.settings import API_KEY

# Access the MongoDB collection
collection = get_collection()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

christmas_categories = {
    'holiday_decor': '117419',
    'christmas_trees': '117406',
    'christmas_lights': '117422',
    'ornaments': '117419',
    'wreaths_garlands': '117421',
    'crackers': '117420',
    'stockings_hangers': '117423',
    'figurines': '117424',
    'table_decor': '117425',
    'yard_decor': '117426',
    'gift_boxes': '102380',
    'gift_tags_stickers': '184488',
    'nativity_items': '156862',
    'christmas_costumes': '53361',
    'christmas_music': '11233',
    'christmas_movies': '11232',
    'christmas_books': '171243',
    'christmas_cards': '170098',
    'christmas_candles': '46782',
    'christmas_crafts': '116724',
    'christmas_cookware': '20628',
    'christmas_tableware': '36027',
    'christmas_bedding': '20444',
    'christmas_clothing': '155241',
    'christmas_jewelry': '10968',
    'christmas_toys': '19028',
    'christmas_games': '233',
    'christmas_electronics': '293',
    'christmas_home_appliances': '20710',
    'christmas_sporting_goods': '888',
    'christmas_health_beauty': '26395',
    'christmas_automotive': '6000',
    'christmas_collectibles': '1',
    'christmas_art': '550',
    'christmas_musical_instruments': '619',
    'christmas_pet_supplies': '1281',
    'christmas_baby_products': '2984',
    'christmas_business_industrial': '12576',
    'christmas_real_estate': '10542',
    'christmas_travel': '3252',
    'christmas_gift_cards': '172008',
}


def get_christmas_data(category_id):
    try:
        api = Finding(appid=API_KEY, config_file=None)
        response = api.execute(
            'findItemsAdvanced', {'categoryId': category_id}
        )
        items = response.dict().get('searchResult', {}).get('item', [])

        if items:
            for item in items:
                document = {
                    'itemId': item.get('itemId'),
                    'title': item.get('title'),
                    'globalId': item.get('globalId'),
                    'primaryCategory': item.get('primaryCategory'),
                    'galleryURL': item.get('galleryURL'),
                    'viewItemURL': item.get('viewItemURL'),
                    'autoPay': item.get('autoPay'),
                    'postalCode': item.get('postalCode'),
                    'location': item.get('location'),
                    'country': item.get('country'),
                    'shippingInfo': item.get('shippingInfo'),
                    'sellingStatus': item.get('sellingStatus'),
                    'listingInfo': item.get('listingInfo'),
                    'returnsAccepted': item.get('returnsAccepted'),
                    'condition': item.get('condition'),
                    'isMultiVariationListing': item.get(
                        'isMultiVariationListing'
                    ),
                    'topRatedListing': item.get('topRatedListing'),
                    'discountPriceInfo': item.get('discountPriceInfo'),
                    'secondaryCategory': item.get('secondaryCategory'),
                    'subtitle': item.get('subtitle'),
                    'productId': item.get('productId'),
                }
                collection.insert_one(document)

            return {'status': 'success', 'inserted_count': len(items)}
        else:
            return {
                'status': 'no_data',
                'message': 'No items found for the given category',
            }
    except ConnectionError as e:
        logger.error(f'Connection error: {e}')
        return {'status': 'error', 'message': str(e)}


def get_all_christmas_data():
    try:
        total_inserted = 0
        api = Finding(appid=API_KEY, config_file=None)
        documents = []
        for category_name, category_id in christmas_categories.items():
            # Fetch data for each category
            response = api.execute(
                'findItemsAdvanced', {'categoryId': category_id}
            )
            items = response.dict().get('searchResult', {}).get('item', [])

            if items:
                # Insert items in batches to MongoDB
                documents = [
                    {
                        'itemId': item.get('itemId'),
                        'title': item.get('title'),
                        'globalId': item.get('globalId'),
                        'primaryCategory': item.get('primaryCategory'),
                        'galleryURL': item.get('galleryURL'),
                        'viewItemURL': item.get('viewItemURL'),
                        'autoPay': item.get('autoPay'),
                        'postalCode': item.get('postalCode'),
                        'location': item.get('location'),
                        'country': item.get('country'),
                        'shippingInfo': item.get('shippingInfo'),
                        'sellingStatus': item.get('sellingStatus'),
                        'listingInfo': item.get('listingInfo'),
                        'returnsAccepted': item.get('returnsAccepted'),
                        'condition': item.get('condition'),
                        'isMultiVariationListing': item.get(
                            'isMultiVariationListing'
                        ),
                        'topRatedListing': item.get('topRatedListing'),
                        'discountPriceInfo': item.get('discountPriceInfo'),
                        'secondaryCategory': item.get('secondaryCategory'),
                        'subtitle': item.get('subtitle'),
                        'productId': item.get('productId'),
                    }
                    for item in items
                ]

                collection.insert_many(documents)
                total_inserted += len(documents)
                logger.info(
                    f"Inserted {len(documents)} items for category '{category_name}'"
                )
            else:
                logger.info(
                    f"No items found for category '{category_name}'"
                )

            return {'status': 'success', 'total_inserted': total_inserted}
    except ConnectionError as e:
        logger.error(f'Connection error: {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')


# Function to retrieve and save data to CSV
def get_christmas_data_to_cscv(category_id):
    try:
        api = Finding(appid=API_KEY, config_file=None)
        response = api.execute(
            'findItemsAdvanced', {'categoryId': category_id}
        )
        items = response.dict().get('searchResult', {}).get('item', [])

        # Convert data to DataFrame
        df = pd.DataFrame(items)

        # Save DataFrame to CSV
        filename = f'christmas_data_{category_id}.csv'
        df.to_csv(filename, index=False)

        return {'status': 'success', 'file': filename}
    except ConnectionError as e:
        logging('Connection error: {e}')
        return {'status': 'error', 'message': str(e)}
