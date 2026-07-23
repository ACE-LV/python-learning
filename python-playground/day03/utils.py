# day03 工具函数模块


def get_frontend_users(users):
    return [item for item in users if item["role"] == "frontend"]


def get_user_names(users):
    return [item["name"] for item in users]


def count_by_field(items, field):
    result = {}

    for item in items:
        key = item[field]
        result[key] = result.get(key, 0) + 1

    return result


def build_dashboard(users):
    return {
        "total_users": len(users),
        "role_count": count_by_field(users, "role"),
        "city_count": count_by_field(users, "city"),
        "frontend_users": get_user_names(get_frontend_users(users)),
    }
