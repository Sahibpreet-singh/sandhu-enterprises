# Sandhu Enterprises App - Setup Guide for New User

## Prerequisites
You need to have MySQL installed on your computer. Follow these steps:

---

## Step 1: Install MySQL
1. Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
2. Run the installer and follow the setup wizard
3. **Important:** Remember the root password you set during installation
4. Choose default options (port 3306, etc.)

---

## Step 2: Create the Database

After MySQL is installed, open **Command Prompt** or **PowerShell** and run:

```bash
mysql -u root -p
```

When prompted, enter your MySQL root password.

Then run these commands:

```sql
CREATE DATABASE sandhu_enterprises;
USE sandhu_enterprises;
```

Paste all the SQL from the `all_sql.sql` file provided to you.

---

## Step 3: Configure Database Access

**CRITICAL: Edit `config.json` with YOUR MySQL password!**

### The error "Access denied for user 'root'@'localhost' (using password: YES)" means the password in config.json doesn't match your MySQL password.

### First, find your MySQL root password:

**Method 1 - Check if you remember setting a password:**
- During MySQL installation, you were asked to set a root password
- If you don't remember, try common passwords: `1234`, `password`, `root`, or `mysql`

**Method 2 - Test your current password:**
1. Open Command Prompt
2. Run: `mysql -u root -p`
3. Enter your password when prompted
4. If it works, that's your password!
5. If it fails, try Method 3

**Method 3 - Reset MySQL root password (if needed):**
1. Stop MySQL: `net stop mysql`
2. Start MySQL in safe mode: `mysqld --skip-grant-tables`
3. In another Command Prompt: `mysql -u root`
4. Set new password:
   ```sql
   USE mysql;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   EXIT;
   ```
5. Stop MySQL: `net stop mysql`
6. Start MySQL normally: `net start mysql`

### Then edit `config.json`:

1. Open `config.json` in Notepad
2. Change `"password": "1234"` to `"password": "YOUR_ACTUAL_PASSWORD"`
3. Save the file

Example:
```json
{
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "1234",
        "database": "sandhu_enterprises"
    }
}
```

---

## Step 4: Run the App

1. Double-click `main.exe` (if using EXE)
   OR
   Run `python main.py` (if running from source)
2. Login with your credentials
3. Start using the app!

---

## Troubleshooting

**"Access denied for user 'root'@'localhost' (using password: YES)"**
- This means the password in `config.json` is wrong
- Follow Step 3 above to find/reset your MySQL password
- Make sure you edit `config.json` with the correct password

**"Can't connect to MySQL server"**
- Make sure MySQL service is running: `net start mysql`
- Check if MySQL is installed: `mysql --version`
- Verify port 3306 is not blocked by firewall

**"Unknown database 'sandhu_enterprises'"**
- You forgot to create the database in Step 2
- Run the SQL commands from `all_sql.sql`

**"Application won't start"**
- Make sure MySQL is running first
- Check your database has all the tables (from `all_sql.sql`)
- Verify `config.json` has the correct password

**Need help?**
- Contact the app owner

---
