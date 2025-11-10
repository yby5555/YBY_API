import scrapy


class VaccineItem(scrapy.Item):
    # 疫苗表数据字段
    _id = scrapy.Field()#str-疫苗ID
    update_time = scrapy.Field()#datatime-采集时间

    # 业务字段
    msg_type = scrapy.Field()
    vaccineName = scrapy.Field() #str-疫苗名称
    vaccineLink = scrapy.Field() #str-疫苗链接
    vaccineSource = scrapy.Field() #str-数据来源
    vaccineHtml = scrapy.Field()  #str-原始页面OSS

    vaccineDepartmentList = scrapy.Field() #list-疫苗相关科室
    vaccineIntroduction = scrapy.Field() #str-疫苗介绍
    vaccineEfficacy = scrapy.Field()  #str-疫苗作用与功效
    vaccineGuidance = scrapy.Field() #str-疫苗指导
    vaccineReaction = scrapy.Field() #str-疫苗不良反应
    vaccineTaboo = scrapy.Field() #str-疫苗接种禁忌
    vaccinePrecautions = scrapy.Field() #str-疫苗注意事项


