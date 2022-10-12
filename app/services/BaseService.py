from importlib import import_module


class BaseService:
    @staticmethod
    def serialize_object(serializer, obj=None, many=False, module_name=None):        
        module = import_module(
            f'api.serializers.{module_name if module_name is not None else serializer}')
        serializer = getattr(module, serializer)
        return serializer(obj, many=many).data

    def get_instance(model_name, **kwargs):
        module = import_module(f'app.models')
        model = getattr(module, model_name)
        return model.objects.get(**kwargs)
