document.getElementById("theme-toggle-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.light_mode !== undefined) {
            document.body.classList.toggle('light-mode', data.light_mode);
            document.getElementById('toggle').textContent = data.light_mode ? 'Light-Mode' : 'Dark-Mode';
        } else {
            console.error('Error toggling mode:', data.error || 'Unknown error');
        }
    })
    .catch(error => console.error('Error:', error));
});



const subdialog = document.getElementById("subject-modal");
const showButton = document.getElementById("openSubjectModal");
const closeButton = document.getElementById("close-subject");

showButton.addEventListener("click", () => {
    subdialog.showModal();
    console.log("modal loaded...")
});

closeButton.addEventListener('close', () => {
    subdialog.close();
});


const deletedialog = document.getElementById("delete-modal");
const showdeleteButton = document.getElementById("openDeleteModal");
const closedeleteButton = document.getElementById("delete-subject");

showdeleteButton.addEventListener("click", () => {
    deletedialog.showModal();
});

closedeleteButton.addEventListener("close", () => {
    deletedialog.close();
});

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

const gradedialog = document.getElementById("grade-modal");
const showgradesbutton = document.getElementById("grade-btn");
const closegrades = document.getElementById("add-grade-btn");

showgradesbutton.addEventListener("click", () => {
    gradedialog.showModal();
});

closegrades.addEventListener("close", () => {
    gradedialog.close();
});

function showGradeForm(subject) {
    document.getElementById('selected-subject').innerText = subject;
    document.getElementById('subject-input').value = subject;
    document.getElementById('grade-modal').style.display = 'block';
}