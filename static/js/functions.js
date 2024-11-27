function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
        (
            +c ^
            (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+c / 4)))
        ).toString(16),
    );
}
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return emailPattern.test(email);
}

function setupRemoveFilePreview(
    button,
    previewElement,
    previewContainer,
    fileInput,
    fileInputContainer,
) {
    button.addEventListener("click", () => {
        if (previewContainer) {
            previewContainer.classList.add("hidden");
        }
        if (fileInputContainer) {
            fileInputContainer.classList.remove("hidden");
        }
        if (previewElement) {
            previewElement.src = "";
        }
        fileInput.value = "";
    });
}

function setupFileInput(
    previewElement,
    previewContainer,
    fileInput,
    fileInputContainer,
) {
    fileInput.addEventListener("change", function (event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                previewElement.src = e.target.result;
                fileInputContainer.classList.add("hidden");
                previewContainer.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });
}

function showTab(
    n,
    class_name,
    prev_button_id,
    next_button_id,
    step_class_name,
) {
    var x = document.getElementsByClassName(class_name);
    x[n].classList.remove("hidden");

    const prevBtn = document.getElementById(prev_button_id);
    const nextBtn = document.getElementById(next_button_id);

    if (n == 0) {
        prevBtn.classList.add("hidden");
    } else {
        prevBtn.classList.remove("hidden");
    }

    if (n == x.length - 1) {
        nextBtn.innerHTML = "Submit";
    } else {
        nextBtn.innerHTML = "Next";
    }
    if (step_class_name != null) {
        fixStepIndicator(n, step_class_name);
    }
}

// OPTIONAL
function fixStepIndicator(n, step_class_name) {
    var i,
        x = document.getElementsByClassName(step_class_name);
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}

async function validate_form(
    tab_class_name,
    form_specific_validation_function,
    current_tab,
    step_class_name,
) {
    var x,
        y,
        i,
        valid = true;
    x = document.getElementsByClassName(tab_class_name);
    y = x[current_tab].getElementsByTagName("input");
    for (i = 0; i < y.length; i++) {
        current_valid = true;
        if (y[i].classList.contains("optional")) {
            continue;
        }
        if (y[i].value == "") {
            if(y[i].type == "file"){
                x[current_tab].querySelector(`[for="${y[i].id}"]`).querySelector("div").classList.add("ring-1", "ring-red-500", "ring-inset")
                x[current_tab].querySelector(`[for="${y[i].id}"]`).querySelector("div").classList.remove("border")
            }else{
                y[i].classList.add("ring-1", "ring-red-500", "ring-inset");
            }

            valid = false;
            current_valid = false;
        }

        if (form_specific_validation_function != null) {
            const result = await form_specific_validation_function(
                valid,
                current_valid,
                y,
                i,
            );
            valid = result[0];
            current_valid = result[1];
        }

        if (current_valid) {
            if(y[i].type == "file"){
                x[current_tab].querySelector(`[for="${y[i].id}"]`).querySelector("div").classList.remove("ring-1", "ring-red-500", "ring-inset");
                x[current_tab].querySelector(`[for="${y[i].id}"]`).querySelector("div").classList.add("border")
            }
            else
            y[i].classList.remove("ring-1", "ring-red-500", "ring-inset");
        }
    }

    if (valid && step_class_name != null) {
        document.getElementsByClassName(step_class_name)[
            current_tab
        ].className += " finish";
    }
    return valid;
}

async function nextPrev(
    n,
    form_specific_validation_function,
    tab_class_name,
    form_id,
    prev_button_id,
    next_button_id,
    step_class_name,
    current_tab,
) {
    var x = document.getElementsByClassName(tab_class_name);
    if (
        n == 1 &&
        !(await validate_form(
            tab_class_name,
            form_specific_validation_function,
            current_tab,
            step_class_name,
        ))
    )
        return current_tab;

    x[current_tab].classList.add("hidden");
    current_tab = current_tab + n;

    if (current_tab >= x.length) {
        x[x.length - 1].classList.remove("hidden");
        document.getElementById(form_id).submit();
        nextBtn.disabled = true;
        return false;
    }
    showTab(
        current_tab,
        tab_class_name,
        prev_button_id,
        next_button_id,
        step_class_name,
    );
    return current_tab;
}

