from django.db.models.fields import PositiveIntegerField
from django.core.exceptions import ObjectDoesNotExist


class CustomPositiveIntegerField(PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # Check if object exists in database
            try:
                qs = self.model.objects.all()

                # if for_fields is not None we filter query set based on field
                # so that we only get objects connected to that field
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)

                last = qs.latest(self.attname)
                value = last.order + 1

            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            super().pre_save(model_instance, add)
