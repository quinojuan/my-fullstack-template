from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv
from contextlib import contextmanager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseConfig:
    """Configuración centralizada de la base de datos"""
    # ✅ SOLO CAMBIO: Valores por defecto REALES para tu VPS
    HOST = os.getenv('DB_HOST', 'localhost')
    DATABASE = os.getenv('DB_NAME', 'personas')  # ← NOMBRE REAL
    USER = os.getenv('DB_USER', 'root')   # ← USUARIO REAL  
    PASSWORD = os.getenv('DB_PASSWORD', '123456')             # ← Vacío por defecto
    POOL_SIZE = 5
    
    @classmethod
    def print_config(cls):
        """Debug: muestra la configuración"""
        logger.info(f"DB Config - Host: {cls.HOST}")
        logger.info(f"DB Config - Database: {cls.DATABASE}")
        logger.info(f"DB Config - User: {cls.USER}")
        logger.info(f"DB Config - Password: {'[SET]' if cls.PASSWORD else '[EMPTY]'}")

class Database:
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        """Inicializa el pool de conexiones"""
        try:
            logger.info(f"Intentando conectar a MySQL con:")
            logger.info(f"  Host: {DatabaseConfig.HOST}")
            logger.info(f"  Database: {DatabaseConfig.DATABASE}")
            logger.info(f"  User: {DatabaseConfig.USER}")
            logger.info(f"  Password length: {len(DatabaseConfig.PASSWORD) if DatabaseConfig.PASSWORD else 0}")

            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name="stock_pool",
                pool_size=DatabaseConfig.POOL_SIZE,
                host=DatabaseConfig.HOST,
                database=DatabaseConfig.DATABASE,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                # Agrega estas opciones para debugging
                autocommit=True,
                connection_timeout=10
            )
            logger.info("✅ Pool de conexiones MySQL inicializado")

            # Probar inmediatamente una conexión
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchall()
                cursor.close()
                logger.info("✅ Conexión de prueba exitosa")

        except Error as e:
            logger.error(f"❌ Error crítico inicializando pool: {e}")
            logger.error("Por favor verifica:")
            logger.error("1. Credenciales en .env")
            logger.error("2. Usuario tiene permisos en MySQL")
            logger.error("3. MySQL está corriendo")
            # No silencies el error, déjalo propagar
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager para manejar conexiones automáticamente"""
        connection = None
        try:
            connection = self._connection_pool.get_connection()
            yield connection
        except Error as e:
            logger.error(f"Error obteniendo conexión: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    @contextmanager
    def get_cursor(self, dictionary=True):
        """Context manager para manejar cursores automáticamente"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=dictionary)
            try:
                yield cursor
                connection.commit()
            except Exception as e:
                connection.rollback()
                logger.error(f"Error en transacción: {e}")
                raise
            finally:
                cursor.close()