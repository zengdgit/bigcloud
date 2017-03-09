from ..models import TemplateMeta, PeriodTemplate, FlavorTemplate
from ..common import timeutils
from .. import db

def sync_timetable(param):
    template_list = db.session.query(TemplateMeta.name, TemplateMeta.modified_time, TemplateMeta.id).filter(
        TemplateMeta.type=='timetable').all()
    template_name_dict = {}
    template_id_dict = {}
    for temp_item in template_list:
        template_name_dict[temp_item[0]] = temp_item[1]
        template_id_dict[temp_item[0]] = temp_item[2]

    data = {'out_of_date':[], 'new':[], 'deleted':[], 'type':'timetable'}
    for old_item in param:
        new_time = template_name_dict.get(old_item[0])
        if new_time:
            if new_time > timeutils.str_to_date(old_item[1]):
                period_list = db.session.query(PeriodTemplate.start_time, PeriodTemplate.end_time).filter(
                    PeriodTemplate.meta_id==template_id_dict[old_item[0]]).all()
                period_list = timeutils.timetable_to_str(period_list)
                data['out_of_date'].append([old_item[0], period_list])
            template_id_dict.pop(old_item[0])
            template_name_dict.pop(old_item[0])
        else:
            data['deleted'].append(old_item[0])

    for item_key in template_name_dict.keys():
        period_list = db.session.query(PeriodTemplate.start_time, PeriodTemplate.end_time).filter(
            PeriodTemplate.meta_id==template_id_dict[item_key]).all()
        period_list = timeutils.timetable_to_str(period_list)
        data['new'].append([item_key, period_list])

    if not data['out_of_date'] and not data['new']:
        data = 'up_of_date'

    return data


def sync_flavor(param):
    template_list = db.session.query(TemplateMeta.name, TemplateMeta.modified_time, TemplateMeta.id).filter(
        TemplateMeta.type == 'flavor').all()
    template_name_dict = {}
    template_id_dict = {}
    for temp_item in template_list:
        template_name_dict[temp_item[0]] = temp_item[1]
        template_id_dict[temp_item[0]] = temp_item[2]

    data = {'out_of_date': [], 'new': [], 'deleted': [], 'type': 'flavor'}
    for old_item in param:
        new_time = template_name_dict.get(old_item[0])
        if new_time:
            if new_time > timeutils.str_to_date(old_item[1]):
                new_flavor = db.session.query(FlavorTemplate.cpunum, FlavorTemplate.ramnum, FlavorTemplate.disknum).filter(
                    FlavorTemplate.meta_id==template_id_dict[old_item[0]]).first()
                data['out_of_date'].append([old_item[0], new_flavor])
            template_id_dict.pop(old_item[0])
            template_name_dict.pop(old_item[0])
        else:
            data['deleted'].append(old_item[0])

    for item_key in template_name_dict.keys():
        new_flavor = db.session.query(FlavorTemplate.cpunum, FlavorTemplate.ramnum, FlavorTemplate.disknum).filter(
            FlavorTemplate.meta_id == template_id_dict[item_key]).first()
        data['new'].append([item_key, new_flavor])

    if not data['out_of_date'] and not data['new']:
        data = 'up_of_date'

    return data