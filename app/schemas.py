from .extensions import ma
from .models import Service, Category
from marshmallow_sqlalchemy.fields import Nested

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True
        include_fk = True

class CategorySchema(ma.SQLAlchemyAutoSchema):
    services = Nested(ServiceSchema, many=True)

    class Meta:
        model = Category
        load_instance = True

category_schema = CategorySchema()
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)