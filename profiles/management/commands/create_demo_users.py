from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import Profile
from interactions.models import Post, Like, Comment

class Command(BaseCommand):
    help = 'Creates 100 users with profiles and interacts with "sudo" user'
    
    def handle(self, *args, **kwargs):
        sudo_user = User.objects.get(username='sudo')

        for i in range(1, 50001):  
            username = f"user_{i}"
            email = f"user{i}@example.com"
            password = f"user_{i}_password"
            user = User.objects.create_user(username=username, email=email, password=password)

            profile = Profile.objects.create(
                user=user,
                first_name=f"First_{i}",
                last_name=f"Last_{i}",
            )
            profile.follows.add(sudo_user.profile)
            profile.save()

            self.stdout.write(self.style.SUCCESS(f"Created user and profile: {username}"))

            sudo_posts = Post.objects.filter(author=sudo_user)
            for post in sudo_posts:
                Like.objects.create(post=post, user=user)
                self.stdout.write(self.style.SUCCESS(f"User {username} liked post by 'sudo'"))

            if i % 25 == 0:
                for post in sudo_posts:
                    Comment.objects.create(post=post, author=user, text=f"Comment by {user.username} on post by {post.author.username}")
                    self.stdout.write(self.style.SUCCESS(f"User {username} added a comment on post by 'sudo'"))

        self.stdout.write(self.style.SUCCESS(f"All users and profiles now follow 'sudo', liked 'sudo' posts, and added comments"))
