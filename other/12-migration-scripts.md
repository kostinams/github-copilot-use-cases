## Migration Scripts

Generate and verify database migration scripts for schema changes, data transformation, and version control using GitHub Copilot.

### Scenario
Your application needs to evolve its database schema over time. You need to:
- Create forward and backward compatible migrations
- Transform existing data during schema changes
- Generate rollback scripts
- Ensure data integrity
- Handle zero-downtime migrations for production systems

GitHub Copilot can help generate migration scripts with proper validation, error handling, and rollback strategies.

### Key Benefits
🔄 **Schema Evolution** - Generate up/down migrations automatically  
🛡️ **Data Safety** - Create migrations with validation and rollback logic  
⚡ **Zero-Downtime** - Design migrations for production systems  
📝 **Documentation** - Auto-generate migration history and change logs  
🧪 **Verification** - Include data integrity checks and constraints  

---

### Example Prompts

#### SQL Migration - Add Column (Ask Mode)
```
Generate a PostgreSQL migration script to:
1. Add a new column 'status' to the users table with default value 'active'
2. Create an index on the status column
3. Add a constraint to ensure status is one of: active, inactive, suspended
4. Include a rollback script
```

#### Data Transformation Migration (Ask Mode)
```
Create a database migration for MongoDB that:
1. Transforms nested user profiles from embedded documents to references
2. Creates a new profiles collection
3. Migrates existing data
4. Updates all queries that reference user.profile
5. Includes a rollback strategy
```

#### Multi-Step Migration (Agent Mode)
```
I need to migrate from MongoDB to PostgreSQL:

Source collection (users):
{
  "_id": ObjectId(),
  "name": "John Doe",
  "email": "john@example.com",
  "tags": ["premium", "verified"],
  "metadata": { "signup_date": "2023-01-01", "country": "US" }
}

Target schema:
- users table: id, name, email
- user_tags table: user_id, tag_id
- user_metadata table: user_id, key, value

Generate:
1. SQL schema creation scripts
2. Data migration script (Python + SQLAlchemy)
3. Validation and integrity checks
4. Rollback procedures
```

#### Zero-Downtime Migration (Ask Mode)
```
Design a zero-downtime migration strategy for changing this table:

Current: orders (id PRIMARY KEY, user_id FOREIGN KEY, amount DECIMAL)
Target: orders (id PRIMARY KEY, user_id FOREIGN KEY, amount DECIMAL, currency VARCHAR)

Requirements:
- Production system with 1000s of concurrent requests
- Must not lock the table for more than 1 second
- Must maintain referential integrity
- Must support rollback
```

#### Migration Validation (Edit Mode)
Select your migration script and ask:
```
Add comprehensive validation and error handling to this migration script, including:
- Pre-flight checks
- Transaction management
- Rollback on failure
- Detailed logging
- Data integrity verification
```

#### Data Type Conversion Migration (Ask Mode)
```
Generate a migration script to convert timestamps from Unix epoch (integer seconds) to ISO 8601 format (VARCHAR) in PostgreSQL:

ALTER TABLE events ADD COLUMN timestamp_new VARCHAR;
-- Need script to: populate timestamp_new from timestamp, validate, then drop old column
```

---

### Best Practices
✅ **Always include rollback scripts**  
✅ **Test migrations on production-like environment first**  
✅ **Use transactions for atomicity**  
✅ **No locking on large tables in production**  
✅ **Include pre and post-migration validation**  
✅ **Document migration dependencies**  
✅ **Version control migration files**  

### Related Topics
- 🗄️ Flyway, Liquibase, Alembic migration frameworks
- 🔒 Transaction isolation levels
- 🔄 Blue-green deployments
- 📊 Data validation strategies
- 🚨 Rollback procedures
- 💾 Backup and recovery

### Sources
- [Liquibase Documentation](https://docs.liquibase.com/)
- [Flyway Migration Tool](https://flywaydb.org/)
- [Alembic for SQLAlchemy](https://alembic.sqlalchemy.org/)
- [PostgreSQL Migrations Best Practices](https://wiki.postgresql.org/wiki/Upgrade_Testing)