function parseDateString(dateString) {
    const [month, day, year, time, period] = dateString.split(/[\s,]+/);
    const months = {
        "Jan.": 0,
        "Feb.": 1,
        "Mar.": 2,
        "Apr.": 3,
        "May": 4,
        "Jun.": 5,
        "Jul.": 6,
        "Aug.": 7,
        "Sept.": 8,
        "Oct.": 9,
        "Nov.": 10,
        "Dec.": 11,
    };
    const [hours, minutes] = time.split(":").map(Number);
    const adjustedHours =
        period === "p.m." && hours !== 12
            ? hours + 12
            : period === "a.m." && hours === 12
                ? 0
                : hours;

    const utcDate = new Date(
        Date.UTC(year, months[month], day, adjustedHours, minutes),
    );

    return utcDate;
}

function timeAgo(datetime) {
    const currentDate = new Date();
    const createdAt = new Date(parseDateString(datetime));
    const timeDifference = currentDate.getTime() - createdAt.getTime();

    const minute = 60 * 1000;
    const hour = minute * 60;
    const day = hour * 24;
    const month = day * 30;
    const year = day * 365;

    if (timeDifference < minute) {
        return "Just now";
    } else if (timeDifference < hour) {
        const minutes = Math.floor(timeDifference / minute);
        return `${minutes} min. ago`;
    } else if (timeDifference < day) {
        const hours = Math.floor(timeDifference / hour);
        return `${hours} hr. ago`;
    } else if (timeDifference < month) {
        const days = Math.floor(timeDifference / day);
        return `${days} day${days > 0 ? "s" : ""} ago`;
    } else if (timeDifference < year) {
        const months = Math.floor(timeDifference / month);
        return `${months} mon. ago`;
    } else {
        const years = Math.floor(timeDifference / year);
        return `${years} yr. ago`;
    }
}

function addRecentPost(post_id, post_title, post_content, community, communityAvatar, voteCount, commentCount) {
    let recent_posts = localStorage.getItem("recent_posts");
    if (recent_posts == null) {
        recent_posts = [];
    } else {
        recent_posts = JSON.parse(recent_posts);
    }
    voteCount = parseInt(voteCount);
    const postExists = recent_posts.some(post => post.post_id === post_id);
    if (!postExists) {
        let post = { post_id, post_title, post_content, community, communityAvatar, voteCount, commentCount };
        recent_posts.unshift(post);
        if (recent_posts.length > 10) {
            recent_posts.pop();
        }
        localStorage.setItem("recent_posts", JSON.stringify(recent_posts));
        addRecentPostItem(post);
    }
};

