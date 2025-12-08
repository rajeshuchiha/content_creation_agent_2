import DOMPurify from 'dompurify';

function PostCard({post}){
    
    const htmlString = post.blog_post;
    const sanitized = DOMPurify.sanitize(htmlString);

    return (
        <div>
            <div>
                <span>Tweet: {post.tweet}</span>
            </div>
            <div>
                <h1>Blog Post</h1>
                <div 
                    className="content-wrapper"
                    dangerouslySetInnerHTML={{ __html: sanitized }}
                />
            </div>
            <div>
                <span>Title: {post.reddit_post.title}</span>
                {post.reddit_post.body}
            </div>
        </div> 
    );
}

export default PostCard;   