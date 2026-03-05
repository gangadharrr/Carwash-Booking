# Database Schema Analysis

## Summary
This analysis examines the database schema of the Car Wash Booking System. The application uses a MySQL database with five main tables to manage users, body shops, services, bookings, and booking status. The schema reveals a simple data model with several design limitations and missing relationships.

## Database Tables Overview

### 1. `users` Table (High Confidence)
Stores user authentication information.

```sql
CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
)
```

**Key Observations:**
- Simple authentication model with username as primary key
- Password stored directly without proper hashing in PHP version (security concern)
- MD5 hashing used in Python version (still insufficient by modern standards)
- No additional user information (email, name, contact details, etc.)

### 2. `bodyshops` Table (High Confidence)
Stores information about car wash locations.

```sql
CREATE TABLE `bodyshops` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL
)
```

**Key Observations:**
- No primary key defined (data integrity concern)
- No constraints to prevent duplicate entries
- Hierarchical location data (city → location → shop name)
- No additional information about body shops (contact details, operating hours, etc.)

### 3. `bookings` Table (High Confidence)
Stores pending booking requests.

```sql
CREATE TABLE `bookings` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL,
  `Phoneno` varchar(15) NOT NULL,
  `model` varchar(50) NOT NULL,
  `servicetype` varchar(50) NOT NULL,
  `userid` varchar(255) NOT NULL
)
```

**Key Observations:**
- No primary key defined (data integrity concern)
- No foreign key constraints to ensure data consistency
- Duplicates location information from bodyshops table (normalization issue)
- Contains both customer information (phone, model) and service details

### 4. `accrejdb` Table (High Confidence)
Stores accepted or rejected bookings.

```sql
CREATE TABLE `accrejdb` (
  `cities` varchar(50) NOT NULL,
  `locations` varchar(50) NOT NULL,
  `bodyshopname` varchar(50) NOT NULL,
  `Phoneno` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `servicetype` varchar(50) NOT NULL,
  `userid` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
)
```

**Key Observations:**
- Nearly identical structure to bookings table with added status field
- No primary key defined (data integrity concern)
- No foreign key constraints to ensure data consistency
- Duplicates location information from bodyshops table (normalization issue)
- Status field limited to 'Accept' or 'Reject' values (based on code)

### 5. `services` Table (High Confidence)
Stores service types and their prices.

```sql
CREATE TABLE `services` (
  `servicetype` varchar(50) NOT NULL,
  `price` int(4) UNSIGNED NOT NULL,
  UNIQUE KEY `servicetype` (`servicetype`)
)
```

**Key Observations:**
- Service type used as unique key
- Price limited to 4 digits (design limitation)
- No additional service information (duration, description, etc.)
- Only table with a defined key constraint

## Entity Relationships

### Implicit Relationships (Medium Confidence)
The database lacks explicit foreign key constraints, but the following relationships are implied:

1. **users → bookings/accrejdb**:
   - `users.username` → `bookings.userid`
   - `users.username` → `accrejdb.userid`

2. **bodyshops → bookings/accrejdb**:
   - `bodyshops.(cities, locations, bodyshopname)` → `bookings.(cities, locations, bodyshopname)`
   - `bodyshops.(cities, locations, bodyshopname)` → `accrejdb.(cities, locations, bodyshopname)`

3. **services → bookings/accrejdb**:
   - `services.servicetype` → `bookings.servicetype`
   - `services.servicetype` → `accrejdb.servicetype`

4. **bookings → accrejdb**:
   - Records move from bookings to accrejdb when processed by admin

## Database Schema Limitations

### 1. Normalization Issues (High Confidence)
- **Duplicate Data**: Location information repeated across tables
- **Missing Junction Tables**: Many-to-many relationships not properly modeled
- **Denormalized Design**: Related data not properly separated

### 2. Integrity Constraints (High Confidence)
- **Missing Primary Keys**: Most tables lack primary key definitions
- **No Foreign Keys**: No referential integrity constraints
- **No Check Constraints**: No validation of data values

