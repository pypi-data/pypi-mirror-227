from netbox.views import generic
from netbox_sync_status.filtersets import SyncStatusFilterForm, SyncStatusFilterSet
from .tables import SyncStatusListTable, SyncSystemListTable
from .models import SyncStatus, SyncSystem
from .forms import SyncSystemForm


class SyncSystemView(generic.ObjectView):
    queryset = SyncSystem.objects.prefetch_related("tags")


class SyncSystemListView(generic.ObjectListView):
    queryset = SyncSystem.objects.prefetch_related("tags")
    table = SyncSystemListTable


class SyncSystemEditView(generic.ObjectEditView):
    queryset = SyncSystem.objects.all()
    form = SyncSystemForm


class SyncSystemDeleteView(generic.ObjectDeleteView):
    queryset = SyncSystem.objects.all()


class SyncStatusListView(generic.ObjectListView):
    queryset = SyncStatus.objects.order_by("-id")
    table = SyncStatusListTable
    filterset = SyncStatusFilterSet
    filterset_form = SyncStatusFilterForm
    actions = ("export")
