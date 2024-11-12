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
            y[i].classList.add("ring-1", "ring-red-500", "ring-inset");
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

function addRecentPost(post_id, post_title, post_content) {
    let recent_posts = localStorage.getItem("recent_posts");
    if (recent_posts == null) {
        recent_posts = [];
    } else {
        recent_posts = JSON.parse(recent_posts);
    }
    const postExists = recent_posts.some(post => post.post_id === post_id);
    if (!postExists) {
        let post = { post_id, post_title, post_content };
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
    const recentPostItem = document.createElement("div");
    recentPostItem.classList.add("recent_post_item", "max-h-[55px]", "line-clamp-2", "border-b", "border-gray-300", "py-2");
    recentPostItem.classList.add("recent_post_item");
    recentPostItem.innerHTML = `
            <a href="/post/${post.post_id}">
                <p class="font-bold">${post.post_title}</p>
                ${post.post_content}
            </a>
        `;
    recentPostItem.querySelectorAll("p")[1].classList.add("text-xs", "line-clamp-1");
    recentPostsContainer.prepend(recentPostItem);
}

function clearRecentPost() {
    localStorage.removeItem("recent_posts");
    const recentPostsContainer = document.getElementById("recent_posts");
    recentPostsContainer.innerHTML = "";
}

function warningToast(message) {
    const toast = document.createElement("div");
    toast.classList.add("fixed", "top-3", "right-3", "z-50", "animate-slideIn");
    toast.innerHTML += `
        <div id="toast-danger" class="flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
            <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200">
                <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
                </svg>
                <span class="sr-only">Error icon</span>
            </div>
            <div class="ms-3 text-sm font-normal">${message}</div>
            <button type="button" class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#toast-danger" aria-label="Close">
                <span class="sr-only">Close</span>
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                </svg>
            </button>
        </div>
        `
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 2000);
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

async function vote(buttonsContainer, postId, voteType) {
    await fetch(`/post/vote/${postId}/${voteType}`, {
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
            if (voteType == "upvote") {
                current_vote_count -= 1
                vote_count.dataset.voted = ""
                buttonsContainer.classList.remove("bg-red-500")
                buttonsContainer.classList.add("bg-button_gray")
                buttonsContainer.classList.remove("text-white")
                buttonsContainer.classList.add("text-black")
            } else {
                current_vote_count -= 2
                vote_count.dataset.voted = "downvote"
                buttonsContainer.classList.remove("bg-red-500")
                buttonsContainer.classList.add("bg-blue-500")
            }
        } else if (voted == "downvote") {
            if (voteType == "downvote") {
                current_vote_count += 1
                vote_count.dataset.voted = ""
                buttonsContainer.classList.remove("bg-blue-500")
                buttonsContainer.classList.add("bg-button_gray")
                buttonsContainer.classList.remove("text-white")
                buttonsContainer.classList.add("text-black")
            } else {
                current_vote_count += 2
                vote_count.dataset.voted = "upvote"
                buttonsContainer.classList.remove("bg-blue-500")
                buttonsContainer.classList.add("bg-red-500")
            }
        } else {
            buttonsContainer.classList.remove("bg-button_gray")
            buttonsContainer.classList.add("text-white")
            if (voteType == "downvote") {
                current_vote_count -= 1
                vote_count.dataset.voted = "downvote"
                buttonsContainer.classList.add("bg-blue-500")
            } else {
                current_vote_count += 1
                vote_count.dataset.voted = "upvote"
                buttonsContainer.classList.add("bg-red-500")
            }
        }
        vote_count.textContent = current_vote_count
    });
}