// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const email = document.getElementById('id_email');

    form.addEventListener('submit', function (event) {
        let valid = true;
        clearErrors();

        if (password1.value !== password2.value) {
            showError(password2, 'Passwords do not match');
            valid = false;
        }

        if (!validateEmail(email.value)) {
            showError(email, 'Enter a valid email address');
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    function showError(element, message) {
        const error = document.createElement('div');
        error.className = 'error';
        error.textContent = message;
        element.parentElement.appendChild(error);
    }

    function clearErrors() {
        const errors = document.querySelectorAll('.error');
        errors.forEach(error => error.remove());
    }

    function validateEmail(email) {
        const re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        return re.test(String(email).toLowerCase());
    }
});


// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const refreshButtons = document.querySelectorAll('a[href*="refresh_search"]');

    refreshButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const url = this.href;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Search results refreshed successfully.');
                        location.reload();
                    } else {
                        alert('Failed to refresh search results.');
                    }
                })
                .catch(error => {
                    console.error('Error refreshing search results:', error);
                    alert('An error occurred while refreshing search results.');
                });
        });
    });
});

// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const keywordInput = document.querySelector('input[name="keyword"]');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const keyword = keywordInput.value.trim();
        
        if (!keyword) {
            alert('Please enter a keyword.');
            return;
        }
        
        fetch(`/check_keyword/?keyword=${encodeURIComponent(keyword)}`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert(`The keyword "${keyword}" has already been searched.`);
                } else {
                    form.submit();
                }
            })
            .catch(error => console.error('Error:', error));
    });
});


// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('search-form');
//     const searchResults = document.getElementById('search-results');
//     const viewPrevious = document.getElementById('view-previous');

//     form.addEventListener('submit', function (event) {
//         event.preventDefault();
//         const formData = new FormData(form);
        
//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => response.text())
//         .then(html => {
//             const parser = new DOMParser();
//             const doc = parser.parseFromString(html, 'text/html');
//             const newResults = doc.getElementById('search-list').innerHTML;
//             document.getElementById('search-list').innerHTML = newResults;
//             searchResults.style.display = 'block';
//         })
//         .catch(error => console.error('Error:', error));
//     });

//     viewPrevious.addEventListener('click', function (event) {
//         event.preventDefault();
//         searchResults.style.display = 'block';
//     });

//     const refreshButtons = document.querySelectorAll('a[href*="refresh_search"]');

//     refreshButtons.forEach(button => {
//         button.addEventListener('click', function (event) {
//             event.preventDefault();
//             const url = this.href;
//             fetch(url)
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         alert('Search results refreshed successfully.');
//                         location.reload();
//                     } else {
//                         alert('Failed to refresh search results.');
//                     }
//                 })
//                 .catch(error => {
//                     console.error('Error refreshing search results:', error);
//                     alert('An error occurred while refreshing search results.');
//                 });
//         });
//     });
// });