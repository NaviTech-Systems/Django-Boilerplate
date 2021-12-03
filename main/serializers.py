from rest_framework import serializers
from rest_framework_cache.cache import cache
from rest_framework_cache.settings import api_settings
from rest_framework_cache.utils import get_cache_key


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        if self.serializer is not None and not issubclass(
            self.serializer, serializers.Serializer
        ):
            raise TypeError('"serializer" is not a valid serializer class')

        super(RelatedFieldAlternative, self).__init__(**kwargs)

    def use_pk_only_optimization(self):
        return not self.serializer

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super(RelatedFieldAlternative, self).to_representation(instance)


class CachedSerializerMixin:
    def _get_cache_key(self, instance):
        request = self.context.get("request")
        protocol = request.scheme if request else "http"
        return get_cache_key(instance, self.__class__, protocol)

    def to_representation(self, instance):
        """
        Checks if the representation of instance is cached and adds to cache
        if is not.
        """
        key = self._get_cache_key(instance)
        cached = cache.get(key)
        if cached:
            return cached

        result = super(CachedSerializerMixin, self).to_representation(instance)
        cache.set(key, result, api_settings.DEFAULT_CACHE_TIMEOUT)
        return result