function addRecentPostItem(post) {
    const recentPostsContainer = document.getElementById("recent_posts");
    if(!recentPostsContainer)return;
    const recentPostItem = document.createElement("div");
    let postContent = post.post_content;
    const img = postContent.match(/<img[^>]*>/i);
    const imgMatch = postContent.match(/<img[^>]*>/i);
    let imgElement = null;
    if (imgMatch) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(imgMatch[0], "text/html");
        imgElement = doc.body.firstChild;
        imgElement.classList.add("w-20", "h-20", "rounded-md");
        imgElement.removeAttribute("style");
    }

    recentPostItem.setAttribute("id", `recent_post_${post.post_id}`);
    recentPostItem.classList.add("recent_post_item", "border-b", "border-gray-300", "py-2", "flex", "flex-col", "gap-2", "break-words", "text-wrap");
    recentPostItem.innerHTML = `
        <div>
            <a href = "/community/${post.community}" class='flex items-center gap-2 py-2 hover:underline'>
                ${post.communityAvatar ? `
                    <img src="${post.communityAvatar.startsWith('http') ? post.communityAvatar : '/media/' + post.communityAvatar}" class="w-6 h-6 rounded-full">` 
                    : '<svg class = "w-6 h-6 rounded-full border border-black" viewBox="0 0 61 61" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M30.8291 27.064C37.0423 27.064 42.0791 22.0272 42.0791 15.814C42.0791 9.60078 37.0423 4.56396 30.8291 4.56396C24.6159 4.56396 19.5791 9.60078 19.5791 15.814C19.5791 22.0272 24.6159 27.064 30.8291 27.064Z" fill="black"/><path d="M53.3291 45.814C53.3291 39.6006 48.2925 34.564 42.0791 34.564H19.5791C13.3659 34.564 8.3291 39.6006 8.3291 45.814V57.064H53.3291V45.814Z" fill="black"/></svg>'
                }
                <p class="font-semibold text-xs">r/${post.community}</p>
            </a>
        </div>
        <div class = "flex flex-row justify-between gap-2 text-wrap break-words h-full hover:cursor-pointer" onclick = "window.location.href = '/post/${post.post_id}'">
            <p class="font-bold text-base break-words text-wrap hover:underline">${post.post_title}</p>
            ${imgElement ? `${imgElement.outerHTML}` : ""}
        </div>
        <div>
            <p class="text-xs text-gray-700">${post.voteCount} ${post.voteCount < 0 ? 'downvotes' : 'upvotes'} • ${post.commentCount} comments</p>
        </div>
        `;
    recentPostItem.querySelectorAll("p")[1].classList.add("text-xs", "line-clamp-1");
    recentPostsContainer.prepend(recentPostItem);
}

function clearRecentPost() {
    localStorage.removeItem("recent_posts");
    const recentPostsContainer = document.getElementById("recent_posts");
    recentPostsContainer.innerHTML = "";
}

async function savePost(button, postId) {
    let data = new FormData();
    data.append("post_id", postId);
    await fetch(`/post/save/`, {
        method: "POST",
        body: data,
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
    }).then(async (response) => {
        button.dataset.saved = 1
        button.querySelector("p").textContent = "Unsave"

        button.querySelector("svg").children[0].setAttribute("d", "M15.372 1H4.628A1.629 1.629 0 0 0 3 2.628v16.256a1.113 1.113 0 0 0 1.709.941L10 16.479l5.282 3.34A1.12 1.12 0 0 0 17 18.873V2.628A1.63 1.63 0 0 0 15.372 1Z")
    });
}

async function unsavePost(button, postId) {
    let data = new FormData();
    data.append("post_id", postId);
    await fetch(`/post/unsave/`, {
        method: "POST",
        body: data,
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
    }).then(async (response) => {
        button.dataset.saved = 0
        button.querySelector("p").textContent = "Save"
        button.querySelector("svg").children[0].setAttribute("d", "M4.114 20A1.117 1.117 0 0 1 3 18.884V2.628A1.629 1.629 0 0 1 4.628 1h10.744A1.63 1.63 0 0 1 17 2.628v16.245a1.12 1.12 0 0 1-1.718.946L10 16.479l-5.291 3.346a1.11 1.11 0 0 1-.595.175Zm.514-17.75a.378.378 0 0 0-.378.378v16.009L10 15l5.75 3.636V2.628a.378.378 0 0 0-.378-.378H4.628Z")
    });
}

