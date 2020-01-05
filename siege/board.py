def board():
    continents = [
        {'id': 'asia', 'name': 'asia', 'bonus': 7},
        {'id': 'north-america', 'name': 'north america', 'bonus': 5},
        {'id': 'europe', 'name': 'europe', 'bonus': 5},
        {'id': 'africa', 'name': 'africa', 'bonus': 3},
        {'id': 'australia', 'name': 'australia', 'bonus': 2},
        {'id': 'south-america', 'name': 'south america', 'bonus': 2},
    ]
    territories = [
        {
            'id': 'alaska',
            'name': 'alaska',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': ['alberta', 'north-west-territory', 'kamchatka']
        },
        {
            'id': 'north-west-territory',
            'name': 'north west territory',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': ['alberta', 'alaska', 'ontario', 'greenland']
        },
        {
            'id': 'greenland',
            'name': 'greenland',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'north-west-territory',
                'quebec',
                'ontario',
                'iceland'
            ]
        },
        {
            'id': 'alberta',
            'name': 'alberta',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'north-west-territory',
                'alaska',
                'ontario',
                'western-united-states'
            ]
        },
        {
            'id': 'ontario',
            'name': 'ontario',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'north-west-territory',
                'alberta',
                'quebec',
                'greenland',
                'western-united-states',
                'eastern-united-states'
            ]
        },
        {
            'id': 'quebec',
            'name': 'quebec',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'ontario',
                'greenland',
                'eastern-united-states'
            ]
        },
        {
            'id': 'western-united-states',
            'name': 'western united states',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'alberta',
                'ontario',
                'eastern-united-states',
                'central-america'
            ]
        },
        {
            'id': 'eastern-united-states',
            'name': 'western united states',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'quebec',
                'ontario',
                'western-united-states',
                'central-america'
            ]
        },
        {
            'id': 'central-america',
            'name': 'central america',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'eastern-united-states',
                'western-united-states',
                'venezuela'
            ]
        },
        {
            'id': 'venezuela',
            'name': 'venezuela',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'central-america',
                'peru',
                'brazil'
            ]
        },
        {
            'id': 'peru',
            'name': 'peru',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'venezuela',
                'brazil',
                'argentina',
            ]
        },
        {
            'id': 'brazil',
            'name': 'brazil',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'venezuela',
                'peru',
                'argentina',
                'north-africa',
            ]
        },
        {
            'id': 'argentina',
            'name': 'argentina',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'peru',
                'brazil',
            ]
        },
        {
            'id': 'north-africa',
            'name': 'north africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'brazil',
                'western-europe',
                'southern-europe',
                'egypt',
                'east-africa',
                'congo',
            ]
        },
        {
            'id': 'egypt',
            'name': 'egypt',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'north-africa',
                'southern-europe',
                'middle-east',
                'east-africa',
            ]
        },
        {
            'id': 'east-africa',
            'name': 'east africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'middle-east',
                'egypt',
                'north-africa',
                'congo',
                'south-africa',
                'madagascar',
            ]
        },
        {
            'id': 'congo',
            'name': 'congo',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'north-africa',
                'east-africa',
                'south-africa',
            ]
        },
        {
            'id': 'south-africa',
            'name': 'south africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'congo',
                'east-africa',
                'madagascar',
            ]
        },
        {
            'id': 'madagascar',
            'name': 'madagascar',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'east-africa',
                'south-africa',
            ]
        },
        {
            'id': 'iceland',
            'name': 'iceland',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'greenland',
                'great-britain',
                'scandinavia',
            ]
        },
        {
            'id': 'scandinavia',
            'name': 'scandinavia',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'ukraine',
                'northern-europe',
                'iceland',
                'great-britain',
            ]
        },
        {
            'id': 'ukraine',
            'name': 'ukraine',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'ural',
                'afghanistan',
                'middle-east',
                'southern-europe',
                'northern-europe',
                'scandinavia',
            ]
        },
        {
            'id': 'northern-europe',
            'name': 'northern europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'scandinavia',
                'ukraine',
                'southern-europe',
                'western-europe',
                'great-britain',
            ]
        },
        {
            'id': 'southern-europe',
            'name': 'southern europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'middle-east',
                'egypt',
                'north-africa',
                'western-europe',
                'northern-europe',
                'ukraine',
            ]
        },
        {
            'id': 'western-europe',
            'name': 'western europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'great-britain',
                'northern-europe',
                'southern-europe',
                'north-africa',
            ]
        },
        {
            'id': 'great-britain',
            'name': 'great britain',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'iceland',
                'scandinavia',
                'northern-europe',
                'western-europe',
            ]
        },
        {
            'id': 'indonesia',
            'name': 'indonesia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'siam',
                'new-guinea',
                'western-australia',
            ]
        },
        {
            'id': 'new-guinea',
            'name': 'new guinea',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'indonesia',
                'new-guinea',
                'western-australia',
                'eastern-australia',
            ]
        },
        {
            'id': 'western-australia',
            'name': 'western australia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'indonesia',
                'new-guinea',
                'eastern-australia',
            ]
        },
        {
            'id': 'eastern-australia',
            'name': 'eastern australia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'new-guinea',
                'eastern-australia',
                'western-australia',
            ]
        },
        {
            'id': 'middle-east',
            'name': 'middle east',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'east-africa',
                'egypt',
                'southern-europe',
                'ukraine',
                'afghanistan',
                'india',
            ]
        },
        {
            'id': 'afghanistan',
            'name': 'afghanistan',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'middle-east',
                'ukraine',
                'ural',
                'china',
                'india',
            ]
        },
        {
            'id': 'ural',
            'name': 'ural',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'afghanistan',
                'ukraine',
                'siberia',
                'china',
            ]
        },
        {
            'id': 'siberia',
            'name': 'siberia',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'ural',
                'china',
                'yakutsk',
                'irkutsk',
                'mongolia',
                'china',
            ]
        },
        {
            'id': 'yakutsk',
            'name': 'yakutsk',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'kamchatka',
                'irkutsk',
                'siberia',
            ]
        },
        {
            'id': 'kamchatka',
            'name': 'kamchatka',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'yakutsk',
                'irkutsk',
                'mongolia',
                'japan',
            ]
        },
        {
            'id': 'japan',
            'name': 'japan',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'kamchatka',
                'mongolia',
            ]
        },
        {
            'id': 'irkutsk',
            'name': 'irkutsk',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'siberia',
                'yakutsk',
                'kamchatka',
                'mongolia',
            ]
        },
        {
            'id': 'mongolia',
            'name': 'mongolia',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'siberia',
                'irkutsk',
                'kamchatka',
                'japan',
                'china',
            ]
        },
        {
            'id': 'china',
            'name': 'china',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'mongolia',
                'siberia',
                'ural',
                'afghanistan',
                'india',
                'siam',
            ]
        },
        {
            'id': 'siam',
            'name': 'siam',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'china',
                'india',
                'indonesia',
            ]
        },
        {
            'id': 'india',
            'name': 'india',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to': [
                'middle-east',
                'afghanistan',
                'china',
                'siam',
            ]
        },
    ]

    return {'continents': continents, 'territories': territories}
