import psycopg2
from psycopg2 import sql
from datetime import datetime

# Function to add a show to the watchlist
def addToWatchlist(user_id, show_id):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn, cur = connect()
    try:
        cur.execute("INSERT INTO watchlist (user_id, movie_id, date_created) VALUES (%s, %s, %s)", (user_id, show_id, date))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error adding to watchlist: {e}")
    finally:
        close(conn, cur)

# Function to remove a show from the watchlist
def removeFromWatchlist(user_id, show_id):
    conn, cur = connect()
    try:
        cur.execute("DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s", (user_id, show_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error removing from watchlist: {e}")
    finally:
        close(conn, cur)

# Function to get a user's watchlist
def getWatchlist(user_id):
    conn, cur = connect()
    try:
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (user_id,))
        results = cur.fetchall()
        return [result[0] for result in results]
    except psycopg2.Error as e:
        print(f"Error getting watchlist: {e}")
        return []
    finally:
        close(conn, cur)

# Function to get details of a movie by its ID
def getMovieInfo(movie_id):
    conn, cur = connect()
    try:
        cur.execute("SELECT show_id, title, type, genre, from_service, description FROM movie_and_tv WHERE show_id = %s", (movie_id,))
        return cur.fetchone()
    except psycopg2.Error as e:
        print(f"Error getting movie info: {e}")
        return None
    finally:
        close(conn, cur)

# Function to check if a username exists
def usernameExists(username):
    conn, cur = connect()
    try:
        cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        return result is not None  # Return True if username exists, False otherwise
    except psycopg2.Error as e:
        print(f"Error querying username: {e}")
        return False
    finally:
        close(conn, cur)

# Function to get a user's ID by username
def getUserID(username):
    conn, cur = connect()
    try:
        cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return -1  # Return -1 if the user does not exist
    except psycopg2.Error as e:
        print(f"Error querying username: {e}")
        return -1
    finally:
        close(conn, cur)

# Function to search for movies or TV shows
def search(query):
    conn, cur = connect()
    try:
        cur.execute(
            sql.SQL(
                "SELECT show_id, title, type, genre, from_service, description FROM movie_and_tv WHERE title ILIKE %s OR genre ILIKE %s"
            ),
            (f"%{query}%", f"%{query}%"),
        )
        results = cur.fetchall()
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
        results = []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        results = []
    finally:
        close(conn, cur)

    return results

# Function to connect to the database
def connect():
    try:
        conn = psycopg2.connect(
            dbname="CS457TVandMovies",
            user="postgres",
            password="password123",
            host="localhost"
        )
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise SystemExit("Database connection failed.")

# Function to close the database connection
def close(conn, cur):
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error closing the database connection: {e}")
