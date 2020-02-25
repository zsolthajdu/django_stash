from rest_framework import serializers
from datetime import datetime

from .models import Bookmark, Tag
import json 

class TagSerializer( serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ( 'id', 'name' )

    def create( self, validated_data):
        tag = Tag.objects.create( **validated_data )
        print( "TagSerializer create: " + tag.name )
        tag.slug = tag.name   # For now same as name
        return tag

class BookmarkSerializer( serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = TagSerializer( many = True )



    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bookmark
        fields = ('id', 'title', 'owner', 'created', 'description', 'url', 'public', 'tags' )

    def create(self, validated_data):
        request = self.context['request']
        # Create tags ourselves
        inTags = validated_data.pop('tags')
        bookmark = Bookmark.objects.create( **validated_data, owner = request.user )
        # Use incoming creation date, in case it comes from a backup or whatnot
        if 'created' in validated_data:
            bookmark.created = validated_data['created']


        for tag in inTags:
            existing = Tag.objects.filter( name = tag['name'] )
            if existing.count() == 0:
                t = Tag.objects.create( **tag ) #name = tag )
                t.save()
                bookmark.tags.add(t)
            else:
                # Get list of current tags, check if 'tag' is among them
                if existing.count() > 1:
                    print( "MORE THAN ONE INSTANCE of tag : " + str(existing[0] ) )
                bookmark.tags.add( existing[0] )

        bookmark.save()
        return bookmark

    # Update function to handle PUT
    def update(self, instance, validated_data):
        inTags = validated_data.pop('tags')
        instance.title = validated_data.get( 'title', instance.title )
        instance.description = validated_data.get( 'description', instance.description )
        instance.created = validated_data.get('created', instance.created )
        instance.public = validated_data.get( 'public', instance.public )

        #print( "Existing = " + str(instance.id ))
        #print( "UPDATE : current tags = " + str( currentTags ) )
        for tag in inTags:
            existing = Tag.objects.filter( name = tag['name'] )
            if existing.count() == 0:
                existing = Tag.objects.create( **tag ) #name = tag )
                existing.save()
                instance.tags.add( existing )
            else:
                # Get list of current tags, check if 'tag' is among them
                if existing.count() > 1:
                    print( "MORE THAN ONE INSTANCE of tag : " + str(existing[0] ) )

                if Tag.objects.filter( bookmark__id = instance.id ).filter( name = tag['name'] ).count() == 0:
                    instance.tags.add( existing[0] )

        instance.save()
        return instance
