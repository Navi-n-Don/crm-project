import datetime
import os
from typing import Any, Dict, List
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from interactions.models import Like, Interaction


def update_to(instance: {}, filename: str) -> str:
    """Method for naming a user image"""
    path = "users"
    ext = filename.split('.')[-1]
    new_filename = f"{instance.pk}_{instance.username.lower()}.{ext}"
    return os.path.join(path, new_filename)


def valid_username(name: Any) -> Any:
    """Method for check valid username to sign up"""
    admin_list = ['anonymus', 'administrator']
    clear_name = ""
    for nm in str(name).strip('!#$%^&*-_?., `\'\"').lower():
        if nm.isalpha():
            clear_name += nm
    if clear_name not in admin_list:
        return name
    else:
        raise ValidationError(_(f'{name} is invalid name, please choose another name.'), )


def total(model: {}, kwargs: Any) -> Dict[Any, int]:
    """Method for getting the total number of likes per interaction"""
    total_action = {}
    total_likes = {}

    if not Like.objects.filter(action_id__project=model.get(slug=kwargs)):
        for like in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            total_action[like.id] = 0
    else:
        for action in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            total_action[action.id] = 0

        for like in Like.objects.filter(action_id__project=model.get(slug=kwargs)):
            if like.action_id in total_likes:
                if like.like_id == 1:
                    total_likes[like.action_id] += 1
                elif like.like_id == 2:
                    total_likes[like.action_id] += -1
            else:
                if like.like_id == 1:
                    total_likes[like.action_id] = 1
                elif like.like_id == 2:
                    total_likes[like.action_id] = -1

    for k, v in total_likes.items():
        if k in total_action:
            total_action[k] = v

    return total_action


def single(model: {}, kwargs: Any, user: {}) -> List[Dict[str, int]]:
    """Method for getting self likes per interaction"""
    all_likes = []
    self_likes = []

    if not Like.objects.filter(action_id__project_id=model.get(slug=kwargs).pk).filter(who_id=user.id):
        all_likes = []
        for like in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            all_likes.append({'like_id': 0, 'action_id': like.id})
    else:
        for action in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            all_likes.append({'like_id': 0, 'action_id': action.id})

        self_likes += list(Like.objects.filter(action_id__project_id=model.get(slug=kwargs).pk).filter(who_id=user.id))

        for item in self_likes:
            for like in all_likes:
                if item.action_id == like['action_id']:
                    like['like_id'] = item.like_id
                    like['action_id'] = item.action_id

    return all_likes


def filter_status(pole: Any, obj: Any) -> Any:
    """Method for getting status to filter list of interactions some project"""
    status = pole
    today = datetime.date.today()
    if status == 'left':
        return obj.filter(begin__gt=today)
    elif status == 'in_progress':
        return obj.filter(begin__lt=today, end__gt=today)
    elif status == 'completed':
        return obj.filter(end__lt=today)
    else:
        return obj
