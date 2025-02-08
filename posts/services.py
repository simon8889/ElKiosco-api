from django.http import Http404
from django.shortcuts import get_object_or_404
from .serializer import VotesSerializer
from .models import Vote

def vote_entity(user, entity, entity_id, request_data):
	entity_instance = get_object_or_404(entity, id=entity_id)
	vote_exists = Vote.objects.filter(voter=user, **{entity._meta.model_name: entity_instance}).exists()
	if vote_exists:
		return None, "Vote already exists"
	
	serializer = VotesSerializer(data=request_data)
	if not serializer.is_valid():
		return None, serializer.errors
		
	serializer.save(voter=user, **{entity._meta.model_name: entity_instance})
	return entity_instance, None

def remove_vote_entity(user, entity, entity_id):
	entity_instance = get_object_or_404(entity, id=entity_id)
	vote = get_object_or_404(Vote, voter=user, **{entity._meta.model_name: entity_instance})
	vote.delete()
	return True

def change_vote_type_entity(user, entity, entity_id):
	try: 
		entity_instance = get_object_or_404(entity, id=entity_id)
		vote = get_object_or_404(Vote, voter=user, **{entity._meta.model_name: entity_instance})
		vote.vote_type = "DOWN" if vote.vote_type == "UP" else "UP"
		vote.save()
		return entity_instance, None
	except Http404:
		return None, "Vote not found"