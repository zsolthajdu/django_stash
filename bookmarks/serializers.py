from rest_framework import serializers
from tagging.models import Tag

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.ListField(child=serializers.CharField(max_length=256))

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bookmark
        fields = ('id', 'title', 'owner', 'created', 'description', 'url','tags' )


    def create(self, validated_data):
        request = self.context['request']
        bookmark = Bookmark(
            title=validated_data['title'],
            description=validated_data['description'],
            url=validated_data['url'],
            owner = request.user
        )

        # TODO: Check if bookmark already in database
        bookmark.save()

        # Update 'tags' field in new bookmark record
        Tag.objects.update_tags(bookmark, validated_data['tags'][0] )
        return bookmark
