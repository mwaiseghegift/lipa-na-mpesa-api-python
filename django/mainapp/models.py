from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_when = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class MpesaCalls(BaseModel):
    ip_address = models.CharField(max_length=200)
    caller = models.CharField(max_length=100)
    conversation_id = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        verbose_name = "Mpesa Call"
        verbose_name_plural = "Mpesa Calls"
        
class MpesaCallBacks(BaseModel):
    ip_address = models.CharField(max_length=200)
    caller = models.CharField(max_length=100)
    conversation_id = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        verbose_name = "Mpesa Call Back"
        verbose_name_plural = "Mpesa Call Backs"
        
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=100)
    type = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100) 
    organization_balace = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Mpesa Payment"
        verbose_name_plural = "Mpesa Payments"
        
    def __str__(self):
        return f"{self.first_name} - {self.amount}"
    
    