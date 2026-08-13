from __future__ import annotations

"""Day14 pandas 入门示例：把数据库数据整理成报表。

pandas 在项目里常用于：
1. 读取数据：从 CSV、Excel、数据库、接口 JSON 读数据。
2. 清洗数据：处理空值、重复值、字段名、日期格式、数字格式。
3. 合并数据：像 SQL join 一样把多张表组合起来。
4. 统计数据：像 Excel 透视表一样做分组统计。
5. 导出数据：生成 CSV / Excel 报表。

这个 demo 用 day14 的 SQLite 数据库演示：
- users 表：用户信息。
- courses 表：课程信息。
- enrollments 表：报名关系。

最终产出：
- 一张报名明细表。
- 一张每门课报名人数统计表。
- 两个 CSV 文件。
"""

import sqlite3

# 习惯写法：把 pandas 简写成 pd。
# 以后看到 pd.read_csv、pd.DataFrame、pd.merge，pd 都是 pandas。
import pandas as pd

# 复用同目录 main.py 里的数据库路径、建表函数、造数函数。
# 这里不是重新写一套数据库逻辑，而是专注学习 pandas 怎么处理已有数据。
import main

# 报表导出目录：python-playground/day14/output。
# pandas 本身只负责写文件；目录不存在时要先用 pathlib 创建。
OUTPUT_DIR = main.BASE_DIR / "output"


def ensure_extra_demo_data() -> None:
    """补充更多演示数据，方便观察 pandas 合并效果。"""
    with sqlite3.connect(main.DB_PATH) as connection:
        cursor = connection.cursor()

        def ensure_user(name: str, role: str) -> int:
            user = cursor.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()
            if user is not None:
                return int(user[0])

            cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", (name, role))
            return int(cursor.lastrowid)

        def ensure_course(title: str, level: str) -> int:
            course = cursor.execute(
                "SELECT id FROM courses WHERE title = ?", (title,)
            ).fetchone()
            if course is not None:
                return int(course[0])

            cursor.execute(
                "INSERT INTO courses (title, level) VALUES (?, ?)", (title, level)
            )
            return int(cursor.lastrowid)

        charlie_id = ensure_user("Charlie", "data")
        ensure_user("Diana", "frontend")
        pandas_course_id = ensure_course("Pandas Data Analysis", "beginner")
        ensure_course("Frontend Testing", "intermediate")

        # Charlie 报名 pandas 课程；Diana 故意不报名，用来演示 left join 的意义。
        cursor.execute(
            "INSERT OR IGNORE INTO enrollments (user_id, course_id) VALUES (?, ?)",
            (charlie_id, pandas_course_id),
        )
        connection.commit()


