from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface.declarations import provider

from . import messageFactory as _


@provider(IFormFieldProvider)
class IRelatedImages(form.Schema):

    related_images = RelationList(
        title=_(u'Related Images'),
        default=[],
        value_type=RelationChoice(
            title=_(u"Pictures"),
            source=CatalogSource(portal_type='Image'),
        ),
        required=False,
    )
