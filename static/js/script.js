// Pagination variables
let offset = 0;
const limit = 6;
let loading = false;
// Fallback image URL if the herb image cannot load
const noImageURL = "https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-no-image-available-icon-flatvector-illustration-pic-design-profile-vector-png-image_40966566.jpg";

function showLoader() {
  document.getElementById('loadingIndicator').style.display = 'flex';
}

function hideLoader() {
  document.getElementById('loadingIndicator').style.display = 'none';
}

function loadMoreHerbs() {
  if (loading) return;
  loading = true;
  showLoader();
  
  fetch(`/api/herbs/?offset=${offset}&limit=${limit}`)
    .then(response => response.json())
    .then(data => {
      const grid = document.getElementById('herbGrid');
      data.herbs.forEach(herb => {
        const card = document.createElement('div');
        card.className = 'card';
        // Use the herb's thumbnail if available; otherwise, use the fallback image.
        const imageUrl = herb.thumbnail ? herb.thumbnail.source : noImageURL;
        card.innerHTML = `
          <h2>${herb.title}</h2>
          <img src="${imageUrl}" alt="${herb.title}" onerror="this.onerror=null;this.src='${noImageURL}';">
          <p>${herb.extract.substring(0, 100)}...</p>
          <button onclick="addToGarden('${herb.title}')">Add to My Garden</button>
        `;
        grid.appendChild(card);
      });
      offset += limit;
      loading = false;
      hideLoader();
    })
    .catch(err => {
      console.error('Error loading herbs:', err);
      loading = false;
      hideLoader();
    });
}

function addToGarden(herbName) {
  alert(herbName + " added to your garden!");
}

window.addEventListener('scroll', () => {
  if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
    loadMoreHerbs();
  }
});

document.addEventListener('DOMContentLoaded', loadMoreHerbs);