def show_join_case_examples() -> None:
    """用专门构造的数据演示不同关联情况的返回结果。"""
    # 这组数据不写入数据库，只用来讲清楚 join 的返回情况。
    # users：左边的用户主表。
    # - Alice：有正常报名。
    # - Bob：有报名记录，但课程 id 不存在。
    # - Diana：没有任何报名记录。
    # - Evan：没有任何报名记录。
    users = pd.DataFrame(
        [
            {"id": 1, "name": "Alice", "role": "frontend"},
            {"id": 2, "name": "Bob", "role": "backend"},
            {"id": 3, "name": "Diana", "role": "frontend"},
            {"id": 4, "name": "Evan", "role": "qa"},
        ]
    )

    # enrollments：报名关系表。
    # - user_id=1/course_id=101：用户存在，课程也存在，正常关联。
    # - user_id=2/course_id=999：用户存在，但课程不存在，常见于脏数据或外键缺失。
    # - user_id=99/course_id=102：用户不存在，但课程存在，也是脏数据。
    enrollments = pd.DataFrame(
        [
            {"user_id": 1, "course_id": 101, "case": "正常：用户和课程都存在"},
            {"user_id": 2, "course_id": 999, "case": "异常：课程不存在"},
            {"user_id": 99, "course_id": 102, "case": "异常：用户不存在"},
        ]
    )

    # courses：课程主表。
    # - 101：被 Alice 报名，正常匹配。
    # - 102：被一条不存在用户的报名记录引用。
    # - 103：没有任何人报名，用来观察“课程存在但没有报名”的情况。
    courses = pd.DataFrame(
        [
            {"id": 101, "title": "Python API", "level": "beginner"},
            {"id": 102, "title": "SQL for Backend", "level": "beginner"},
            {"id": 103, "title": "Frontend Testing", "level": "intermediate"},
        ]
    )

    # 情况 1：inner join。
    # 只保留左右两边都匹配到的数据。
    # 这里最终只剩 Alice + Python API，因为：
    # - Bob 的 course_id=999 在 courses 里找不到。
    # - user_id=99 在 users 里找不到。
    # - Diana/Evan 没有报名记录。
    #
    # 第一次 merge 后，临时结果大概是：
    # user_id | course_id | case                 | id | name  | role
    # 1       | 101       | 正常：用户和课程都存在 | 1  | Alice | frontend
    # 2       | 999       | 异常：课程不存在       | 2  | Bob   | backend
    #
    # 注意：user_id=99 因为 users 里没有 id=99，所以 inner join 后被丢掉。
    #
    # 第二次 merge 后，临时结果大概是：
    # user_id | course_id | case                 | id_x | name  | role     | id_y | title      | level
    # 1       | 101       | 正常：用户和课程都存在 | 1    | Alice | frontend | 101  | Python API | beginner
    #
    # 注意：Bob 的 course_id=999 因为 courses 里没有 id=999，所以第二次 inner join 后被丢掉。
    # 最后再通过 [["name", "role", "title", "level", "case"]] 只保留学习报表需要的列。
    inner_join_result = (
        enrollments.merge(users, left_on="user_id", right_on="id", how="inner")
        .merge(courses, left_on="course_id", right_on="id", how="inner")
        [["name", "role", "title", "level", "case"]]
    )

    # 情况 2：以 users 为左表做 left join。
    # 业务意义：我要一份“所有用户的报名情况”，即使用户没报名也要出现。
    # 返回特点：
    # - Alice：能匹配到报名记录。
    # - Bob：能匹配到报名记录，但后面课程可能不存在。
    # - Diana/Evan：没有报名记录，但仍然保留，course_id 为空。
    #
    # merge 后、fillna 前的数据大概是：
    # id | name  | role     | user_id | course_id | case
    # 1  | Alice | frontend | 1       | 101       | 正常：用户和课程都存在
    # 2  | Bob   | backend  | 2       | 999       | 异常：课程不存在
    # 3  | Diana | frontend | NaN     | NaN       | NaN
    # 4  | Evan  | qa       | NaN     | NaN       | NaN
    #
    # fillna 后，Diana/Evan 的空值会显示成“无报名”和“用户存在，但没有报名记录”。
    users_left_join = (
        users.merge(enrollments, left_on="id", right_on="user_id", how="left")
        [["id", "name", "role", "course_id", "case"]]
        .fillna({"course_id": "无报名", "case": "用户存在，但没有报名记录"})
    )

    # 情况 3：以 enrollments 为左表做 left join。
    # 业务意义：我要检查“所有报名关系是否都能找到用户和课程”。
    # 返回特点：
    # - 正常数据会补出 name/title。
    # - user_id=2 能找到 Bob，但 course_id=999 找不到课程，title 显示“课程不存在”。
    # - user_id=99 找不到用户，但 course_id=102 能找到 SQL for Backend。
    #
    # 第一次 merge 后，临时结果大概是：
    # user_id | course_id | case                 | id  | name  | role
    # 1       | 101       | 正常：用户和课程都存在 | 1   | Alice | frontend
    # 2       | 999       | 异常：课程不存在       | 2   | Bob   | backend
    # 99      | 102       | 异常：用户不存在       | NaN | NaN   | NaN
    #
    # 第二次 merge 后，临时结果大概是：
    # user_id | course_id | name  | title           | case
    # 1       | 101       | Alice | Python API      | 正常：用户和课程都存在
    # 2       | 999       | Bob   | NaN             | 异常：课程不存在
    # 99      | 102       | NaN   | SQL for Backend | 异常：用户不存在
    #
    # fillna 后，NaN 会分别显示成“用户不存在”或“课程不存在”。
    enrollment_left_join = (
        enrollments.merge(users, left_on="user_id", right_on="id", how="left")
        .merge(courses, left_on="course_id", right_on="id", how="left")
        [["user_id", "course_id", "name", "title", "case"]]
        .fillna({"name": "用户不存在", "title": "课程不存在"})
    )

    # 情况 4：以 courses 为左表做 left join。
    # 业务意义：我要一份“所有课程的报名情况”，即使课程没人报名也要出现。
    # 返回特点：
    # - Python API：有报名记录。
    # - SQL for Backend：有报名记录，但报名记录里的 user_id=99 用户不存在。
    # - Frontend Testing：课程存在，但没人报名。
    #
    # 第一次 merge 后，临时结果大概是：
    # id  | title            | level        | user_id | course_id | case
    # 101 | Python API       | beginner     | 1       | 101       | 正常：用户和课程都存在
    # 102 | SQL for Backend  | beginner     | 99      | 102       | 异常：用户不存在
    # 103 | Frontend Testing | intermediate | NaN     | NaN       | NaN
    #
    # 第二次 merge 后，临时结果大概是：
    # title            | level        | user_id | name
    # Python API       | beginner     | 1       | Alice
    # SQL for Backend  | beginner     | 99      | NaN
    # Frontend Testing | intermediate | NaN     | NaN
    #
    # fillna 后，课程没有匹配到用户时会显示成“无报名用户”。
    courses_left_join = (
        courses.merge(enrollments, left_on="id", right_on="course_id", how="left")
        .merge(users, left_on="user_id", right_on="id", how="left")
        [["title", "level", "user_id", "name"]]
        .fillna({"user_id": "无报名", "name": "无报名用户"})
    )

    print("\n=== 关联情况原始数据：users ===")
    print(users.to_string(index=False))

    print("\n=== 关联情况原始数据：enrollments ===")
    print(enrollments.to_string(index=False))

    print("\n=== 关联情况原始数据：courses ===")
    print(courses.to_string(index=False))

    print("\n=== 情况 1：inner join，只返回用户和课程都匹配成功的数据 ===")
    print(inner_join_result.to_string(index=False))

    print("\n=== 情况 2：users left join enrollments，保留所有用户 ===")
    print(users_left_join.to_string(index=False))

    print("\n=== 情况 3：enrollments left join users/courses，检查报名关系脏数据 ===")
    print(enrollment_left_join.to_string(index=False))

    print("\n=== 情况 4：courses left join enrollments/users，保留所有课程 ===")
    print(courses_left_join.to_string(index=False))

    OUTPUT_DIR.mkdir(exist_ok=True)
    users_left_join.to_csv(
        OUTPUT_DIR / "join_case_users_left_join.csv", index=False, encoding="utf-8-sig"
    )
    enrollment_left_join.to_csv(
        OUTPUT_DIR / "join_case_enrollment_check.csv",
        index=False,
        encoding="utf-8-sig",
    )
    courses_left_join.to_csv(
        OUTPUT_DIR / "join_case_courses_left_join.csv",
        index=False,
        encoding="utf-8-sig",
    )