async function vote(buttonsContainer, type, contentId, vote) {
    let url = `/post/vote/${contentId}/${vote}/${type}/`;

    await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
    }).then(async (response) => {
        const data = await response.json();

        let vote_count = buttonsContainer.querySelector(".vote_count");
        let current_vote_count = parseInt(vote_count.textContent, 10);

        let voted = vote_count.dataset.voted
        let upvote = buttonsContainer.querySelectorAll("button")[0]
        let downvote = buttonsContainer.querySelectorAll("button")[1]

        if (voted == "upvote") {
            if (vote == "upvote") {
                current_vote_count -= 1
                vote_count.dataset.voted = ""
                buttonsContainer.classList.remove("bg-red-500")
                buttonsContainer.classList.add("dark:bg-dark_3")
                buttonsContainer.classList.remove("text-white")
                buttonsContainer.classList.add("text-black")
            } else {
                current_vote_count -= 2
                vote_count.dataset.voted = "downvote"
                buttonsContainer.classList.remove("bg-red-500")
                buttonsContainer.classList.add("bg-blue-500")
                downvote.querySelector("path").setAttribute("d", "M10 1c.072 0 .145 0 .218.006A4.1 4.1 0 0 1 14 5.184V9h3.138a1.751 1.751 0 0 1 1.234 2.993L10.59 19.72a.836.836 0 0 1-1.18 0l-7.782-7.727A1.751 1.751 0 0 1 2.861 9H6V5.118a4.134 4.134 0 0 1 .854-2.592A3.99 3.99 0 0 1 10 1Z")
            }
            upvote.querySelector("path").setAttribute("d", "M10 19c-.072 0-.145 0-.218-.006A4.1 4.1 0 0 1 6 14.816V11H2.862a1.751 1.751 0 0 1-1.234-2.993L9.41.28a.836.836 0 0 1 1.18 0l7.782 7.727A1.751 1.751 0 0 1 17.139 11H14v3.882a4.134 4.134 0 0 1-.854 2.592A3.99 3.99 0 0 1 10 19Zm0-17.193L2.685 9.071a.251.251 0 0 0 .177.429H7.5v5.316A2.63 2.63 0 0 0 9.864 17.5a2.441 2.441 0 0 0 1.856-.682A2.478 2.478 0 0 0 12.5 15V9.5h4.639a.25.25 0 0 0 .176-.429L10 1.807Z")
        } else if (voted == "downvote") {
            if (vote == "downvote") {
                current_vote_count += 1
                vote_count.dataset.voted = ""
                buttonsContainer.classList.remove("bg-blue-500")
                buttonsContainer.classList.add("dark:bg-dark_3")
                buttonsContainer.classList.remove("text-white")
                buttonsContainer.classList.add("text-black")
            } else {
                current_vote_count += 2
                vote_count.dataset.voted = "upvote"
                buttonsContainer.classList.remove("bg-blue-500")
                buttonsContainer.classList.add("bg-red-500")
                upvote.querySelector("path").setAttribute("d", "M10 19c-.072 0-.145 0-.218-.006A4.1 4.1 0 0 1 6 14.816V11H2.862a1.751 1.751 0 0 1-1.234-2.993L9.41.28a.836.836 0 0 1 1.18 0l7.782 7.727A1.751 1.751 0 0 1 17.139 11H14v3.882a4.134 4.134 0 0 1-.854 2.592A3.99 3.99 0 0 1 10 19Z")
            }
            downvote.querySelector("path").setAttribute("d", "M10 1c.072 0 .145 0 .218.006A4.1 4.1 0 0 1 14 5.184V9h3.138a1.751 1.751 0 0 1 1.234 2.993L10.59 19.72a.836.836 0 0 1-1.18 0l-7.782-7.727A1.751 1.751 0 0 1 2.861 9H6V5.118a4.134 4.134 0 0 1 .854-2.592A3.99 3.99 0 0 1 10 1Zm0 17.193 7.315-7.264a.251.251 0 0 0-.177-.429H12.5V5.184A2.631 2.631 0 0 0 10.136 2.5a2.441 2.441 0 0 0-1.856.682A2.478 2.478 0 0 0 7.5 5v5.5H2.861a.251.251 0 0 0-.176.429L10 18.193Z")
        } else {
            buttonsContainer.classList.remove("dark:bg-dark_3")
            buttonsContainer.classList.add("text-white")
            if (vote == "downvote") {
                current_vote_count -= 1
                vote_count.dataset.voted = "downvote"
                buttonsContainer.classList.add("bg-blue-500")
                downvote.querySelector("path").setAttribute("d", "M10 1c.072 0 .145 0 .218.006A4.1 4.1 0 0 1 14 5.184V9h3.138a1.751 1.751 0 0 1 1.234 2.993L10.59 19.72a.836.836 0 0 1-1.18 0l-7.782-7.727A1.751 1.751 0 0 1 2.861 9H6V5.118a4.134 4.134 0 0 1 .854-2.592A3.99 3.99 0 0 1 10 1Z")
            } else {
                current_vote_count += 1
                vote_count.dataset.voted = "upvote"
                buttonsContainer.classList.add("bg-red-500")
                upvote.querySelector("path").setAttribute("d", "M10 19c-.072 0-.145 0-.218-.006A4.1 4.1 0 0 1 6 14.816V11H2.862a1.751 1.751 0 0 1-1.234-2.993L9.41.28a.836.836 0 0 1 1.18 0l7.782 7.727A1.751 1.751 0 0 1 17.139 11H14v3.882a4.134 4.134 0 0 1-.854 2.592A3.99 3.99 0 0 1 10 19Z")
            }
        }
        vote_count.textContent = current_vote_count
    });
}

