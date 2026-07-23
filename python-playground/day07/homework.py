# 第七天作业
# 主题：给用户统计逻辑补测试和日志

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


# 作业 1：实现 count_active_users(users)
# 输入 users（list[dict]），返回 active=True 的数量。
def count_active_users(users: list[dict[str, object]]) -> int:
    return len([item for item in users if item.get("active", False) is True])


# 作业 2：实现 count_by_role(users)
# 返回每个 role 的人数统计，例如 {"frontend": 2, "backend": 1}。
def count_by_role(users: list[dict[str, object]]) -> dict[str, int]:
    role: dict[str, int] = {}
    for item in users:
        if "role" not in item:
            continue
        role_name = str(item["role"])
        role[role_name] = role.get(role_name, 0) + 1
    return role


# 作业 3：实现 build_report(users)
# 返回：
# - total
# - active_count
# - role_count


def build_report(users: list[dict[str, object]]) -> dict[str, object]:
    logging.info(f"start: {users}")
    if not users:
        logging.warning("users is empty")

    total = len(users)
    active_count = count_active_users(users)
    role_count = count_by_role(users)

    logging.info(f"total: {total}")
    logging.info(f"active_count: {active_count}")
    logging.info(f"role_count: {role_count}")

    return {
        "total": total,
        "active_count": active_count,
        "role_count": role_count,
    }


# 作业 4：在上述函数里加日志
# 要求至少有：
# - 开始处理（info）
# - 关键结果（info）
# - 空列表场景提示（warning）


# 作业 5（可选）：
# 写一个最小的自测入口 if __name__ == "__main__":
# 构造样例 users，打印 report。
if __name__ == "__main__":
    # 直接运行本文件时会进入这里。
    # 场景 A：正常计算。
    print(
        build_report(
        [
            {"id": 1, "name": "Ace", "role": "frontend", "active": True},
            {"id": 2, "name": "Lily", "role": "backend", "active": True},
        ]
        )
    )

    # 场景 B：空列表，演示 warning 日志。
    print(build_report([]))
