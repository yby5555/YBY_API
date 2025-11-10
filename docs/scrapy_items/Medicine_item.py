import scrapy


class MedicineItem(scrapy.Item):
    #药品表数据字段
    _id = scrapy.Field()#str-药品id(链接生成)
    update_time = scrapy.Field()#datatime-采集时间
    source = scrapy.Field()#str-数据来源

    # 索引页与图片
    IndexOss = scrapy.Field() #str-首页oss
    medicinePrescriptionDrug = scrapy.Field() #str-是否处方药(1是)
    medicineApprovalNumber = scrapy.Field() #str-批准文号
    medicineImage = scrapy.Field() #str-药品图片oss
    medicineImageLink = scrapy.Field() #str-药品图片链接

    # 介绍页与分类
    IntroductionOss = scrapy.Field() #str-介绍页oss
    medicineClassification = scrapy.Field()  #list of dict-疾病分类路径-{first_class:一级路径(str),second_class:二级路径(str)}

    # 详情信息
    medicineName = scrapy.Field() #str-药品名
    medicineLink = scrapy.Field() #str-药品链接
    medicineIntroduction = scrapy.Field() #str-药品介绍
    medicineSpecifications = scrapy.Field() #str-药品规格
    medicineUsage = scrapy.Field() #str-药品用法
    medicineIndications = scrapy.Field() #str-药品适应症
    medicineManufacturer = scrapy.Field() #str-药品生产企业
    medicineIngredient = scrapy.Field() #str-药品成分