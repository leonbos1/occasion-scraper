"""Migration script to create car_images table"""
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URI = 'mysql+pymysql://root:kaaskaas123@localhost:3306/occasions'
engine = create_engine(DATABASE_URI)

# SQL to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS car_images (
    id VARCHAR(36) NOT NULL,
    car_id VARCHAR(36) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    `order` INT NOT NULL DEFAULT 0,
    created DATETIME DEFAULT NULL,
    updated DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    KEY car_id (car_id),
    KEY idx_order (`order`),
    CONSTRAINT car_images_ibfk_1 FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

# Execute the SQL
try:
    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.commit()
    print("✅ car_images table created successfully")
except Exception as e:
    print(f"Error creating table: {e}")