async function submitComment(postId, parentId = null, commentBox = null){
    if(commentBox == null){
        commentBox = document.getElementById("commentBox");
    }

    comment = commentBox.value;

    if(commentBox){
        commentBox.value = "";
    }

    let data = new FormData();
    data.append("comment", comment);
    if (parentId)
        data.append('parent_id', parentId);

    await fetch(`/post/comment/${postId}`, {
        method: "POST",
        body: data,
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
    }).then(async (response) => {
        const data = await response.json();
        if (response.status == 200) {
            document.querySelector("#comment_count").textContent = parseInt(document.querySelector("#comment_count").textContent) + 1
            let comment = document.createElement('div');
            comment.classList.add('pl-4', 'flex', 'flex-col', 'gap-4', 'border-l', "break-words", 'text-wrap');
            comment.setAttribute("id", 'comment-'+ data.id)
            
            let profilePicture = document.querySelector("#btn_drop_down_profile").querySelector("img").src;            
            let username = document.querySelector("#username").textContent.substring(2)

            comment.innerHTML = `
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-2 items-start relative">
                        <div class="w-[30px] h-[30px] rounded-full relative">
                            <img src="${profilePicture}" alt="profile picture" class="w-full h-full object-cover rounded-full">
                        </div>

                        <div class="flex flex-row gap-2 items-center">
                            <a href="/account/profile/${username}" 
                               class="font-semibold text-sm">
                                ${username}
                            </a>
                            <p class="text-xs text-gray-500">•</p>
                            <p class="text-xs text-gray-500" data-created-at="${data.created_at}">
                                ${timeAgo(data.created_at)} 
                            </p>
                        </div>
                    </div>

                    <p class="text-sm">${data.content}</p>

                    <div class="flex flex-row gap-4 mt-4">
                        <div class="flex flex-row gap-2 px-3 py-1 rounded-xl bg-button_gray">

                            <button 
                                onclick="
                                    event.stopPropagation(); 
                                    vote(this.parentElement, 'comment', '${data.id}', 'upvote')
                                ">

                                <svg rpl="" fill="currentColor" height="16" icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M10 19c-.072 0-.145 0-.218-.006A4.1 4.1 0 0 1 6 14.816V11H2.862a1.751 1.751 0 0 1-1.234-2.993L9.41.28a.836.836 0 0 1 1.18 0l7.782 7.727A1.751 1.751 0 0 1 17.139 11H14v3.882a4.134 4.134 0 0 1-.854 2.592A3.99 3.99 0 0 1 10 19Zm0-17.193L2.685 9.071a.251.251 0 0 0 .177.429H7.5v5.316A2.63 2.63 0 0 0 9.864 17.5a2.441 2.441 0 0 0 1.856-.682A2.478 2.478 0 0 0 12.5 15V9.5h4.639a.25.25 0 0 0 .176-.429L10 1.807Z"></path>
                                </svg>
                            </button>

                            <h1 class="vote_count">
                                0
                            </h1>

                            <button 
                                onclick="
                                    event.stopPropagation(); 
                                    vote(this.parentElement, 'comment', '${data.id}', 'downvote')
                                ">

                                <svg rpl="" fill="currentColor" height="16" icon-name="downvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M10 1c.072 0 .145 0 .218.006A4.1 4.1 0 0 1 14 5.184V9h3.138a1.751 1.751 0 0 1 1.234 2.993L10.59 19.72a.836.836 0 0 1-1.18 0l-7.782-7.727A1.751 1.751 0 0 1 2.861 9H6V5.118a4.134 4.134 0 0 1 .854-2.592A3.99 3.99 0 0 1 10 1Zm0 17.193 7.315-7.264a.251.251 0 0 0-.177-.429H12.5V5.184A2.631 2.631 0 0 0 10.136 2.5a2.441 2.441 0 0 0-1.856.682A2.478 2.478 0 0 0 7.5 5v5.5H2.861a.251.251 0 0 0-.176.429L10 18.193Z"></path>
                                </svg>
                            </button>
                        </div>

                        <button 
                            class="flex flex-row gap-2 items-center justify-center px-2 py-1 rounded-xl dark:bg-dark_3 border dark:border-white_3"
                            onclick="showCommentReplyBox(this.parentElement.parentElement, '${postId}', '${data.id}')">
                            <svg rpl="" aria-hidden="true" class="icon-comment" fill="currentColor" height="20" icon-name="comment-outline" viewBox="0 0 20 20" width="20" xmlns="http://www.w3.org/2000/svg">
                                <path d="M10 19H1.871a.886.886 0 0 1-.798-.52.886.886 0 0 1 .158-.941L3.1 15.771A9 9 0 1 1 10 19Zm-6.549-1.5H10a7.5 7.5 0 1 0-5.323-2.219l.54.545L3.451 17.5Z"></path>
                            </svg>
                            <h1 class="text-xs">Reply</h1>
                        </button>

                        <button id = "dropdownButton-${data.id}" onclick="event.stopPropagation()"
                            data-dropdown-toggle="dropdown-${data.id}"
                            class="">
                            <svg rpl="" fill="currentColor" height="16" icon-name="overflow-horizontal-fill" viewBox="0 0 20 20" width="16"
                                xmlns="http://www.w3.org/2000/svg">
                                <path d="M6 10a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z">
                                </path>
                            </svg>
                        </button>

                        <div id="dropdown-${data.id}"
                            class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700">
                            <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownButton-${data.id}">
                                <li>
                                    <button onclick="event.stopPropagation(); document.querySelector('#delete-comment-modal').querySelector('input[name=comment_id]').value = '${data.id}'"
                                        data-modal-target="delete-comment-modal" data-modal-toggle="delete-comment-modal"
                                        class="flex flex-row gap-2 px-4 py-2 w-full hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                        <svg rpl="" fill="currentColor" height="20" icon-name="delete-outline" viewBox="0 0 20 20" width="20"
                                            xmlns="http://www.w3.org/2000/svg">
                                            <path
                                                d="M15.751 6.023 17 6.106l-.761 11.368a2.554 2.554 0 0 1-.718 1.741A2.586 2.586 0 0 1 13.8 20H6.2a2.585 2.585 0 0 1-1.718-.783 2.553 2.553 0 0 1-.719-1.737L3 6.106l1.248-.083.761 11.369c-.005.333.114.656.333.908.22.252.525.415.858.458h7.6c.333-.043.64-.207.859-.46.22-.254.338-.578.332-.912l.76-11.363ZM18 2.983v1.243H2V2.983h4v-.372A2.737 2.737 0 0 1 6.896.718 2.772 2.772 0 0 1 8.875.002h2.25c.729-.03 1.44.227 1.979.716.538.488.86 1.169.896 1.893v.372h4Zm-10.75 0h5.5v-.372a1.505 1.505 0 0 0-.531-1.014 1.524 1.524 0 0 0-1.094-.352h-2.25c-.397-.03-.79.097-1.094.352-.304.256-.495.62-.531 1.014v.372Z">
                                            </path>
                                        </svg>
                                        <p>
                                            Delete comment
                                        </p>
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="children flex flex-col gap-4">

                </div>
            `

            if (parentId) {
                const childrenContainer = document.getElementById(`comment-${parentId}`).querySelector(".children");
                childrenContainer.prepend(comment);
                commentBox.parentElement.parentElement.remove()
            } else {
                document.querySelector("#commentsSection").prepend(comment);
            }
        }
    });
}

