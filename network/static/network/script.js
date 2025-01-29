const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    load_likes();
    load_edit_buttons();

    // add eventlistiner to follow and unfollow botton
    const follow_btn = document.querySelector('#follow-btn');
    const unfollow_btn = document.querySelector('#unfollow-btn');

    if (follow_btn) {
        follow_btn.addEventListener('click', () => toggleFollowUnfollow(follow_btn));
    }
    else if(unfollow_btn) {
        unfollow_btn.addEventListener('click', () => toggleFollowUnfollow(unfollow_btn));
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function change_like_ui(is_liked, like_svg) {
    if (is_liked) {
        like_svg.style.fill = '#f00';
        like_svg.style.stroke = '#f00';
    } else {
        like_svg.style.fill = 'none';
        like_svg.style.stroke = '#000';
    }
}

function load_likes() {
    /* update no. of likes and likes SVGs of every posts */
    const likes_container = document.querySelectorAll('.likes-container');
    likes_container.forEach(like_content => {
        let like = like_content.querySelector('.likes');
        let id = like.dataset.postid;
        fetch(`/api/like/${id}`)
        .then(response => response.json())
        .then(obj => {
            like.innerHTML = obj.likes_count;

            // change like svg to red if user has already liked the post
            svg_like = like_content.querySelector('svg');
            change_like_ui(obj.is_liked, svg_like);

            // add click eventlistiner to like-content element
            like_content.addEventListener('click', () => toggle_like(id));
        })
    })
}

function toggle_like(post_id) {
    // find like container with dataset postid equals to post_id
    let like_container;
    document.querySelectorAll('.likes-container')
    .forEach(container => {
        if (container.dataset.postid === post_id) {
            like_container = container;
        }
    })
    let like_svg = like_container.querySelector('svg');

    /* Change UI of like SVG and update no. of likes */
    fetch(`/api/like/${post_id}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    }).then(response => response.json())
    .then(result => {
        let is_liked = result['is_liked'];
        change_like_ui(is_liked, like_svg);
        let likes = like_container.querySelector('.likes');
        likes.innerText = result['likes_count'];
    })
}

function toggleFollowUnfollow(btn) {
    let user_id = btn.dataset.user_id;
    fetch(`/api/follow/${user_id}`)
    .then(response => response.json())
    .then(data => {
        const followers = document.getElementById('followers');
        followers.innerText = data['followers_count'];

        if (btn.id === 'follow-btn') {
            btn.id = 'unfollow-btn';
            btn.innerText = 'Unfollow';
        }
        else {
            btn.id = 'follow-btn';
            btn.innerText = 'Follow';
        }

    })
}


function load_edit_buttons() {
    /* Add edit button to only current user post */
    const edit_buttons = document.querySelectorAll('.edit-btns');
    // Check if the post is own by the current user
    // if its user's post then add edit button
    edit_buttons.forEach(btn => {
        let post_id = btn.dataset.postid;
        fetch(`/api/isuserpost/${post_id}`)
        .then(response => response.json())
        .then(result => {
            let isUserPost = result["isUserPost"];
            if (isUserPost) {
                let button = document.createElement('button');
                button.className = 'btn btn-outline-secondary px-3';
                button.innerText = 'Edit';
                btn.append(button);

                // Add click event listiner to each Edit button
                button.addEventListener('click', () => edit_post_ui(post_id));
            }
        })
    })
}

function edit_post_ui(post_id) {
    /* 
    -> Change post content to editable text area
    -> add save button
    -> add click eventlistiner to save button 
    */
    document.querySelectorAll('.posts')
    .forEach(post => {
        let content_div = post.querySelector('.post-content');
        if (post.dataset.postid === post_id) {
            let content = content_div.innerText;

            // textarea
            let textarea = document.createElement('textarea')
            textarea.className = 'form-control post-textarea';
            textarea.innerText = content;

            // save button
            let save_btn = document.createElement('button');
            save_btn.className = 'btn btn-primary save-btn';
            save_btn.innerText = 'Save';

            content_div.innerHTML = '';
            content_div.appendChild(textarea);
            content_div.appendChild(save_btn);

            // add eventlistener to save button
            save_btn.addEventListener('click', () => edit_post(post_id));
        }
    })
}

function edit_post(post_id) {
    /* Called When save button is clicked while editing
        -> Get textarea text and send to backend
        -> fetch the result
        -> Change textarea back to normal post content view
    */
    let content_div;
    document.querySelectorAll('.posts')
    .forEach(post => {
        if (post.dataset.postid === post_id) {
            content_div = post.querySelector('.post-content');
        }
    })

    const text_div = content_div.querySelector('.post-textarea');
    
    fetch(`http://127.0.0.1:8000/api/post/${post_id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            content: text_div.value
        })
    })
    .then(() => {
        fetch(`http://127.0.0.1:8000/api/post/${post_id}`, {
            method: 'GET',
            headers: {'X-CSRFToken': csrftoken}
        })
        .then(response => response.json())
        .then(result => {
            let content = result['content'];
            content_div.innerHTML = content;
        });
    })

}
