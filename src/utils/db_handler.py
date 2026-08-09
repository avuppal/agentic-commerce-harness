import psycopg2
import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "agentic_commerce"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "postgres"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", 5432)
        )
        logger.info("Database connection established successfully.")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise

def initialize_db():
    """Creates the pending_approvals table if it does not exist."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS pending_approvals (
            order_id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            cart_data JSONB NOT NULL,
            order_cost NUMERIC(10, 2) NOT NULL,
            claim_verification_score NUMERIC(5, 2) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'PENDING_HUMAN_APPROVAL',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        logger.info("Database initialized with pending_approvals table.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_pending_approval(session_id: str, cart_data: dict, order_cost: float, claim_verification_score: float) -> int:
    """
    Creates a new pending order approval in the database.
    Returns the order_id of the newly created order.
    """
    conn = None
    cur = None
    order_id = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        insert_query = """
        INSERT INTO pending_approvals (session_id, cart_data, order_cost, claim_verification_score, status, updated_at)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        RETURNING order_id;
        """
        
        cur.execute(insert_query, (session_id, json.dumps(cart_data), order_cost, claim_verification_score, 'PENDING_HUMAN_APPROVAL'))
        order_id = cur.fetchone()[0]
        conn.commit()
        logger.info(f"Pending approval created with ID: {order_id}")
    except Exception as e:
        logger.error(f"Failed to create pending approval: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return order_id

def get_pending_approval(order_id: int):
    """Retrieves a pending approval by its ID."""
    conn = None
    cur = None
    order = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        select_query = """
        SELECT order_id, session_id, cart_data, order_cost, claim_verification_score, status, created_at, updated_at
        FROM pending_approvals WHERE order_id = %s;
        """
        
        cur.execute(select_query, (order_id,))
        row = cur.fetchone()
        
        if row:
            order = {
                "order_id": row[0],
                "session_id": row[1],
                "cart_data": row[2],
                "order_cost": float(row[3]),
                "claim_verification_score": float(row[4]),
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7]
            }
    except Exception as e:
        logger.error(f"Failed to retrieve pending approval {order_id}: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return order

def get_all_pending_approvals() -> list:
    """Retrieves all pending approvals from the database."""
    conn = None
    cur = None
    orders = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        select_query = """
        SELECT order_id, session_id, cart_data, order_cost, claim_verification_score, status, created_at, updated_at
        FROM pending_approvals WHERE status = 'PENDING_HUMAN_APPROVAL';
        """
        
        cur.execute(select_query)
        rows = cur.fetchall()
        
        for row in rows:
            orders.append({
                "order_id": row[0],
                "session_id": row[1],
                "cart_data": row[2],
                "order_cost": float(row[3]),
                "claim_verification_score": float(row[4]),
                "status": row[5],
                "created_at": row[6].isoformat() if row[6] else None,
                "updated_at": row[7].isoformat() if row[7] else None
            })
    except Exception as e:
        logger.error(f"Failed to retrieve pending approvals: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return orders

def update_approval_status(order_id: int, status: str):
    """Updates the status of a pending approval."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_query = """
        UPDATE pending_approvals
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE order_id = %s;
        """
        
        cur.execute(update_query, (status, order_id))
        conn.commit()
        logger.info(f"Approval ID: {order_id} status updated to {status}")
    except Exception as e:
        logger.error(f"Failed to update approval status for ID {order_id}: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
