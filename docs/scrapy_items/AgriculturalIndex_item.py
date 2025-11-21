import scrapy


class AgriculturalIndexItem(scrapy.Item):
    # 农业指数表字段
    _id = scrapy.Field()  #str-Source_indexName_publishTime(字符串形式) 生成

    # 业务数据字段
    publishTime = scrapy.Field()  #datatime-发布时间
    currentIndexValue = scrapy.Field()  #float-当前指数值
    previousIndexValue = scrapy.Field()  #float-上一天指数值
    indexName = scrapy.Field()  #str-指数名称
    indexType = scrapy.Field()  #str-指数类型
    chainRatio = scrapy.Field()  #float-环比
    collectTime = scrapy.Field()  #datatime-采集时间

    # 元数据字段
    update_time = scrapy.Field()  #datatime-数据更新时间
    Source = scrapy.Field()  #str-数据来源
    rawData = scrapy.Field()  #str-原始数据存储