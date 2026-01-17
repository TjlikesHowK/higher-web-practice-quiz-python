from django.db import models
from django.shortcuts import get_object_or_404


def update_object(
    model: models.Model,
    id: int,
    data: dict,
):
    object = get_object_or_404(model, id=id)

    for field, value in data.items():
        setattr(object, field, value)

    object.save()
    return object
