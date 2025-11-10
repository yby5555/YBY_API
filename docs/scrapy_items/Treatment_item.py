import scrapy


class TreatmentItem(scrapy.Item):
    # 治疗表数据字段
    _id = scrapy.Field()#str-治疗id(链接生成)
    update_time = scrapy.Field()#datatime-采集时间

    # 业务字段
    msg_type = scrapy.Field()
    treatmentName = scrapy.Field() #str-治疗名称
    treatmentLink = scrapy.Field() #str-治疗链接
    treatmentSource = scrapy.Field() #str-数据来源
    treatmentHtml = scrapy.Field()  #str-原始页面OSS

    treatmentDepartmentList = scrapy.Field() #list-治疗相关科室
    treatmentIntroduction = scrapy.Field() #str-治疗介绍
    treatmentDisease = scrapy.Field() #str-治疗相关疾病
    treatmentPrepare = scrapy.Field() #str-治疗准备
    treatmentTaboo = scrapy.Field() #str-治疗禁忌
    treatmentRisk = scrapy.Field() #str-治疗风险
    treatmentNutritionAndDiet = scrapy.Field() #str-治疗营养与饮食
    treatmentPrecautions = scrapy.Field() #str-治疗注意事项
    treatmentRehabilitation = scrapy.Field() #str-治疗康复锻炼
    treatmentRegularCheck = scrapy.Field() #str-治疗定期检查
    treatmentHospitalList = scrapy.Field() #list of dict-疾病检查相关医院-{name:医院名称(str),goodVoteCnt:好评数(str),nameId:医院名称映射Id(str),nameIdSource:映射来源(str)}
    treatmentDiseaseRelatedList = scrapy.Field() #list of dict-疾病相关疾病-{name:疾病名称(str),nameId:疾病名称映射Id(str),nameIdSource:映射来源(str)}