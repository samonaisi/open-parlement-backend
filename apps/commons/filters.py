from django.db.models import Func, QuerySet
from django.db.models.constants import LOOKUP_SEP
from django_filters import filters
from rest_framework.filters import SearchFilter


class MultiValueCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    """Allows for empty value in the filter."""

    def filter(self, queryset: QuerySet, value: str) -> QuerySet:  # noqa: A003
        if value:
            return super(MultiValueCharFilter, self).filter(queryset, value)
        return queryset


class UnaccentSearchFilter(SearchFilter):
    """Search filter that uses PostgreSQL unaccent feature."""

    class PostgresUnaccent(Func):
        function = "UNACCENT"

    def construct_search(self, field_name, queryset):
        lookup = super().construct_search(field_name, queryset)
        lookup = lookup.split(LOOKUP_SEP)
        lookup.insert(len(lookup) - 1, "unaccent")
        return LOOKUP_SEP.join(lookup)
