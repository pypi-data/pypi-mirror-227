# _*_ coding: UTF-8 _*_
"""
@file            : time_util
@Author          : qtclm
@Date            : 2023/1/29 19:44
@Desc            : 时间处理类
"""
import calendar
import traceback
import pytz
from dateutil import parser
import re
import sys
import time
import datetime
import dateutil
from turtle_utils.other_util import otherUtil


class timeUtil(otherUtil):

    def dispose_datetime_format_datetime_string(self, is_date=False, is_mongo_format=False):
        date_format_string = "%Y-%m-%d"
        time_format_string = "%H:%M:%S"
        if is_mongo_format:
            format_string = f'{date_format_string}T{time_format_string}.000Z'
        else:
            if is_date:
                return date_format_string
            format_string = f"{date_format_string} {time_format_string}"
        return format_string

    # 把datetime转成字符串
    def datetime_to_datetime_string(self, date_time, is_date=False):
        format_string = self.dispose_datetime_format_datetime_string(is_date=is_date)
        return date_time.strftime(format_string)

    # 把字符串转成datetime
    def datetime_string_to_datetime(self, data_time_string, is_date=False):
        string_index = str(data_time_string).find(".")
        # print("string_index,%s"%string_index)
        if string_index != -1:
            data_time_string = data_time_string[:string_index]
        data_time_string = data_time_string.replace('T', ' ').replace('Z', '')
        format_string = self.dispose_datetime_format_datetime_string(is_date=is_date)
        return datetime.datetime.strptime(data_time_string, format_string)

    # 把字符串转成时间戳形式
    def datetime_string_to_timestamp(self, data_time_string='1970-01-01 00:00:00', is_timestamp_second: bool = False,
                                     is_date=False):
        '''isTimestamp_second:是否输出时间为秒，默认为false即13位时间戳，true：返回10位时间戳'''
        # print("strTime,%s"%strTime)
        try:
            if data_time_string == '1970-01-01 00:00:00':
                data_time_string = self.timestamp_to_datetime_string(timeStamp=0)
            if is_date:
                self.get_zero_timestamp(self.datetime_string_to_datetime(data_time_string=data_time_string))
            timeStamp = int(time.mktime(self.datetime_string_to_datetime(data_time_string).timetuple()))
            if not is_timestamp_second:
                timeStamp *= 1000
            return timeStamp
        except Exception as error:
            print("数据处理失败，原因为:\n%s" % (error))

    # 获取当前时间的0点整时间戳
    def get_zero_timestamp(self, now=None, millisecond=False):
        if not now:
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(now, "%Y-%m-%d")

        today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        timestamp = int(time.mktime(today.timetuple()))
        if millisecond:
            return timestamp * 1000
        return timestamp

    def string_to_utc(self, data_time_string, utc_tag=True):
        if not utc_tag:
            format = self.dispose_datetime_format_datetime_string(is_date=False, is_mongo_format=utc_tag)
            dt = datetime.datetime.strptime(data_time_string, format)
            return dt.astimezone(pytz.utc)
        timestamp = self.datetime_string_to_timestamp(data_time_string=data_time_string, is_date=False)
        return self.timestamp_to_datetime_string(timeStamp=timestamp, is_utc=True)

    def timestamp_to_datetime_string(self, timeStamp=0, is_date=False, is_utc=False):
        # 把时间戳转成字符串形式
        '''
        Args:
            timeStamp: 默认为当前时间
            is_date: 是否输出日期

        Returns:

        '''
        try:
            if not timeStamp:
                timeStamp = self.get_timestamp()
            timeStamp = int(timeStamp)
            if len(str(timeStamp)) >= 13:
                timeStamp /= 1000
            if not timeStamp and timeStamp != 0:
                timeStamp = time.time()
            format_string = self.dispose_datetime_format_datetime_string(is_date=is_date, is_mongo_format=is_utc)
            if is_utc:
                timeStamp = timeStamp - 8 * 3600
            return time.strftime(format_string, time.localtime(timeStamp))
        except:
            traceback.print_exc()

    # 把datetime类型转外时间戳形式
    def datetime_to_timestamp(self, date_time, millisecond=False):
        if millisecond:
            return int(time.mktime(date_time.timetuple())) * 1000
        return int(time.mktime(date_time.timetuple()))

    def datetime_to_iso_date(self, date_time):
        return dateutil.parser.parse(date_time)

    # 将iso_date转换为时间字符串，iso_date主要是mongo存储得时间格式
    def iso_date_to_string(self, iso_date_in=None, time_diffence=0, is_date=False):
        '''time_diffence:时间差，目前只支持指定小时'''
        if iso_date_in is None:
            iso_date_in = datetime.datetime.now()
            return str(iso_date_in)
        else:
            re_date = re.search('(\d.+\d)', iso_date_in)
            if re_date:
                re_date = re_date.group()
                if ":" in re_date:
                    # print(re_date)
                    iso_date_in = dateutil.parser.parse(re_date)  # 转换为iso_date为时间字符串
                    format_string = self.dispose_datetime_format_datetime_string(is_date=is_date)
                    time_out = datetime.datetime.strptime(iso_date_in.strftime(format_string), format_string)
                    # datetime.timedelta对象代表两个时间之间的时间差,这里需要计算八个小时后得时间，所以指定hours=8，
                    # 当前也指定其他时间对象day、seconds、microseconds、milliseconds、minutes、hours、weeks、fold等
                    delta = datetime.timedelta(hours=time_diffence)
                    iso_date_out = str(time_out + delta)
                else:
                    iso_date_out = self.timestamp_to_datetime_string(int(re_date))
                return iso_date_out
            else:
                return str(iso_date_in)

    # 处理robo 3t复制出来的mongo查询结果，序列化为list
    def mongodata_serialize(self, str_in, space_one='NumberLong\(\W?\d+\)', space_two="\/\*\s?\d+\s?\*\/",
                            space_date='iso_date\(.*\)'):
        str_out = str(self.json_str_to_pyobject(str_in))
        '''处理NumberLong'''
        mongo_numberLong_list = re.findall(space_one, str_out)
        if mongo_numberLong_list:
            for i in mongo_numberLong_list:
                mongo_numberLong = re.search('[-+]?\d+', i)
                if mongo_numberLong:
                    mongo_numberLong = mongo_numberLong.group()
                    str_out = str_out.replace(i, mongo_numberLong)
        else:
            str_out = str_out
        '''处理iso_date'''
        iso_date = re.findall(space_date, str_out)
        if iso_date:
            for iso_date_in_str in list(set(iso_date)):
                # print(iso_date_in_str)
                iso_date_out_str = str(
                    self.datetime_string_to_datetime(self.iso_date_to_string(iso_date_in=iso_date_in_str)))
                str_out = str_out.replace(iso_date_in_str, iso_date_out_str)
        else:
            str_out = str_out
        '''处理集合间的分隔符'''
        mongo_separator_list = re.findall(space_two, str_out)
        if not mongo_separator_list:
            return eval(str_out)
        for i in mongo_separator_list:
            mongo_separator = re.search('[-+]?\d+', i)
            if mongo_separator:
                if mongo_separator.group() == '1':
                    mongo_separator = '['
                else:
                    mongo_separator = ','
                str_out = str_out.replace(i, mongo_separator)
        str_out += ']'
        return eval(str_out)

    # 字符串转换为时间戳,支持调整
    def datetime_string_to_timestamp_adjust(self, date_time_str=None, type: int = 2, num: int = 0,
                                            is_timestamp_second: bool = False):
        time_to_str = self.adjust_time(type=type, num=num, date_time_str=date_time_str)
        timestamp = self.datetime_string_to_timestamp(data_time_string=time_to_str,
                                                      is_timestamp_second=is_timestamp_second)
        return timestamp

    # # 字符串转换为时间戳,支持调整
    def timestamp_to_datetime_string_ajdust(self, date_time_str=None, type: int = 2, num: int = 0, is_date=False):
        timeStamp = self.timestamp_to_datetime_string_ajdust(type=type, num=num, date_time_str=date_time_str)
        return self.timestamp_to_datetime_string(timeStamp, is_date=is_date)

    #  输出当前时间的13位时间戳
    def get_timestamp(self, is_secends=False):
        '''
        Args:
            is_secends: 是否单位输出为秒
        Returns:
        '''
        if is_secends:
            current_milli_time = lambda: int(round(time.time()))
        else:
            current_milli_time = lambda: int(round(time.time())) * 1000
            # 输出13位时间戳,round:对浮点数进行四舍五入
        return str(current_milli_time())

    # 时间调整
    def adjust_time(self, date_time_str=None, type: int = 2, num: int = 0, is_timestamp=False,
                    millisecond=False, is_date=False, is_utc=False):
        '''days seconds microseconds milliseconds minutes hours weeks fold'''
        '''type: 周 天 时 分 秒
        isDate: 是否是日期， 默认否'''
        if not date_time_str:
            strTime = datetime.datetime.now()  # 默认取当前时间
        else:
            strTime = self.datetime_string_to_datetime(date_time_str)
            # strTime=date_time_str
        if type == 1:
            day = strTime + datetime.timedelta(weeks=num)
        elif type == 2:
            day = strTime + datetime.timedelta(days=num)
        elif type == 3:
            day = strTime + datetime.timedelta(hours=num)
        elif type == 4:
            day = strTime + datetime.timedelta(minutes=num)
        elif type == 5:
            day = strTime + datetime.timedelta(seconds=num)
        else:
            print("暂不支持的调整单位")
            sys.exit()
        # print(day)
        # 将当前时间转换后时间戳，然后在将时间戳转换为时间字符串
        if is_timestamp:
            return self.datetime_to_timestamp(day, millisecond=millisecond)
        return self.timestamp_to_datetime_string(self.datetime_to_timestamp(day, millisecond=False), is_date=is_date,
                                        is_utc=is_utc)

    # 生成mongo时间字符
    def genrate_mongo_iso_date(self, date_time_str=None, type: int = 2, num: int = 0, is_date: bool = False,
                               is_mongo=True, is_utc=False):
        '''
        :param date_time_str: 默认取当前时间，如果传入了时间则取传入的时间
        :param type: 调整时间的类型
        :param num: 调整时间的数值
        :param isDate： 是否输出日期
        :param isMongo: 是否输出mongo格式
        :return:
        '''
        '''days seconds microseconds milliseconds minutes hours weeks fold'''
        '''type: 周 天 时 分 秒
        isDate: 是否是日期， 默认否'''
        # 输出当前日期
        temp_datetime = self.datetime_string_to_datetime(
            self.adjust_time(date_time_str=date_time_str, type=type, num=num, is_utc=is_utc))
        is_mongo = True if is_utc else is_mongo
        format_string = self.dispose_datetime_format_datetime_string(is_date=is_date, is_mongo_format=is_mongo)
        utctime_obj = temp_datetime.strftime(format_string)
        if is_utc:
            return utctime_obj
        if is_mongo:
            iso_date = parser.parse(utctime_obj)
            return iso_date
        else:
            return utctime_obj

    def is_today(self, timestamp):
        # 将时间戳转换为可读取的日期字符串
        timestamp_day = self.timestamp_to_datetime_string(timeStamp=timestamp, is_date=True)
        # 获取当前日期
        today = self.timestamp_to_datetime_string(timeStamp=0, is_date=True)
        # 比较日期是否相同
        return timestamp_day == today

    #
    def get_mondays(self, start_date, end_date):
        '''返回给定日期范围所有周一的日期'''
        # 将字符串日期转换为 datetime 对象
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # 确保起始日期是周一
        if start.weekday() != 0:
            start += datetime.timedelta(days=(7 - start.weekday()))

        # 构建结果列表
        mondays = []
        current = start
        while current <= end:
            mondays.append(current.strftime("%Y-%m-%d"))
            current += datetime.timedelta(days=7)

        return mondays

    def get_first_days(self, start_date, end_date):
        '''返回给定日期范围每月第一天的日期'''
        # 将字符串日期转换为 datetime 对象
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # 构建结果列表
        first_days = []
        current = start.replace(day=1)  # 将当前日期设置为该月的第一天

        while current <= end:
            first_days.append(current.strftime("%Y-%m-%d"))

            # 获取下一个月的第一天
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        return first_days

    def get_last_day_of_each_month(self, start_date, end_date):
        '''返回给定日期范围每月最后一天的日期'''
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        start_year, start_month = start.year, start_date.month
        end_year, end_month = end.year, end.month
        last_days = []

        for year in range(start_year, end_year + 1):
            month_range = range(1, 13) if year != end_year else range(1, end_month + 1)

            for month in month_range:
                last_day = calendar.monthrange(year, month)[1]
                date = datetime.date(year, month, last_day)
                last_days.append(date)

        return last_days

    def get_days_in_month(self, date):
        '''获取每个月的天数'''
        date_fm = datetime.datetime.strptime(date, "%Y-%m-%d")
        return calendar.monthrange(date_fm.year, date_fm.month)[1]


