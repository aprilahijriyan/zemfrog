from zemfrog.decorators import auto_status_code, authenticate
from zemfrog.helper import db_add, db_delete, db_update, get_column_names
from zemfrog.models import DefaultResponseSchema
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields
from {{ "" if main_app else ".." }}extensions.marshmallow import ma
from {{ "" if main_app else ".." }}{{src_model}} import {{name}}

class Create{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}
        exclude = ("id",)

class Read{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}

class Update{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}
        exclude = ("id",)

# class Delete{{name}}Schema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = {{name}}

class Limit{{name}}Schema(ma.Schema):
    offset = fields.Integer()
    limit = fields.Integer()


@authenticate()
@use_kwargs(Limit{{name}}Schema(), location="query")
@marshal_with(Read{{name}}Schema(many=True), 200)
def read(**kwds):
    """
    Read all data.
    """

    offset = kwds.get("offset")
    limit = kwds.get("limit")
    data = {{name}}.query.offset(offset).limit(limit).all()
    return data

@authenticate()
@use_kwargs(Create{{name}}Schema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def create(**kwds):
    """
    Add data.
    """

    found = {{name}}.query.filter_by(**kwds).first()
    if not found:
        model = {{name}}(**kwds)
        db_add(model)
        status_code = 200
        reason = "Successfully added data."

    else:
        status_code = 403
        reason = "Data already exists."

    return {
        "status_code": status_code,
        "reason": reason
    }

@authenticate()
@use_kwargs(Update{{name}}Schema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def update(id, **kwds):
    """
    Update data.
    """

    model = {{name}}.query.get(id)
    if model:
        db_update(model, **kwds)
        status_code = 200
        reason = "Successfully updating data."

    else:
        status_code = 404
        reason = "Data not found."

    return {
        "status_code": status_code,
        "reason": reason
    }

@authenticate()
# @use_kwargs(Delete{{name}}Schema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def delete(id):
    """
    Delete data.
    """

    model = {{name}}.query.get(id)
    if model:
        db_delete(model)
        status_code = 200
        reason = "Data deleted successfully."

    else:
        status_code = 404
        reason = "Data not found."

    return {
        "status_code": status_code,
        "reason": reason
    }


docs = {"tags": ["{{name}}"]}
endpoint = "{{url_prefix | lower}}"
url_prefix = "/{{url_prefix | lower}}"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"])
]
