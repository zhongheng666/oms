from django.core.management.base import BaseCommand
from django.utils import timezone
from report.models import ReportAutoConfig
from report.auto_generate import ReportGenerator
import schedule
import time
import logging
import pytz
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
config = ReportAutoConfig.objects.first()
print("配置对象:", config)
print("execute_time:", config.execute_time)
print("save_path:", config.save_path)


#class Command(BaseCommand):
#    help = '自动日报生成服务'
#
#    def handle(self, *args, **options):
#        #print("当前时间:", timezone.localtime())
#        while True:
#            config = ReportAutoConfig.objects.first()
#            if config and config.is_active:
#                # 每天指定时间执行
#                schedule.every().day.at(
#                    config.execute_time.strftime("%H:%M")
#                ).do(
#                    ReportGenerator.generate_daily_report, 
#                    config.save_path
#                )
#            
#            time.sleep(60)  # 每分钟检查一次
#            schedule.run_pending()
#


class Command(BaseCommand):
    help = '自动日报生成服务'

    def handle(self, *args, **options):
        local_tz = pytz.timezone(settings.TIME_ZONE)
        last_scheduled_time = None  # 上次注册的时间点（避免重复注册）

        logger.info("✅ 自动日报生成服务已启动")
        print("✅ 自动日报生成服务已启动")

        while True:
            try:
                config = ReportAutoConfig.objects.first()

                if config and config.is_active and config.execute_time:
                    # 构造带日期的 datetime 对象（将 TimeField 拼接到今天的日期）
                    time_obj = config.execute_time  # 例如 10:30:00
                    today = timezone.localtime(timezone.now(), local_tz).date()
                    combined_dt = datetime.combine(today, time_obj)

                    # 加入时区，得到 aware datetime
                    aware_time = timezone.make_aware(combined_dt, timezone=local_tz)

                    # 转换为 "HH:MM" 字符串格式，用于调度注册
                    execute_time_str = aware_time.strftime("%H:%M")

                    # 避免重复注册
                    if last_scheduled_time != execute_time_str:
                        schedule.clear()
                        logger.info(f"🕒 注册新的日报任务时间: {execute_time_str}")
                        print(f"🕒 注册新的日报任务时间: {execute_time_str}")

                        schedule.every().day.at(execute_time_str).do(
                            self.run_report_job,
                            config.save_path
                        )

                        last_scheduled_time = execute_time_str

                # 打印当前时间（本地）
                now_local = timezone.localtime(timezone.now(), local_tz)
                print(f"⏱ 当前本地时间: {now_local.strftime('%Y-%m-%d %H:%M:%S')}")

                # 执行调度任务
                schedule.run_pending()
                time.sleep(1)

            except Exception as e:
                logger.error(f"❌ 自动任务运行出错: {str(e)}")
                print(f"❌ 自动任务运行出错: {str(e)}")
                time.sleep(1)

    def run_report_job(self, save_path):
        """任务执行包装器，含日志输出"""
        now_str = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"📄 [{now_str}] 开始生成日报，保存路径: {save_path}")
        print(f"📄 [{now_str}] 开始生成日报，保存路径: {save_path}")
        ReportGenerator.generate_daily_report(save_path)
