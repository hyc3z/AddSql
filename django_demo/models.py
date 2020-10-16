from django.db import models


# 购货表
class ghb(models.Model):

# 产品编号
    cpbh = models.CharField("产品编号", max_length=20)
# 产品名称
    cpmc = models.CharField("产品名称", max_length=20)
# 规格型号
    ggxh = models.CharField("规格型号", max_length=20)
# 单位
    dw = models.CharField("单位", max_length=20)
# 单价
    dj = models.DecimalField("单价", max_digits=8, decimal_places=2)
# 数量
    sl = models.IntegerField("数量")
# 总价
    zj = models.DecimalField("总价", max_digits=8, decimal_places=2)
# 款式
    ks = models.CharField("款式", max_length=20)
# 购进时间
    gjsj = models.DateTimeField("购进时间")
# 备注
    bz = models.CharField("备注", max_length=20)


# 销售表
class xsb(models.Model):

# 业务员
    ywy = models.CharField("业务员", max_length=20)
# 购货单位
    ghdw = models.CharField("购货单位", max_length=20)
# 购货单位性质（学校、个人等）
    ghdwxz = models.CharField("购货单位性质", max_length=20)
# 销售日期
    xsrq = models.DateField("销售日期")
# 产品编号
    cpbh = models.CharField("产品编号", max_length=20)
# 产品名称
    cpmc = models.CharField("产品名称", max_length=20)
# 规格型号（颜色、片/盒）
    ggxh = models.CharField("规格型号", max_length=20)
# 单位
    dw = models.CharField("单位", max_length=20)
# 单价
    dj = models.DecimalField("单价", max_digits=8, decimal_places=2)
# 数量
    sl = models.IntegerField("数量")
# 总价
    zj = models.DecimalField("总价", max_digits=8, decimal_places=2)
# 款式
    ks = models.CharField("款式", max_length=20)
# 收款时间
    sksj = models.DateTimeField("收款时间")
# 收款金额
    skje = models.CharField("收款金额", max_length=20)
# 欠款
    qk = models.CharField("欠款", max_length=20)
# 销售形式（赠送、销售、样品、返厂、代发等）
    xsxs = models.CharField("销售形式", max_length=20)
# 发货形式（邮寄现付、邮寄到付、邮寄垫付、自取）
    fhxs = models.CharField("发货形式", max_length=20)