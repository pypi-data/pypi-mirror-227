from circles_local_database_python import connector
from circles_local_database_python.generic_crud.src import generic_crud
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from language_local_python_package.src.language_enum_class import LanguageCode
import mysql.connector
import datetime

PERSON_LOCAL_PYTHON_COMPONENT_ID = 169
PERSON_LOCAL_PYTHON_COMPONENT_NAME = 'person-local'

object_init = {
    'component_id': PERSON_LOCAL_PYTHON_COMPONENT_ID,
    'component_name':PERSON_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email":"jenya.b@circ.zone"
}
logger = Logger.create_logger(object=object_init)

class Person(generic_crud.GenericCRUD):
    db_conn = connector.Connector.connect("person")

    def __init__(self) -> None:
        pass

    def conn_db(query: str) -> None:
        logger.start("Sending query to db",object={"query":query})
        db_cursor = connector.Connector.cursor(Person.db_conn)
        db_cursor.execute(query)
        Person.db_conn.commit()
        logger.end()

    def delete(person_id: int) -> None:
        logger.start("Delete person by ID",object={"person_id":person_id})
        query = ("UPDATE person_table SET end_timestamp = CURRENT_TIMESTAMP WHERE person_id = {}".format(person_id))
        Person.conn_db(query)
        logger.end()

    def insert_person(number: int, gender_id: int, last_coordinate: str, location_id: int) -> int:
        logger.start("Insert person",object={"number": number, "gender_id": gender_id, "last_coordinate": last_coordinate , "location_id": location_id})
        try:
            query = ("INSERT INTO person_table (number, gender_id, last_coordinate, location_id,start_timestamp) VALUES ({}, {}, {}, {}, CURRENT_TIMESTAMP)".
                    format(number, gender_id, last_coordinate, location_id))
            Person.conn_db(query)
            logger.info("Person inserted successfully.")
            query = ("SELECT LAST_INSERT_ID()")
            db_cursor = connector.Connector.cursor(Person.db_conn)
            db_cursor.execute(query)
            person_id = db_cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logger.exception(err)
            raise
        logger.end("Person added", object={'person_id': person_id})
        return person_id    

    def insert_person_ml( person_id: int, lang_code: LanguageCode,first_name: str,last_name: str) -> int:
        logger.start("Insert person",object={"person_id":person_id,"lang_code": lang_code,"first_name": first_name,"last_name": last_name})
        query = ("INSERT INTO person_ml_table (person_id,lang_code,first_name,last_name) VALUES ({},{},{},{})".format(person_id,lang_code,first_name,last_name))
        Person.conn_db(query)
        logger.end("Person added", object={'person_id': person_id})
        return person_id

    def update_person_day(id: int,day: int) -> None:
        logger.start("Update day by ID",object={"id":id,"day":day})
        query = ("UPDATE person_table SET day = {} WHERE person_id = {}".format(day,id))
        Person.conn_db(query)
        logger.end()

    def update_person_month(id: int,month: int) -> None:
        logger.start("Update month by ID",object={"id":id,"month":month})
        query = ("UPDATE person_table SET month = {} WHERE person_id = {}".format(month,id))
        Person.conn_db(query)
        logger.end()

    def update_person_year(id: int,year: int) -> None:
        logger.start("Update year by ID",object={"id":id,"year":year})
        query = ("UPDATE person_table SET year = {} WHERE person_id = {}".format(year,id))
        Person.conn_db(query)
        logger.end()

    def update_person_birthday_date(id: int,birthday_date: datetime.date) -> None:
        logger.start("Update birthday date by ID",object={"id":id,"birthday_date":birthday_date})
        query = ("UPDATE person_table SET birthday_date = '{}' WHERE person_id = {}".format(birthday_date,id))
        Person.conn_db(query)
        logger.end()

    def update_person_first_name(id: int,first_name: str) -> None:
        logger.start("Update first name by ID",object={"id":id,"first_name":first_name})
        query = ("UPDATE person_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
        Person.conn_db(query)
        Person.update_person_ml_first_name(id,first_name)
        logger.end()

    def update_person_ml_first_name(id: int,first_name: str) -> None:
        logger.start("Update first name in ml table by ID",object={"id":id,"first_name":first_name})
        query = ("UPDATE person_ml_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
        Person.conn_db(query)
        logger.end() 

    def update_person_nickname(id: int,nickname: str) -> None:
        logger.start("Update nickname by ID",object={"id":id,"nickname":nickname})
        query = ("UPDATE person_table SET nickname = '{}' WHERE person_id = {}".format(nickname,id))
        Person.conn_db(query)
        logger.end()

    def update_person_last_name(id: int,last_name: str) -> None:
        logger.start("Update last name by ID",object={"id":id,"last_name":last_name})
        query = ("UPDATE person_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
        Person.conn_db(query)
        Person.update_person_ml_last_name(id,last_name)
        logger.end()

    def update_person_ml_last_name(id: int,last_name: str) -> None:
        logger.start("Update last name in ml table by ID",object={"id":id,"last_name":last_name})
        query = ("UPDATE person_ml_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
        Person.conn_db(query)
        logger.end()

    