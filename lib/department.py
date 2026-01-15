from __init__ import CURSOR, CONN


class Department:
    all = {} # dictionary (class attribute) for the objects in our class

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit() #save python object into the db

        self.id = CURSOR.lastrowid
        # conver the tuple(row data in the db to dict list)
        type(self).all[self.id] = self #self is class (Department) seif.id is id of our instance object all is the class attribute a dictionary for storing all the instance objects and self.id is the key used to identify a particular instace or object

    @classmethod
    def instance_from_db(cls,row):
        """Return a Department object having the attribute values from the table row."""
        department = cls.all.get(row[0])

        if department:
            department.name = row[1]
            department.location = row[2]                      
        else:
            department = cls(row[1], row[2])
            department.id = row[0]
            cls.all[department.id] = department

        return department
     
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM departments"""
        rows= CURSOR.execute(sql).fetchall() #returns tupples
        return [cls.instance_from_db(row) for row in rows] # tupple are conevrted to objects
    
    @classmethod
    def find_by_id(cls, id):
        sql = """SELECT * FROM departments WHERE id = ? """
        row = CURSOR.execute(sql, (id,)).fetchone()
        object = cls.instance_from_db(row) if row  else print("no record found")
        return object
    @classmethod
    def find_by_name(cls, name):
        sql = """SELECT * FROM departments 
                 WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        object = cls.instance_from_db(row) if row else print("no department with that name exist's")
        return object

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """


        CURSOR.execute(sql, (self.id,))
        CONN.commit()


        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]
        self.id = None
