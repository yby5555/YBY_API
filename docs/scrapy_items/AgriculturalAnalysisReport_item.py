import scrapy


class AgriculturalAnalysisReportItem(scrapy.Item):
    # 农业分析报告表字段
    _id = scrapy.Field()  #str-Source_reportUrl 生成

    # 业务数据字段
    publishTime = scrapy.Field()  #datetime-发布时间
    reportTitle = scrapy.Field()  #str-报告标题
    reportContent = scrapy.Field()  #str-报告内容
    reportType = scrapy.Field()  #str-报告类型
    reportSource = scrapy.Field() #str-报告来源
    reportUrl = scrapy.Field()  #str-报告链接

    # 元数据字段
    update_time = scrapy.Field()  #datetime-数据更新时间
    Source = scrapy.Field()  #str-数据来源
    rawData = scrapy.Field()  #str-原始数据存储