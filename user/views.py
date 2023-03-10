from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .utils import validate_bvn, generate_username


@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        data = request.POST
        bvn = data.get('BVN')

        if User.objects.filter(BVN=bvn).exists():
            return JsonResponse({'message': 'User with provided BVN has already registered'}, status=400)

        validate_bvn_response = validate_bvn(bvn)
        if validate_bvn_response['status'] != 'success':
            return JsonResponse({'message': validate_bvn_response['message']}, status=400)

        user = User(
            first_name=validate_bvn_response['data']['first_name'],
            middle_name=validate_bvn_response['data']['middle_name'],
            last_name=validate_bvn_response['data']['last_name'],
            date_of_birth=validate_bvn_response['data']['date_of_birth'],
            BVN=bvn,
            username=generate_username(validate_bvn_response['data']['first_name'], validate_bvn_response['data']['last_name']),
            address=validate_bvn_response['data']['address'],
            email=validate_bvn_response['data']['email'],
            phoneNumber=validate_bvn_response['data']['phone_number'],
            gender=validate_bvn_response['data']['gender'],
            password=data.get('password'),
            nationality=validate_bvn_response['data']['nationality'],
            profileImageUrl=data.get('profileImageUrl'),
            hasVotedForPresident=False,
            hasVotedForGovernor=False,
            hasVotedForHouseOfRepMember=False,
            hasVotedForSenateMember=False,
            hasVotedForHouseOfAssemblyMember=False,
        )
        user.save()

        return JsonResponse({'message': 'User profile successfully created'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)