def main_demo() -> None:
    # 先复用 day14 的数据库初始化和演示数据。
    # init_db()：确保 users/courses/enrollments 三张表存在。
    # seed_data()：插入 Alice、Bob 和两门课程，方便后面分析。
    main.init_db()
    main.seed_data()
    ensure_extra_demo_data()

    with sqlite3.connect(main.DB_PATH) as connection:
        # read_sql_query()：把 SQL 查询结果直接读成 DataFrame。
        # DataFrame 可以理解成“代码里的 Excel 表格”：
        # - 每一列有列名，比如 id/name/role。
        # - 每一行是一条记录，比如一个用户。
        # users 长这样：
        #   id | name  | role
        #   1  | Alice | frontend
        #   2  | Bob   | backend
        users = pd.read_sql_query(
            "SELECT id, name, role FROM users ORDER BY id", connection
        )

        # courses 也是一个 DataFrame，保存课程表数据。
        # 这里只读取报表需要的字段，不把整张表所有字段都查出来。
        courses = pd.read_sql_query(
            "SELECT id, title, level FROM courses ORDER BY id", connection
        )

        # enrollments 是中间表，只有 user_id 和 course_id。
        # 它本身不适合直接给人看，因为只有 id，没有用户名字和课程标题。
        # 后面会用 merge() 把 id 对应的详细信息补上。
        enrollments = pd.read_sql_query(
            "SELECT user_id, course_id FROM enrollments ORDER BY user_id, course_id",
            connection,
        )

    # merge()：合并两张 DataFrame，类似 SQL JOIN，也类似 Excel 的 VLOOKUP/XLOOKUP。
    # 第一步：enrollments + users。
    # - enrollments.left_on="user_id" 表示用 enrollments.user_id。
    # - users.right_on="id" 表示匹配 users.id。
    # - 结果会把报名记录里的 user_id 替换/补充成用户 name、role。
    #
    # 用当前演示数据举例：
    # enrollments 里有一行：user_id=1, course_id=1。
    # users 里有一行：id=1, name="Alice", role="frontend"。
    # left_on="user_id" + right_on="id" 的意思就是：
    # - 拿左表 enrollments.user_id 的值 1。
    # - 去右表 users.id 里找同样等于 1 的行。
    # - 找到 Alice 后，把 Alice 的 name/role 拼到这条报名记录上。
    #
    # 合并前：
    # enrollments: user_id=1, course_id=1
    # users:       id=1, name=Alice, role=frontend
    # 合并后：
    # user_id=1, course_id=1, id=1, name=Alice, role=frontend
    #
    # 第二步：上一步结果 + courses。
    # - left_on="course_id" 匹配 courses.id。
    # - 结果补充课程 title、level。
    #
    # 继续用同一行举例：
    # 上一步结果里有 course_id=1。
    # courses 里有一行：id=1, title="Python API", level="beginner"。
    # left_on="course_id" + right_on="id" 的意思就是：
    # - 拿左表里的 course_id 值 1。
    # - 去右表 courses.id 里找同样等于 1 的课程。
    # - 找到 Python API 后，把 title/level 拼到报名记录上。
    #
    # 最终这一行会变成：
    # name=Alice, role=frontend, title=Python API, level=beginner
    #
    # suffixes=("_user", "_course")：
    # - users 和 courses 都有 id 列。
    # - 合并后为了避免同名列冲突，pandas 会给重复列名加后缀。
    #
    # 最后的 [["name", "role", "title", "level"]]：
    # - 只保留最终报表需要展示的列。
    # - 这一步类似前端 table columns，只选择要展示的字段。
    report = (
        enrollments.merge(users, left_on="user_id", right_on="id", how="inner")
        .merge(
            courses,
            left_on="course_id",
            right_on="id",
            how="inner",
            suffixes=("_user", "_course"),
        )
        [["name", "role", "title", "level"]]
    )

    # 上面的 report 使用的是 inner join：只保留左右两边都匹配到的数据。
    # 这很适合做“报名明细”，因为没有报名的人本来就不在 enrollments 表里。
    #
    # left join / 左联的意义：以左表为主，左表每一行都保留。
    # 如果右表匹配不到，就用 NaN 表示缺失。
    #
    # 这里我们以 users 为左表：
    # users.merge(enrollments, left_on="id", right_on="user_id", how="left")
    # 意思是：保留所有用户，即使这个用户没有报名记录。
    #
    # 用当前演示数据看：
    # users 里有 Diana。
    # enrollments 里没有 Diana 的 user_id。
    # inner join：Diana 会消失，因为她没有报名记录。
    # left join：Diana 会保留，课程字段是 NaN，后面用 fillna() 显示成“未报名”。
    #
    # 项目里 left join 常用于：
    # - 导出完整用户列表，即使部分用户没有订单/课程/权限。
    # - 找出“没有关联数据”的记录，比如没有报名的用户、没有订单的客户。
    # - 做数据质量检查，比如用户存在但缺少配置。
    all_users_course_report = (
        users.merge(enrollments, left_on="id", right_on="user_id", how="left")
        .merge(
            courses,
            left_on="course_id",
            right_on="id",
            how="left",
            suffixes=("_user", "_course"),
        )
        [["name", "role", "title", "level"]]
        .fillna({"title": "未报名", "level": "-"})
    )

    # groupby()：按某一列分组，类似 SQL 的 GROUP BY，也类似 Excel 透视表。
    # report.groupby("title")：按课程标题分组。
    # size()：统计每组有多少行，也就是每门课有多少报名记录。
    # reset_index(name="student_count")：把统计结果变回普通 DataFrame，并把计数列命名为 student_count。
    # sort_values(..., ascending=False)：按报名人数从多到少排序。
    course_counts = (
        report.groupby("title")
        .size()
        .reset_index(name="student_count")
        .sort_values("student_count", ascending=False)
    )

    # mkdir(exist_ok=True)：如果 output 目录不存在就创建；如果已存在也不报错。
    OUTPUT_DIR.mkdir(exist_ok=True)

    # to_csv()：把 DataFrame 导出成 CSV 文件。
    # index=False：不导出 pandas 自动生成的行号，否则 CSV 第一列会多一列 0/1/2。
    # encoding="utf-8-sig"：方便 Windows Excel 打开中文不乱码。
    report.to_csv(OUTPUT_DIR / "enrollment_report.csv", index=False, encoding="utf-8-sig")
    all_users_course_report.to_csv(
        OUTPUT_DIR / "all_users_course_report.csv", index=False, encoding="utf-8-sig"
    )
    course_counts.to_csv(
        OUTPUT_DIR / "course_student_counts.csv", index=False, encoding="utf-8-sig"
    )

    print("\n报名明细：")

    # to_string(index=False)：把 DataFrame 格式化成适合终端阅读的表格。
    # 默认会显示行号；index=False 表示隐藏行号。
    print(report.to_string(index=False))

    print("\n每门课报名人数：")
    print(course_counts.to_string(index=False))

    print("\n所有用户课程情况（left join，包含未报名用户）：")
    print(all_users_course_report.to_string(index=False))

    print(f"\n已导出：{OUTPUT_DIR / 'enrollment_report.csv'}")
    print(f"已导出：{OUTPUT_DIR / 'all_users_course_report.csv'}")
    print(f"已导出：{OUTPUT_DIR / 'course_student_counts.csv'}")

    show_join_case_examples()


if __name__ == "__main__":
    main_demo()
