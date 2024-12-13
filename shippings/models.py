from django.db import models  

class Shipping(models.Model):
    cliente = models.CharField(max_length=255, default=None)
    nfe = models.IntegerField(primary_key=True)
    data_emissao = models.DateField()
    data_limite = models.DateField()
    volumes = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default='PENDENTE')

    def __repr__(self) -> str:
        return f'{self.nfe}, {self.cliente}, {self.data_emissao}, {self.volumes}, {self.peso}'

class ShippingItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.IntegerField(default=None)
    descricao = models.CharField(max_length=255)
    un = models.CharField(max_length=6)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unit = models.DecimalField(max_digits=10, decimal_places=2)
    nfe_remessa = models.ForeignKey(Shipping, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codigo', 'nfe_remessa')

    def __repr__(self) -> str:
        return f'{self.codigo}, {self.descricao}, {self.un}, {self.quantidade}, {self.valor_unit}'

class ShippingStorage(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.IntegerField(default=None)
    descricao = models.CharField(max_length=255)
    un = models.CharField(max_length=6)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unit = models.DecimalField(max_digits=10, decimal_places=2)
    nfe_remessa = models.ForeignKey(Shipping, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codigo', 'nfe_remessa')

    def __repr__(self) -> str:
        return f'{self.codigo}, {self.descricao}, {self.un}, {self.quantidade}, {self.valor_unit}'


class ReturnOfShip(models.Model):
    cliente = models.CharField(max_length=255, default=None)
    nfe = models.IntegerField(primary_key=True)
    data_emissao = models.DateField()
    volumes = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    nfe_remessa = models.ForeignKey(Shipping, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f'{self.cliente}, {self.nfe}, {self.data_emissao}, {self.data_limite}, {self.volumes},\
            {self.peso}, {self.nfe_remessa}'


class ReturnItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.IntegerField(default=None)
    descricao = models.CharField(max_length=255)
    un = models.CharField(max_length=6)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unit = models.DecimalField(max_digits=10, decimal_places=2)
    nfe_retorno = models.ForeignKey(ReturnOfShip, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codigo', 'nfe_retorno')

    def __repr__(self) -> str:
        return f'{self.codigo}, {self.descricao}, {self.un}, {self.quantidade}, {self.valor_unit}'