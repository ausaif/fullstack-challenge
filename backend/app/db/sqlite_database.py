import sqlite3
from contextlib import closing

from app.models.property import Property, PropertyResponse
from app.models.query import UserPropertyQuery
from app.models.user import UserSignUp, UserLogin, UserProperty
from app.utils.util import crypt


class DBConfig:
    db_name = "enodo.db"


def __execute(*args):
    with sqlite3.connect(DBConfig.db_name) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(*args)
            conn.commit()


def __execute_script(*args):
    with sqlite3.connect(DBConfig.db_name) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(*args)


def __fetch_all(*args):
    with sqlite3.connect(DBConfig.db_name) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(*args)
            return cursor.fetchall()


def setup_schema():
    __execute_script("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS user (
        firstname varchar(50) NOT NULL,
        lastname varchar(50) NOT NULL,
        username varchar(50),
        hashed_password varchar(64) NOT NULL,
        email varchar(100) NOT NULL,
        primary key(username)
    );
    CREATE TABLE IF NOT EXISTS user_property (
        username TEXT NOT NULL,
        property_id TEXT NOT NULL,
        PRIMARY KEY (username, property_id)
    );
    CREATE TABLE IF NOT EXISTS class (
        class_id INTEGER PRIMARY KEY,
        description TEXT
    );
    CREATE TABLE IF NOT EXISTS property (
        property_id TEXT,
        full_address TEXT NOT NULL,
        estimated_market_value INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        building_use TEXT,
        building_sq_ft REAL
    );
    COMMIT;
    """)


def add_user(user: UserSignUp):
    hashed_password = crypt(user.username, user.password)
    sql = "insert into user (firstname, lastname, username, hashed_password, email) values(?,?,?,?,?)"
    __execute(sql, (user.firstname, user.lastname, user.username, hashed_password, user.email))


def authorize_user(user: UserLogin):
    hashed_password = crypt(user.username, user.password)
    sql = "select username from user where username=? and hashed_password=?"
    rows = __fetch_all(sql, (user.username, hashed_password))
    if len(rows) > 0 and len(rows[0]) > 0:
        return rows[0][0] == user.username
    else:
        return None


def get_user_property(user: str, skip: int = 0, limit: int = 100):
    sql = f"""select pc.property_id, pc.full_address, pc.description,
pc.estimated_market_value, pc.building_use, pc.building_sq_ft  
from user_property u
left join (
select * from property p
left join class c on c.class_id = p.class_id
) pc on pc.property_id = u.property_id
where u.username = ? order by pc.full_address limit {limit} offset {skip}"""
    rows = __fetch_all(sql, (user,))
    data = []
    for row in rows:
        data.append(Property(property_id=row[0], full_address=row[1],
                             class_description=row[2],
                             estimated_market_value=row[3],
                             building_use=row[4],
                             building_sq_ft=row[5]))
    count = len(data)
    if len(data) == limit:
        sql = f"""select count(*) from user_property u
left join (
select * from property p
left join class c on c.class_id = p.class_id
) pc on pc.property_id = u.property_id
where u.username = ?"""
        count = __fetch_all(sql, (user,))[0][0]
    response = PropertyResponse(limit=limit, skip=skip, total_count=count, data=data)
    return response


def add_user_property(user: UserProperty):
    sql = "insert into user_property (username, property_id) values(?,?)"
    __execute(sql, (user.username, str(user.property_id)))


def remove_user_property(user: UserProperty):
    sql = "delete from user_property where username=? and property_id=?"
    __execute(sql, (user.username, str(user.property_id)))


def search_properties(property_filters: UserPropertyQuery):
    where_clause = []
    where_params = []
    if property_filters.full_address:
        where_clause.append("p.full_address like ?")
        where_params.append('%' + property_filters.full_address + '%')
    if property_filters.class_id:
        where_clause.append("c.class_id = ?")
        where_params.append(property_filters.class_id)
    if property_filters.min_estimated_market_value:
        where_clause.append("p.estimated_market_value >= ?")
        where_params.append(property_filters.min_estimated_market_value)
    if property_filters.max_estimated_market_value:
        where_clause.append("p.estimated_market_value <= ?")
        where_params.append(property_filters.max_estimated_market_value)
    if property_filters.building_use:
        where_clause.append("p.building_use = ?")
        where_params.append(property_filters.building_use)
    if property_filters.min_building_sq_ft:
        where_clause.append("p.building_sq_ft >= ?")
        where_params.append(property_filters.min_building_sq_ft)
    if property_filters.max_building_sq_ft:
        where_clause.append("p.building_sq_ft <= ?")
        where_params.append(property_filters.max_building_sq_ft)
    where_clause_str = "where " + " and ".join(where_clause) if where_clause else ""
    sql = f"""select p.property_id, p.full_address, c.description, p.estimated_market_value,
p.building_use, p.building_sq_ft from property p
left join class c on p.class_id = c.class_id
{where_clause_str}
order by p.full_address limit {property_filters.limit} offset {property_filters.skip}"""
    rows = __fetch_all(sql, where_params)
    data = []
    for row in rows:
        data.append(Property(property_id=row[0], full_address=row[1],
                             class_description=row[2],
                             estimated_market_value=row[3],
                             building_use=row[4],
                             building_sq_ft=row[5]))
    count = len(data)
    if len(data) == property_filters.limit:
        sql = f"""select count(*) from property p
left join class c on p.class_id = c.class_id
{where_clause_str}"""
        count = __fetch_all(sql, where_params)[0][0]
    response = PropertyResponse(limit=property_filters.limit, skip=property_filters.skip, total_count=count, data=data)
    return response


def get_class():
    sql = "select class_id, description from class"
    return [{'class_id': row[0], 'description': row[1]} for row in __fetch_all(sql)]
