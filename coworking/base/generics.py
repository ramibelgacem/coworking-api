from rest_framework import generics, mixins


class ActivateModelMixin(mixins.UpdateModelMixin):
    """
    Activate a model instance.
    """

    def activate(self, request, *args, **kwargs):
        request.data.update({'active': True})
        return self.partial_update(request, *args, **kwargs)


class ActivateAPIView(ActivateModelMixin, generics.GenericAPIView):
    """
    Concrete view for activating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.activate(request, *args, **kwargs)


class DesactivateModelMixin(mixins.UpdateModelMixin):
    """
    Desactivate a model instance.
    """

    def desactivate(self, request, *args, **kwargs):
        request.data.update({'active': False})
        return self.partial_update(request, *args, **kwargs)


class DesactivateAPIView(DesactivateModelMixin, generics.GenericAPIView):
    """
    Concrete view for activating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.desactivate(request, *args, **kwargs)
