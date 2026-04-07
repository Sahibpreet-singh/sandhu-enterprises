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

**Edit the `config.json` file** with your MySQL credentials:

1. Open `config.json` in a text editor (like Notepad)
2. Change the password to your MySQL root password
3. Save the file

Example `config.json`:
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

**If your MySQL username is different from `root`:**
- Change the `"user"` field to your MySQL username

---

## Step 4: Run the App

1. Double-click `main.exe` (if using EXE)
   OR
   Run `python main.py` (if running from source)
2. Login with your credentials
3. Start using the app!

---

## Troubleshooting

**"Can't connect to MySQL server"**
- Make sure MySQL is running (check Windows Services)
- Verify you created the `sandhu_enterprises` database
- Check your MySQL username/password is correct

**"Application won't start"**
- Make sure MySQL is running first
- Check your database has all the tables (from `all_sql.sql`)

**Need help?**
- Contact the app owner

---
