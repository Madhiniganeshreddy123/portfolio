const API_BASE = '/api';

class ProjectDashboard {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.projects = [];
        this.editingId = null;
        this.filterCategory = 'all';
        this.searchQuery = '';
        this.draggedItem = null;
        this.init();
    }

    async init() {
        await this.loadProjects();
        this.render();
    }

    async loadProjects() {
        try {
            const response = await fetch(`${API_BASE}/projects/`);
            this.projects = await response.json();
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    async saveProject(formData) {
        const method = this.editingId ? 'PUT' : 'POST';
        const url = this.editingId ? `${API_BASE}/projects/${this.editingId}/` : `${API_BASE}/projects/`;
        
        try {
            const response = await fetch(url, {
                method,
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            });
            
            if (response.ok) {
                await this.loadProjects();
                this.editingId = null;
                this.render();
                this.showNotification(this.editingId ? 'Project updated!' : 'Project created!');
            }
        } catch (error) {
            console.error('Error saving project:', error);
        }
    }

    async deleteProject(id) {
        if (!confirm('Are you sure you want to delete this project?')) return;
        
        try {
            await fetch(`${API_BASE}/projects/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            });
            await this.loadProjects();
            this.render();
            this.showNotification('Project deleted!');
        } catch (error) {
            console.error('Error deleting project:', error);
        }
    }

    async reorderProjects(newOrder) {
        try {
            await fetch(`${API_BASE}/projects/reorder/`, {
                method: 'POST',
                body: JSON.stringify({ order: newOrder }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            });
        } catch (error) {
            console.error('Error reordering projects:', error);
        }
    }

    getFilteredProjects() {
        let filtered = [...this.projects];
        
        if (this.filterCategory !== 'all') {
            filtered = filtered.filter(p => p.category === this.filterCategory);
        }
        
        if (this.searchQuery) {
            const query = this.searchQuery.toLowerCase();
            filtered = filtered.filter(p => 
                p.title.toLowerCase().includes(query) ||
                p.tech_stack.toLowerCase().includes(query) ||
                p.description.toLowerCase().includes(query)
            );
        }
        
        return filtered;
    }

    render() {
        const filtered = this.getFilteredProjects();
        
        this.container.innerHTML = `
            <div class="space-y-6">
                ${this.renderHeader()}
                ${this.renderForm()}
                ${this.renderStats()}
                ${this.renderFilters()}
                ${this.renderProjectList(filtered)}
            </div>
        `;
        
        this.attachEventListeners();
    }

    renderHeader() {
        return `
            <div class="flex items-center justify-between">
                <h2 class="text-2xl font-bold">Project Manager</h2>
                <button id="addProjectBtn" class="px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors">
                    <i class="fas fa-plus mr-2"></i>Add Project
                </button>
            </div>
        `;
    }

    renderForm() {
        const project = this.editingId ? this.projects.find(p => p.id === this.editingId) : null;
        
        return `
            <div id="projectForm" class="${this.editingId ? 'block' : 'hidden'} bg-dark-card rounded-xl border border-dark-border p-6">
                <h3 class="text-lg font-semibold mb-4">${this.editingId ? 'Edit Project' : 'Create New Project'}</h3>
                <form id="formElement" class="space-y-4">
                    <div class="grid md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">Title *</label>
                            <input type="text" name="title" required value="${project?.title || ''}"
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Category *</label>
                            <select name="category" required
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">
                                <option value="analysis" ${project?.category === 'analysis' ? 'selected' : ''}>Analysis</option>
                                <option value="development" ${project?.category === 'development' ? 'selected' : ''}>Development</option>
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">Description *</label>
                        <textarea name="description" required rows="3"
                            class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">${project?.description || ''}</textarea>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">Detailed Description</label>
                        <textarea name="detailed_description" rows="5"
                            class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">${project?.detailed_description || ''}</textarea>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">Tech Stack * (comma separated)</label>
                        <input type="text" name="tech_stack" required value="${project?.tech_stack || ''}"
                            class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500"
                            placeholder="Python, Django, React, ML">
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">GitHub URL</label>
                            <input type="url" name="github_link" value="${project?.github_link || ''}"
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Live URL</label>
                            <input type="url" name="demo_link" value="${project?.demo_link || ''}"
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">
                        </div>
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">Image URL</label>
                            <input type="text" name="image" value="${project?.image || ''}"
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500"
                                placeholder="https://example.com/image.jpg">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Order</label>
                            <input type="number" name="order" value="${project?.order || 0}"
                                class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500">
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-4">
                        <input type="checkbox" name="is_featured" id="is_featured" ${project?.is_featured ? 'checked' : ''}>
                        <label for="is_featured" class="text-sm">Featured Project</label>
                    </div>
                    
                    <div class="flex gap-4">
                        <button type="submit" class="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors">
                            ${this.editingId ? 'Update Project' : 'Create Project'}
                        </button>
                        <button type="button" id="cancelBtn" class="px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        `;
    }

    renderStats() {
        const total = this.projects.length;
        const analysis = this.projects.filter(p => p.category === 'analysis').length;
        const development = this.projects.filter(p => p.category === 'development').length;
        const featured = this.projects.filter(p => p.is_featured).length;
        
        return `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-dark-card rounded-xl p-4 border border-dark-border">
                    <p class="text-gray-400 text-sm">Total Projects</p>
                    <p class="text-2xl font-bold text-primary-500">${total}</p>
                </div>
                <div class="bg-dark-card rounded-xl p-4 border border-dark-border">
                    <p class="text-gray-400 text-sm">Analysis</p>
                    <p class="text-2xl font-bold text-blue-500">${analysis}</p>
                </div>
                <div class="bg-dark-card rounded-xl p-4 border border-dark-border">
                    <p class="text-gray-400 text-sm">Development</p>
                    <p class="text-2xl font-bold text-purple-500">${development}</p>
                </div>
                <div class="bg-dark-card rounded-xl p-4 border border-dark-border">
                    <p class="text-gray-400 text-sm">Featured</p>
                    <p class="text-2xl font-bold text-green-500">${featured}</p>
                </div>
            </div>
        `;
    }

    renderFilters() {
        return `
            <div class="flex flex-wrap gap-4">
                <div class="flex-1 min-w-[200px]">
                    <input type="text" id="searchInput" placeholder="Search projects..."
                        class="w-full px-4 py-3 bg-dark-card border border-dark-border rounded-lg focus:ring-2 focus:ring-primary-500"
                        value="${this.searchQuery}">
                </div>
                <div class="flex gap-2">
                    <button class="filter-btn px-4 py-2 rounded-lg transition-colors ${this.filterCategory === 'all' ? 'bg-primary-600' : 'bg-dark-card border border-dark-border hover:bg-dark-border'}" data-category="all">
                        All
                    </button>
                    <button class="filter-btn px-4 py-2 rounded-lg transition-colors ${this.filterCategory === 'analysis' ? 'bg-primary-600' : 'bg-dark-card border border-dark-border hover:bg-dark-border'}" data-category="analysis">
                        Analysis
                    </button>
                    <button class="filter-btn px-4 py-2 rounded-lg transition-colors ${this.filterCategory === 'development' ? 'bg-primary-600' : 'bg-dark-card border border-dark-border hover:bg-dark-border'}" data-category="development">
                        Development
                    </button>
                </div>
            </div>
        `;
    }

    renderProjectList(projects) {
        if (projects.length === 0) {
            return `
                <div class="bg-dark-card rounded-xl border border-dark-border p-8 text-center">
                    <i class="fas fa-folder-open text-4xl text-gray-500 mb-4"></i>
                    <p class="text-gray-400">No projects found</p>
                </div>
            `;
        }

        return `
            <div id="projectList" class="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
                <div class="p-4 border-b border-dark-border bg-dark-border/30">
                    <p class="text-sm text-gray-400"><i class="fas fa-arrows-alt mr-2"></i>Drag to reorder</p>
                </div>
                <div class="divide-y divide-dark-border">
                    ${projects.map(project => this.renderProjectCard(project)).join('')}
                </div>
            </div>
        `;
    }

    renderProjectCard(project) {
        const categoryColor = project.category === 'analysis' ? 'text-blue-500' : 'text-purple-500';
        const categoryBg = project.category === 'analysis' ? 'bg-blue-500/20' : 'bg-purple-500/20';
        const techStackArray = project.tech_stack.split(',').map(t => t.trim()).filter(t => t);
        
        return `
            <div class="project-card p-4 hover:bg-dark-border/30 transition-colors cursor-move" data-id="${project.id}" draggable="true">
                <div class="flex items-start gap-4">
                    <div class="flex items-center gap-2 text-gray-400 cursor-move handle">
                        <i class="fas fa-grip-vertical"></i>
                    </div>
                    <div class="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0 bg-dark-bg">
                        ${project.image ? 
                            `<img src="${project.image}" alt="${project.title}" class="w-full h-full object-cover">` :
                            `<div class="w-full h-full flex items-center justify-center text-gray-500"><i class="fas fa-image"></i></div>`
                        }
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-semibold truncate">${project.title}</h4>
                            <span class="px-2 py-0.5 rounded text-xs ${categoryBg} ${categoryColor} capitalize">${project.category}</span>
                            ${project.is_featured ? '<span class="px-2 py-0.5 rounded text-xs bg-yellow-500/20 text-yellow-500"><i class="fas fa-star"></i></span>' : ''}
                        </div>
                        <p class="text-sm text-gray-400 line-clamp-2 mb-2">${project.description}</p>
                        <div class="flex flex-wrap gap-1 mb-2">
                            ${techStackArray.slice(0, 5).map(tech => `
                                <span class="px-2 py-0.5 bg-dark-bg rounded text-xs text-gray-400">${tech}</span>
                            `).join('')}
                            ${techStackArray.length > 5 ? `<span class="text-xs text-gray-500">+${techStackArray.length - 5}</span>` : ''}
                        </div>
                        <div class="flex items-center gap-4 text-xs text-gray-500">
                            <span><i class="fas fa-sort mr-1"></i>Order: ${project.order}</span>
                            ${project.github_link ? `<a href="${project.github_link}" target="_blank" class="hover:text-primary-500"><i class="fab fa-github mr-1"></i>Code</a>` : ''}
                            ${project.demo_link ? `<a href="${project.demo_link}" target="_blank" class="hover:text-primary-500"><i class="fas fa-external-link-alt mr-1"></i>Demo</a>` : ''}
                        </div>
                    </div>
                    <div class="flex flex-col gap-2">
                        <button class="edit-btn px-3 py-1 bg-primary-600/20 text-primary-500 rounded hover:bg-primary-600/30 transition-colors text-sm" data-id="${project.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="delete-btn px-3 py-1 bg-red-600/20 text-red-500 rounded hover:bg-red-600/30 transition-colors text-sm" data-id="${project.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const addBtn = document.getElementById('addProjectBtn');
        const form = document.getElementById('formElement');
        const cancelBtn = document.getElementById('cancelBtn');
        const searchInput = document.getElementById('searchInput');

        if (addBtn) {
            addBtn.addEventListener('click', () => {
                this.editingId = null;
                this.render();
            });
        }

        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                
                if (formData.get('is_featured') === 'on') {
                    formData.set('is_featured', 'true');
                } else {
                    formData.set('is_featured', 'false');
                }
                
                await this.saveProject(formData);
            });
        }

        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                this.editingId = null;
                this.render();
            });
        }

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value;
                this.render();
            });
        }

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.filterCategory = btn.dataset.category;
                this.render();
            });
        });

        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.editingId = parseInt(btn.dataset.id);
                this.render();
                document.getElementById('projectForm').scrollIntoView({ behavior: 'smooth' });
            });
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.deleteProject(parseInt(btn.dataset.id));
            });
        });

        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const list = document.getElementById('projectList');
        if (!list) return;

        const cards = list.querySelectorAll('.project-card');

        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                this.draggedItem = card;
                card.classList.add('opacity-50');
                e.dataTransfer.effectAllowed = 'move';
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('opacity-50');
                this.draggedItem = null;
            });

            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            });

            card.addEventListener('drop', async (e) => {
                e.preventDefault();
                if (this.draggedItem && this.draggedItem !== card) {
                    const allCards = [...list.querySelectorAll('.project-card')];
                    const draggedIdx = allCards.indexOf(this.draggedItem);
                    const targetIdx = allCards.indexOf(card);

                    if (draggedIdx < targetIdx) {
                        card.parentNode.insertBefore(this.draggedItem, card.nextSibling);
                    } else {
                        card.parentNode.insertBefore(this.draggedItem, card);
                    }

                    const newOrder = [...list.querySelectorAll('.project-card')].map(c => parseInt(c.dataset.id));
                    await this.reorderProjects(newOrder);
                    await this.loadProjects();
                    this.render();
                }
            });
        });
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'fixed bottom-4 right-4 px-6 py-3 bg-green-600 text-white rounded-lg shadow-lg z-50';
        notification.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('projectDashboard');
    if (container) {
        window.projectDashboard = new ProjectDashboard('projectDashboard');
    }
});
