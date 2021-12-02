import inspect

# from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.openapi import AutoSchema
from .serializers import RelatedFieldAlternative


class CustomSchema(AutoSchema):
    def _map_serializer_field(self, field, direction, collect_meta=True):

        if isinstance(field, RelatedFieldAlternative) and hasattr(
            field, "serializer"
        ):
            print(
                self.view.__dict__,
                direction,
                self.method.lower(),
            )
            # print(3)
            frame = inspect.currentframe()

            while frame is not None:
                # print(self.get_operation_id())

                method_name = frame.f_code.co_name
                if self.method.lower() != "get":
                    break
                elif self.method.lower() == "get":
                    # print(56565)
                    field = field.serializer()
                    return super(CustomSchema, self)._map_serializer_field(
                        field, direction, collect_meta
                    )

                frame = frame.f_back

        return super(CustomSchema, self)._map_serializer_field(
            field, direction, collect_meta
        )
