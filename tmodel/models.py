from django.db import models
from django.core.exceptions import ValidationError

from softdelete.models import SoftDeleteObject, SoftDeleteManager


class BaseModel(SoftDeleteObject):

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def save(self, **kwargs):
        if not self.deleted:
            unique_fields = getattr(self, "unique_fields", ())
            for unique_field in unique_fields:
                if self.__class__.objects.filter(**{unique_field: getattr(self, unique_field)}).exists():
                    raise ValidationError("{}数据库字段unique唯一性验证不合法".format(unique_field))

            unique_together_fields = getattr(self, "unique_together_fields", ())
            for unique_together_field in unique_together_fields:
                if self.__class__.objects.filter(**{item: getattr(self, item)
                                                    for item in unique_together_field}).exists():
                    raise ValidationError("{}数据库联合主键字段unique唯一性验证不合法".format(unique_together_fields))
        super().save(**kwargs)

    def delete(self, *args, **kwargs):
        super(BaseModel, self).delete()


class Category(BaseModel):
    cate = models.CharField(max_length=10)


class Good(BaseModel):
    cate = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="商品", max_length=233, db_index=True)
    province = models.CharField(verbose_name="省", max_length=10, default="江苏")
    city = models.CharField(verbose_name="城市", max_length=10, default="南京")

    @property
    def unique_fields(self):
        return ('name', )

    @property
    def unique_together_fields(self):
        return (("province", "city"), )


from rest_framework import serializers


class GoodSer(serializers.ModelSerializer):

    class Meta:
        model = Good
        fields = '__all__'

    def validate(self, attrs):
        import pdb
        pdb.set_trace()
        model = self.__class__.Meta.model
        model.objects.filter()
