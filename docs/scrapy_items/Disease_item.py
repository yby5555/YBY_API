import scrapy

class DiseaseItem(scrapy.Item):# 疾病表数据字段
    _id = scrapy.Field()  #str-疾病ID(链接生成)
    diseaseClassification = scrapy.Field() #list of dict-疾病分类路径-{first_class:一级路径(str),second_class:二级路径(str),third_class:三级路径(str)}
    diseaseName = scrapy.Field() #str-疾病名
    diseaseAlias = scrapy.Field() #str-疾病别名

    diseaseIntroduction = scrapy.Field() #str-介绍
    diseaseCauses = scrapy.Field() #str-发病原因
    diseaseSymptoms = scrapy.Field() #str-症状表现
    diseasePrevention= scrapy.Field() #str-如何预防
    diseaseExaminations = scrapy.Field() #str-检查
    diseaseTreatment = scrapy.Field() #str-治疗

    diseaseHtml = scrapy.Field() #str-原始页面oss
    diseaseSource = scrapy.Field() #str-来源
    diseaseLink = scrapy.Field() #str-链接
    update_time = scrapy.Field() #str-更新时间

    diseaseRelatedList = scrapy.Field() #list of dict-疾病相关疾病-{name:疾病名称(str),nameId:疾病名称映射Id(str),nameIdSource:映射来源(str)}
    diseaseRelatedCheckList = scrapy.Field() #list of dict-疾病相关检查-{name:检查名称(str),nameId:检查名称映射Id(str),nameIdSource:映射来源(str)}
    diseaseCheckHospitalList = scrapy.Field() #list of dict-疾病检查相关医院-{name:医院名称(str),goodVoteCnt:好评数(str),nameId:医院名称映射Id(str),nameIdSource:映射来源(str)}

