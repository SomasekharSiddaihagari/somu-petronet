from datetime import date, timedelta
 
POLICY = {
    "Mobile Handset": {
        "frequency_years": 2,
        "grades": {
            "E1": 30000,
            "E2": 30000,
            "E3": 30000,
            "E4": 30000,
            "E5": 30000,
            "E6": 40000,
            "E7": 40000,
        }
    },
    "Laptop / Desktop": {
        "frequency_years": 3,
        "buyback_years": 3,
        "grades": {
            "E1": 50000, "E2": 50000, "E3": 50000,
            "E4": 50000, "E5": 50000,
            "E6": 60000, "E7": 60000,
        },
        "requires_permanent": True,
        "buyback": True
    },
 
    "Data Card": {
        "frequency_years": 3,
        "ceiling": 1000,
        "requires_laptop": True,
        "requires_permanent": True
    },
 
    "Furniture": {
        "Electronics": {
            "buyback_years": 4,
            "min_item_value": 5000,
            "grades": {
                "E1": 100000, "E2": 100000,
                "E3": 140000, "E4": 140000,
                "E5": 165000, "E6": 225000, "E7": 280000
            }
        },
        "Utility & Decorative Furniture": {
            "buyback_years": 6,
            "min_item_value": 5000,
            "grades": {
                "E1": 50000, "E2": 50000,
                "E3": 70000, "E4": 70000,
                "E5": 82500, "E6": 112500, "E7": 140000
            }
        },
        "Soft Furnishing": {
            "buyback_years": 4,
            "min_item_value": 5000,
            "grades": {
                "E1": 50000, "E2": 50000,
                "E3": 70000, "E4": 70000,
                "E5": 82500, "E6": 112500, "E7": 140000
        }
        },
        
        "Sports Equipment": {
            "buyback_years": 4,
            "min_item_value": 5000,
            "grades": {
                "E1": 50000, "E2": 50000,
                "E3": 70000, "E4": 70000,
                "E5": 82500, "E6": 112500, "E7": 140000
        }
        }
        
    }
}
 
 
def calculate_next_date(d: date, years: int):
    return date(d.year + years, d.month, d.day)