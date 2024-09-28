"""Main configurations information."""
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Details for authentication module."""

    name = 'cpovc_auth'
    verbose_name = 'User Management'


class MainAppConfig(AppConfig):
    """Details for common application module."""

    name = 'cpovc_main'
    verbose_name = 'System Lookups and Settings'


class RegAppConfig(AppConfig):
    """Details for Registry modules."""

    name = 'cpovc_registry'
    verbose_name = 'Registry Management'


class AccessAppConfig(AppConfig):
    """Details for Registry modules."""

    name = 'cpovc_access'
    verbose_name = 'Access Management'


# """Main configurations information."""
# from django.apps import AppConfig


# class AuthAppConfig(AppConfig):
#     """Details for authentication module."""
#     name = 'cpovc_auth'
#     verbose_name = 'User Management'


# class MainAppConfig(AppConfig):
#     """Details for common application module."""
#     name = 'cpovc_main'
#     verbose_name = 'System Lookups and Settings'


# class RegAppConfig(AppConfig):
#     """Details for Registry modules."""
#     name = 'cpovc_registry'
#     verbose_name = 'Registry Management'


# class AccessAppConfig(AppConfig):
#     """Details for Access Management module."""
#     name = 'cpovc_access'
#     verbose_name = 'Access Management'


# class FormsAppConfig(AppConfig):
#     """Details for Forms module."""
#     name = 'cpovc_forms'
#     verbose_name = 'Forms Management'


# class GisAppConfig(AppConfig):
#     """Details for GIS module."""
#     name = 'cpovc_gis'
#     verbose_name = 'Geographical Information Systems'


# class SettingsAppConfig(AppConfig):
#     """Details for Settings module."""
#     name = 'cpovc_settings'
#     verbose_name = 'System Settings'


# class OvcAppConfig(AppConfig):
#     """Details for OVC module."""
#     name = 'cpovc_ovc'
#     verbose_name = 'OVC Management'


# class ManageAppConfig(AppConfig):
#     """Details for Manage module."""
#     name = 'cpovc_manage'
#     verbose_name = 'Management Tools'


# class NotificationsAppConfig(AppConfig):
#     """Details for Notifications module."""
#     name = 'notifications'
#     verbose_name = 'Notification System'

# class OfflineModeAppConfig(AppConfig):
#     """Details for Notifications module."""
#     name = 'cpovc_offline_mode'
#     verbose_name = 'cpovc_offline_mode'
    

# class HelpAppConfig(AppConfig):
#     """Details for Help module."""
#     name = 'cpovc_help'
#     verbose_name = 'Help and Support'


# class PreventiveAppConfig(AppConfig):
#     """Details for Preventive module."""
#     name = 'cpovc_preventive'
#     verbose_name = 'Preventive Management'


# class PmtctAppConfig(AppConfig):
#     """Details for PMTCT module."""
#     name = 'cpovc_pmtct'
#     verbose_name = 'PMTCT Management'


# class DashboardAppConfig(AppConfig):
#     """Details for Dashboard module."""
#     name = 'cpovc_dashboard'
#     verbose_name = 'Dashboard'


# class DreamsAppConfig(AppConfig):
#     """Details for DREAMS module."""
#     name = 'cpovc_dreams'
#     verbose_name = 'DREAMS Management'


# class ApiAppConfig(AppConfig):
#     """Details for API module."""
#     name = 'cpovc_api'
#     verbose_name = 'API Integration'


# class DashboardsAppConfig(AppConfig):
#     """Details for Dashboards module."""
#     name = 'cpovc_dashboards'
#     verbose_name = 'Dashboards'


# class MobileAppConfig(AppConfig):
#     """Details for Mobile module."""
#     name = 'cpovc_mobile'
#     verbose_name = 'Mobile Interface'


# class HesAppConfig(AppConfig):
#     """Details for HES module."""
#     name = 'cpovc_hes'
#     verbose_name = 'Health Information System'

# class CrispyFormsConfig(AppConfig):
#     """Details for Crispy Forms integration."""
#     name = 'crispy_forms'
#     verbose_name = 'Crispy Forms'


# class CrispyBootstrap3Config(AppConfig):
#     """Details for Crispy Bootstrap 3 integration."""
#     name = 'crispy_bootstrap3'
#     verbose_name = 'Crispy Bootstrap 3'


# class ImportExportConfig(AppConfig):
#     """Details for Django Import Export integration."""
#     name = 'import_export'
#     verbose_name = 'Django Import Export'


# class RestFrameworkConfig(AppConfig):
#     """Details for Django REST Framework integration."""
#     name = 'rest_framework'
#     verbose_name = 'Django REST Framework'


# class DataCleanupConfig(AppConfig):
#     """Details for Data Cleanup integration."""
#     name = 'data_cleanup'
#     verbose_name = 'Data Cleanup'


# class RestFrameworkSimpleJwtConfig(AppConfig):
#     """Details for Django REST Framework Simple JWT integration."""
#     name = 'rest_framework_simplejwt'
#     verbose_name = 'Django REST Framework Simple JWT'


# class DrfSpectacularConfig(AppConfig):
#     """Details for Django REST Framework Spectacular integration."""
#     name = 'drf_spectacular'
#     verbose_name = 'Django REST Framework Spectacular'


# class DrfSpectacularSidecarConfig(AppConfig):
#     """Details for Django REST Framework Spectacular Sidecar integration."""
#     name = 'drf_spectacular_sidecar'
#     verbose_name = 'Django REST Framework Spectacular Sidecar'