from NEMO.urls import router
from django.urls import path

from NEMO_rs2_access import api, views

router.register(r"rs2/logged_in_users", api.LoggedInUsersViewSet, basename="logged_in_users")
router.registry.sort(key=lambda x: (x[0].count('/'), x[0]))

urlpatterns = [
    # Override user preferences to add default project selection
    path("user_preferences/", views.custom_user_preferences, name="user_preferences"),

    path("rs2_sync_readers/", views.rs2_sync_reader, name="rs2_sync_readers"),
    path("rs2_sync_access/", views.rs2_sync_access, name="rs2_sync_access"),
]
