from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Candidate
from .utils import validate_bvn, generate_username
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        data = request.POST
        bvn = data.get('BVN')
        password = data.get('password')
        hashed_password = make_password(password)

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
            username=generate_username(validate_bvn_response['data']['first_name'],
                                       validate_bvn_response['data']['last_name']),
            address=validate_bvn_response['data']['address'],
            email=validate_bvn_response['data']['email'],
            phoneNumber=validate_bvn_response['data']['phone_number'],
            gender=validate_bvn_response['data']['gender'],
            password=data.get(hashed_password),
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


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = request.POST
        bvn = data.get('bvn')
        password = data.get('password')
        user = validateUserCredentials(bvn, password)
        if user != null:
            return JsonResponse({'message': 'You have successfully logged in! '})


def validateUserCredentials(bvn, password):
    try:
        user = User.objects.get(BVN=bvn)
        if user.BVN != bvn:
            raise ValueError('Incorrect bvn or password')
        if check_password(password, user.password):
            return user
        else:
            raise ValueError('Incorrect bvn or password')
    except User.DoesNotExist:
        raise ValueError('Incorrect bvn or password')


@csrf_exempt
def castVoteForCandidate(request):
    if request.method == 'POST':
        data = request.POST
        party = data.get('party')
        bvn = data.get('bvn')
        voteCategory = data.get('voteCategory')
        password = data.get('password')
        user = validateUserCredentials(bvn, password)
        if user.hasVotedForPresident:
            raise ValueError('You have already voted for the candidate of your choice')
        if not vote_category_is_valid(voteCategory):
            raise ValueError('Incorrect vote category, please check again..')
        if not party_is_valid(party):
            raise ValueError("Incorrect party, please check again")
        try:
            candidate = Candidate.objects.get(party=party, vote_category=voteCategory)
            candidate.vote_count = candidate.vote_count + 1
            user.hasVotedForPresident = True
            candidate.save()
            user.save()
            return JsonResponse({'message': 'You have successfully voted! '})
        except Candidate.DoesNotExist:
            raise ValueError('Candidate does not exist')


def party_is_valid(party_choice):
    choices = [choice[0] for choice in Candidate.PARTY_CHOICES]
    if party_choice in choices:
        return True
    else:
        return False


def vote_category_is_valid(vote_category):
    vote_categories = [result[0] for result in Candidate.VOTE_CATEGORY_CHOICES]
    if vote_category in vote_categories:
        return True
    else:
        return False


@csrf_exempt
def view_presidential_result_in_percentage(request):
    if request.method == 'GET':
        view_result('President')


@csrf_exempt
def view_governorship_result_in_percentage(request):
    if request.method == 'GET':
        view_result('Governor')


@csrf_exempt
def view_senatorial_result_in_percentage(request):
    if request.method == 'GET':
        view_result('Senate')


@csrf_exempt
def view_house_of_rep_result_in_percentage(request):
    if request.method == 'GET':
        view_result('House of Representative')


@csrf_exempt
def view_house_of_assembly_result_in_percentage(request):
    if request.method == 'GET':
        view_result('House of Assembly')


def view_result(vote_category):
    presidential_candidates = Candidate.objects.filter(vote_category=vote_category)

    total_votes = sum(candidate.vote_count for candidate in presidential_candidates)

    result = {}
    for candidate in presidential_candidates:
        result[candidate.party] = f"{(candidate.vote_count / total_votes) * 100:.2f}%"
    data = {'result': result}
    return JsonResponse(data)
