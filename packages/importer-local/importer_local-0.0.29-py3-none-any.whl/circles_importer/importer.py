from circles_local_database_python.connector import Connector
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
load_dotenv()

IMPORTER_LOCAL_PYTHON_COMPONENT_ID = 114
IMPORTER_LOCAL_COMPONENT_NAME = 'importer-local-python-package'

logger_code_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': IMPORTER_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'developer_email': 'idan.a@circlez.ai'
}
logger = Logger.create_logger(object=logger_code_init)

class Importer:
    def __init__(self):
        pass

    def insert_record_data_source(self, data_source_id: int, location_id: int, entity_type_id: int, entity_id: int, url: str, user_id: int):
        object1 = {
            'source_id': data_source_id,
            'entity_type_name': entity_type_id,
            'entity_id': entity_id,
            'url': url,
            'location_id': location_id,
            'user_id': user_id
        }
        logger.start(object=object1)
        try:
            database_conn = Connector.connect("importer")
            cursor = database_conn.cursor()

            cursor.execute(
                "SELECT country_id FROM location.location_table WHERE id = '{}'".format(location_id))
            country_id = cursor.fetchone()[0]
            query_importer = "INSERT INTO importer.importer_table(`source_id`,`country_id`,`entity_type_id`,`entity_id`,`url`,`created_user_id`,`updated_user_id`)" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor = database_conn.cursor()
            cursor.execute(
                query_importer, (data_source_id, country_id, entity_type_id, entity_id, url, user_id, user_id))
            cursor.close()
            database_conn.commit()
            logger.info("add importer record succeeded")#view logger_local.end at the end of the function
        except Exception as e:
            logger.exception(object=e)
        logger.end(object={})


if __name__ == "__main__":
    pass
