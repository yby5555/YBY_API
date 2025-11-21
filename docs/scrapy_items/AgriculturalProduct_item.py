import scrapy


class AgriculturalProductItem(scrapy.Item):
    # 农产品表字段
    _id = scrapy.Field()  #str-productName生成
    Classification = scrapy.Field() #list of dict-农产品分类路径-{first_class:一级路径(str),second_class:二级路径(str)}

    # 业务数据字段
    productName = scrapy.Field()  #str-农产品名称
    productImage = scrapy.Field()  #str-农产品图片
    productImageUrl = scrapy.Field()  #str-农产品图片url

    # 元数据字段
    update_time = scrapy.Field()  #datetime-数据更新时间
    Source = scrapy.Field()  #str-数据来源
    rawData = scrapy.Field()  #str-原始数据存储