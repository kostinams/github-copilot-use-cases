## Database Query Optimization

Optimize slow database queries and improve application performance using GitHub Copilot's analysis and suggestions.

### Scenario
Your application has performance issues due to inefficient database queries. You have slow SQL or NoSQL queries that need optimization. GitHub Copilot can:
- Analyze query performance patterns
- Identify missing indexes
- Suggest query rewrites
- Add execution plan analysis
- Generate optimized versions with better execution metrics

### Key Benefits
🚀 **Performance Gains** - Reduce query execution time by 10-100x  
🔍 **Index Optimization** - Identify and suggest missing indexes  
📊 **Query Analysis** - Understand execution plans and bottlenecks  
🔄 **Refactoring** - Rewrite inefficient queries for better performance  
💡 **Best Practices** - Learn optimization patterns for your database system  

---

### Example Prompts

#### SQL Query Optimization (Ask Mode)
```
Analyze this SQL query for performance issues and suggest optimizations:

SELECT u.id, u.name, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01'
AND u.status = 'active'
GROUP BY u.id, u.name, u.email
```

#### NoSQL Query Optimization (Ask Mode)
```
I have a slow MongoDB query. How can I optimize it?

db.products.find({
  category: "electronics",
  $or: [
    { rating: { $gte: 4 } },
    { reviews_count: { $gt: 100 } }
  ]
}).sort({"price": -1})
```

#### Add Indexes and Explain Plan (Ask Mode)
```
Generate the necessary indexes and EXPLAIN plan analysis for this PostgreSQL query:

SELECT p.id, p.name, SUM(ol.quantity) as total_sold
FROM products p
JOIN order_lines ol ON p.id = ol.product_id
WHERE ol.created_at BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY p.id, p.name
HAVING SUM(ol.quantity) > 50
ORDER BY total_sold DESC;
```

#### Query Refactoring (Edit Mode)
Select the slow query and ask:
```
Refactor this query to improve performance without changing the result set
```

#### Agent Mode - Comprehensive Optimization
```
I have a database performance issue. Here's my slow query:

[Insert query]

1. Analyze the query execution plan
2. Identify performance bottlenecks
3. Suggest 3 different optimization approaches
4. Create the necessary indexes
5. Provide the optimized query
6. Estimate the expected performance improvement
```

---

### Related Topics
- 🗄️ Index strategies (B-tree, Hash, Full-text)
- 📈 Query execution plans
- 🔄 Denormalization patterns
- 💾 Caching strategies (Redis, Memcached)
- 🛠️ Database profiling tools
- 🧮 Query cost analysis

### Sources
- [PostgreSQL Query Optimization](https://www.postgresql.org/docs/current/using-explain.html)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MongoDB Performance Best Practices](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)
