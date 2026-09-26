import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "data"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "agridds.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign keys
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# DATABASE MIGRATION HELPERS
# ============================================================

def add_column_if_missing(connection, table_name, column_name, column_definition):

    cursor = connection.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    if column_name not in columns:

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_definition}
            """
        )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # FARMERS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS farmers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            phone TEXT,

            village TEXT,

            province TEXT,

            created_at TEXT NOT NULL

        )
        """
    )

    # --------------------------------------------------------
    # FARMS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS farms (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            farmer_id INTEGER NOT NULL,

            farm_name TEXT NOT NULL,

            area_acres REAL,

            province TEXT,

            district TEXT,

            tehsil TEXT,

            place_name TEXT,

            latitude REAL,

            longitude REAL,

            irrigation_system TEXT,

            soil_type TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (farmer_id)
                REFERENCES farmers(id)
                ON DELETE CASCADE

        )
        """
    )

    # --------------------------------------------------------
    # FIELDS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fields (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            farm_id INTEGER NOT NULL,

            field_name TEXT NOT NULL,

            crop TEXT,

            variety TEXT,

            sowing_date TEXT,

            crop_stage TEXT,

            area_acres REAL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (farm_id)
                REFERENCES farms(id)
                ON DELETE CASCADE

        )
        """
    )

    # ========================================================
    # MIGRATE EXISTING FARMS TABLE
    # ========================================================

    add_column_if_missing(
        connection,
        "farms",
        "province",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "farms",
        "district",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "farms",
        "tehsil",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "farms",
        "place_name",
        "TEXT",
    )

    # Existing farms already have latitude/longitude,
    # so those columns are NOT added again.

    connection.commit()

    connection.close()


# ============================================================
# FARMER FUNCTIONS
# ============================================================

def add_farmer(
    name,
    phone="",
    village="",
    province="",
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO farmers (
            name,
            phone,
            village,
            province,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            village,
            province,
            created_at,
        ),
    )

    farmer_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return farmer_id


def get_farmers():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM farmers
        ORDER BY id DESC
        """
    )

    farmers = cursor.fetchall()

    connection.close()

    return farmers


def get_farmer(farmer_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM farmers
        WHERE id = ?
        """,
        (farmer_id,),
    )

    farmer = cursor.fetchone()

    connection.close()

    return farmer


def update_farmer(
    farmer_id,
    name,
    phone="",
    village="",
    province="",
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE farmers

        SET
            name = ?,
            phone = ?,
            village = ?,
            province = ?

        WHERE id = ?
        """,
        (
            name,
            phone,
            village,
            province,
            farmer_id,
        ),
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_farmer(farmer_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM farmers
        WHERE id = ?
        """,
        (farmer_id,),
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# ============================================================
# FARM FUNCTIONS
# ============================================================

def add_farm(
    farmer_id,
    farm_name,
    area_acres,
    latitude,
    longitude,
    irrigation_system,
    soil_type,
    province="",
    district="",
    tehsil="",
    place_name="",
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO farms (

            farmer_id,
            farm_name,
            area_acres,

            province,
            district,
            tehsil,
            place_name,

            latitude,
            longitude,

            irrigation_system,
            soil_type,

            created_at

        )

        VALUES (
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?
        )
        """,
        (
            farmer_id,
            farm_name,
            area_acres,

            province,
            district,
            tehsil,
            place_name,

            latitude,
            longitude,

            irrigation_system,
            soil_type,

            created_at,
        ),
    )

    farm_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return farm_id


def get_farms():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            farms.*,
            farmers.name AS farmer_name

        FROM farms

        LEFT JOIN farmers
            ON farms.farmer_id = farmers.id

        ORDER BY farms.id DESC
        """
    )

    farms = cursor.fetchall()

    connection.close()

    return farms


def get_farm(farm_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            farms.*,
            farmers.name AS farmer_name

        FROM farms

        LEFT JOIN farmers
            ON farms.farmer_id = farmers.id

        WHERE farms.id = ?
        """,
        (farm_id,),
    )

    farm = cursor.fetchone()

    connection.close()

    return farm


def get_farms_by_farmer(farmer_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM farms
        WHERE farmer_id = ?
        ORDER BY id DESC
        """,
        (farmer_id,),
    )

    farms = cursor.fetchall()

    connection.close()

    return farms


def update_farm(
    farm_id,
    farmer_id,
    farm_name,
    area_acres,
    latitude,
    longitude,
    irrigation_system,
    soil_type,
    province="",
    district="",
    tehsil="",
    place_name="",
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE farms

        SET
            farmer_id = ?,
            farm_name = ?,
            area_acres = ?,

            province = ?,
            district = ?,
            tehsil = ?,
            place_name = ?,

            latitude = ?,
            longitude = ?,

            irrigation_system = ?,
            soil_type = ?

        WHERE id = ?
        """,
        (
            farmer_id,
            farm_name,
            area_acres,

            province,
            district,
            tehsil,
            place_name,

            latitude,
            longitude,

            irrigation_system,
            soil_type,

            farm_id,
        ),
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_farm(farm_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM farms
        WHERE id = ?
        """,
        (farm_id,),
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# ============================================================
# FIELD FUNCTIONS
# ============================================================

def add_field(
    farm_id,
    field_name,
    crop,
    variety,
    sowing_date,
    crop_stage,
    area_acres,
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO fields (

            farm_id,
            field_name,
            crop,
            variety,
            sowing_date,
            crop_stage,
            area_acres,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            farm_id,
            field_name,
            crop,
            variety,
            sowing_date,
            crop_stage,
            area_acres,
            created_at,
        ),
    )

    field_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return field_id


def get_fields():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            fields.*,
            farms.farm_name,
            farmers.name AS farmer_name

        FROM fields

        LEFT JOIN farms
            ON fields.farm_id = farms.id

        LEFT JOIN farmers
            ON farms.farmer_id = farmers.id

        ORDER BY fields.id DESC
        """
    )

    fields = cursor.fetchall()

    connection.close()

    return fields


def get_field(field_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            fields.*,
            farms.farm_name,
            farmers.name AS farmer_name

        FROM fields

        LEFT JOIN farms
            ON fields.farm_id = farms.id

        LEFT JOIN farmers
            ON farms.farmer_id = farmers.id

        WHERE fields.id = ?
        """,
        (field_id,),
    )

    field = cursor.fetchone()

    connection.close()

    return field


def get_fields_by_farm(farm_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM fields
        WHERE farm_id = ?
        ORDER BY id DESC
        """,
        (farm_id,),
    )

    fields = cursor.fetchall()

    connection.close()

    return fields


def update_field(
    field_id,
    farm_id,
    field_name,
    crop,
    variety,
    sowing_date,
    crop_stage,
    area_acres,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE fields

        SET
            farm_id = ?,
            field_name = ?,
            crop = ?,
            variety = ?,
            sowing_date = ?,
            crop_stage = ?,
            area_acres = ?

        WHERE id = ?
        """,
        (
            farm_id,
            field_name,
            crop,
            variety,
            sowing_date,
            crop_stage,
            area_acres,
            field_id,
        ),
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_field(field_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM fields
        WHERE id = ?
        """,
        (field_id,),
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM farmers"
    )

    farmer_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM farms"
    )

    farm_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM fields"
    )

    field_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fields
        WHERE crop IS NOT NULL
        AND crop != ''
        """
    )

    crop_count = cursor.fetchone()[0]

    connection.close()

    return {
        "farmers": farmer_count,
        "farms": farm_count,
        "fields": field_count,
        "crops": crop_count,
    }


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()
