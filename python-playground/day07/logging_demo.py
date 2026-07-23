import logging

# 第 1 步：配置日志系统（只需要配置一次）。
# level=logging.INFO 表示：INFO / WARNING / ERROR 会显示，DEBUG 不显示。
# format 定义每条日志长什么样：时间 | 级别 | 文本。
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def divide(a: float, b: float) -> float:
    # 第 2 步：函数开始时记录入参，便于排查“谁传了什么值”。
    logging.info("Start divide: a=%s, b=%s", a, b)

    # 第 3 步：处理非法输入。
    if b == 0:
        # error 表示发生了错误事件。
        logging.error("Divide by zero")
        # raise 会中断函数，把错误抛给调用方处理。
        raise ValueError("b cannot be 0")

    # 第 4 步：正常计算并记录结果。
    result = a / b
    logging.info("Divide result: %s", result)
    return result


if __name__ == "__main__":
    # 直接运行本文件时会进入这里。
    # 场景 A：正常计算。
    print(divide(10, 2))

    # 场景 B：故意触发错误，演示 try/except + warning 日志。
    try:
        divide(10, 0)
    except ValueError as error:
        # warning 表示“有异常但可预期、已被处理”。
        logging.warning("Caught expected error: %s", error)
