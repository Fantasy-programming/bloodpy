import mysql.connector
from mysql.connector import Error
import config


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def fetch_all_blood_records(self):
        """
        Fetches all records from the BloodBank table.
        Returns:
            List of dictionaries with keys: blood_group, units_available.
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM BloodBank")
        records = cursor.fetchall()
        cursor.close()
        return records

    def update_blood_units(self, blood_group, new_units):
        """
        Updates the units_available for a given blood group.
        """
        cursor = self.connection.cursor()
        sql = "UPDATE BloodBank SET units_available = %s WHERE blood_group = %s"
        cursor.execute(sql, (new_units, blood_group))
        self.connection.commit()
        cursor.close()

    def get_units_for_blood_group(self, blood_group):
        """
        Retrieves the current units available for a given blood group.
        """
        cursor = self.connection.cursor()
        sql = "SELECT units_available FROM BloodBank WHERE blood_group = %s"
        cursor.execute(sql, (blood_group,))
        record = cursor.fetchone()
        cursor.close()
        if record:
            return record[0]
        else:
            return None

    def add_donation(self, blood_group, units):
        """
        Increases the blood units for the given blood group.
        If the blood group does not exist, it inserts a new record.
        """
        current_units = self.get_units_for_blood_group(blood_group)
        if current_units is not None:
            new_units = current_units + units
            self.update_blood_units(blood_group, new_units)
        else:
            cursor = self.connection.cursor()
            sql = "INSERT INTO BloodBank (blood_group, units_available) VALUES (%s, %s)"
            cursor.execute(sql, (blood_group, units))
            self.connection.commit()
            cursor.close()

    def process_request(self, blood_group, units):
        """
        Checks if the requested blood units are available. If yes,
        it deducts the units and returns a success message. Otherwise,
        it returns a failure message.
        """
        current_units = self.get_units_for_blood_group(blood_group)
        if current_units is None:
            return False, "Blood group not found."
        if current_units < units:
            return False, "Insufficient units available."
        new_units = current_units - units
        self.update_blood_units(blood_group, new_units)
        return True, "Request completed successfully."

    def authenticate_admin(self, username, password):
        """Authenticate admin credentials against the Admins table."""
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM Admins WHERE username = %s AND password_hash = %s"
        cursor.execute(sql, (username, password))
        admin = cursor.fetchone()
        cursor.close()
        return admin is not None

    def register_donor(self, name, blood_group, contact, donation_date):
        """Register a new donor and record the donation date."""
        cursor = self.connection.cursor()
        sql = "INSERT INTO Donors (name, blood_group, contact, donation_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, blood_group, contact, donation_date))
        self.connection.commit()
        cursor.close()

    def fetch_transaction_history(self):
        """Fetch all blood transactions (donations and requests) sorted by date."""
        cursor = self.connection.cursor(dictionary=True)
        sql = """
            SELECT name, blood_group, units, transaction_date, transaction_type 
            FROM BloodTransactions 
            ORDER BY transaction_date DESC, id DESC
        """
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        return records

    def add_transaction(self, name, blood_group, units, transaction_type):
        """Record a blood transaction (donation or request)."""
        cursor = self.connection.cursor()
        sql = """
            INSERT INTO BloodTransactions 
            (name, blood_group, units, transaction_date, transaction_type) 
            VALUES (%s, %s, %s, CURDATE(), %s)
        """
        cursor.execute(sql, (name, blood_group, units, transaction_type))
        self.connection.commit()
        cursor.close()

    def fetch_donors(self):
        """Fetch all registered donors."""
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT name, blood_group FROM Donors ORDER BY name"
        cursor.execute(sql)
        donors = cursor.fetchall()
        cursor.close()
        return donors

    def get_donor_details(self, donor_name):
        """Fetch details for a specific donor."""
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM Donors WHERE name = %s"
        cursor.execute(sql, (donor_name,))
        donor = cursor.fetchone()
        cursor.close()
        return donor

    def fetch_full_donor_list(self):
        """Fetch all donors with complete information."""
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT id, name, blood_group, contact, donation_date FROM Donors ORDER BY name"
        cursor.execute(sql)
        donors = cursor.fetchall()
        cursor.close()
        return donors

    def delete_donor(self, donor_id):
        """
        Delete a donor by ID.
        This only removes the donor from the Donors table but keeps their donation 
        history in the BloodTransactions table intact.
        """
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM Donors WHERE id = %s"
            cursor.execute(sql, (donor_id,))
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except Error as e:
            print(f"Error deleting donor: {e}")
            return False

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