function showCommentReplyBox(container, postId, commentId) {
    let div = document.createElement('div');
    let opened = container.dataset.opened;
    if(opened == 1)return;
    let textarea = `
            <div class="w-full rounded-lg border border-gray-300 bg-white-500 overflow-hidden">
                <textarea class="w-full p-2 transition-all h-16 resize-none"
                      style="border: none; outline: none; padding: 10px; resize: none; box-shadow: none;" placeholder="Add a reply..." maxlength="2048"></textarea>
                <div id="" class="justify-end p-2.5 border-t-none bg-white float-right">
                    <button class="cancel-button inline-flex items-center px-2 py-1 bg-gray-200 border border-gray-300 rounded-full hover:bg-gray-300 mr-2 text-sm">
                        Cancel
                    </button>
                    <button class="inline-flex items-center px-2 py-1 bg-blue-600 text-white rounded-full hover:bg-blue-700 text-sm">
                        Comment
                    </button>
                </div>
            </div>
        `;

    div.innerHTML = textarea;

    div.querySelector('.cancel-button').addEventListener('click', () => {
        div.remove();
        container.dataset.opened = 0
    });

    div.querySelectorAll('button')[1].addEventListener('click', async () => {
        await submitComment(postId, commentId, div.querySelector("textarea"));
        container.dataset.opened = 0;
    })

    container.appendChild(div)
    container.dataset.opened = 1 
}

