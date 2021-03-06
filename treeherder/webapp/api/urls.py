import copy

from django.conf.urls import (include,
                              url)
from rest_framework import routers

from treeherder.webapp.api import (artifact,
                                   auth,
                                   bug,
                                   bugzilla,
                                   classifiedfailure,
                                   failureline,
                                   job_log_url,
                                   jobs,
                                   note,
                                   performance_data,
                                   refdata,
                                   resultset,
                                   runnable_jobs,
                                   seta,
                                   text_log_error,
                                   text_log_summary,
                                   text_log_summary_line)

# router for views that are bound to a project
# i.e. all those views that don't involve reference data
project_bound_router = routers.SimpleRouter()

project_bound_router.register(
    r'jobs',
    jobs.JobsViewSet,
    base_name='jobs',
)

project_bound_router.register(
    r'runnable_jobs',
    runnable_jobs.RunnableJobsViewSet,
    base_name='runnable_jobs',
)

project_bound_router.register(
    r'seta/job-priorities',
    seta.SetaJobPriorityViewSet,
    base_name='seta-job-priorities'
)

project_bound_router.register(
    r'seta/job-types',
    seta.SetaJobTypes,
    base_name='seta-job-types'
)

project_bound_router.register(
    r'resultset',
    resultset.ResultSetViewSet,
    base_name='resultset',
)

project_bound_router.register(
    r'artifact',
    artifact.ArtifactViewSet,
    base_name='artifact',
)

project_bound_router.register(
    r'note',
    note.NoteViewSet,
    base_name='note',
)

project_bound_router.register(
    r'bug-job-map',
    bug.BugJobMapViewSet,
    base_name='bug-job-map',
)

project_bound_router.register(
    r'job-log-url',
    job_log_url.JobLogUrlViewSet,
    base_name='job-log-url',
)

project_bound_router.register(
    r'performance/data',
    performance_data.PerformanceDatumViewSet,
    base_name='performance-data')

project_bound_router.register(
    r'performance/signatures',
    performance_data.PerformanceSignatureViewSet,
    base_name='performance-signatures')

project_bound_router.register(
    r'performance/platforms',
    performance_data.PerformancePlatformViewSet,
    base_name='performance-signatures-platforms')


# this is the default router for plain restful endpoints
class ExtendedRouter(routers.DefaultRouter):
    routes = copy.deepcopy(routers.DefaultRouter.routes)
    routes[0].mapping[u"put"] = u"update_many"


# refdata endpoints:
default_router = ExtendedRouter()
default_router.register(r'product', refdata.ProductViewSet)
default_router.register(r'machine', refdata.MachineViewSet)
default_router.register(r'machineplatform', refdata.MachinePlatformViewSet)
default_router.register(r'buildplatform', refdata.BuildPlatformViewSet)
default_router.register(r'jobgroup', refdata.JobGroupViewSet)
default_router.register(r'jobtype', refdata.JobTypeViewSet)
default_router.register(r'repository', refdata.RepositoryViewSet)
default_router.register(r'optioncollectionhash', refdata.OptionCollectionHashViewSet,
                        base_name='optioncollectionhash')
default_router.register(r'failureclassification', refdata.FailureClassificationViewSet)
default_router.register(r'user', refdata.UserViewSet, base_name='user')
default_router.register(r'exclusion-profile', refdata.ExclusionProfileViewSet)
default_router.register(r'job-exclusion', refdata.JobExclusionViewSet)
default_router.register(r'matcher', refdata.MatcherViewSet)
default_router.register(r'failure-line', failureline.FailureLineViewSet,
                        base_name='failure-line')
default_router.register(r'classified-failure',
                        classifiedfailure.ClassifiedFailureViewSet,
                        base_name='classified-failure')
default_router.register(r'text-log-error',
                        text_log_error.TextLogErrorViewSet,
                        base_name='text-log-error')
default_router.register(r'text-log-summary',
                        text_log_summary.TextLogSummaryViewSet,
                        base_name='text-log-summary')
default_router.register(r'text-log-summary-line',
                        text_log_summary_line.TextLogSummaryLineViewSet,
                        base_name='text-log-summary-line')
default_router.register(r'performance/alertsummary',
                        performance_data.PerformanceAlertSummaryViewSet,
                        base_name='performance-alert-summaries')
default_router.register(r'performance/alert',
                        performance_data.PerformanceAlertViewSet,
                        base_name='performance-alerts')
default_router.register(r'performance/framework',
                        performance_data.PerformanceFrameworkViewSet,
                        base_name='performance-frameworks')
default_router.register(r'performance/bug-template',
                        performance_data.PerformanceBugTemplateViewSet,
                        base_name='performance-bug-template')
default_router.register(r'bugzilla', bugzilla.BugzillaViewSet,
                        base_name='bugzilla')
default_router.register(r'jobdetail', jobs.JobDetailViewSet,
                        base_name='jobdetail')
default_router.register(r'auth', auth.TaskclusterAuthViewSet,
                        base_name='auth')
default_router.register(r'seta/failures-fixed-by-commit',
                        seta.SetaFailuresFixedByCommit,
                        base_name='seta_failures_fixed_by_commit')

urlpatterns = [
    url(r'^project/(?P<project>[\w-]{0,50})/',
        include(project_bound_router.urls)),
    url(r'^',
        include(default_router.urls)),
]
