from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery, OuterRef, Q

from Product.models import Work


class StatusDisplayFilter(SimpleListFilter):
    title = "Status"
    parameter_name = "status_display"

    def lookups(self, request, model_admin):
        return [
            (Work.Status.NOT_RECEIVED, Work.Status(Work.Status.NOT_RECEIVED).label),
            (Work.Status.IN_PROCESS, Work.Status(Work.Status.IN_PROCESS).label),
            (Work.Status.DONE, Work.Status(Work.Status.DONE).label),
            (Work.Status.REJECTED, Work.Status(Work.Status.REJECTED).label),
            (Work.Status.APPROVED, Work.Status(Work.Status.APPROVED).label),
        ]

    def queryset(self, request, queryset):
        if self.value():
            latest_work = Work.objects.filter(order=OuterRef('pk')).order_by('-id')
            if self.value() == str(Work.Status.NOT_RECEIVED):
                return queryset.annotate(
                    last_work_status=Subquery(latest_work.values('status')[:1])
                ).filter(Q(last_work_status__isnull=True) | Q(last_work_status=self.value()))
            else:
                return queryset.annotate(
                    last_work_status=Subquery(latest_work.values('status')[:1])
                ).filter(last_work_status=self.value())
        return queryset
