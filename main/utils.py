import os
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from interactions.models import Like, Interaction


def update_to(instance, filename):
    path = "users"
    ext = filename.split('.')[-1]
    new_filename = f"{instance.pk}_{instance.username.lower()}.{ext}"
    return os.path.join(path, new_filename)


def valid_username(name):
    admin_list = ['anonymus', 'administrator']
    clear_name = ""
    for nm in str(name).strip('!#$%^&*-_?., `\'\"').lower():
        if nm.isalpha():
            clear_name += nm
    if clear_name not in admin_list:
        return name
    else:
        raise ValidationError(_(f'{name} is invalid name, please choose another name.'), )


def total(model, kwargs):
    total_action = {}
    total_likes = {}

    if not Like.objects.filter(action_id__project_id=model.get(slug=kwargs).pk):
        for like in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            total_action[like.id] = 0
    else:
        for action in Interaction.objects.filter(project_id=model.get(slug=kwargs).pk):
            total_action[action.id] = 0

        for like in Like.objects.filter(action_id__project_id=model.get(slug=kwargs).pk):
            total_likes[like.action_id] = 0
            if like.like_id == 1:
                total_likes[like.action_id] += 1
            elif like.like_id == 2:
                total_likes[like.action_id] += -1
    for k, v in total_likes.items():
        if k in total_action:
            total_action[k] = v

    return total_action


def single(model, kwargs, user):
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
