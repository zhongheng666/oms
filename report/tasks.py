import os
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from .models import ReportConfig

def generate_daily_report():
    config = ReportConfig.objects.first()
    if not config or not config.IS_ACTIVE:
        return

    # 计算前一天日期
    target_date = timezone.localdate() - timezone.timedelta(days=1)
    
    # 复用已有生成逻辑
    from .admin import generate_report
    html_content = generate_report(target_date)  # 需要稍作改造
    
    # 保存文件
    filename = f"report-{target_date.strftime('%Y%m%d')}.html"
    full_path = os.path.join(config.SAVE_PATH, filename)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

class Command(BaseCommand):
    help = 'Start report scheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        config = ReportConfig.objects.first()

        if config and config.IS_ACTIVE:
            scheduler.add_job(
                generate_daily_report,
                'cron',
                hour=config.DAILY_TIME.hour,
                minute=config.DAILY_TIME.minute
            )
            scheduler.start()

