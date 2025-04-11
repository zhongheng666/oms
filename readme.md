### 数据库迁移
```
python manage.py makemigrations 

python manage.py migrate
```

#### 创建管理员

```python manage.py createsuperuser```


### 手动生成报告（将保存到/tmp目录）
python manage.py shell
from report.auto_generate import ReportGenerator
ReportGenerator.generate_daily_report("/tmp/")


### 监控生成报表 

python3 manage.py auto_report
