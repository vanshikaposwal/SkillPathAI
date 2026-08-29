// Mark item complete via AJAX
async function completeRoadmapItem(itemId, btnElement) {
    btnElement.disabled = true;
    btnElement.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span>';
    
    try {
        const res = await fetch(`/api/roadmap/item/${itemId}/complete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await res.json();
        if (data.success) {
            showToast('Item marked as completed! Overall progress updated.');
            // Update UI card
            const itemRow = document.getElementById(`item-row-${itemId}`);
            if (itemRow) {
                itemRow.classList.add('bg-light');
                const badge = itemRow.querySelector('.item-status-badge');
                if (badge) {
                    badge.className = 'badge bg-success item-status-badge';
                    badge.innerText = 'Completed';
                }
                btnElement.outerHTML = '<span class="text-success fw-bold"><i class="bi bi-check-circle-fill me-1"></i>Completed</span>';
            }
            // Update overall progress meter if present
            const bar = document.getElementById('overall-progress-bar');
            if (bar) {
                bar.style.width = `${data.progress_percentage}%`;
                bar.innerText = `${data.progress_percentage}%`;
            }
        }
    } catch (e) {
        showToast('Error completing item', 'danger');
        btnElement.disabled = false;
        btnElement.innerText = 'Mark Complete';
    }
}

// Show Explainable Recommendation Modal
async function showWhyModal(itemId) {
    const modalBody = document.getElementById('whyModalBody');
    const modalTitle = document.getElementById('whyModalTitle');
    modalBody.innerHTML = '<div class="text-center py-4"><span class="spinner-border text-primary" role="status"></span></div>';
    
    const whyModal = new bootstrap.Modal(document.getElementById('whyModal'));
    whyModal.show();
    
    try {
        const res = await fetch(`/api/roadmap/item/${itemId}/why/`);
        const data = await res.json();
        modalTitle.innerText = `Why "${data.title}"?`;
        modalBody.innerHTML = `
            <div class="p-3 bg-light rounded-3 border mb-3">
                <h6 class="text-primary fw-bold mb-2"><i class="bi bi-cpu-fill me-2"></i>AI Recommendation Rationale:</h6>
                <p class="mb-0 leading-relaxed text-secondary">${data.why_recommended}</p>
            </div>
            <div class="small text-muted">
                <i class="bi bi-info-circle me-1"></i> Calibrated based on your career goal, verified skill gaps, and prerequisite dependency graph.
            </div>
        `;
    } catch (e) {
        modalBody.innerText = 'Failed to load recommendation rationale.';
    }
}

// Submit Adaptive Feedback
let activeFeedbackItemId = null;

function openFeedbackModal(itemId, itemTitle) {
    activeFeedbackItemId = itemId;
    document.getElementById('feedbackItemTitle').innerText = itemTitle;
    const feedbackModal = new bootstrap.Modal(document.getElementById('feedbackModal'));
    feedbackModal.show();
}

async function submitFeedback(feedbackType) {
    if (!activeFeedbackItemId) return;
    const userNote = document.getElementById('feedbackUserNote').value;
    
    try {
        const res = await fetch(`/api/roadmap/item/${activeFeedbackItemId}/feedback/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                feedback_type: feedbackType,
                user_note: userNote
            })
        });
        const data = await res.json();
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('feedbackModal')).hide();
            showToast(`Learning path adapted: ${data.action_summary}`);
            setTimeout(() => window.location.reload(), 1500);
        }
    } catch (e) {
        showToast('Error submitting feedback', 'danger');
    }
}
