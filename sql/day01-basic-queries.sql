-- SQLTools 第一天练习
-- 连接：Python Learning SQLite

-- 1. 查询所有用户
SELECT * FROM users;

-- 2. 只查询前端开发
SELECT * FROM users WHERE role = 'Frontend Developer';

-- 3. 按工作年限倒序
SELECT * FROM users ORDER BY years DESC;

-- 4. 查询所有课程
SELECT * FROM courses;

-- 5. 查询入门难度课程
SELECT * FROM courses WHERE difficulty = 'Beginner';

-- 6. 统计课程数量
SELECT COUNT(*) AS course_count FROM courses;

-- 7. 按分类统计课程数量
SELECT category, COUNT(*) AS total FROM courses GROUP BY category;
