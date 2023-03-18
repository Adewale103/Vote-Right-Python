from django.urls import path
from .views import create_account,login,castVoteForCandidate,view_house_of_assembly_result_in_percentage,\
    view_senatorial_result_in_percentage,view_presidential_result_in_percentage,view_governorship_result_in_percentage, \
    view_house_of_rep_result_in_percentage

urlpatterns = [
    path('create-account/', create_account, name='create_account'),
    path('login/', login, name='login'),
    path('castvote/', castVoteForCandidate, name='cast_vote'),
    path('viewresult/presidency', view_presidential_result_in_percentage, name='view_presidency_result'),
    path('viewresult/governorship', view_governorship_result_in_percentage, name='view_governorship_result'),
    path('viewresult/senate', view_senatorial_result_in_percentage, name='view_senatorial_result'),
    path('viewresult/house_of_rep', view_house_of_rep_result_in_percentage, name='view_house_of_rep_result'),
    path('viewresult/house_of_assembly', view_house_of_assembly_result_in_percentage, name='view_house_of_assem_result')
]
