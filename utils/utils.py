import re

def get_walmart_product_id(url: str) -> str:
    """
    Extracts the Walmart product ID from a given URL.
    
    Args:
        url (str): The URL to extract the product ID from.
        
    Returns:
        str: The extracted product ID.
    """
    pattern = r"(?<=\/)\d{10,14}"
    match = re.search(pattern, url)
    product_id = match.group() 
    return product_id
