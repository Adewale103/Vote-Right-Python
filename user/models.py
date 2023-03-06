from django.db import models


# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    BVN = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    profileImageUrl = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    hasVotedForPresident = models.BooleanField(default=False)
    hasVotedForGovernor = models.BooleanField(default=False)
    hasVotedForHouseOfRepMember = models.BooleanField(default=False)
    hasVotedForSenateMember = models.BooleanField(default=False)
    hasVotedForHouseOfAssemblyMember = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


PARTY_CHOICES = [
    ('PDP', 'PDP'),
    ('APC', 'APC'),
    ('LP', 'LP'),
    ('NNPP', 'NNPP'),
    ('ACN', 'ACN'),
    ('CPP', 'CPP'),
    ('CPC', 'CPC')
]

VOTE_CATEGORY_CHOICES = [
    ('President', 'President'),
    ('Governor', 'Governor'),
    ('House of Representatives', 'House of Representatives'),
    ('Senate', 'Senate'),
    ('House of Assembly', 'House of Assembly')
]


class Candidate(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=100)
    party = models.CharField(max_length=10, choices=PARTY_CHOICES)
    vote_category = models.CharField(max_length=100, choices=VOTE_CATEGORY_CHOICES)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name
