MARGIN = {
    'electronics' : 25 , 
    'stationary' : 20 , 
    'gift' : 24 , 
    'food' : 20 , 
    'clothes' : 35 , 
    'wearables' : 30
}

def create_filters(filters:dict) : 
    new_filters = {} 

    for key in filters : 
        if filters[key] : 
            if key == 'category' and filters[key] not in MARGIN  :
                continue 
            new_filters[key] = filters[key]  
    return new_filters


