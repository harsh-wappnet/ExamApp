from django.db import models


# Create your models here.
class TestTable(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False, null=False)
    retailer_pool_id = models.CharField(max_length=50, null=False)
    retailer_name = models.CharField(max_length=50, null=False)
    logo_url = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = "test_table"

    def __str__(self):
        return f"retailer_pool_id : {self.retailer_pool_id} " \
               f"retailer_name : {self.retailer_name}" \
               f"logo_url : {self.logo_url}"
