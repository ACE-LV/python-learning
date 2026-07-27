# Python 第十一天：路由、Schema、Service 分层

## 今日目标

把一个大文件 API 拆成更接近真实项目的结构。

你需要掌握：

1. `schemas.py` 放请求和响应模型。
2. `models.py` 放内部数据结构。
3. `services.py` 放业务逻辑。
4. `main.py` 只负责路由入口。

## 学习顺序

1. 先阅读 `main.py`，看路由有多薄。
2. 再阅读 `services.py`，看业务逻辑在哪里。
3. 运行服务并打开 `/docs`。
4. 完成 `practice.py`。
5. 完成 `homework.py`。
6. 更新 `summary.md`。

## 启动服务

```powershell
python -m uvicorn python-playground.day11.main:app --reload
```

## 今日验收标准

- 能说清楚 schema、model、service 的分工。
- 能把一个新增接口放到正确文件里。
- 能避免把所有逻辑继续堆在 `main.py`。
