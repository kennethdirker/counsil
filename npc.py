from app.models import Discussion, User, Post
import json
from backend.agent_client import AgentClient


class NPC:
    def __init__(
            self, 
            member: User, 
            discussion: Discussion, 
            client: AgentClient,
            verbose = False
        ):
        self.member_id = member.id
        self.about = json.loads(member.about_me)
        self.personality = self._assemble_personality()
        self.proposal = discussion.get_subject()    # Includes setting
        self.client = client
        self.viewpoint = self._form_viewpoint()
        if verbose:
            with open("backend_loop.log", "a") as myfile:
                myfile.write(f"Initial post body from {self.about['name']}:\n{self.viewpoint}")


    def reconsider_viewpoint(self, posts: list[str]):
        """
        Adjust current viewpoint according to new information and NPC personality.
        """
        external = " ".join(posts)
        summary = self.client.summarize(external)
        self.viewpoint = self.client.adjust_opinion(
            self.proposal,
            self.personality,
            self.viewpoint,
            summary
        )
        return self.viewpoint
    
    def vote(self) -> bool:
        """
        Accept or reject the proposal. Return True if the proposal is accepted
        or False otherwise.
        """
        return self.client.vote(
            self.proposal,
            self.viewpoint,
            self.personality
        )


    def _assemble_personality(self):
        info = self.about
        personality = f"""
You are roleplaying as a city counselor and will answer questions like a city counselor would. \
Answer all questions considering the following personality: \
Your name is {info["name"]}, aged 47 years old. You are a member of the city council \
and are currently in a meeting to discuss a proposal about the city. \
You live in the {info["lives in"]}. Your main mode of transport is \
{info["main mode of transport"]} and your preferred mode of transport is \
{info["preferred mode of transport"]}. You have \
{"" if info["has kids"] else "no "}kids. Regarding city legislation, you \
think that {info["main concern"]} is a very important subject, which you \
are passionate about. Other legaslation issues that you think are \
important to have in your city are: {", ".join(info["important issues"])}. \
Issues that you are totally against are: {", ".join(info["is against"])}.
        """ # ugly template
        return personality


    def _form_viewpoint(self):
        """
        Generate a initial viewpoint about the discussion topic        
        """
        self.viewpoint = self.client.form_opinion(self.proposal, self.personality)
        return self.viewpoint