import scrapy


class AgriculturalProductQuotationItem(scrapy.Item):
    # 农产品报价信息表字段
    _id = scrapy.Field()  #str-Source_date(字符类型)_marketName_productName 生成

    # 业务数据字段
    productId = scrapy.Field()  #str-农产品信息表的_id
    productName = scrapy.Field()  #str-农产品名称
    marketId = scrapy.Field()  #str-报价批发表的_id
    marketName = scrapy.Field()  #str-报价批发市场
    highestPrice = scrapy.Field()  #float-最高价
    lowestPrice = scrapy.Field()  #float-最低价
    bulkPrice = scrapy.Field()  #float-大宗价
    origin = scrapy.Field()  #str-产地
    unit = scrapy.Field()  #str-单位
    date = scrapy.Field()  #datetime-日期

    # 元数据字段
    update_time = scrapy.Field()  #datetime-数据更新时间
    Source = scrapy.Field()  #str-数据来源
    rawData = scrapy.Field()  #str-原始数据存储