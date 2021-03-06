# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia.utils import get_media_root
from plone import api
from plone.dexterity.utils import createContentInContainer
from z3c.relationfield import create_relation
from z3c.relationfield.event import _setRelation


def create_media_base_path(obj, event):
    """ automatically create related base path
    """

    if obj.related_media_base_path or getattr(obj.REQUEST, 'translation_info', {}):  # noqa
        # if we already have a value or we create a translation just return
        return

    media_root = get_media_root(obj)

    if media_root is None:
        # do nothing ... no media root path is defined
        return

    # we use UID for media container id to avoid duplicate ids in media root
    media_base_id = obj.UID()

    if media_base_id not in media_root:
        # create base path
        media_base = createContentInContainer(
            media_root,
            'Folder',
            id=media_base_id,
            title=obj.Title(),
        )
    else:
        # XXX: this should never happen?
        media_base = media_root[media_base_id]

    _rel = create_relation('/'.join(media_base.getPhysicalPath()))
    # fix RelationValue properties
    _setRelation(obj, 'related_media_base_path', _rel)
    obj.related_media_base_path = _rel


def sync_workflow_state(obj, event):
    """ keep workflow of base path in sync
    """

    if not obj.related_media_base_path:
        return

    try:
        api.content.transition(
            obj=obj.related_media_base_path,
            transition=event.status['action'],
        )
    except api.exc.InvalidParameterError:
        # possibly unsynced state ...
        pass
