
function deleteSubject(subjectId, subjectName) {
    if (confirm('Are you sure you want to delete the subject: ' + subjectName + '?')) {
        const csrf_token = document.querySelector('input[name="csrf_token"]').value;
        fetch('/grades/delete/' + subjectId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token  // Use the passed csrf_token variable
            }
        }).then(response => {
            if (response.ok) {
                location.reload();  // Reload the page to see the changes
            } else {
                alert('Failed to delete subject.');
            }
        });
    }
}


function showGradeForm(subject) {
    document.getElementById('selected-subject').innerText = subject;
    document.getElementById('subject-input').value = subject;
    document.getElementById('grade-modal').style.display = 'block';
}

const menudialog = document.querySelector(".nav-sidebar");
const openmenu = document.querySelector("#hamburger-btn");
const closemenu = document.querySelector(".close-menu")

openmenu.addEventListener("click", () => {
    menudialog.style.display = "flex";
});

closemenu.addEventListener("click", () => {
    menudialog.style.display = "none";
});

document.querySelectorAll('.theme-form').forEach(form => {
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent form submission

        // Get the selected theme from the current form
        const selectedTheme = form.querySelector('select[name="theme"]').value;
        document.documentElement.setAttribute('data-theme', selectedTheme);

        // Get the CSRF token from the current form
        const csrfToken = form.querySelector('input[name="csrf_token"]').value;

        // Send the selected theme to the server
        fetch('/update-theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ theme: selectedTheme })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log('Theme updated successfully:', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});





const newtodo = document.querySelector("#add-todo-btn");
const newtododialog = document.querySelector("#add-todo");
const closenewtodo = document.querySelector("#close-dialog");

newtodo.addEventListener("click", () => {
    newtododialog.showModal();
})

closenewtodo.addEventListener("click", () => {
    newtododialog.close();
})

function openEditModal(taskId) {
    // Find the dialog element
    console.log("Editing task with ID:", taskId);
    const modal = document.getElementById('edit-todo');

    // Populate the form fields in the modal with task data
    const task = JSON.parse(document.getElementById(`task-data-${taskId}`).textContent);
    document.querySelector('#edit-todo [name="title"]').value = task.title;
    document.querySelector('#edit-todo [name="description"]').value = task.description;
    document.querySelector('#edit-todo [name="deadline"]').value = task.deadline || ''; // Ensure the date input works

    // Update the form action with the task_id
    const form = modal.querySelector('form');
    form.action = `/todos/edit/${taskId}`; // Set the correct action URL

    // Show the modal
    modal.showModal();
}
