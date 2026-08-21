from src.db.connection import get_connection


def save_coordinates(key, address, latitude, longitude):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO geocode_cache (
                    key,
                    address,
                    latitude,
                    longitude
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (key)
                DO UPDATE SET
                    address = EXCLUDED.address, 
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude
                """,
                (key, address, latitude, longitude),
            )
            
def get_coordinates(key):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT latitude, longitude
                FROM geocode_cache
                WHERE key = %s
                """,
                (key,),
            )
            
            return cur.fetchone()
        
