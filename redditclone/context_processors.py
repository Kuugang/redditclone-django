from community.models import Community
from post.models import Comment, Vote
from post.models import Post

def context(request):
    query = """
        SELECT c.*, cm.role
        FROM community_community c
        LEFT JOIN community_communitymember cm ON cm.community_id = c.id
        WHERE cm.user_id = %s
        ORDER BY c.name;
    """
     
    user_communities = Community.objects.raw(query, [request.user.id])
    user_posts = Post.objects.filter(user=request.user.id).order_by('created_at')

    user_comments = Comment.objects.filter(user=request.user.id)
    user_upvotes = Vote.objects.filter(user=request.user.id, vote="upvote")
    user_downvotes = Vote.objects.filter(user=request.user.id, vote="downvote")

    user_commented_posts = sorted(set(comment.post for comment in user_comments), key=lambda x: x.created_at, reverse=True)
    user_upvoted_posts = sorted(set(vote.post for vote in user_upvotes), key=lambda x: x.created_at, reverse=True)
    user_downvoted_posts = sorted(set(vote.post for vote in user_downvotes), key=lambda x: x.created_at, reverse=True)


    user_overview = sorted(
        list(user_posts) + list(user_commented_posts),
        key=lambda x: x.created_at,
        reverse=True
    )

    return {
        'user_posts' : user_posts,
        'user_overview' : user_overview,
        'user_communities': user_communities,
        'user_comments' : user_comments,
        'user_upvotes' : user_upvotes,
        'user_downvotes' : user_downvotes,

        'user_commented_posts' : user_commented_posts,
        'user_upvoted_posts': user_upvoted_posts,
        'user_downvoted_posts' : user_downvoted_posts
    }