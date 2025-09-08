import pymysql
from common.yaml_handler import config_data
from common.logger import logger


class DatabaseHandler:
    """数据库连接和操作处理器"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接到MySQL数据库"""
        try:
            self.connection = pymysql.connect(
                host=config_data['database']['host'],
                port=config_data['database']['port'],
                user=config_data['database']['user'],
                password=config_data['database']['password'],
                database=config_data['database']['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            logger.info("数据库连接成功")
            return True
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接时出错: {e}")
    
    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        try:
            if not self.connection or not self.cursor:
                logger.error("数据库未连接")
                return None
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            logger.info(f"查询执行成功，返回 {len(results)} 条记录")
            return results
        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            return None
    
    def get_user_asset_logs(self, user_id, table_name="t_user_asset_log_202509", limit=None, start_ts=None):
        """获取指定用户的资产日志记录"""
        query = f"""
        SELECT * FROM {table_name} 
        WHERE userId = %s and createTime >= %s and opt =1
        ORDER BY createTime DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query, (user_id, start_ts))
    
