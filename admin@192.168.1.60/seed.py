"""Run once to populate the database with sample bakery products."""

from app.database import SessionLocal, engine
import app.models as models

models.Base.metadata.create_all(bind=engine)

PRODUCTS = [
    {"name": "Sourdough Loaf",       "category": "Bread",   "price": 8.50, "description": "Classic artisan sourdough with a crispy crust and chewy interior."},
    {"name": "Baguette",             "category": "Bread",   "price": 3.00, "description": "Traditional French baguette with a golden crust and airy crumb."},
    {"name": "Croissant",            "category": "Pastry",  "price": 3.50, "description": "Buttery, flaky French croissant baked fresh every morning."},
    {"name": "Cinnamon Roll",        "category": "Pastry",  "price": 4.50, "description": "Soft spiral roll with cinnamon sugar filling and cream cheese glaze."},
    {"name": "Almond Danish",        "category": "Pastry",  "price": 4.00, "description": "Flaky pastry layered with almond cream and topped with sliced almonds."},
    {"name": "Chocolate Eclair",     "category": "Pastry",  "price": 4.25, "description": "Light choux pastry filled with vanilla cream and topped with dark chocolate."},
    {"name": "Blueberry Muffin",     "category": "Muffin",  "price": 3.00, "description": "Moist muffin loaded with fresh blueberries and a crumbly sugar top."},
    {"name": "Chocolate Cake Slice", "category": "Cake",    "price": 6.00, "description": "Rich triple-layer chocolate cake with silky ganache frosting."},
    {"name": "Carrot Cake Slice",    "category": "Cake",    "price": 5.50, "description": "Spiced carrot cake with walnuts and smooth cream cheese frosting."},
    {"name": "Lemon Tart",           "category": "Tart",    "price": 5.50, "description": "Buttery pastry shell filled with smooth tangy lemon curd."},
]


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Product).count() > 0:
            print("Database already seeded. Skipping.")
            return
        for p in PRODUCTS:
            db.add(models.Product(**p))
        db.commit()
        print(f"Seeded {len(PRODUCTS)} products.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
