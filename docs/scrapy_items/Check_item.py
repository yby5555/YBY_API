import scrapy


class CheckItem(scrapy.Item):
    # 检查表数据字段
    _id = scrapy.Field() #str-链接生成
    update_time = scrapy.Field() #datatime-采集时间

    # 业务字段
    msg_type = scrapy.Field()
    checkName = scrapy.Field() #str-名称
    checkLink = scrapy.Field() #str-链接
    checkSource = scrapy.Field() #str-数据来源
    checkHtml = scrapy.Field()  #str-原始页面OSS
    checkHospitalList = scrapy.Field() #list of dict-检查相关医院列表-{name:医院名称(str),goodVoteCnt:好评数(str),nameId:医院名称映射Id(str),nameIdSource:映射来源(str)}
    checkDiseaseRelatedList = scrapy.Field() #list of dict-检查相关疾病-{name:疾病名称(str),nameId:疾病名称映射Id(str),nameIdSource:映射来源(str)}

    checkDepartmentList = scrapy.Field() #list-检查科室列表
    checkIntroduction = scrapy.Field() #str-检查介绍
    checkDisease = scrapy.Field() #str-检查相关疾病
    checkPurpose = scrapy.Field()  #str-检查目的
    checkPrepare = scrapy.Field() #str-检查准备
    checkBody = scrapy.Field()  #str-检查部位
    checkMethod = scrapy.Field() #str-检查方式
    checkTaboo = scrapy.Field() #str-检查禁忌
    checkRisk = scrapy.Field() #str-检查风险