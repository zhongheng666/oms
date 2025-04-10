# report/auto_generate.py
import os
import logging
import sys
from datetime import date, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from tickets.models import TicketList
from organization.models import Department, ServiceType, IncidentType
from collections import defaultdict

logger = logging.getLogger(__name__)

class ReportGenerator:
    @staticmethod
    def generate_daily_report(save_path):
        """独立日报生成核心逻辑（修复版）"""
        try:
            # 1. 计算目标日期（昨日）
            target_date = timezone.localdate() - timedelta(days=1)
            logger.info(f"⏳ 开始生成 {target_date} 日报")

            # 2. 获取基础数据
            departments = Department.objects.prefetch_related('location_set__floor').order_by('id')
            service_types = ServiceType.objects.all()
            incident_types = IncidentType.objects.all()

            # 3. 获取相关工单
            tickets = TicketList.objects.filter(date=target_date).select_related(
                'department', 'floor', 'service_type', 'incident_type'
            )

            # 4. 构建工单索引
            ticket_index = defaultdict(list)
            for ticket in tickets:
                key = (ticket.department_id, ticket.floor_id)
                ticket_index[key].append(ticket)

            # 5. 初始化报表数据结构
            report_data = {
                'total': {
                    'services': {st.name: 0 for st in service_types},
                    'incidents': {it.name: 0 for it in incident_types}
                },
                'departments': {},
                'now': timezone.now()  # 用于模板显示生成时间
            }

            # 6. 部门统计（完整数据）
            for dept in departments:
                dept_data = {
                    'total': {
                        'services': {st.name: 0 for st in service_types},
                        'incidents': {it.name: 0 for it in incident_types}
                    },
                    'floors': {},
                    'location_details': []  # 新增详细数据
                }

                locations = dept.location_set.select_related('floor')
                for loc in locations:
                    floor = loc.floor
                    floor_tickets = ticket_index.get((dept.id, floor.id), [])

                    # 楼层基础统计
                    floor_data = {
                        'services': {st.name: 0 for st in service_types},
                        'incidents': {it.name: 0 for it in incident_types},
                        'tickets': []  # 工单明细
                    }

                    # 工单详细信息
                    for ticket in floor_tickets:
                        # 记录明细
                        floor_data['tickets'].append({
                            'id': ticket.id,
                            'service_type': ticket.service_type.name,
                            'incident_type': ticket.incident_type.name if ticket.incident_type else "无",
                            'created_at': ticket.created_at.strftime("%H:%M")
                        })
                        
                        # 统计服务类型
                        service_name = ticket.service_type.name
                        floor_data['services'][service_name] += 1
                        dept_data['total']['services'][service_name] += 1
                        report_data['total']['services'][service_name] += 1

                        # 统计故障类型
                        if ticket.incident_type:
                            incident_name = ticket.incident_type.name
                            floor_data['incidents'][incident_name] += 1
                            dept_data['total']['incidents'][incident_name] += 1
                            report_data['total']['incidents'][incident_name] += 1

                    dept_data['floors'][floor.name] = floor_data
                    dept_data['location_details'].append({
                        'floor_name': floor.name,
                        'ticket_count': len(floor_tickets),
                        'last_ticket_time': max([t.created_at for t in floor_tickets], default=None)
                    })

                report_data['departments'][dept.name] = dept_data

            # 7. 生成HTML
            html_content = render_to_string(
                'report/daily_report.html',
                {
                    'query_date': target_date,
                    'report_data': report_data,
                    'service_types': service_types,
                    'incident_types': incident_types,
                }
            )

            # 8. 保存文件（增强错误处理）
            filename = f"report-{target_date.strftime('%Y%m%d')}.html"
            full_path = os.path.join(save_path, filename)
            
            try:
                os.makedirs(save_path, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"✅ 成功生成日报：{full_path}")
                return True
            except OSError as e:  # 统一捕获系统级错误
                logger.error(f"❌ 文件操作失败：{str(e)}")
                return False

        except ObjectDoesNotExist as e:
            logger.error(f"❌ 数据查询失败：{str(e)}")
        except Exception as e:
            logger.error(f"❌ 生成日报异常：{str(e)}", exc_info=sys.exc_info())
        
        return False

