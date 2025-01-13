from app.models import Discussion, User, Post
import json


class NPC:
    def __init__(self, member: User, discussion: Discussion):
        self.member_id = member.id
        self.about = json.loads(member.about_me)
        self.viewpoint = self._form_viewpoint(discussion.posts)
        self.arguments = self._prepare_arguments()

    def _form_viewpoint(self, posts):
        # Generate a viewpoint about the discussion topic
        return "placeholder"

    def _prepare_arguments(self):
        # As described by Mathijs: generate a number of arguments, then randomly discard some of them
        return ['placeholder', 'placeholder']
