from rest_framework import serializers
from tagging.models import Tag
from datetime import datetime

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.ListField(child=serializers.CharField(max_length=256))

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bookmark
        fields = ('id', 'title', 'owner', 'created', 'description', 'url', 'public', 'tags' )


    def create(self, validated_data):
        request = self.context['request']
        bookmark = Bookmark(title=validated_data['title'],description=validated_data['description'],
                        public=validated_data['public'], url=validated_data['url'], owner = request.user )
        bookmark.owner = request.user
        # Use incoming creation date, in case it comes from a backup or whatnot
        if 'created' in validated_data:
            bookmark.created = validated_data['created']
        bookmark.save()

        # Update 'tags' field in new bookmark record
        Tag.objects.update_tags(bookmark, validated_data['tags'][0] )
        return bookmark

    # Update function to handle PUT
    def update(self, instance, validated_data):
        instance.title = validated_data.get( 'title', instance.title )
        instance.description = validated_data.get( 'description', instance.description )
        instance.created = validated_data.get('created', instance.created )
        instance.public = validated_data.get( 'public', instance.public )
        instance.save()
        Tag.objects.update_tags( instance, validated_data['tags'][0] )
        return instance
        
