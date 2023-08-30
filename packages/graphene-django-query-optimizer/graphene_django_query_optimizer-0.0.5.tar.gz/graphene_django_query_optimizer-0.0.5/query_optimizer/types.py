import graphene_django
from django.db.models import Model, QuerySet
from graphene.relay.connection import Connection
from graphene.types.definitions import GrapheneObjectType
from graphql.type.definition import GraphQLNonNull

from .optimizer import optimize
from .settings import optimizer_settings
from .typing import PK, GQLInfo, Optional, TypeVar

TModel = TypeVar("TModel", bound=Model)


__all__ = [
    "DjangoObjectType",
]


class DjangoObjectType(graphene_django.types.DjangoObjectType):
    """DjangoObjectType that automatically optimizes its queryset."""

    class Meta:
        abstract = True

    @classmethod
    def max_complexity(cls) -> int:
        return optimizer_settings.MAX_COMPLEXITY  # type: ignore[no-any-return]

    @classmethod
    def can_optimize_resolver(cls, info: GQLInfo) -> bool:
        return_type = info.return_type
        if isinstance(return_type, GraphQLNonNull):
            return_type = return_type.of_type

        return isinstance(return_type, GrapheneObjectType) and (
            issubclass(return_type.graphene_type, (cls, Connection))
        )

    @classmethod
    def get_queryset(cls, queryset: QuerySet[TModel], info: GQLInfo) -> QuerySet[TModel]:
        if cls.can_optimize_resolver(info):
            queryset = optimize(queryset, info, cls.max_complexity())
        return queryset

    @classmethod
    def get_node(cls, info: GQLInfo, id: PK) -> Optional[TModel]:  # noqa: A002
        queryset: QuerySet[TModel] = cls._meta.model.objects.all()
        setattr(queryset, optimizer_settings.PK_CACHE_KEY, id)
        queryset = cls.get_queryset(queryset, info)
        return queryset.first()