function showEditCommentTextArea(commentId){
    let commentContainer = document.getElementById(`comment-${commentId}`).querySelector(".comment_container");
    let commentTag = commentContainer.querySelector("p");
    let comment = commentTag.textContent.trim();
    console.log(comment)

    let editor = `
        <div class="w-full rounded-lg border border-gray-300 bg-white-500 overflow-hidden">
            <textarea class="w-full p-2 transition-all h-16 resize-none"
                      style="border: none; outline: none; padding: 10px; resize: none; box-shadow: none;">${comment}</textarea>
            <div class="justify-end pb-2.5 border-t-none bg-white float-right">
                <button class="btn-cancel inline-flex items-center px-2 py-1 bg-gray-200 border border-gray-300 rounded-full hover:bg-gray-300 mr-2 text-sm">
                    Cancel
                </button>
                <button class="btn-save inline-flex items-center px-2 py-1 bg-blue-600 text-white rounded-full hover:bg-blue-700 text-sm">
                    Save
                </button>
            </div>
        </div>
    `;
    commentTag.remove();
    commentContainer.innerHTML = editor;

    let cancelButton = commentContainer.querySelector(".btn-cancel");
    let saveButton = commentContainer.querySelector(".btn-save");

    cancelButton.addEventListener('click', () => {
        commentContainer.innerHTML = `<p>${comment}</p>`;
    });

    saveButton.addEventListener('click', async () => {
        let comment = commentContainer.querySelector("textarea").value;
        let data = new FormData();
        data.append("comment", comment);
        await fetch(`/post/comment/edit/${commentId}`, {
            method: "POST",
            body: data,
            headers: {
                "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                commentContainer.innerHTML = `<p>${comment}</p>`;
            }
        });
    });
}