### 3. Data Type Issues (Medium Confidence)
- **Oversized Fields**: Many varchar fields are larger than necessary
- **Inconsistent Sizing**: Phone number field is varchar(15) in bookings but varchar(50) in accrejdb
- **No Date/Time Fields**: No timestamps for bookings or audit trails

### 4. Security Concerns (High Confidence)
- **Plain Text Passwords**: Passwords stored without proper hashing (PHP version)
- **Weak Hashing**: MD5 used for password hashing (Python version)
- **No Audit Trails**: No tracking of data changes

## Data Flow in Application

### Booking Process (High Confidence)
1. User selects city, location, body shop, and service type
2. System checks if the selected body shop has fewer than 5 bookings
3. If available, booking is added to the bookings table
4. Admin reviews bookings and accepts or rejects them
5. Accepted/rejected bookings move to the accrejdb table with appropriate status
6. Booking is removed from the bookings table

```php
// From userhome.php - Booking creation
$s="select * from bookings where cities='$city' && locations='$loc'&& bodyshopname='$bshop'"; 
$result=mysqli_query($con,$s);
$num=mysqli_num_rows($result);
if($num<=5){
    $reg="insert into bookings values ('$city','$loc','$bshop','$phone','$model')";
    mysqli_query($con,$reg);
    echo " Booking Successful";
}
```

```python
# From main.py - Booking acceptance
sql = "INSERT INTO accrejdb VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
db.execute(sql, sn)
sql = "DELETE FROM bookings WHERE cities=%s AND locations=%s AND bodyshopname=%s AND Phoneno=%s AND model=%s AND servicetype=%s AND userid=%s"
sn.pop()
db.execute(sql, sn)
```

### User Registration Process (High Confidence)
1. User provides username and password
2. System checks if username already exists
3. If username is available and password meets complexity requirements, user is added to the users table

```php
// From registration.php
$s="select * from users where username='$name'"; 
$result=mysqli_query($con,$s);
$num=mysqli_num_rows($result);

if($num==1){
    echo "Username Already Taken";
} 

if(preg_match("@[A-Z]@",$pass)&&preg_match("@[a-z]@",$pass)&&preg_match("@[0-9]@",$pass)&&preg_match("@[^\w]@",$pass)&&strlen($pass)>7){
    $reg="insert into users values ('$name','$pass')";
    mysqli_query($con,$reg);
    echo " Registration Successful";
}
```

## Schema Improvement Recommendations

### 1. Normalization (High Priority)
- Create separate tables for cities and locations
- Establish proper foreign key relationships
- Remove redundant data across tables

```sql
-- Example improved schema
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    location_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE KEY city_location (city_id, location_name)
);

CREATE TABLE bodyshops (
    shop_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    shop_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    UNIQUE KEY location_shop (location_id, shop_name)
);
```

### 2. Add Integrity Constraints (High Priority)
- Define primary keys for all tables
- Implement foreign key constraints
- Add check constraints for data validation

### 3. Enhance Data Model (Medium Priority)
- Add timestamps for created/updated records
- Include additional user information (email, name, etc.)
- Add more details for body shops (contact, hours, etc.)
- Create a proper booking status workflow

### 4. Security Improvements (High Priority)
- Use proper password hashing (bcrypt or Argon2)
- Implement role-based access control
- Add audit logging for sensitive operations

## Conclusion

The Car Wash Booking System database schema reveals a simple, prototype-level data model with significant room for improvement. The lack of proper integrity constraints, normalization issues, and security concerns suggest this was developed as a learning project or proof of concept rather than a production-ready system.

The schema would benefit from restructuring to follow database design best practices, including proper normalization, integrity constraints, and security considerations. Despite its limitations, the current schema does provide the basic functionality needed for the application to operate, demonstrating a functional if not optimal approach to data modeling.