if __name__ == "__main__":
    du = timeUtil()
    # print(du.get_zero_timestamp('2023-07-04'))
    # print(du.get_days_in_month('2023-06-04'))
    start_timestamp = du.adjust_time(type=2, num=-365, is_timestamp=True)
    start_date = du.timestamp_to_datetime_string(timeStamp=start_timestamp, is_date=True)
    end_date = du.timestamp_to_datetime_string(is_date=True)
    print(du.get_mondays(start_date=start_date, end_date=end_date))
    # date_time_str = du.timestamp_to_datetime_string(1688118095)
    # print(date_time_str)
    # print(du.adjust_time(date_time_str=date_time_str, type=4, num=4, is_timestamp=True,
    #                      millisecond=True))
    # date_time_str2 = du.timestamp_to_datetime_string(1688118275173)
    # print(du.adjust_time(date_time_str=date_time_str2, type=2, num=-1, is_timestamp=True,
    #                      millisecond=True))
    # print(du.is_today(1687798861))
    # data_time_str=du.timestamp_to_datetime_string(1687763176175)
    # print(du.adjust_time(date_time_str=data_time_str,type=2, num=-1, is_timestamp=True, millisecond=True))
    # print(du.timestamp_to_datetime_string(is_date=True))
    # print(du.genrate_mongo_iso_date(isMongo=True,isDate=False,num=10))
    # print(du.genrate_mongo_iso_date(isDate=True,isMongo=False))
    # print(du.adjust_time(is_timestamp=False,millisecond=True))
    # print(du.adjust_time(is_timestamp=False,date_time_str='2023-01-19 16:57:17',millisecond=True,type=5,num=2223))
    # print(du.adjust_time(date_time_str="2021-06-02 11:14:27"))
    # print(du.adjust_time(date_time_str=None))
    # print(du.genrate_mongoiso_date(isMongo=False))
    # print(du.adjust_time(strTime="2021-06-03 16:32:36",num=2))
    # print(du.timestamp_toString_ajdust(strTime="2021-06-03 16:32:36",num=2))
    # print(du.string_toTimestamp())
    # print(du.timestamp_toString(stamp=0))
    # print(du.string_toTimestamp_adjust(num=1))
    # print(du.timestamp_toString_ajdust(num=2))
    # print(parser.parse("2021-05-26 17:33:55.000003"))
    # print(du.datetime_toiso_date("2021-05-26 17:33:55"))
    # print(du.adjust_time(type=1))
    # print(du.string_toTimestamp_adjust(num=2,isTimestamp_second=True))
