function PostCard({post}){
    return (
        <div>
            <div>
                <span>Tweet: {post.tweet}</span>
            </div>
            <div>
                <h1>Blog Post</h1>
                {post.blog_post}
            </div>
            <div>
                <span>Title: {post.reddit_post.title}</span>
                {post.reddit_post.body}
            </div>
        </div> 
    );
}

export default PostCard;   